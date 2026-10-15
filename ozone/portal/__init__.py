"""What the producer dashboard reads and changes, one module per area (profile, facilities).
Each function takes the producer from ozone.producer.require_producer(), works only on its
records, and sets only allowlisted fields, as Frappe's Web Forms do
(docs/producer_dashboard/access.md). The whitelisted wrappers are in ozone/api/portal.py."""

import frappe
from frappe import _


def pick(data: dict | None, fields: tuple[str, ...]) -> dict:
	"""Only the allowlisted fields of what the client sent."""
	data = data or {}
	return {field: data[field] for field in fields if field in data}


def own_doc(doctype: str, name: str, producer: frappe._dict):
	"""One of the producer's records, or PermissionError (also for a name that doesn't exist, so
	nothing reveals whether another producer's record does)."""
	from ozone.producer import owns

	if not owns(doctype, name, producer):
		frappe.throw(_("Not permitted."), frappe.PermissionError)
	return frappe.get_doc(doctype, name)
