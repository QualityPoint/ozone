"""A record's comments with Ozone's team: a Service Request while it requires clarification, a Service
Quotation the producer is answering. Desk users write in the form's comment box; the producer writes here.
Both are Frappe Comments of type Comment on the record, so the Desk shows the producer's in its timeline.
The producer's files go with its comment: attached to the record (the Desk lists them in its attachments)
and linked in the comment, up to the record's DocType's Max Attachments."""

from urllib.parse import unquote

import frappe
from bs4 import BeautifulSoup
from frappe import _
from frappe.utils import cint, cstr, escape_html, get_fullname

LIMIT = 4000


def thread(doc) -> list[dict]:
	"""The record's comments, oldest first, as plain text with their files: the producer's own, and the
	team's (desk users, whose names aren't shown)."""
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
	return [_comment(doc, row, row.owner in staff) for row in rows]


def _comment(doc, row, from_team: bool) -> dict:
	"""One comment: its text, and the files it links to that are attached to the record and that the
	producer may open (its own, or a public one; not the team's private files)."""
	soup = BeautifulSoup(row.content or "", "html.parser")
	attachments = []
	for link in soup.find_all("a", href=True):
		file = _attached_file(doc, link["href"])
		if file:
			attachments.append({"name": file.file_name, "url": file.file_url})
			link.decompose()
	return {
		"name": row.name,
		"text": soup.get_text("\n").strip(),
		"from_team": from_team,
		"creation": row.creation,
		"attachments": attachments,
	}


def _attached_file(doc, url: str):
	name = frappe.db.get_value(
		"File",
		{
			"file_url": ["in", list({url, unquote(url)})],
			"attached_to_doctype": doc.doctype,
			"attached_to_name": doc.name,
		},
	)
	file = name and frappe.get_doc("File", name)
	return file if file and file.is_downloadable() else None


def post(doc, text: str | None, files: list[str] | None = None):
	"""The producer's comment on one of its records (the caller decides whether it may write now): its
	text, and the files it uploaded for it (Frappe's upload_file), attached to the record."""
	text = cstr(text).strip()
	files = _own_files(files or [])
	if not text and not files:
		frappe.throw(_("Write your answer."))
	if len(text) > LIMIT:
		frappe.throw(_("Keep your answer under {0} characters.").format(LIMIT))
	left = attachments_left(doc)
	if left is not None and len(files) > left:
		frappe.throw(_("You can attach {0} more files here.").format(left))
	for file in files:
		file.attached_to_doctype, file.attached_to_name = doc.doctype, doc.name
		file.save(ignore_permissions=True)
	links = "".join(
		f'<p><a href="{escape_html(file.file_url)}" target="_blank">{escape_html(file.file_name)}</a></p>'
		for file in files
	)
	doc.add_comment(
		"Comment",
		escape_html(text).replace("\n", "<br>") + links,
		comment_email=frappe.session.user,
		comment_by=get_fullname(frappe.session.user),
	)


def attachments_left(doc) -> int | None:
	"""How many more files the record takes: its DocType's Max Attachments less every file attached to it
	(File.validate_attachment_limit's count, which Frappe checks only when a file is inserted attached;
	ours are attached after their upload), or None when the DocType sets no limit."""
	limit = cint(frappe.get_meta(doc.doctype).max_attachments)
	if not limit:
		return None
	attached = frappe.db.count("File", {"attached_to_doctype": doc.doctype, "attached_to_name": doc.name})
	return max(limit - attached, 0)


def _own_files(urls: list[str]) -> list:
	"""The files this user uploaded and hasn't attached to a record yet, so a comment can't take someone
	else's file, or one already on another record."""
	urls = list(dict.fromkeys(cstr(url).strip() for url in urls if cstr(url).strip()))
	files = []
	for url in urls:
		name = frappe.db.get_value(
			"File",
			{
				"file_url": url,
				"owner": frappe.session.user,
				"is_folder": 0,
				"attached_to_doctype": ["is", "not set"],
			},
		)
		if not name:
			frappe.throw(_("Upload the file first."), frappe.PermissionError)
		files.append(frappe.get_doc("File", name))
	return files
