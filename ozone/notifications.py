"""The producer's notifications in its dashboard (docs/producer_dashboard/notifications.md): Frappe's Notification Log of
type Alert, which is never e-mailed, for each website user of the party a record belongs to (producer.party_users), in
that user's language. Written by document hooks (hooks.py doc_events) when Ozone's team acts on the producer's records:

- a quotation sent to them (Open), waiting for their answer;
- a Service Request they are asked to clarify;
- a contract awaiting their payment (its Sales Order submitted, its Service requiring one);
- a payment received against a contract's Sales Order;
- a contract issued (submitted) or renewed."""

import frappe
from frappe import _
from frappe.utils import flt

from ozone.producer import party_users

# The dashboard section each notified record opens in (the frontend's localized path)
SECTIONS = {
	"Service Quotation": "quotations",
	"Service Request": "requests",
	"Service Contract": "contracts",
}


def notify(party_type: str, party: str, doctype: str, name: str, message):
	"""An Alert for each of the party's website users; `message(lang)` is its text in that user's language."""
	default = frappe.db.get_default("lang") or "en"
	for user in party_users(party_type, party):
		lang = frappe.db.get_value("User", user, "language") or default
		frappe.get_doc(
			{
				"doctype": "Notification Log",
				"type": "Alert",
				"for_user": user,
				"from_user": frappe.session.user,
				"subject": message(lang),
				"document_type": doctype,
				"document_name": name,
				"link": SECTIONS[doctype],
			}
		).insert(ignore_permissions=True)


def _money(amount: float, currency: str | None) -> str:
	return frappe.format(flt(amount), {"fieldtype": "Currency", "options": currency})


def _became(doc, field: str, value: str) -> bool:
	"""The document's field became `value` on this save."""
	before = doc.get_doc_before_save()
	return doc.get(field) == value and (not before or before.get(field) != value)


def quotation_sent(quotation, method=None):
	"""Service Quotation on_update: sent to the client (Open), waiting for their answer."""
	if _became(quotation, "status", "Open"):
		notify(
			quotation.quotation_to,
			quotation.party_name,
			quotation.doctype,
			quotation.name,
			lambda lang: _("Quotation {0} is ready for your answer.", lang=lang).format(quotation.name),
		)


def clarification_asked(request, method=None):
	"""Service Request on_update_after_submit: Ozone's team asks the client to clarify it."""
	if _became(request, "status", "Require Clarification"):
		notify(
			request.request_from,
			request.party,
			request.doctype,
			request.name,
			lambda lang: _("Ozone's team asks you to clarify request {0}.", lang=lang).format(request.name),
		)


def contract_awaits_payment(order, method=None):
	"""Sales Order on_submit: the contract it was made from awaits the client's payment (naqel's link_sales_order has
	made it the contract's)."""
	from naqel.utils.contract.payment_request import amount_to_pay

	if not order.get("service_contract"):
		return
	contract = frappe.get_doc("Service Contract", order.service_contract)
	if contract.docstatus != 0 or (amount := amount_to_pay(contract)) <= 0:
		return
	notify(
		"Customer",
		contract.customer,
		contract.doctype,
		contract.name,
		lambda lang: _("Contract {0} awaits your payment of {1}.", lang=lang).format(
			contract.name, _money(amount, contract.currency)
		),
	)


def payment_received(entry, method=None):
	"""Payment Entry on_submit: a payment received against a contract's Sales Order."""
	if entry.payment_type != "Receive":
		return
	for row in entry.get("references") or []:
		if row.reference_doctype != "Sales Order":
			continue
		contract = frappe.db.get_value("Sales Order", row.reference_name, "service_contract")
		if not contract:
			continue
		customer, currency = frappe.db.get_value("Service Contract", contract, ["customer", "currency"])
		notify(
			"Customer",
			customer,
			"Service Contract",
			contract,
			lambda lang, contract=contract, row=row, currency=currency: _(
				"{0} received for contract {1}. Thank you.", lang=lang
			).format(_money(row.allocated_amount, currency), contract),
		)


def contract_issued(contract, method=None):
	"""Service Contract on_submit: issued."""
	notify(
		"Customer",
		contract.customer,
		contract.doctype,
		contract.name,
		lambda lang: _("Contract {0} has been issued.", lang=lang).format(contract.name),
	)


def contract_renewed(contract, method=None):
	"""Service Contract on_update_after_submit: renewed for a new period (its previous one archived)."""
	before = contract.get_doc_before_save()
	if not before or len(contract.get("contract_records") or []) <= len(before.get("contract_records") or []):
		return
	notify(
		"Customer",
		contract.customer,
		contract.doctype,
		contract.name,
		lambda lang: _("Contract {0} has been renewed.", lang=lang).format(contract.name),
	)
