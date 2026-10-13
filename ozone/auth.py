"""Authentication rules for the Ozone website (frontend/ SPA); its endpoints are in
api/auth.py.

The SPA's login pages replace Frappe's /login (website_route_rules in hooks.py) and use
Frappe's own endpoints for password login, password reset and email login links. The website
has no client accounts: after logging in, staff go to the Desk.
"""

import frappe
from frappe.utils.oauth import get_oauth_keys
from frappe.utils.password import get_decrypted_password


def enabled_providers() -> list[frappe._dict]:
	"""Social Login Keys that are enabled and fully configured (the same checks as Frappe's
	/login)."""
	providers = frappe.get_all(
		"Social Login Key",
		filters={"enable_social_login": 1},
		fields=["name", "provider_name", "client_id", "base_url"],
		order_by="name",
	)
	return [
		provider
		for provider in providers
		if provider.client_id
		and provider.base_url
		and get_decrypted_password("Social Login Key", provider.name, "client_secret", raise_exception=False)
		and get_oauth_keys(provider.name)
	]
