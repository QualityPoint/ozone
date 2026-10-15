"""The producer's service requests: the list, the form to raise one for a facility, and what each
facility has led to (docs/producer_dashboard/api.md).

A request is a Draft the producer can change until it submits it; then it is Under Process, the
transporter's sales team's. The team may ask for clarification, which the producer answers in the
request's comments, before making its quotation. The producer gives what only it
knows: the facility (and, for a composite facility, the annexes it covers), the service, its size in
the Service Setup's unit, the wastes of each waste type (the setup's defaults stay; others may be
added), when the service starts and for how long, and the license it holds when the service grants
one. The Service Setup and the activity come from the facility and the service
(ServiceRequest.before_validate)."""

import frappe
from frappe import _
from frappe.query_builder import Criterion
from frappe.utils import add_days, cint, cstr, flt, getdate
from naqel.naqel.doctype.waste_type.waste_type import get_wastes
from naqel.naqel_calculator.doctype.waste_calculator.waste_calculator import (
	get_allowed_facility_uoms,
	get_facility_uom_hierarchy,
)
from naqel.naqel_contracting.doctype.service_quotation.service_quotation import _resolve_default_sc
from naqel.naqel_contracting.doctype.service_request.service_request import (
	WASTE_SEP,
	facility_document,
	open_request,
	registration_documents,
	split_wastes,
)

from ozone.portal import comments, own_doc, pick
from ozone.portal.facilities import _document_types, document, set_credential
from ozone.producer import main_party, owned_names

REQUEST_FIELDS = (
	"facility",
	"service_type",
	"facility_uom",
	"facility_measurement",
	"start_date",
	"end_date",
	"license_status",
	"license_no",
	"license_document",
)
DURATION_UOMS = ("Day", "Month", "Year")
LICENSE_STATUSES = ("New Issue", "Renewal")


# A request that has turned into a quotation moves to the Quotations page (portal/quotations.py: get_quotations)
QUOTED = "Quotation"


def get_service_requests(
	producer: frappe._dict, filters: dict | None = None, include_quoted: bool = False
) -> list[dict]:
	"""The producer's requests, newest first, optionally for one facility, service or status. Those that
	have turned into a quotation are on the Quotations page, unless `include_quoted` (a facility's history)."""
	conditions = {"name": ["in", owned_names("Service Request", producer) or [""]]}
	if not include_quoted:
		conditions["status"] = ["!=", QUOTED]
	for field in ("facility", "service_type", "status"):
		if (filters or {}).get(field):
			conditions[field] = filters[field]
	requests = frappe.get_all(
		"Service Request",
		filters=conditions,
		fields=["name", "service_type", "facility", "status", "start_date", "creation"],
		order_by="creation desc",
	)
	services = _labels("Service", [r.service_type for r in requests], "service_name")
	facilities = _labels("Facility", [r.facility for r in requests], "facility_name")
	from ozone.portal.quotations import request_quotations

	quotations = request_quotations(producer, [r.name for r in requests])
	for request in requests:
		# The quotations Ozone's team has sent for it
		request.quotations = quotations.get(request.name, [])
		request.service_title = _(services.get(request.service_type) or request.service_type or "")
		request.facility_title = facilities.get(request.facility) or request.facility
		request.status_label = _(request.status)
	return requests


def get_request_options(producer: frappe._dict) -> dict:
	"""What the list filters by and the form picks from: services, the producer's facilities, statuses."""
	statuses = frappe.get_meta("Service Request").get_field("status").options.split("\n")
	return {
		"service_types": [
			{"value": row.name, "label": _(row.service_name or row.name), "image": row.image}
			for row in frappe.get_all(
				"Service", fields=["name", "service_name", "image"], order_by="service_name"
			)
		],
		"facilities": [
			{"value": row.name, "label": row.facility_name}
			for row in frappe.get_all(
				"Facility",
				filters={"name": ["in", owned_names("Facility", producer) or [""]]},
				fields=["name", "facility_name"],
				order_by="lft",
			)
		],
		"statuses": [
			{"value": status, "label": _(status)} for status in statuses if status and status != QUOTED
		],
	}


