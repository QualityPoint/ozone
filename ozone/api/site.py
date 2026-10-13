"""The website's public data, for the SPA's dev server (production gets it in the page's boot
data, www/frontend.py)."""

import frappe

from ozone.site_contact import site_contact


@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_site_contact() -> dict:
	"""Email, phone, WhatsApp, address, map link and published social links (Ozone Settings)."""
	return site_contact()
