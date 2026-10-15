"""Authentication rules for the Ozone website (frontend/ SPA); its endpoints are in api/auth.py.

The SPA's login pages replace Frappe's /login (website_route_rules in hooks.py) and use Frappe's
own endpoints for password login, password reset and email login links (docs/frontend/auth.md).
Clients (producers) have accounts too: where a login goes is in docs/producer_dashboard/routing.md.

- `get_website_user_home_page`: hook that sends producers (Website Users) to their dashboard
  after any kind of login. Staff (System Users) keep Frappe's default and land in the Desk.
- `enabled_providers`: the social logins that are enabled and fully configured.
- `create_signup_lead`: the Lead a website sign-up makes, before Frappe creates the User.
"""

import frappe
from frappe.contacts.doctype.contact.contact import get_contact_name
from frappe.utils.oauth import get_oauth_keys
from frappe.utils.password import get_decrypted_password

# SPA route producers land on after logging in (frontend/src/router/routes.ts).
PRODUCER_HOME_PAGE = "dashboard"


def get_website_user_home_page(user: str) -> str | None:
	"""Hook (`get_website_user_home_page`): the dashboard for Website Users.

	Returning None keeps Frappe's default, which matters for guests: "/" must still resolve to the
	landing page through the `home_page` hook.
	"""
	if user == "Guest":
		return None
	if frappe.db.get_value("User", user, "user_type") == "Website User":
		return PRODUCER_HOME_PAGE
	return None


def enabled_providers() -> list[frappe._dict]:
	"""Social Login Keys that are enabled and fully configured (same checks as /login)."""
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


def create_signup_lead(email: str, full_name: str) -> str | None:
	"""The Lead behind a website sign-up, with one Contact for the email (docs/producer_dashboard/
	accounts.md). Called before Frappe's sign_up creates the User, so Frappe's create_contact then
	finds this Contact by email and sets its `user` instead of making a second one.

	- An email already on a Customer's contact gets no Lead: the transporter adds the user to the
	  Customer's Portal Users (ERPNext's rule).
	- An existing Lead with that email is reused (ERPNext refuses duplicates by email).
	"""
	contact = get_contact_name(email)
	if contact and frappe.db.exists(
		"Dynamic Link", {"parenttype": "Contact", "parent": contact, "link_doctype": "Customer"}
	):
		return None

	if lead_name := frappe.db.get_value("Lead", {"email_id": email}):
		lead = frappe.get_doc("Lead", lead_name)
	else:
		# No Lead Owner: it defaults to the session's user, which ERPNext refuses when that is the Lead's own email
		# (an account linking itself: ozone.api.auth.start_producer); the sales team assigns one
		lead = frappe.get_doc(
			{"doctype": "Lead", "first_name": full_name, "email_id": email, "lead_owner": ""}
		)
		lead.insert(ignore_permissions=True)
		# With CRM Settings → Auto Creation of Contact on, ERPNext's Lead made a Contact of its own
		# (lead.py: before_insert). Keep it, unless the email already had one: then it's a twin.
		made = getattr(lead, "contact_doc", None)
		if made and contact:
			frappe.delete_doc("Contact", made.name, ignore_permissions=True)
		contact = contact or (made and made.name)

	if not contact:
		# ERPNext's own steps (lead.py: create_contact, link_to_contact).
		lead.contact_doc = lead.create_contact()
		lead.link_to_contact()
	elif not frappe.db.exists(
		"Dynamic Link",
		{"parenttype": "Contact", "parent": contact, "link_doctype": "Lead", "link_name": lead.name},
	):
		existing = frappe.get_doc("Contact", contact)
		existing.append(
			"links", {"link_doctype": "Lead", "link_name": lead.name, "link_title": lead.lead_name}
		)
		existing.save(ignore_permissions=True)
	return lead.name
