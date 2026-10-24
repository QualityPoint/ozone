"""The producer's quotations: what Ozone's team offers for one of its requests, and the producer's answer
(docs/producer_dashboard/api.md).

A Service Quotation is the team's until they send it (Open); the producer sees only Open, Accepted and
Rejected ones (naqel's CLIENT_STATUSES). It shows the amount to pay, each container line's collection
mechanism and frequency, the service period and the waste calculation report. It names a line's
container type only when its collection deploys a container at the facility. The producer accepts or rejects an Open quotation
and reads its comments with the team, but doesn't write there: the reason it gives for a rejection is the one comment
it adds (questions go through the request's clarification)."""

import frappe
from frappe import _
from frappe.utils import cint, flt
from naqel.naqel_contracting.doctype.service_quotation.service_quotation import (
	CLIENT_STATUSES,
	client_waste_report,
)
from naqel.utils.service_term import (
	has_end_date,
)

from ozone.portal import comments, own_doc, status_color
from ozone.producer import owned_names

DECISIONS = ("Accepted", "Rejected")


def request_quotations(producer: frappe._dict, requests: list[str]) -> dict[str, list[dict]]:
	"""The quotations the producer answers, by request: {request: [{name, status, status_label, grand_total,
	currency}]}, newest first. Not the submitted ones: those are on the Contracts page (portal/contracts.py)."""
	if not requests:
		return {}
	out: dict[str, list[dict]] = {}
	for row in frappe.get_all(
		"Service Quotation",
		filters={
			"name": ["in", owned_names("Service Quotation", producer) or [""]],
			"service_request": ["in", requests],
			"status": ["in", CLIENT_STATUSES],
			"docstatus": 0,
		},
		fields=["name", "service_request", "status", "rounded_total", "grand_total", "currency"],
		order_by="creation desc",
	):
		out.setdefault(row.service_request, []).append(
			{
				"name": row.name,
				"status": row.status,
				"status_label": _(row.status),
				"status_color": status_color("Service Quotation", row.status),
				"grand_total": flt(row.rounded_total) or flt(row.grand_total),
				"currency": row.currency,
			}
		)
	return out


def get_quotations(producer: frappe._dict) -> list[dict]:
	"""The producer's requests that have turned into a quotation, newest first: each with the quotations the
	team has sent for it (none yet while the team prepares it). A request whose quotation has been submitted
	has moved on to the Contracts page."""
	from ozone.portal.requests import QUOTED, get_service_requests

	submitted = set(
		frappe.get_all(
			"Service Quotation",
			filters={"name": ["in", owned_names("Service Quotation", producer) or [""]], "docstatus": 1},
			pluck="service_request",
		)
	)
	return [
		request
		for request in get_service_requests(producer, {"status": QUOTED}, include_quoted=True)
		if request.name not in submitted
	]


def count_quotations(producer: frappe._dict) -> int:
	"""How many quotations the team has sent the producer and not yet submitted (the overview's count)."""
	return frappe.db.count(
		"Service Quotation",
		{
			"name": ["in", owned_names("Service Quotation", producer) or [""]],
			"status": ["in", CLIENT_STATUSES],
			"docstatus": 0,
		},
	)


def get_quotation(producer: frappe._dict, name: str) -> dict:
	quotation = _visible(name, producer)
	ends = has_end_date(quotation.service_term)
	return {
		"name": quotation.name,
		"status": quotation.status,
		"status_label": _(quotation.status),
		"status_color": status_color("Service Quotation", quotation.status),
		"service_request": quotation.service_request,
		"service_title": _(
			frappe.db.get_value("Service", quotation.service_type, "service_name") or quotation.service_type
		),
		"facility_title": frappe.db.get_value("Facility", quotation.facility, "facility_name")
		or quotation.facility,
		"transaction_date": quotation.transaction_date,
		"valid_till": quotation.valid_till,
		"period": {
			"start_date": quotation.start_date,
			"end_date": quotation.end_date if ends else None,
			"duration": flt(quotation.service_duration) if ends else None,
			"duration_uom": quotation.duration_uom if ends else None,
		},
		"collections": [_collection(row) for row in quotation.containers],
		"amounts": {
			"currency": quotation.currency,
			"net_total": flt(quotation.net_total),
			"taxes": [
				{"description": _(row.description or row.account_head or ""), "amount": flt(row.tax_amount)}
				for row in quotation.taxes
				if flt(row.tax_amount)
			],
			"discount": flt(quotation.discount_amount) if quotation.apply_discount_on else 0,
			"grand_total": flt(quotation.grand_total),
			"rounded_total": flt(quotation.rounded_total) or flt(quotation.grand_total),
			"in_words": quotation.in_words,
		},
		"report": _report(quotation),
		"can_decide": quotation.status == "Open" and quotation.docstatus == 0,
		"can_reply": False,
		"comments": comments.thread(quotation),
	}


def decide_quotation(producer: frappe._dict, name: str, decision: str, comment: str | None = None) -> dict:
	"""Accept or reject an Open quotation. A rejection says why, in the quotation's comments for the team;
	an acceptance carries no comment."""
	quotation = _visible(name, producer)
	if decision not in DECISIONS:
		frappe.throw(_("Accept or reject the quotation."))
	if decision == "Rejected" and not (comment or "").strip():
		frappe.throw(_("Tell Ozone's team why you reject the quotation."))
	quotation.set_client_decision(decision)
	if decision == "Rejected":
		comments.post(quotation, comment)
	return get_quotation(producer, name)


def get_quotation_thread(producer: frappe._dict, name: str) -> dict:
	"""What the conversation refreshes: the comments, and the status (an answer given, or the quotation
	sent again, changes what the panel shows)."""
	quotation = _visible(name, producer)
	return {
		"status": quotation.status,
		"can_reply": False,
		"comments": comments.thread(quotation),
	}


def _collection(row) -> dict:
	"""How one of the quotation's container lines is collected: its waste type, mechanism and frequency, and
	the container the collection deploys at the facility (its type and count), only when it deploys one."""
	mechanism = (
		frappe.get_cached_value(
			"Collection Mechanism",
			row.collection_mechanism,
			["collection_mechanism_name", "description"],
			as_dict=True,
		)
		if row.collection_mechanism
		else None
	) or frappe._dict()
	deploys = cint(row.requires_container_deployment) and row.collection_container_type
	return {
		"waste_type": _(row.waste_type or ""),
		"mechanism": _(mechanism.collection_mechanism_name or row.collection_mechanism or ""),
		"description": _(mechanism.description or ""),
		"count": cint(row.collection_count) or 1,
		"period_count": cint(row.collection_period_count) or 1,
		"period_uom": row.collection_period_uom or "Day",
		"container": {
			"container_type": _(row.collection_container_type),
			"count": cint(row.collection_container_count),
			"image": frappe.get_cached_value("Container Type", row.collection_container_type, "image"),
		}
		if deploys
		else None,
	}


def _report(quotation) -> str:
	"""The waste calculation report, in the producer's language (naqel renders it when read). A calculation
	that no longer runs (its Service Setup disabled since) leaves the quotation without it, not unreadable."""
	try:
		return client_waste_report(quotation)
	except frappe.ValidationError:
		frappe.clear_messages()
		return ""


def _visible(name: str, producer: frappe._dict):
	"""One of the producer's quotations that the team has sent it, or PermissionError (as for another
	producer's: nothing reveals that a draft exists)."""
	quotation = own_doc("Service Quotation", name, producer)
	if quotation.status not in CLIENT_STATUSES:
		frappe.throw(_("Not permitted."), frappe.PermissionError)
	return quotation
