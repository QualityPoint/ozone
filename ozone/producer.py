"""Who a producer is: the single place that decides which party a website account belongs to,
and which records that party owns (docs/producer_dashboard/identity.md, access.md).

A producer is a Website User who belongs to:
- a Customer, through the Customer's Portal Users table: ERPNext's own rule
  (erpnext/controllers/website_list_for_contact.py: get_parents_for_user); or else
- a Lead, through the user's Contact and its links: Frappe's own rule for portal users without a
  Customer (frappe/contacts/doctype/address/address.py: has_website_permission). A Converted
  Lead no longer counts: its Customer does.

A producer's parties are what it may see: its Lead, or its Customer and the Lead it came from
(`Customer.lead_name`), because ERPNext leaves Lead-stage records (quotations…) on the Lead.
"""

import frappe
from frappe import _
from frappe.query_builder import Criterion
from frappe.utils.user import is_website_user

# How each DocType names its owner, the patterns ERPNext uses (access.md):
# - "links": Dynamic Link rows, like Address and Contact;
# - (type field, name field): a Dynamic Link pair, like Quotation's quotation_to / party_name;
# - a Link field to Customer, like Sales Order's customer.
OWNER_FIELDS: dict[str, str | tuple[str, str]] = {
	"Address": "links",
	"Facility": "links",
	"Service Request": ("request_from", "party"),
	"Service Quotation": ("quotation_to", "party_name"),
	"Operation Order": "customer",
	"Service Contract": "customer",
}


def get_producer(user: str | None = None) -> frappe._dict | None:
	"""`{doctype, name, title, parties}` for a producer's account, None for anyone else (guests,
	staff, a Website User nobody has linked yet). Callers resolve it once per request and pass it
	on (owned_names)."""
	user = user or frappe.session.user
	if user in ("Guest", "Administrator") or not is_website_user(user):
		return None

	if customer := _customer_of(user):
		lead = frappe.db.get_value("Customer", customer, "lead_name")
		parties = [("Customer", customer)] + ([("Lead", lead)] if lead else [])
		return _producer("Customer", customer, parties)
	if lead := _lead_of(user):
		return _producer("Lead", lead, [("Lead", lead)])
	return None


def require_producer() -> frappe._dict:
	"""The session's producer, or PermissionError: every dashboard method starts here."""
	producer = get_producer()
	if not producer:
		frappe.throw(_("This account isn't linked to a producer yet."), frappe.PermissionError)
	return producer


def owned_names(doctype: str, producer: frappe._dict) -> list[str]:
	"""The names of `doctype`'s records that belong to one of the producer's parties (not cancelled
	ones). The base of every list: filter by these first, then read with ignore_permissions, as
	ERPNext's get_transaction_list does."""
	owner = OWNER_FIELDS[doctype]
	if owner == "links":
		link = frappe.qb.DocType("Dynamic Link")
		match = Criterion.any(
			(link.link_doctype == party_type) & (link.link_name == name)
			for party_type, name in producer.parties
		)
		query = (
			frappe.qb.from_(link)
			.select(link.parent)
			.distinct()
			.where((link.parenttype == doctype) & (link.parentfield == "links") & match)
		)
	else:
		table = frappe.qb.DocType(doctype)
		if isinstance(owner, tuple):
			type_field, name_field = owner
			match = Criterion.any(
				(table[type_field] == party_type) & (table[name_field] == name)
				for party_type, name in producer.parties
			)
		else:
			customers = [name for party_type, name in producer.parties if party_type == "Customer"]
			if not customers:
				return []
			match = table[owner].isin(customers)
		query = frappe.qb.from_(table).select(table.name).where(match)
		if frappe.get_meta(doctype).is_submittable:
			# Cancelled records are history for the transporter, not the producer.
			query = query.where(table.docstatus < 2)
	return query.run(pluck=True)


