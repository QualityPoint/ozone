"""The dashboard's first page (docs/producer_dashboard/api.md): the producer, how many records it has, what waits for
it (next steps: a contract to pay, a quotation to answer, a clarification to give, a draft to submit), where each
stage of its journey stands (facility, request, quotation, contract: the latest of each) and its latest contracts.
The counts are those each page lists."""

import frappe
from frappe import _
from frappe.utils import flt
from naqel.naqel_contracting.doctype.service_quotation.service_quotation import (
	CLIENT_STATUSES,
)
from naqel.utils.contract.contract_status import (
	AWAITING_PAYMENT,
)

from ozone.portal import (
	status_color,
)
from ozone.portal.contracts import (
	get_contracts,
)
from ozone.producer import (
	owned_names,
)

# The contracts the page lists; the Contracts page has them all
LATEST_CONTRACTS = 3


def get_overview(producer: frappe._dict) -> dict:
	facilities = frappe.get_all(
		"Facility",
		filters={"name": ["in", owned_names("Facility", producer) or [""]]},
		fields=["name", "facility_name", "region"],
		order_by="creation desc",
	)
	requests = frappe.get_all(
		"Service Request",
		filters={"name": ["in", owned_names("Service Request", producer) or [""]]},
		fields=["name", "service_type", "facility", "status"],
		order_by="creation desc",
	)
	quotations = frappe.get_all(
		"Service Quotation",
		filters={
			"name": ["in", owned_names("Service Quotation", producer) or [""]],
			"status": ["in", CLIENT_STATUSES],
			"docstatus": 0,
		},
		fields=["name", "service_type", "facility", "status", "rounded_total", "grand_total", "currency"],
		order_by="creation desc",
	)
	contracts = get_contracts(producer)

	services = _titles("Service", [row.service_type for row in requests + quotations], "service_name")
	facility_titles = {row.name: row.facility_name or row.name for row in facilities}
	for row in requests + quotations:
		row.service_title = _(services.get(row.service_type) or row.service_type or "")
		row.facility_title = facility_titles.get(row.facility) or row.facility

	return {
		"producer": {"doctype": producer.doctype, "name": producer.name, "title": producer.title},
		"counts": {
			"facilities": len(facilities),
			"service_requests": len(requests),
			"quotations": len(quotations),
			"contracts": len(contracts),
		},
		"next_steps": _next_steps(facilities, requests, quotations, contracts),
		"stages": {
			"facilities": _facility_stage(facilities[0]) if facilities else None,
			"requests": _stage(requests[0], "Service Request") if requests else None,
			"quotations": _stage(quotations[0], "Service Quotation") if quotations else None,
			"contracts": _contract_stage(contracts[0]) if contracts else None,
		},
		"contracts": contracts[:LATEST_CONTRACTS],
	}


def _next_steps(facilities, requests, quotations, contracts) -> list[dict]:
	"""What waits for the producer, the most pressing first (a contract to pay, a contract to sign, a quotation to
	answer, a clarification, a draft): `{kind, section, name, title, facility}`, a payment's
	`payment` (as get_contracts gives it) and a quotation's `amount` and `currency`. A new producer is pointed to its
	first facility, then to its first request."""
	steps = [
		{
			"kind": "payment",
			"section": "contracts",
			"name": entry["contract"]["name"],
			"title": entry["service_title"],
			"facility": entry["facility_title"],
			"payment": entry["contract"]["payment"],
		}
		for entry in contracts
		if entry["contract"] and entry["contract"]["status"] == AWAITING_PAYMENT
	]
	steps += [
		{
			"kind": "sign",
			"section": "contracts",
			"name": entry["contract"]["name"],
			"title": entry["service_title"],
			"facility": entry["facility_title"],
		}
		for entry in contracts
		if entry["contract"] and entry["contract"]["can_sign"]
	]
	steps += [
		{
			"kind": "quotation",
			"section": "quotations",
			"name": row.name,
			"title": row.service_title,
			"facility": row.facility_title,
			"amount": flt(row.rounded_total) or flt(row.grand_total),
			"currency": row.currency,
		}
		for row in quotations
		if row.status == "Open"
	]
	for kind, status in (("clarification", "Require Clarification"), ("draft", "Draft")):
		steps += [
			{
				"kind": kind,
				"section": "requests",
				"name": row.name,
				"title": row.service_title,
				"facility": row.facility_title,
			}
			for row in requests
			if row.status == status
		]
	if not facilities:
		steps.append({"kind": "facility", "section": "facilities"})
	elif not requests:
		steps.append({"kind": "request", "section": "requests"})
	return steps


def _facility_stage(facility) -> dict:
	region = facility.region and frappe.db.get_value("Region", facility.region, "region_name")
	return {"title": facility.facility_name or facility.name, "detail": region or None}


def _stage(row, doctype: str) -> dict:
	return {
		"title": row.service_title,
		"detail": row.facility_title,
		"status_label": _(row.status),
		"status_color": status_color(doctype, row.status),
	}


def _contract_stage(entry: dict) -> dict:
	contract = entry["contract"]
	return {
		"title": entry["service_title"] or (contract and contract["name"]),
		"detail": entry["facility_title"] or None,
		# None while the team prepares it
		"status_label": contract and contract["status_label"],
		"status_color": contract and contract["status_color"],
	}


def _titles(doctype: str, names: list[str], field: str) -> dict:
	names = list({name for name in names if name})
	if not names:
		return {}
	return dict(
		frappe.get_all(doctype, filters={"name": ["in", names]}, fields=["name", field], as_list=True)
	)
