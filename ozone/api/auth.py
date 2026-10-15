"""The login pages' endpoints (all open to guests): who is logged in, which sign-in methods are
enabled, sign-up, and the start of a social login. The rules are in ozone/auth.py and
ozone/producer.py (docs/producer_dashboard/api.md)."""

import frappe
from frappe import _
from frappe.core.doctype.user.user import sign_up as frappe_sign_up
from frappe.utils import cint
from frappe.utils.oauth import get_oauth2_authorize_url
from frappe.website.utils import is_signup_disabled

from ozone.auth import create_signup_lead, enabled_providers
from ozone.producer import get_producer, owned_names

GUEST = {"name": "Guest", "full_name": None, "user_type": None, "producer": None}


@frappe.whitelist(allow_guest=True)
def get_session_user() -> dict:
	"""The current user for the SPA: `user_type` is None for guests, and `producer` is the party a
	Website User's account belongs to (None when nobody has linked it yet)."""
	user = frappe.session.user
	info = (
		None
		if user == "Guest"
		else frappe.db.get_value("User", user, ["full_name", "user_type"], as_dict=True)
	)
	if not info:
		# A guest, or a session that outlived its user: logged out.
		return GUEST
	producer = get_producer(user)
	return {
		"name": user,
		"full_name": info.full_name,
		"user_type": info.user_type,
		# A producer starts by registering its facility: the dashboard opens there until it has one
		"producer": producer
		and {
			"doctype": producer.doctype,
			"name": producer.name,
			"title": producer.title,
			"facilities": len(owned_names("Facility", producer)),
		},
	}


@frappe.whitelist(methods=["POST"])
def start_producer() -> dict:
	"""A website account nobody has linked yet (made in the Desk, or by a social login) becomes a producer of
	its own, as a sign-up does: its Lead, linked through its Contact (ozone/auth.py: create_signup_lead). It
	can then register its facility at once. An email on a Customer's contact stays unlinked: the transporter
	adds the user to the Customer's Portal Users (ERPNext's rule). Returns the session user, as
	get_session_user does."""
	user = frappe.session.user
	if (
		user != "Guest"
		and frappe.db.get_value("User", user, "user_type") == "Website User"
		and not get_producer(user)
	):
		email, full_name = frappe.db.get_value("User", user, ["email", "full_name"])
		create_signup_lead(email, full_name or email)
	return get_session_user()


@frappe.whitelist(allow_guest=True)
def get_login_options() -> dict:
	"""Sign-in methods enabled on this site, for the SPA login page."""
	return {
		"password_login": not cint(frappe.get_system_settings("disable_user_pass_login")),
		# Besides the account name (email, or "Administrator"), Frappe can accept these.
		"login_with_username": bool(cint(frappe.get_system_settings("allow_login_using_user_name"))),
		"login_with_mobile": bool(cint(frappe.get_system_settings("allow_login_using_mobile_number"))),
		"email_link": bool(cint(frappe.get_system_settings("login_with_email_link"))),
		"signup": not is_signup_disabled(),
		"providers": [
			{"name": provider.name, "label": provider.provider_name} for provider in enabled_providers()
		],
	}


@frappe.whitelist(allow_guest=True, methods=["POST"])
def sign_up(email: str, full_name: str, redirect_to: str | None = None) -> tuple[int, str]:
	"""Frappe's sign_up, with the producer's Lead made first (ozone/auth.py: create_signup_lead).

	Frappe answers on its own when sign-up is off or the email is taken, so no Lead is made then.
	Everything runs in one request: if Frappe refuses, the Lead is rolled back with it.
	"""
	email = (email or "").strip().lower()
	full_name = (full_name or "").strip()
	if not is_signup_disabled() and email and full_name and not frappe.db.exists("User", {"email": email}):
		create_signup_lead(email, full_name)
	return frappe_sign_up(email, full_name, redirect_to or "")


@frappe.whitelist(allow_guest=True, methods=["GET"])
def social_login(provider: str, redirect_to: str | None = None):
	"""Redirect to the provider's consent screen.

	The SPA links here instead of embedding an authorize URL, because the OAuth state token inside
	that URL expires after 10 minutes. After the provider calls back, Frappe logs the user in and
	redirects to `redirect_to` (same site only), or else by user type: Desk for staff, the
	dashboard for producers via `get_website_user_home_page`.
	"""
	if provider not in {p.name for p in enabled_providers()}:
		frappe.throw(_("This sign-in method is not available."), frappe.PermissionError)

	from frappe.www.login import sanitize_redirect

	frappe.local.response["type"] = "redirect"
	frappe.local.response["location"] = get_oauth2_authorize_url(provider, sanitize_redirect(redirect_to))
