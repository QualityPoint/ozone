"""The producer's contracts (docs/producer_dashboard/api.md): each quotation it accepted that the team has
submitted, with the Service Contract that follows it ("being prepared" until the team issues one), and any other
contract of its Customer. Read only. A contract still in Draft, or cancelled, is the team's and isn't shown."""

import frappe
from frappe import _
from frappe.utils import cint, flt

from ozone.producer import owned_names

HIDDEN_STATUSES = ("Draft", "Cancelled")
CONTRACT_FIELDS = [
	"name",
	"status",
	"contract_date",
	"start_date",
	"end_date",
	"is_milestone_based",
	"net_total",
	"currency",
	"service_quotation",
]


def get_contracts(producer: frappe._dict) -> list[dict]:
	"""Newest first: `{quotation, service_title, facility_title, amount, currency, start_date, end_date,
	milestone_based, contract}`. `quotation` is None for a contract that follows none of the producer's
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
			"is_milestone_based",
		],
		order_by="modified desc",
	)
	names = [q.name for q in quotations] or [""]
	issued = {
		row.service_quotation: row
		for row in frappe.get_all(
			"Service Contract",
			filters={
				"service_quotation": ["in", names],
				"status": ["not in", HIDDEN_STATUSES],
				"docstatus": ["<", 2],
			},
			fields=CONTRACT_FIELDS,
			order_by="creation asc",  # the newest wins
		)
	}
	entries = [
		_entry(
			quotation=q.name,
			service_type=q.service_type,
			facility=q.facility,
			amount=flt(q.rounded_total) or flt(q.grand_total),
			currency=q.currency,
			start_date=q.start_date,
			end_date=q.end_date,
			milestone_based=q.is_milestone_based,
			contract=issued.get(q.name),
		)
		for q in quotations
	]

	# The Customer's other contracts, made without one of these quotations
	for contract in frappe.get_all(
		"Service Contract",
		filters={
			"name": ["in", owned_names("Service Contract", producer) or [""]],
			"status": ["not in", HIDDEN_STATUSES],
		},
		fields=CONTRACT_FIELDS,
		order_by="creation desc",
	):
		if contract.service_quotation in names:
			continue  # listed with its quotation above
		entries.append(
			_entry(
				quotation=None,
				service_type=None,
				facility=None,
				amount=flt(contract.net_total),
				currency=contract.currency,
				start_date=contract.start_date,
				end_date=contract.end_date,
				milestone_based=contract.is_milestone_based,
				contract=contract,
			)
		)
	return entries


def count_contracts(producer: frappe._dict) -> int:
	"""The overview's count: what the Contracts page lists."""
	return len(get_contracts(producer))


def _entry(
	*, quotation, service_type, facility, amount, currency, start_date, end_date, milestone_based, contract
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
		"end_date": None if cint(milestone_based) else end_date,
		"milestone_based": cint(milestone_based),
		"contract": contract
		and {
			"name": contract.name,
			"status": contract.status,
			"status_label": _(contract.status),
			"contract_date": contract.contract_date,
		},
	}
