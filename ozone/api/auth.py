"""The login pages' endpoints (all open to guests): who is logged in, which sign-in methods
are enabled, and the start of a social login. The rules are in ozone/auth.py."""

import frappe
from frappe import _
from frappe.utils import cint
from frappe.utils.oauth import get_oauth2_authorize_url

from ozone.auth import enabled_providers


@frappe.whitelist(allow_guest=True)
def get_session_user() -> dict:
	"""The current user for the SPA. `user_type` is None for guests."""
	user = frappe.session.user
	info = None if user == "Guest" else frappe.db.get_value("User", user, ["user_type"], as_dict=True)
	if not info:
		# A guest, or a session that outlived its user: logged out.
		return {"name": "Guest", "user_type": None}
	return {"name": user, "user_type": info.user_type}


@frappe.whitelist(allow_guest=True)
def get_login_options() -> dict:
	"""Sign-in methods enabled on this site, for the SPA login page."""
	return {
		"password_login": not cint(frappe.get_system_settings("disable_user_pass_login")),
		# Besides the account name (email, or "Administrator"), Frappe can accept these.
		"login_with_username": bool(cint(frappe.get_system_settings("allow_login_using_user_name"))),
		"login_with_mobile": bool(cint(frappe.get_system_settings("allow_login_using_mobile_number"))),
		"email_link": bool(cint(frappe.get_system_settings("login_with_email_link"))),
		"providers": [
			{"name": provider.name, "label": provider.provider_name} for provider in enabled_providers()
		],
	}


@frappe.whitelist(allow_guest=True, methods=["GET"])
def social_login(provider: str, redirect_to: str | None = None):
	"""Redirect to the provider's consent screen.

	The SPA links here instead of embedding an authorize URL, because the OAuth state token
	inside that URL expires after 10 minutes. After the provider calls back, Frappe logs the
	user in and redirects to `redirect_to` (same site only), else to the Desk.
	"""
	if provider not in {p.name for p in enabled_providers()}:
		frappe.throw(_("This sign-in method is not available."), frappe.PermissionError)

	from frappe.www.login import sanitize_redirect

	frappe.local.response["type"] = "redirect"
	frappe.local.response["location"] = get_oauth2_authorize_url(provider, sanitize_redirect(redirect_to))
