"""Contact details the website shows (ozone/site_contact.py), from Ozone Settings."""

import frappe
from frappe.tests import IntegrationTestCase

from ozone.site_contact import site_contact


class TestSiteContact(IntegrationTestCase):
	def setUp(self):
		settings = frappe.get_doc("Ozone Settings")
		settings.update(
			{
				"email": "info@example.com",
				"contact_phone": "",
				"whatsapp": "+966500000000",
				"addresses": [{"language": "ar", "address": "المدينة المنورة"}],
				"map_link": "https://maps.example.com/ozone",
				"social_media_links": [
					{"platform": "X", "link": "https://x.com/ozone", "published": 1},
					{"platform": "Instagram", "link": "https://instagram.com/ozone", "published": 0},
				],
			}
		)
		settings.save()

	def tearDown(self):
		# Undo the test values, including the cached copy site_contact() reads, so the site's
		# real settings come back.
		frappe.db.rollback()
		frappe.clear_document_cache("Ozone Settings", "Ozone Settings")

	def test_shows_filled_details_and_hides_empty_ones(self):
		contact = site_contact()
		self.assertEqual(contact["email"], "info@example.com")
		self.assertIsNone(contact["phone"])
		self.assertEqual(contact["address"], {"ar": "المدينة المنورة"})
		self.assertEqual(contact["map"], "https://maps.example.com/ozone")

	def test_lists_only_published_socials(self):
		self.assertEqual(site_contact()["socials"], [{"platform": "X", "url": "https://x.com/ozone"}])
