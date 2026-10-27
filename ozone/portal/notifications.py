"""The producer's notifications (docs/producer_dashboard/notifications.md): the Alerts written for its user
(ozone/notifications.py), newest first, and marking them read. Only the session user's own."""

import frappe

from ozone.notifications import SECTIONS

LIMIT = 30


def _filters() -> dict:
	return {"for_user": frappe.session.user, "type": "Alert", "document_type": ["in", list(SECTIONS)]}


def get_notifications(producer: frappe._dict) -> dict:
	"""`{unread, items: [{name, subject, doctype, docname, section, read, creation}]}`: the latest ones."""
	items = frappe.get_all(
		"Notification Log",
		filters=_filters(),
		fields=["name", "subject", "document_type", "document_name", "link", "read", "creation"],
		order_by="creation desc",
		limit=LIMIT,
	)
	return {
		"unread": frappe.db.count("Notification Log", {**_filters(), "read": 0}),
		"items": [
			{
				"name": row.name,
				"subject": row.subject,
				"doctype": row.document_type,
				"docname": row.document_name,
				"section": row.link or SECTIONS.get(row.document_type),
				"read": bool(row.read),
				"creation": row.creation,
			}
			for row in items
		],
	}


def mark_read(producer: frappe._dict, names: list[str] | None = None) -> dict:
	"""Mark the given notifications read, or all of them; only the user's own."""
	filters = {**_filters(), "read": 0}
	if names:
		filters["name"] = ["in", names]
	for name in frappe.get_all("Notification Log", filters=filters, pluck="name"):
		frappe.db.set_value("Notification Log", name, "read", 1, update_modified=False)
	return get_notifications(producer)
