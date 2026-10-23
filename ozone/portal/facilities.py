"""The producer's facilities and annexes (the Facility tree), and the ISIC activities to pick
from (docs/producer_dashboard/api.md).

A facility's documents (its credentials) come with the services it requests: each Service lists the documents it
requires (Registration Documents), and the request form adds the one given to the facility (portal/requests.py).
Only a composite facility gives one here, when it is registered: the shared document its annexes carry too (naqel's
Facility requires it)."""

import json

import frappe
from frappe import _
from frappe.utils import cint, cstr, flt
from naqel.utils.location.map_location import _point, resolve_map_location
from naqel.utils.location.regions.lookup import address_of, region_path, region_titles
from naqel.utils.location.regions.policy import pin_region, region_policy
from naqel.utils.credentials import (
	CREDENTIAL_FIELDS,
	CREDENTIAL_FLAGS,
	CREDENTIAL_TYPES,
	credential_flags,
	set_facility_credential,
)

from ozone.portal import own_doc, pick
from ozone.producer import main_party, owned_names

# Not the rating: it is the desk's own assessment of the facility, never shown to or set by the producer. The
# region is checked against Naqel Settings (region_divisions) before it is set.
FACILITY_FIELDS = ("facility_name", "isic_classification", "parent_facility", "is_group", "region")
# The facility's own address: the dashboard requires a street, city and country; naqel's documents show it from
# these fields (naqel.utils.location.facility_address). The country defaults to the system's.
ADDRESS_FIELDS = ("street", "building_no", "secondary_no", "district", "city", "pincode", "country")
# A facility's credentials (commercial registration, licenses): a producer sets naqel's CREDENTIAL_FIELDS on each
# row; the expiry and multi-branch flags follow the document type (naqel.utils.credentials.credential_flags).


def get_facilities(producer: frappe._dict) -> list[dict]:
	"""Main facilities first, each followed by its branches (the tree's order)."""
	facilities = frappe.get_all(
		"Facility",
		filters={"name": ["in", owned_names("Facility", producer)]},
		fields=[
			"name",
			"facility_name",
			"parent_facility",
			"is_group",
			"isic_classification",
			"region",
			"latitude",
			"longitude",
			"google_maps_location",
			*ADDRESS_FIELDS,
		],
		order_by="lft",
	)
	isic = _titles("ISIC Classification", [f.isic_classification for f in facilities], "category_name")
	regions = _titles("Region", [f.region for f in facilities], "region_name")
	credentials = _credentials([f.name for f in facilities])
	for facility in facilities:
		facility.credentials = credentials.get(facility.name, [])
		facility.isic_title = isic.get(facility.isic_classification)
		facility.region_title = regions.get(facility.region)
	return facilities


