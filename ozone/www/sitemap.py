import re
from urllib.parse import urlsplit

import frappe
from frappe.utils import get_url, nowdate
from frappe.www import sitemap as frappe_sitemap

from ozone.locales import SUPPORTED_LOCALES
from ozone.www.frontend import alternates, localized_path, page_meta

no_cache = 1
base_template_path = "www/sitemap.xml"

# Replaces Frappe's /sitemap.xml (the last installed app's www page wins): the website SPA's
# pages in every language, with their hreflang alternates, then Frappe's own links, minus the
# pages that only redirect (website_redirects: /about, /contact).


def get_context(context):
	links = spa_links()
	links.extend(link for link in frappe_sitemap.get_context(context)["links"] if not redirects(link["loc"]))
	return {"links": links}


def spa_links() -> list[dict]:
	"""Each public page of the SPA (meta.json paths) in each language."""
	return [
		{"loc": get_url(localized_path(base, lang)), "lastmod": nowdate(), "alternates": alternates(base)}
		for base in page_meta()["paths"].values()
		for lang in SUPPORTED_LOCALES
	]


def redirects(url: str) -> bool:
	"""Whether a website_redirects rule matches the URL's path, as Frappe's resolve_redirect does."""
	path = urlsplit(url).path.strip("/")
	return any(
		re.match(rule["source"].strip("/ ") + "$", path) for rule in frappe.get_hooks("website_redirects")
	)
