"""The website SPA's server side (ozone/www/frontend.py): addresses and SEO, which must
follow the SPA's own rules (frontend/src/config/site.ts) and texts (meta.json)."""

from urllib.parse import urlsplit

import frappe
from frappe.tests import IntegrationTestCase
from frappe.website.path_resolver import resolve_redirect

from ozone.locales import shared_json
from ozone.www import sitemap
from ozone.www.frontend import localized_path, resolve_page, seo_context


class TestFrontendAddresses(IntegrationTestCase):
	def test_localized_path(self):
		self.assertEqual(localized_path("/", "ar"), "/")
		self.assertEqual(localized_path("/x", "ar"), "/x")
		self.assertEqual(localized_path("/", "en"), "/en")
		self.assertEqual(localized_path("/x", "en"), "/en/x")

	def test_resolve_page(self):
		self.assertEqual(resolve_page("/"), ("landing", "ar", "/"))
		self.assertEqual(resolve_page("/en"), ("landing", "en", "/"))
		self.assertEqual(resolve_page("/capabilities"), ("capabilities", "ar", "/capabilities"))
		self.assertEqual(resolve_page("/en/capabilities"), ("capabilities", "en", "/capabilities"))
		self.assertEqual(resolve_page("/english"), (None, "ar", "/english"))  # not the /en prefix
		self.assertEqual(resolve_page("/en/nothing"), (None, "en", "/nothing"))


class TestFrontendSeo(IntegrationTestCase):
	def test_landing_in_each_language(self):
		meta = shared_json("meta.json")
		for path, lang, direction in (("/", "ar", "rtl"), ("/en", "en", "ltr")):
			seo = seo_context(path)
			self.assertEqual((seo["lang"], seo["dir"]), (lang, direction))
			self.assertEqual(seo["title"], meta[lang]["landing"]["title"])
			self.assertEqual(seo["site_name"], meta["site"][lang])
			self.assertIsNone(seo["robots"])
			self.assertTrue(seo["canonical"].endswith(path if path != "/" else ""))
			hreflangs = {alt["hreflang"]: alt["href"] for alt in seo["alternates"]}
			self.assertEqual(set(hreflangs), {"ar", "en", "x-default"})
			self.assertEqual(hreflangs["x-default"], hreflangs["ar"])

	def test_unknown_page_is_not_indexed(self):
		seo = seo_context("/en/nothing")
		self.assertEqual(seo["robots"], "noindex, nofollow")
		self.assertEqual(seo["alternates"], [])


class TestFrappePagesRedirect(IntegrationTestCase):
	def test_about_and_contact_go_to_the_landing_sections(self):
		for path, target in (("about", "/#about"), ("contact", "/#contact")):
			frappe.cache.hdel("website_redirects", path)
			with self.assertRaises(frappe.Redirect):
				resolve_redirect(path)
			self.assertEqual(frappe.flags.redirect_location, target)


class TestSitemap(IntegrationTestCase):
	def test_lists_the_spa_in_each_language_without_redirected_pages(self):
		links = {urlsplit(link["loc"]).path: link for link in sitemap.get_context(frappe._dict())["links"]}
		for page in ("/", "/en", "/capabilities", "/en/capabilities"):
			self.assertIn(page, links)
		self.assertNotIn("/about", links)
		self.assertNotIn("/contact", links)
		hreflangs = {alt["hreflang"] for alt in links["/en"]["alternates"]}
		self.assertEqual(hreflangs, {"ar", "en", "x-default"})
