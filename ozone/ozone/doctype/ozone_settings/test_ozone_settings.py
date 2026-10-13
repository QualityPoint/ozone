# Copyright (c) 2026, QualityPoint and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


class IntegrationTestOzoneSettings(IntegrationTestCase):
	def settings(self, **values):
		doc = frappe.get_doc("Ozone Settings")
		doc.update({"map_link": None, "addresses": [], "social_media_links": [], **values})
		return doc

	def test_links_must_be_https(self):
		self.assertRaises(frappe.ValidationError, self.settings(map_link="http://maps.example.com").validate)
		doc = self.settings(
			social_media_links=[{"platform": "X", "link": "x.com/ozone"}],
		)
		self.assertRaises(frappe.ValidationError, doc.validate)

	def test_one_row_per_platform(self):
		doc = self.settings(
			social_media_links=[
				{"platform": "X", "link": "https://x.com/a"},
				{"platform": "X", "link": "https://x.com/b"},
			]
		)
		self.assertRaises(frappe.ValidationError, doc.validate)

	def test_one_address_per_language(self):
		doc = self.settings(
			addresses=[
				{"language": "ar", "address": "المدينة المنورة"},
				{"language": "ar", "address": "الرياض"},
			]
		)
		self.assertRaises(frappe.ValidationError, doc.validate)
		self.settings(
			addresses=[
				{"language": "ar", "address": "المدينة المنورة"},
				{"language": "en", "address": "Madinah"},
			]
		).validate()

	def test_links_are_trimmed(self):
		doc = self.settings(
			map_link="  https://maps.example.com/ozone  ",
			social_media_links=[{"platform": "Instagram", "link": " https://instagram.com/ozone "}],
		)
		doc.validate()
		self.assertEqual(doc.map_link, "https://maps.example.com/ozone")
		self.assertEqual(doc.social_media_links[0].link, "https://instagram.com/ozone")
