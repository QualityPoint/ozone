"""The producer's details: the user's own Contact, its party, and the party's addresses
(docs/producer_dashboard/api.md)."""

import frappe
from frappe import _
from frappe.utils import cstr

from ozone.portal import own_doc, pick
from ozone.producer import main_party, owned_names

CONTACT_FIELDS = ("first_name", "last_name", "mobile_no")
ADDRESS_FIELDS = ("address_type", "address_line1", "address_line2", "city", "state", "pincode")
# The address types a producer picks from (Frappe's Address.address_type options).
ADDRESS_TYPES = ("Billing", "Office", "Shipping", "Warehouse")
# What Frappe lets a Website User upload as a picture (frappe/handler.py: ALLOWED_MIMETYPES).
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")


def get_profile(producer: frappe._dict) -> dict:
	contact = _own_contact()
	return {
		"email": frappe.session.user,
		"first_name": contact.first_name,
		"last_name": contact.last_name,
		"mobile_no": contact.mobile_no,
		"user_image": frappe.db.get_value("User", frappe.session.user, "user_image"),
		"party": {"doctype": producer.doctype, "title": producer.title},
		"addresses": get_addresses(producer),
		"address_types": ADDRESS_TYPES,
	}


def update_profile(producer: frappe._dict, data: dict) -> dict:
	"""The name and mobile number on the user's Contact. The email is the login: not changed here."""
	values = pick(data, CONTACT_FIELDS)
	contact = _own_contact()
	for field in ("first_name", "last_name"):
		if field in values:
			contact.set(field, cstr(values[field]).strip())
	if not contact.first_name:
		frappe.throw(_("Enter your first name."))
	if "mobile_no" in values:
		_set_mobile(contact, cstr(values["mobile_no"]).strip())
	contact.save(ignore_permissions=True)
	return get_profile(producer)


def update_avatar(producer: frappe._dict, file_url: str | None) -> dict:
	"""The user's picture: an image the user uploaded (Frappe's upload_file), or none to remove it."""
	file_url = cstr(file_url).strip() or None
	if file_url:
		uploaded = frappe.db.get_value(
			"File", {"file_url": file_url, "owner": frappe.session.user}, ["name", "file_name"], as_dict=True
		)
		if not uploaded:
			frappe.throw(_("Upload the picture first."), frappe.PermissionError)
		if not cstr(uploaded.file_name).lower().endswith(IMAGE_EXTENSIONS):
			frappe.throw(_("Choose an image (JPG or PNG)."))
	frappe.db.set_value("User", frappe.session.user, "user_image", file_url)
	return get_profile(producer)


def get_addresses(producer: frappe._dict) -> list[dict]:
	names = owned_names("Address", producer)
	return frappe.get_all(
		"Address",
		filters={"name": ["in", names], "disabled": 0},
		fields=["name", *ADDRESS_FIELDS, "country"],
		order_by="creation",
	)


def save_address(producer: frappe._dict, data: dict) -> dict:
	"""A new address for the producer's party, or one of its own updated."""
	values = pick(data, ADDRESS_FIELDS)
	# A type outside the producer's choices is ignored; an edit that leaves it out keeps the
	# address's own, and a new address without one gets the first.
	if "address_type" in values and values["address_type"] not in ADDRESS_TYPES:
		values.pop("address_type")
	if not data.get("name"):
		values.setdefault("address_type", ADDRESS_TYPES[0])
	if data.get("name"):
		address = own_doc("Address", data["name"], producer)
		address.update(values)
	else:
		doctype, name = main_party(producer)
		address = frappe.new_doc("Address")
		address.update(values)
		address.address_title = producer.title
		address.country = frappe.db.get_default("country")
		address.append("links", {"link_doctype": doctype, "link_name": name})
	address.save(ignore_permissions=True)
	return {"name": address.name, "addresses": get_addresses(producer)}


def _own_contact():
	"""The session user's Contact (Frappe keeps one per user: Contact.user)."""
	name = frappe.db.get_value("Contact", {"user": frappe.session.user})
	if not name:
		frappe.throw(_("Your contact details aren't set up yet."), frappe.PermissionError)
	return frappe.get_doc("Contact", name)


def _set_mobile(contact, number: str) -> None:
	"""The primary mobile number, in the Contact's phone table (Frappe derives `mobile_no` from it)."""
	row = next((phone for phone in contact.phone_nos if phone.is_primary_mobile_no), None)
	if row and number:
		row.phone = number
	elif row:
		contact.remove(row)
	elif number:
		contact.add_phone(number, is_primary_mobile_no=1)