def save_facility(producer: frappe._dict, data: dict) -> dict:
	"""A new facility linked to the producer's party, or one of its own updated. Its pin comes from
	a pasted Google Maps value, resolved on the server as the Desk's form does, or from `latitude`
	and `longitude` dropped on the form's map."""
	values = pick(data, FACILITY_FIELDS + ADDRESS_FIELDS)
	if "region" in values:
		divisions = region_policy().divisions
		if not divisions:
			# No region policy: the pin decides it (naqel's Facility.set_region)
			values.pop("region")
		elif (
			values["region"]
			and frappe.db.get_value("Region", values["region"], "division_type") not in divisions
		):
			frappe.throw(_("Choose the region from the list."))
	if "is_group" in values:
		values["is_group"] = cint(values["is_group"])
	if values.get("parent_facility"):
		parent = own_doc("Facility", values["parent_facility"], producer)
		if not parent.is_group:
			frappe.throw(_("Annexes go under a composite facility."))
	elif "parent_facility" in values:
		values["parent_facility"] = None
	if values.get("isic_classification") and not frappe.db.exists(
		"ISIC Classification", {"name": values["isic_classification"], "is_group": 0}
	):
		frappe.throw(_("Choose an activity from the list."))

	if data.get("name"):
		facility = own_doc("Facility", data["name"], producer)
		facility.update(values)
	else:
		doctype, name = main_party(producer)
		facility = frappe.new_doc("Facility")
		facility.update(values)
		facility.country = facility.country or frappe.db.get_default("country")
		facility.append("links", {"link_doctype": doctype, "link_name": name})

	if facility.is_group:
		# The shared documents: added or updated by document type; the others (from requests) stay
		kept = {row.credential for row in facility.get("credentials") if row.credential}
		shared = {row["document_type"] for row in _document_types(shared_only=True)}
		for row in data.get("credentials") or []:
			values = document(row, kept)
			if values.get("document_type") not in shared:
				frappe.throw(_("A composite facility's document must be one its annexes share."))
			set_facility_credential(facility, values)
	elif facility.parent_facility:
		# An annex carries its composite facility's shared documents (naqel requires the same numbers)
		for row in frappe.get_all(
			"Facility Credential",
			filters={
				"parenttype": "Facility",
				"parent": facility.parent_facility,
				"eligible_for_multiple_facility_branches": 1,
			},
			fields=list(CREDENTIAL_FIELDS),
		):
			set_facility_credential(facility, dict(row))

	location = cstr(data.get("google_maps_location")).strip()
	if location and location != facility.google_maps_location:
		_place(facility, location)
	elif data.get("latitude") is not None and data.get("longitude") is not None:
		pin = _point(data["latitude"], data["longitude"])
		if not pin:
			frappe.throw(_("Those coordinates aren't on the map."))
		if (pin["latitude"], pin["longitude"]) != (facility.latitude, facility.longitude):
			_pin(facility, pin)
	facility.save(ignore_permissions=True)
	return {"name": facility.name, "facilities": get_facilities(producer)}


def get_facility_settings() -> dict:
	"""What the facility form needs to know: the documents a composite facility may share with its annexes,
	whether a region or a pin is required, and where the map opens."""
	address = frappe.get_cached_doc("Address Settings")
	policy = region_policy()
	return {
		"shared_document_types": _document_types(shared_only=True),
		# naqel's region policy: a region is required, picked at the assigned division's level (District, City…)
		"requires_region": bool(policy.divisions),
		"region_level": policy.level if policy.divisions else None,
		"requires_pin": bool(address.requires_pinned_location),
		"map": {
			"latitude": address.default_map_latitude or 24.7136,
			"longitude": address.default_map_longitude or 46.6753,
			"zoom": address.default_map_zoom or 6,
		},
		"country": frappe.db.get_default("country"),
	}


def _document_types(pairs: list[tuple[str, str]] | None = None, shared_only: bool = False) -> list[dict]:
	"""Document types with their expiry and multi-branch flags: the given (credential_type, document_type) pairs
	(a service's Registration Documents), or every Government ID and Service License; `shared_only`, those a
	composite facility's annexes may share (Eligible For Multi-branched Facility; a Service License never is)."""
	if pairs is None:
		pairs = [
			(credential_type, name)
			for credential_type in CREDENTIAL_TYPES
			for name in frappe.get_all(credential_type, pluck="name", order_by="name")
		]
	out = []
	for credential_type, document_type in pairs:
		flags = credential_flags(credential_type, document_type)
		if not flags or (shared_only and not flags["eligible_for_multiple_facility_branches"]):
			continue
		out.append(
			{"credential_type": credential_type, "document_type": document_type, "label": _(document_type), **flags}
		)
	return out


def search_regions(txt: str = "") -> list[dict]:
	"""Regions the facility may be in (naqel's region policy) matching a name or an alias, each with where it
	lies and the address it fills."""
	divisions = region_policy().divisions
	if not divisions:
		return []
	txt = cstr(txt).strip()
	or_filters = {"region_name": ["like", f"%{txt}%"], "alias": ["like", f"%{txt}%"]} if txt else None
	names = frappe.get_all(
		"Region",
		filters={"division_type": ["in", divisions]},
		or_filters=or_filters,
		pluck="name",
		order_by="region_name",
		limit=20,
	)
	return [region_option(name) for name in names]


