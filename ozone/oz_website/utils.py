# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import frappe

ACCESSIBILITY_APP = "accessibility"

# Shape of the contact block when the accessibility app is not installed, so
# templates can test `contact.email` etc. without guarding every access.
EMPTY_CONTACT = {
	"email": None,
	"whatsapp": None,
	"whatsappUrl": None,
	"addressLine": None,
	"contactRoute": None,
	"socialLinks": [],
}


def accessibility_installed():
	return ACCESSIBILITY_APP in frappe.get_installed_apps()


def get_contact():
	"""Contact details and social links, from Accessibility Settings when the
	`accessibility` app is installed; empty otherwise (the sections that show
	them simply don't render)."""
	if not accessibility_installed():
		return EMPTY_CONTACT
	from accessibility.utils.toolbar import get_contact as accessibility_contact

	return accessibility_contact()


def get_website_context(context):
	"""Context every ozone www/ page needs.

	Each page's controller is a one-line call to this, so a site-wide addition
	is made once here rather than in thirty files.

	The `accessibility` app is an optional add-on. When present it provides the
	toolbar bar and the single source of contact details / social links (the
	same record that feeds the bar, so header, footer and bar can never
	disagree) and owns language resolution through its before_request hook.
	`context.accessibility` lets templates include its snippets only then.
	Ozone Website Settings keeps only brand assets.
	"""
	context.settings = frappe.get_cached_doc("Ozone Website Settings")
	context.accessibility = accessibility_installed()
	context.contact = get_contact()
	context.year = frappe.utils.now_datetime().year
	# For <html lang>: frappe exposes no bare `lang` to www templates (its own
	# base.html reads boot.lang).
	context.lang = frappe.local.lang

	user = frappe.session.user
	context.is_logged_in = user != "Guest"
	# The field on User is named `user_image`.
	context.user_image_url = frappe.db.get_value("User", user, "user_image") if context.is_logged_in else None
