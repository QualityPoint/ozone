"""The producer's contracts (docs/producer_dashboard/api.md): each quotation it accepted that the team has
submitted, and each request the team contracts straight away (its Service allows it), with the Service Contract that
follows it ("being prepared" until the team issues one), and any other contract of its Customer. Read only. A
contract still in Draft, or cancelled, is the team's and isn't shown."""

import frappe
from frappe import _
from frappe.utils import cint, flt
from naqel.utils.service_term import (
	has_end_date,
)

from ozone.portal import status_color
from ozone.producer import owned_names

HIDDEN_STATUSES = ("Draft", "Cancelled")
CONTRACT_FIELDS = [
	"name",
	"status",
	"contract_date",
	"start_date",
	"end_date",
	"service_term",
	"net_total",
	"currency",
	"document_type",
	"document_name",
]


def get_contracts(producer: frappe._dict) -> list[dict]:
	"""Newest first: `{quotation, service_title, facility_title, amount, currency, start_date, end_date,
	contract}`, with no end date for a service without one. `quotation` is None for a contract that follows none of the producer's
	quotations, and `contract` None while the team prepares it."""
	quotations = frappe.get_all(
		"Service Quotation",
		filters={"name": ["in", owned_names("Service Quotation", producer) or [""]], "docstatus": 1},
		fields=[
			"name",
			"service_type",
			"facility",
			"rounded_total",
			"grand_total",
			"currency",
			"start_date",
			"end_date",
			"service_term",
		],
		order_by="modified desc",
	)
	names = [q.name for q in quotations] or [""]
	issued = _issued("Service Quotation", names)
	entries = [
		_entry(
			quotation=q.name,
			service_type=q.service_type,
			facility=q.facility,
			amount=flt(q.rounded_total) or flt(q.grand_total),
			currency=q.currency,
			start_date=q.start_date,
			end_date=q.end_date,
			service_term=q.service_term,
			contract=issued.get(q.name),
		)
		for q in quotations
	]

	# The requests the team contracts straight away: listed from their contract's draft on
	direct = frappe.get_all(
		"Service Contract",
		filters={
			"document_type": "Service Request",
			"document_name": ["in", owned_names("Service Request", producer) or [""]],
			"docstatus": ["<", 2],
		},
		pluck="document_name",
	)
	requests = frappe.get_all(
		"Service Request",
		filters={"name": ["in", direct or [""]]},
		fields=["name", "service_type", "facility", "start_date", "end_date", "service_term"],
		order_by="modified desc",
	)
	contracted = _issued("Service Request", [r.name for r in requests] or [""])
	for request in requests:
		contract = contracted.get(request.name)
		entries.append(
			_entry(
				quotation=None,
				service_type=request.service_type,
				facility=request.facility,
				amount=flt(contract.net_total) if contract else 0,
				currency=contract.currency if contract else None,
				start_date=request.start_date,
				end_date=request.end_date,
				service_term=request.service_term,
				contract=contract,
			)
		)
	listed = {("Service Quotation", name) for name in names} | {("Service Request", r.name) for r in requests}

	# The Customer's other contracts, made without one of these quotations or requests
	for contract in frappe.get_all(
		"Service Contract",
		filters={
			"name": ["in", owned_names("Service Contract", producer) or [""]],
			"status": ["not in", HIDDEN_STATUSES],
		},
		fields=CONTRACT_FIELDS,
		order_by="creation desc",
	):
		if (contract.document_type, contract.document_name) in listed:
			continue  # listed with its quotation or request above
		entries.append(
			_entry(
				quotation=None,
				service_type=None,
				facility=None,
				amount=flt(contract.net_total),
				currency=contract.currency,
				start_date=contract.start_date,
				end_date=contract.end_date,
				service_term=contract.service_term,
				contract=contract,
			)
		)
	return entries


def _issued(document_type: str, names: list[str]) -> dict:
	"""The issued contracts (not Draft nor Cancelled) following these documents, by document."""
	return {
		row.document_name: row
		for row in frappe.get_all(
			"Service Contract",
			filters={
				"document_type": document_type,
				"document_name": ["in", names],
				"status": ["not in", HIDDEN_STATUSES],
				"docstatus": ["<", 2],
			},
			fields=CONTRACT_FIELDS,
			order_by="creation asc",  # the newest wins
		)
	}


def count_contracts(producer: frappe._dict) -> int:
	"""The overview's count: what the Contracts page lists."""
	return len(get_contracts(producer))


def _entry(
	*, quotation, service_type, facility, amount, currency, start_date, end_date, service_term, contract
):
	return {
		"quotation": quotation,
		"service_title": _(frappe.db.get_value("Service", service_type, "service_name") or service_type)
		if service_type
		else "",
		"facility_title": (frappe.db.get_value("Facility", facility, "facility_name") or facility)
		if facility
		else "",
		"amount": amount,
		"currency": currency,
		"start_date": start_date,
		"end_date": end_date if has_end_date(service_term) else None,
		"contract": contract
		and {
			"name": contract.name,
			"status": contract.status,
			"status_label": _(contract.status),
			"status_color": status_color("Service Contract", contract.status),
			"contract_date": contract.contract_date,
		},
	}
