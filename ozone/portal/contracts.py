"""The producer's contracts (docs/producer_dashboard/api.md): each quotation it accepted that the team has
submitted, and each request the team contracts straight away (its Service allows it), with the Service Contract that
follows it ("being prepared" until the team issues one), and any other contract of its Customer. A contract still in
Draft is the team's and isn't shown, unless it awaits the producer's payment (its Service requires an advance or a full
payment, and its Sales Order is submitted): the producer pays it here (pay_contract), online through its Payment
Request. A cancelled one isn't shown."""

import frappe
from frappe import _
from frappe.utils import cint, flt
from naqel.utils.contract.contract_status import (
	AWAITING_PAYMENT,
	PAYMENT_STATUSES,
)
from naqel.utils.contract.payment_request import (
	amount_to_pay,
	can_pay_online,
	contract_payment_url,
)
from naqel.utils.contract.sales_order import (
	received_payment,
	required_payment,
)
from naqel.utils.service_term import (
	has_end_date,
)

from ozone.portal import own_doc, status_color
from ozone.producer import owned_names

# A draft awaiting the producer's payment, or with it received while the team issues it, has a status of its own
# (naqel's contract_status.PAYMENT_STATUSES) and shows
HIDDEN_STATUSES = ("Draft", "Cancelled")
CONTRACT_FIELDS = [
	"name",
	"docstatus",
	"status",
	"company",
	"sales_order",
	"payment_requirement",
	"advance_payment_percentage",
	"rounded_total",
	"grand_total",
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
		filters={"name": ["in", owned_names("Service Contract", producer) or [""]], "docstatus": ["<", 2]},
		fields=CONTRACT_FIELDS,
		order_by="creation desc",
	):
		if not _shown(contract) or (contract.document_type, contract.document_name) in listed:
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


def _shown(contract) -> bool:
	"""Issued, or a draft taking the producer's payment (Awaiting Payment, Payment Received): not a plain Draft, nor
	Cancelled."""
	return contract.status not in HIDDEN_STATUSES


def _pays_first(contract) -> bool:
	"""A draft whose Service requires a payment before it is issued, with its Sales Order submitted: the producer pays
	it here, and sees it received while the team issues the contract."""
	return contract.docstatus == 0 and contract.status in PAYMENT_STATUSES


def _issued(document_type: str, names: list[str]) -> dict:
	"""The contracts the producer sees (_shown) following these documents, by document."""
	return {
		row.document_name: row
		for row in frappe.get_all(
			"Service Contract",
			filters={"document_type": document_type, "document_name": ["in", names], "docstatus": ["<", 2]},
			fields=CONTRACT_FIELDS,
			order_by="creation asc",  # the newest wins
		)
		if _shown(row)
	}


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
		"contract": contract and _contract(contract),
	}


def _contract(contract) -> dict:
	"""A contract as the producer sees it; a draft taking its payment says how much, and whether it pays online."""
	pays_first = _pays_first(contract)
	return {
		"name": contract.name,
		"status": contract.status,
		"status_label": _(contract.status),
		"status_color": status_color("Service Contract", contract.status),
		"contract_date": contract.contract_date,
		"payment": pays_first
		and {
			"requirement": contract.payment_requirement,
			"requirement_label": _(contract.payment_requirement),
			"required": required_payment(contract),
			"received": received_payment(contract),
			"to_pay": amount_to_pay(contract),
			"currency": contract.currency,
			"can_pay_online": contract.status == AWAITING_PAYMENT and can_pay_online(contract),
		},
	}


def pay_contract(producer: frappe._dict, name: str) -> dict:
	"""The checkout the producer pays its contract's required payment at (`{url}`): its Payment Request's, made for
	what is still required (naqel.utils.contract.payment_request)."""
	contract = own_doc("Service Contract", name, producer)
	if not can_pay_online(contract):
		frappe.throw(_("This contract can't be paid online."), title=_("No Online Payment"))
	return {"url": contract_payment_url(contract.name)}