def region_at(latitude: float, longitude: float) -> dict | None:
	"""The region a dropped pin falls in, if naqel's region policy accepts it (pin_region)."""
	if not region_policy().divisions:
		return None
	found = pin_region(latitude, longitude)
	return region_option(found["region"]) if found["region"] else None


def region_option(name: str) -> dict:
	"""A region as the picker shows it: its name, the regions above it (nearest first, short of the top one) and the
	address parts it fills (naqel's address_of)."""
	path = region_titles(region_path(name))
	return {"value": name, "label": path[0], "within": path[1:-1], **address_of(name)}


def search_isic(txt: str = "") -> list[dict]:
	"""Activities (the tree's leaves) matching a code or a name, for the facility form."""
	txt = cstr(txt).strip()
	or_filters = (
		{"category_code": ["like", f"%{txt}%"], "category_name": ["like", f"%{txt}%"]} if txt else None
	)
	return frappe.get_all(
		"ISIC Classification",
		filters={"is_group": 0},
		or_filters=or_filters,
		fields=["name", "category_code as code", "category_name as title"],
		order_by="category_code",
		limit=20,
	)


def _place(facility, value: str) -> None:
	"""Pin the facility from a Google Maps link, plus code, address or "lat, lng"
	(naqel.utils.location.map_location); the controller then sets its region."""
	facility.google_maps_location = value
	_pin(facility, resolve_map_location(value))


def _pin(facility, pin: dict) -> None:
	"""Set the facility's pin: its coordinates and the Geolocation field the Desk shows."""
	facility.latitude = pin["latitude"]
	facility.longitude = pin["longitude"]
	facility.location = json.dumps(
		{
			"type": "FeatureCollection",
			"features": [
				{
					"type": "Feature",
					"properties": {},
					"geometry": {"type": "Point", "coordinates": [pin["longitude"], pin["latitude"]]},
				}
			],
		}
	)


def _credential(row: dict, kept: set[str]) -> dict:
	"""One credential row. Its file must be one the user uploaded (Frappe's upload_file), or the one
	the row already had, so a row can't point at someone else's file."""
	values = pick(row, CREDENTIAL_FIELDS)
	if values.get("credential_type") not in CREDENTIAL_TYPES:
		frappe.throw(_("Choose a government ID or a service license."))
	file_url = cstr(values.get("credential")).strip()
	if (
		file_url
		and file_url not in kept
		and not frappe.db.exists("File", {"file_url": file_url, "owner": frappe.session.user})
	):
		frappe.throw(_("Upload the document first."), frappe.PermissionError)
	return values


def document(row: dict, kept: set[str]) -> dict:
	"""A document the producer gives (a request's, or a composite facility's shared one): a credential row with
	its number and its uploaded file."""
	values = _credential(row, kept)
	values["document_number"] = cstr(values.get("document_number")).strip()
	if not values.get("document_type") or not values["document_number"]:
		frappe.throw(_("Choose the document and give its number."))
	if not cstr(values.get("credential")).strip():
		frappe.throw(_("Upload the document."))
	return values


def _credentials(facilities: list[str]) -> dict[str, list[dict]]:
	"""Each facility's credentials, in table order."""
	rows = frappe.get_all(
		"Facility Credential",
		filters={"parenttype": "Facility", "parent": ["in", facilities or [""]]},
		fields=["parent", *CREDENTIAL_FIELDS, *CREDENTIAL_FLAGS],
		order_by="idx",
	)
	out: dict[str, list[dict]] = {}
	for row in rows:
		out.setdefault(row.pop("parent"), []).append(row)
	return out


def _titles(doctype: str, names: list[str | None], field: str) -> dict[str, str]:
	names = [name for name in set(names) if name]
	if not names:
		return {}
	return dict(
		frappe.get_all(doctype, filters={"name": ["in", names]}, fields=["name", field], as_list=True)
	)