def get_request_form(
	producer: frappe._dict, facility: str, service_type: str, name: str | None = None
) -> dict:
	"""How a request for this service at this facility is measured, and what else it asks for. The
	Service Setup is the one the request itself will resolve (the service and the facility's activity):
	its units, and its waste types with their default wastes."""
	site = own_doc("Facility", facility, producer)
	service = _service(service_type)
	# One open request at a time for a facility and a service (naqel's ServiceRequest.validate_one_open_request):
	# said as soon as both are chosen. `name` is the Draft being changed.
	if other := open_request(site.name, service.name, exclude=name):
		frappe.throw(
			_(
				"This facility already has a request for this service ({0}). You can raise another once its quotation is cancelled."
			).format(other)
		)
	configuration = _service_setup(service_type, site)
	uoms = []
	for name in get_allowed_facility_uoms(configuration):
		uom = frappe.db.get_value(
			"Facility UOM", name, ["must_be_whole_number", "is_composite_uom"], as_dict=True
		)
		if not uom:
			continue
		uoms.append(
			{
				"value": name,
				"label": _(name),
				"whole_number": uom.must_be_whole_number or 0,
				"composite": uom.is_composite_uom or 0,
				# A composite unit is measured part by part (e.g. floors, then rooms).
				"parts": [
					{
						"value": part["uom"],
						"label": _(part["uom"]),
						"whole_number": part["must_be_whole_number"],
					}
					for part in get_facility_uom_hierarchy(name)
				]
				if uom.is_composite_uom
				else [],
			}
		)
	return {
		"service_setup": configuration,
		"uoms": uoms,
		"waste_types": _waste_types(configuration),
		# A composite facility's annexes, all covered unless the producer unticks some
		"annexes": _annexes(site, producer),
		"documents": _documents(site.name, service_type),
		"milestone_based": service.is_milestone_based or 0,
		"duration_uoms": [{"value": uom, "label": _(uom)} for uom in DURATION_UOMS],
		"grants_license": service.grants_license or 0,
		"license_statuses": [{"value": status, "label": _(status)} for status in LICENSE_STATUSES],
	}


def save_service_request(producer: frappe._dict, data: dict) -> dict:
	"""A Draft request from the producer's party for one of its facilities: a new one, or a change to one of
	its drafts (`name`). With `submit`, it is then submitted: Under Process, the sales team's to review, and
	no longer the producer's to change."""
	values = pick(data, REQUEST_FIELDS)
	site = own_doc("Facility", values.get("facility"), producer)
	service = _service(values.get("service_type"))
	configuration = _service_setup(values.get("service_type"), site)
	for field in ("start_date", "end_date"):
		values[field] = getdate(values.get(field)) if values.get(field) else None

	request = _draft(data["name"], producer) if data.get("name") else frappe.new_doc("Service Request")
	request.update(values)
	# The party the facility belongs to (a Customer before a Lead, as the Facility decides), which the
	# request's own check requires; a facility of a Lead converted before its links carried over
	# still belongs to the Lead. own_doc has made sure it is one of the producer's parties.
	site.set_party_from_links()
	request.request_from, request.party = (
		(site.party_type, site.party) if site.party else main_party(producer)
	)

	# The producer gives the dates: the start, and the end unless the service is milestone-based. naqel works
	# out the duration and its unit from them (ServiceRequest: set_duration_from_dates).
	if not request.start_date:
		frappe.throw(_("Give the date the service starts."))
	if service.is_milestone_based:
		request.end_date = request.service_duration = request.duration_uom = None
	elif not request.end_date:
		frappe.throw(_("Give the date the service ends."))
	elif request.end_date < request.start_date:
		frappe.throw(_("The service can't end before it starts."))

	if not service.grants_license:
		request.license_status = request.license_no = request.license_document = None
	elif request.license_status not in LICENSE_STATUSES:
		frappe.throw(_("Say whether this is a new license or a renewal."))
	elif request.license_status != "Renewal":
		# A new issue has no number or document yet.
		request.license_no = request.license_document = None
	elif request.license_document and not frappe.db.exists(
		"File", {"file_url": request.license_document, "owner": frappe.session.user}
	):
		frappe.throw(_("Upload the document first."), frappe.PermissionError)

	# The document the service requires, kept with the facility (its credentials), not the request: given
	# once, it answers every later request that needs it
	required = registration_documents(service.name)
	if required and not facility_document(site.name, service.name):
		if not data.get("document"):
			frappe.throw(
				_(
					"This service requires one of these documents: {0}. Choose it, give its number and upload it."
				).format(", ".join(_(row.document_type) for row in required))
			)
		kept = {row.credential for row in site.get("credentials") if row.credential}
		given = document(data["document"], kept)
		if (given.get("credential_type"), given.get("document_type")) not in {
			(row.credential_type, row.document_type) for row in required
		}:
			frappe.throw(_("Choose one of the documents this service requires."))
		set_credential(site, given)
		site.save(ignore_permissions=True)

	# The wastes of each waste type: the setup's defaults stay (ServiceRequest.set_waste_types), the
	# producer's additions must be wastes of that type (ServiceRequest.validate_wastes)
	added = {
		cstr(row.get("waste_type")): [cstr(name) for name in row.get("wastes") or []]
		for row in data.get("waste_types") or []
	}
	request.set(
		"waste_types",
		[
			{"waste_type": row["waste_type"], "waste_item": WASTE_SEP.join(added.get(row["waste_type"], []))}
			for row in _waste_types(configuration)
		],
	)

	chosen = [cstr(name) for name in data.get("annexes") or []] if site.is_group else []
	allowed = {row["value"] for row in _annexes(site, producer)}
	if any(name not in allowed for name in chosen):
		frappe.throw(_("Choose annexes of this facility."), frappe.PermissionError)
	# A composite request lists the annexes it covers (the request requires them then); none chosen, it
	# covers the facility alone
	request.is_composite_facility = 1 if chosen else 0
	request.set("annexes", [{"annex": name} for name in chosen])

	request.set(
		"facility_uoms",
		[
			{"uom": cstr(part.get("uom")), "uom_value": flt(part.get("uom_value"))}
			for part in data.get("facility_uoms") or []
		],
	)
	request.flags.ignore_permissions = True
	request.save()
	if data.get("submit"):
		request.submit()
	return {"name": request.name, "requests": get_service_requests(producer)}


