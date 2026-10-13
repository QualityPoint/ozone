"""The login pages' endpoints (ozone/api/auth.py) and the route that replaces Frappe's /login."""

import frappe
from frappe.tests import IntegrationTestCase

from ozone.api.auth import get_login_options, get_session_user, social_login


class TestAuthEndpoints(IntegrationTestCase):
	def test_session_user(self):
		frappe.set_user("Guest")
		self.assertEqual(get_session_user(), {"name": "Guest", "user_type": None})
		frappe.set_user("Administrator")
		self.assertEqual(get_session_user(), {"name": "Administrator", "user_type": "System User"})

	def test_login_options(self):
		options = get_login_options()
		self.assertEqual(
			set(options),
			{"password_login", "login_with_username", "login_with_mobile", "email_link", "providers"},
		)
		self.assertIsInstance(options["providers"], list)

	def test_social_login_refuses_unknown_providers(self):
		with self.assertRaises(frappe.PermissionError):
			social_login("no-such-provider")


class TestLoginRoute(IntegrationTestCase):
	def test_login_pages_are_the_spa(self):
		rules = {rule["from_route"]: rule["to_route"] for rule in frappe.get_hooks("website_route_rules")}
		self.assertEqual(rules.get("/login"), "frontend")
		self.assertEqual(rules.get("/forgot-password"), "frontend")
