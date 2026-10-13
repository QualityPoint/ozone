import frappe
import frappe.sessions
from frappe.utils import get_url

from ozone.locales import DEFAULT_LOCALE, SUPPORTED_LOCALES, shared_json

no_cache = 1

# Server-rendered SEO for the SPA shell (index.html's seo block, see
# frontend/vite-plugins/seo-head.ts). Each public page's base path and its title and
# description in each language are the SPA's own (frontend/src/i18n/locales/meta.json), so
# the two never differ. The default language's pages have no prefix ("/"); the others are
# under "/<code>" ("/en"), as in the SPA's config/site.ts.
OG_LOCALE = {"ar": "ar_SA", "en": "en_US"}
RTL_LOCALES = {"ar"}


def page_meta() -> dict:
	"""{"paths": {page: base path}, "site": {language: name}, language: {page: {title, description}}}
	(meta.json)."""
	return shared_json("meta.json")


def localized_path(path: str, lang: str) -> str:
	"""A page's address in `lang` (the SPA's localePath): "/" → "/en", "/x" → "/en/x"."""
	if lang == DEFAULT_LOCALE:
		return path
	return f"/{lang}" if path == "/" else f"/{lang}{path}"


def resolve_page(path: str) -> tuple[str | None, str, str]:
	"""(page key or None, language, base path) for a request path: "/en" → ("landing", "en", "/")."""
	for lang in SUPPORTED_LOCALES:
		if lang != DEFAULT_LOCALE and (path == f"/{lang}" or path.startswith(f"/{lang}/")):
			base = path[len(lang) + 1 :] or "/"
			break
	else:
		lang, base = DEFAULT_LOCALE, path
	page = next((key for key, pattern in page_meta()["paths"].items() if pattern == base), None)
	return page, lang, base


def seo_context(path: str) -> dict:
	"""What index.html's seo block renders. A known page is indexed under each language's own
	address; an unknown one gets the landing page's texts and noindex."""
	page, lang, base = resolve_page(path)
	texts = page_meta()[lang][page or "landing"]
	return {
		"lang": lang,
		"dir": "rtl" if lang in RTL_LOCALES else "ltr",
		"title": texts["title"],
		"description": texts["description"],
		"site_name": page_meta()["site"][lang],
		"og_locale": OG_LOCALE[lang],
		"canonical": get_url(path),
		"robots": None if page else "noindex, nofollow",
		"og_image": get_url("/assets/ozone/frontend/og-image.png"),
		"alternates": _alternates(base) if page else [],
	}


def get_context():
	# get_csrf_token() may generate a new token on the session; GET requests are
	# rolled back unless committed, so persist it before rendering.
	csrf_token = frappe.sessions.get_csrf_token()
	frappe.db.commit()

	context = frappe._dict()
	# Namespaced under `seo`: Frappe's page renderer overwrites top-level keys such as
	# `canonical`, `title` and `lang`.
	context.seo = seo_context(_request_path())
	# Each key is set on `window` by the Jinja loop that frappe-ui's jinjaBootData
	# vite plugin injects into www/frontend.html.
	context.boot = {
		"csrf_token": csrf_token,
		"site_name": frappe.local.site,
	}
	return context


def _alternates(base: str) -> list[dict]:
	"""hreflang links to a public page in every language; x-default is the default language."""
	links = [{"hreflang": lang, "href": get_url(localized_path(base, lang))} for lang in SUPPORTED_LOCALES]
	return [*links, {"hreflang": "x-default", "href": get_url(localized_path(base, DEFAULT_LOCALE))}]


def _request_path() -> str:
	"""The requested path without a trailing slash ("/" for the home page)."""
	path = frappe.request.path if getattr(frappe, "request", None) else "/"
	return path.rstrip("/") or "/"