def owns(doctype: str, name: str, producer: frappe._dict | None) -> bool:
	"""Whether a record belongs to the producer: the single check behind every read or change of
	one record (Facility.has_website_permission, ozone/portal)."""
	return bool(producer and name) and name in owned_names(doctype, producer)


def facility_website_permission(doc, ptype=None, user=None, verbose=False) -> bool:
	"""Hook (`has_website_permission`): a producer may see one of its own facilities."""
	return owns("Facility", doc.name, get_producer(user))


def main_party(producer: frappe._dict) -> tuple[str, str]:
	"""The party a producer's new records are linked to: its Customer, or else its Lead."""
	return producer.doctype, producer.name


def carry_lead_users(customer, method=None):
	"""Customer `after_insert` hook: a Customer made from a Lead lists the Lead's website users in
	its Portal Users, so their accounts carry over (identity.md). ERPNext re-links the Lead's
	Contacts on the same save; the rows are inserted directly, as ERPNext's own patch
	(migrate_supplier_portal_users) does."""
	if not customer.lead_name:
		return
	contacts = frappe.get_all(
		"Dynamic Link",
		filters={"parenttype": "Contact", "link_doctype": "Lead", "link_name": customer.lead_name},
		pluck="parent",
	)
	users = frappe.get_all("Contact", filters={"name": ["in", contacts], "user": ["is", "set"]}, pluck="user")
	listed = {row.user for row in customer.get("portal_users")}
	for user in users:
		if user not in listed and is_website_user(user):
			customer.append("portal_users", {"user": user}).db_insert()
			listed.add(user)


def party_users(party_type: str | None, party: str | None) -> list[str]:
	"""The website users a party's records belong to, the reverse of get_producer: a Customer's Portal Users, and the
	users of its Lead's Contacts while the Lead is open; a Lead's, through its Contacts."""
	if not party or party_type not in ("Customer", "Lead"):
		return []
	users = []
	if party_type == "Customer":
		users = frappe.get_all(
			"Portal User", filters={"parenttype": "Customer", "parentfield": "portal_users", "parent": party}, pluck="user"
		)
	else:
		contacts = frappe.get_all(
			"Dynamic Link", filters={"parenttype": "Contact", "link_doctype": "Lead", "link_name": party}, pluck="parent"
		)
		users = frappe.get_all("Contact", filters={"name": ["in", contacts or [""]], "user": ["is", "set"]}, pluck="user")
	return [user for user in dict.fromkeys(users) if is_website_user(user)]


def _customer_of(user: str) -> str | None:
	"""The first enabled Customer listing the user in its Portal Users (ERPNext's get_parents_for_user,
	for any user rather than only the session's)."""
	customers = frappe.get_all(
		"Portal User",
		filters={"parenttype": "Customer", "parentfield": "portal_users", "user": user},
		pluck="parent",
		order_by="creation",
	)
	enabled = frappe.get_all("Customer", filters={"name": ["in", customers], "disabled": 0}, pluck="name")
	return next((name for name in customers if name in enabled), None)


def _lead_of(user: str) -> str | None:
	"""The open Lead linked to the user's Contact (Contact.user, which Frappe sets from the email)."""
	contacts = frappe.get_all("Contact", filters={"user": user}, pluck="name")
	if not contacts:
		return None
	leads = frappe.get_all(
		"Dynamic Link",
		filters={"parenttype": "Contact", "parent": ["in", contacts], "link_doctype": "Lead"},
		pluck="link_name",
		order_by="creation",
	)
	return next((lead for lead in leads if frappe.db.get_value("Lead", lead, "status") != "Converted"), None)


def _producer(doctype: str, name: str, parties: list[tuple[str, str]]) -> frappe._dict:
	title_field = "customer_name" if doctype == "Customer" else "company_name"
	title = frappe.db.get_value(doctype, name, title_field)
	if not title and doctype == "Lead":
		title = frappe.db.get_value("Lead", name, "lead_name")
	return frappe._dict(doctype=doctype, name=name, title=title or name, parties=parties)
