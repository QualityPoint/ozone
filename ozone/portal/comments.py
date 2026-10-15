"""A record's comments with Ozone's team: a Service Request while it requires clarification, a Service
Quotation the producer is answering. Desk users write in the form's comment box; the producer writes here.
Both are Frappe Comments of type Comment on the record, so the Desk shows the producer's in its timeline."""

import frappe
from bs4 import BeautifulSoup
from frappe import _
from frappe.utils import cstr, escape_html, get_fullname

LIMIT = 4000


def thread(doc) -> list[dict]:
	"""The record's comments, oldest first, as plain text: the producer's own, and the team's (desk users,
	whose names aren't shown)."""
	rows = frappe.get_all(
		"Comment",
		filters={"reference_doctype": doc.doctype, "reference_name": doc.name, "comment_type": "Comment"},
		fields=["name", "content", "owner", "creation"],
		order_by="creation asc",
	)
	staff = set(
		frappe.get_all(
			"User",
			filters={"name": ["in", list({row.owner for row in rows}) or [""]], "user_type": "System User"},
			pluck="name",
		)
	)
	return [
		{
			"name": row.name,
			"text": BeautifulSoup(row.content or "", "html.parser").get_text("\n").strip(),
			"from_team": row.owner in staff,
			"creation": row.creation,
		}
		for row in rows
	]


def post(doc, text: str | None):
	"""The producer's comment on one of its records (the caller decides whether it may write now)."""
	text = cstr(text).strip()
	if not text:
		frappe.throw(_("Write your answer."))
	if len(text) > LIMIT:
		frappe.throw(_("Keep your answer under {0} characters.").format(LIMIT))
	doc.add_comment(
		"Comment",
		escape_html(text).replace("\n", "<br>"),
		comment_email=frappe.session.user,
		comment_by=get_fullname(frappe.session.user),
	)
