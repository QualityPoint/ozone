"""Public contact details for the website (frontend/ SPA), from Ozone Settings.

The SPA gets them in its boot data (www/frontend.py → `window.site_contact`), so the footer
renders with no extra request. The dev server has no boot data and calls
`ozone.api.site.get_site_contact` instead.
"""

import frappe


def site_contact() -> dict:
	"""Email, phone, WhatsApp, the address in each language it was written in ({"ar": …}), the
	map link and the published social links, in the table's order.

	Empty values are None, so the page hides them rather than showing stale ones.
	get_cached_doc is cleared whenever the settings are saved.
	"""
	settings = frappe.get_cached_doc("Ozone Settings")
	return {
		"email": settings.email or None,
		"phone": settings.contact_phone or None,
		"whatsapp": settings.whatsapp or None,
		"address": {row.language: row.address for row in settings.addresses if row.language and row.address},
		"map": settings.map_link or None,
		"socials": [
			{"platform": row.platform, "url": row.link}
			for row in settings.social_media_links
			if row.published and row.platform and row.link
		],
	}