def get_service_request(producer: frappe._dict, name: str) -> dict:
	"""One of the producer's requests: what it asks for (to change it while it is a Draft) and its
	comments with the sales team."""
	request = own_doc("Service Request", name, producer)
	defaults = (
		{
			row["waste_type"]: {d["value"] for d in row["defaults"]}
			for row in _waste_types(request.service_setup)
		}
		if request.service_setup
		else {}
	)
	return {
		"name": request.name,
		"status": request.status,
		"status_label": _(request.status),
		"service_title": _(
			frappe.db.get_value("Service", request.service_type, "service_name") or request.service_type
		),
		"facility_title": frappe.db.get_value("Facility", request.facility, "facility_name")
		or request.facility,
		"can_edit": request.docstatus == 0,
		"can_reply": request.status == "Require Clarification",
		"values": {
			**{field: request.get(field) for field in REQUEST_FIELDS},
			"facility_uoms": [{"uom": row.uom, "uom_value": row.uom_value} for row in request.facility_uoms],
			# The wastes the producer added (the setup's defaults are kept anyway)
			"waste_types": [
				{
					"waste_type": row.waste_type,
					"wastes": [
						w for w in split_wastes(row.waste_item) if w not in defaults.get(row.waste_type, ())
					],
				}
				for row in request.waste_types
			],
			"annexes": [row.annex for row in request.annexes],
		},
		"comments": comments.thread(request),
	}


def submit_service_request(producer: frappe._dict, name: str) -> dict:
	"""Send one of the producer's drafts to the sales team: Under Process, and no longer the producer's
	to change. Its checks run again (ServiceRequest.validate)."""
	request = _draft(name, producer)
	request.flags.ignore_permissions = True
	request.submit()
	return {"name": request.name, "requests": get_service_requests(producer)}


def add_request_comment(producer: frappe._dict, name: str, text: str) -> list[dict]:
	"""The producer's answer, in the request's comments, while the sales team asks for clarification
	(the Desk shows it in the request's timeline)."""
	request = own_doc("Service Request", name, producer)
	if request.status != "Require Clarification":
		frappe.throw(_("You can write here while the request requires clarification."))
	comments.post(request, text)
	return comments.thread(request)


