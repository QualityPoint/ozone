# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class OzoneSettings(Document):
	def validate(self):
		self.map_link = https_link(self.map_link, _("Map Link"))
		unique_rows(self.addresses, "language")
		unique_rows(self.social_media_links, "platform")
		for row in self.social_media_links:
			row.link = https_link(row.link, _("Row {0}: {1} link").format(row.idx, row.platform))


def unique_rows(rows: list, fieldname: str) -> None:
	"""One row per value of `fieldname` (a Select or Link can't be made unique in a child table):
	one address per language, one link per platform."""
	seen = {}
	for row in rows:
		value = row.get(fieldname)
		if value in seen:
			frappe.throw(
				_("Row {0}: {1} is already added in row {2}").format(row.idx, value, seen[value]),
				title=_("Duplicate {0}").format(_(row.meta.get_label(fieldname))),
			)
		seen[value] = row.idx


def https_link(link: str | None, label: str) -> str | None:
	"""`link` trimmed, or an error naming `label` when it isn't a full https URL."""
	link = (link or "").strip() or None
	if link and not frappe.utils.validate_url(link, valid_schemes=["https"]):
		frappe.throw(
			_("{0} must be a full URL starting with https://").format(label),
			title=_("Invalid Link"),
		)
	return link
