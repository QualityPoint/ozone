"""The producer's establishment: its own Lead or Customer (docs/producer_dashboard/api.md).

A producer edits only what describes its business: industry, market segment and website. The name,
the customer type and group, and the territory stay with the transporter (access.md), so they are
shown read-only."""

import frappe
from frappe import _
from frappe.utils import cstr

from ozone.portal import pick

EDITABLE = ("industry", "market_segment", "website")
# Shown, never changed here; the Customer-only ones are absent for a Lead.
READ_ONLY = {
	"Lead": ("company_name", "territory"),
	"Customer": ("customer_type", "customer_group", "territory"),
}
# The Links a producer picks from, and the DocType each lists.
OPTIONS = {"industry": "Industry Type", "market_segment": "Market Segment"}


def get_establishment(producer: frappe._dict) -> dict:
	party = frappe.get_doc(producer.doctype, producer.name)
	return {
		"doctype": producer.doctype,
		"title": producer.title,
		**{field: party.get(field) for field in READ_ONLY[producer.doctype]},
		**{field: party.get(field) for field in EDITABLE},
		"options": {field: _options(doctype) for field, doctype in OPTIONS.items()},
	}


def update_establishment(producer: frappe._dict, data: dict) -> dict:
	values = pick(data, EDITABLE)
	for field, doctype in OPTIONS.items():
		if values.get(field) and not frappe.db.exists(doctype, values[field]):
			frappe.throw(_("Choose a {0} from the list.").format(_(doctype)))
	if "website" in values:
		values["website"] = cstr(values["website"]).strip()
	party = frappe.get_doc(producer.doctype, producer.name)
	party.update({field: value or None for field, value in values.items()})
	party.save(ignore_permissions=True)
	return get_establishment(producer)


def _options(doctype: str) -> list[dict]:
	"""Every record of a small master (Industry Type, Market Segment), translated for the page."""
	return [
		{"value": name, "label": _(name)} for name in frappe.get_all(doctype, pluck="name", order_by="name")
	]