def get_facility_activity(producer: frappe._dict, facility: str) -> dict:
	"""What a facility has led to: its requests, the quotations made for it, the contracts that
	followed, and its operation orders. Only the producer's own records."""
	own_doc("Facility", facility, producer)
	requests = get_service_requests(producer, {"facility": facility}, include_quoted=True)
	quotation = frappe.qb.DocType("Service Quotation")
	quotations = (
		frappe.qb.from_(quotation)
		.select(
			quotation.name,
			quotation.status,
			quotation.transaction_date,
			quotation.grand_total,
			quotation.currency,
		)
		.where(quotation.facility == facility)
		.where(quotation.docstatus < 2)
		.where(
			Criterion.any(
				(quotation.quotation_to == party_type) & (quotation.party_name == party)
				for party_type, party in producer.parties
			)
		)
		.orderby(quotation.creation, order=frappe.qb.desc)
		.run(as_dict=True)
	)
	customers = [party for party_type, party in producer.parties if party_type == "Customer"]
	contracts = (
		frappe.get_all(
			"Service Contract",
			filters={
				"service_quotation": ["in", [q.name for q in quotations]],
				"customer": ["in", customers],
				"docstatus": ["<", 2],
			},
			fields=["name", "status", "contract_date"],
			order_by="creation desc",
		)
		if quotations and customers
		else []
	)
	orders = (
		frappe.get_all(
			"Operation Order",
			filters={"facility": facility, "customer": ["in", customers], "docstatus": ["<", 2]},
			fields=["name", "status", "service_type"],
			order_by="creation desc",
		)
		if customers
		else []
	)
	for row in (*quotations, *contracts, *orders):
		row.status_label = _(row.status)
	return {
		"requests": requests,
		"quotations": quotations,
		"contracts": contracts,
		"operation_orders": orders,
	}


def _draft(name: str, producer: frappe._dict):
	request = own_doc("Service Request", name, producer)
	if request.docstatus != 0:
		frappe.throw(_("This request has been submitted; it can't be changed."))
	return request


def _service_setup(service_type: str, site) -> str:
	"""The Service Setup a request for this service at this facility resolves (the general one, else
	the nearest up the activity's ISIC tree), or a refusal: the service isn't offered for it yet."""
	configuration = site.isic_classification and _resolve_default_sc(service_type, site.isic_classification)
	if not configuration:
		frappe.throw(_("This service isn't available for your facility's activity yet."))
	return configuration


def _waste_types(configuration: str) -> list[dict]:
	"""The setup's waste types: each with its share, its default wastes (kept on every request) and the
	wastes the producer may add (those of the type and its sub-types)."""
	out = []
	for dist in frappe.get_all(
		"Waste Distribution",
		filters={"parent": configuration, "parenttype": "Service Setup"},
		fields=["waste_type", "distribution_percentage", "default_waste_item"],
		order_by="idx",
	):
		out.append(
			{
				"waste_type": dist.waste_type,
				"label": _(dist.waste_type),
				"percentage": flt(dist.distribution_percentage),
				"defaults": [
					{"value": name, "label": _(name)} for name in split_wastes(dist.default_waste_item)
				],
				"wastes": [{"value": name, "label": _(name)} for name in get_wastes(dist.waste_type)],
			}
		)
	return out


def _documents(facility: str, service_type: str) -> dict:
	"""The documents the service requires (Service → Registration Documents), and the facility's one that
	answers them already, if any: then the form only shows it."""
	required = registration_documents(service_type)
	on_file = facility_document(facility, service_type) if required else None
	return {
		"required": _document_types([(row.credential_type, row.document_type) for row in required]),
		"on_file": on_file
		and {
			"credential_type": on_file.credential_type,
			"document_type": on_file.document_type,
			"label": _(on_file.document_type),
			"document_number": on_file.document_number,
			"expiry_date": on_file.expiry_date,
		},
	}


def _annexes(site, producer: frappe._dict) -> list[dict]:
	"""A composite facility's annexes (its child facilities, the producer's own), in the tree's order."""
	if not site.is_group:
		return []
	owned = set(owned_names("Facility", producer))
	return [
		{"value": row.name, "label": row.facility_name}
		for row in frappe.get_all(
			"Facility",
			filters={"parent_facility": site.name},
			fields=["name", "facility_name"],
			order_by="lft",
		)
		if row.name in owned
	]


def _service(service_type: str | None) -> frappe._dict:
	service = service_type and frappe.db.get_value(
		"Service",
		service_type,
		["name", "grants_license", "is_milestone_based"],
		as_dict=True,
	)
	if not service:
		frappe.throw(_("Choose a service from the list."))
	return service


def _labels(doctype: str, names: list[str | None], field: str) -> dict[str, str]:
	names = [name for name in set(names) if name]
	if not names:
		return {}
	return dict(
		frappe.get_all(doctype, filters={"name": ["in", names]}, fields=["name", field], as_list=True)
	)
