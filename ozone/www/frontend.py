import frappe
import frappe.sessions

no_cache = 1


def get_context():
	# get_csrf_token() may generate a new token on the session; GET requests are
	# rolled back unless committed, so persist it before rendering.
	csrf_token = frappe.sessions.get_csrf_token()
	frappe.db.commit()

	context = frappe._dict()
	# Each key is set on `window` by the Jinja loop that frappe-ui's jinjaBootData
	# vite plugin injects into www/frontend.html.
	context.boot = {
		"csrf_token": csrf_token,
		"site_name": frappe.local.site,
	}
	return context
