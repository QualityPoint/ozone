"""What the waste transport contract shows (the print format "Ozone Waste Transport Contract", for Service
Quotation): the Madinah Regional Municipality's standard contract for transporting non-hazardous waste, filled
from the quotation. Exposed to Jinja (hooks.py: jinja) as `waste_transport_contract(doc)`.

The two parties' registration numbers come from their credentials, matched by the document type's name (the
facility's for the producer, the Company's for the transporter); what isn't on record prints as a line to fill
by hand."""

import base64
from functools import cache
from pathlib import Path

import frappe
from frappe.utils import cint, flt, getdate, money_in_words, strip_html
from naqel.utils.location.regions.lookup import region_at_level

WEEKDAYS = ("الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد")
# Arabic counted words by plural form (Intl/CLDR): "one" and "two" are whole phrases, the others follow the number
COUNTED = {
	"Day": {"one": "يوم واحد", "two": "يومان", "few": "أيام", "many": "يومًا", "other": "يوم"},
	"Week": {"one": "أسبوع واحد", "two": "أسبوعان", "few": "أسابيع", "many": "أسبوعًا", "other": "أسبوع"},
	"Month": {"one": "شهر واحد", "two": "شهران", "few": "أشهر", "many": "شهرًا", "other": "شهر"},
	"Year": {"one": "سنة واحدة", "two": "سنتان", "few": "سنوات", "many": "سنة", "other": "سنة"},
	"times": {"one": "مرة واحدة", "two": "مرتان", "few": "مرات", "many": "مرة", "other": "مرة"},
}
EVERY = {
	"Day": {"one": "يوميًا", "two": "كل يومين", "few": "أيام", "many": "يومًا", "other": "يوم"},
	"Week": {"one": "أسبوعيًا", "two": "كل أسبوعين", "few": "أسابيع", "many": "أسبوعًا", "other": "أسبوع"},
	"Month": {"one": "شهريًا", "two": "كل شهرين", "few": "أشهر", "many": "شهرًا", "other": "شهر"},
	"Year": {"one": "سنويًا", "two": "كل سنتين", "few": "سنوات", "many": "سنة", "other": "سنة"},
}
# The waste type rows, in the form's colours (organic green, recyclable blue, the rest black)
WASTE_COLOURS = (
	("عضوي", "organic"),
	("organic", "organic"),
	("تدوير", "recyclable"),
	("recycl", "recyclable"),
)
# Credentials by what their document type is called (Arabic or English)
DOCUMENTS = {
	"commercial_registration": ("سجل", "commercial registration"),
	"national_id": ("هوية", "إقامة", "national id", "iqama"),
	"tax": ("ضريب", "vat", "tax"),
	"mwan": ("موان", "المركز الوطني لإدارة النفايات", "mwan", "waste management"),
	"municipal": ("بلدي", "municipal"),
	"qualification": ("تأهيل", "qualification"),
}
COLLECTION_ROOM = ("غرفة", "room")


def waste_transport_contract(doc) -> dict:
	"""Everything the contract prints, from a Service Quotation: in Arabic, as the form is, whoever prints it."""
	lang = frappe.local.lang
	frappe.local.lang = "ar"
	try:
		return _contract(doc)
	finally:
		frappe.local.lang = lang


def _contract(doc) -> dict:
	facility = frappe.get_doc("Facility", doc.facility) if doc.facility else frappe._dict()
	company = frappe.get_cached_doc("Company", doc.company) if doc.company else frappe._dict()
	mechanism = (
		frappe.db.get_value(
			"Collection Mechanism",
			doc.single_collection_mechanism,
			["collection_mechanism_name", "requires_container_deployment"],
			as_dict=True,
		)
		or frappe._dict()
	)
	concluded = getdate(doc.transaction_date)
	return {
		"logo": _image_data("madinah_municipality.jpeg"),
		"company_logo": company.get("company_logo"),
		"number": doc.name,
		"follows": doc.amended_from or "",
		"start_date": _date(doc.start_date),
		"end_date": "" if doc.is_milestone_based else _date(doc.end_date),
		"duration": ""
		if doc.is_milestone_based or not doc.service_duration
		else counted(cint(doc.service_duration), COUNTED.get(doc.duration_uom, COUNTED["Day"])),
		"activity": frappe.db.get_value("ISIC Classification", doc.isic_classification, "category_name")
		or doc.isic_classification
		or "",
		"area": _area(doc),
		"license_no": doc.license_no or "",
		"license_renewal": doc.license_status == "Renewal",
		"license_new": doc.license_status == "New Issue",
		"municipality": _region_name(facility.get("region"), "Municipality"),
		"wastes": _wastes(doc),
		"concluded": {
			"weekday": WEEKDAYS[concluded.weekday()],
			"gregorian": _date(concluded),
			"hijri": _hijri(concluded),
		},
		"first": _first_party(doc, facility),
		"second": _second_party(doc, company),
		"mechanism": frappe._(mechanism.collection_mechanism_name or doc.single_collection_mechanism or ""),
		"rows": _rows(doc, facility),
		"currency": doc.currency,
		"net_total": flt(doc.net_total),
		"taxes": flt(doc.total_taxes_and_charges),
		"grand_total": flt(doc.rounded_total) or flt(doc.grand_total),
		"in_words": money_in_words(flt(doc.rounded_total) or flt(doc.grand_total), doc.currency),
		"collection_room": any(
			word in (mechanism.collection_mechanism_name or doc.single_collection_mechanism or "").lower()
			for word in COLLECTION_ROOM
		),
	}


def counted(count: int, forms: dict) -> str:
	"""An Arabic counted phrase: "شهران", "3 أشهر", "11 شهرًا"."""
	form = _plural(count)
	return forms[form] if form in ("one", "two") else f"{count} {forms[form]}"


def _plural(count: int) -> str:
	# CLDR's Arabic rules for whole numbers
	if count == 1:
		return "one"
	if count == 2:
		return "two"
	if 3 <= count % 100 <= 10:
		return "few"
	if 11 <= count % 100 <= 99:
		return "many"
	return "other"


def _frequency(count: int, period_count: int, period_uom: str) -> str:
	""" "مرتان يوميًا", "مرة واحدة كل 3 أيام"."""
	times = counted(count or 1, COUNTED["times"])
	forms = EVERY.get(period_uom, EVERY["Day"])
	form = _plural(period_count or 1)
	every = forms[form] if form in ("one", "two") else f"كل {period_count} {forms[form]}"
	return f"{times} {every}"


def _wastes(doc) -> list[dict]:
	from naqel.naqel_contracting.doctype.service_request.service_request import split_wastes

	out = []
	for row in doc.get("waste_types") or []:
		name = (row.waste_type or "").lower()
		colour = next((c for word, c in WASTE_COLOURS if word in name), "residual")
		out.append(
			{
				"label": frappe._(row.waste_type),
				"colour": colour,
				"items": [frappe._(item) for item in split_wastes(row.waste_item)],
			}
		)
	return out


def _rows(doc, facility) -> list[dict]:
	coordinates = (
		f"{flt(facility.latitude):.6f}, {flt(facility.longitude):.6f}"
		if facility.get("latitude") and facility.get("longitude")
		else ""
	)
	area = _area(doc)
	return [
		{
			"container": frappe._(row.container_type),
			"count": cint(row.container_count),
			"coordinates": coordinates,
			"frequency": _frequency(
				cint(row.collection_count), cint(row.collection_period_count), row.collection_period_uom
			),
			"amount": flt(row.amount),
			"area": area,
		}
		for row in doc.get("containers") or []
	]


def _first_party(doc, facility) -> dict:
	"""The producer: the quotation's party, its facility's documents, its contact."""
	party = (
		frappe.db.get_value(doc.quotation_to, doc.party_name, ["*"], as_dict=True)
		if doc.quotation_to and doc.party_name
		else frappe._dict()
	)
	documents = _documents("Facility", doc.facility) if doc.facility else {}
	address = strip_html(doc.customer_address_display or "").strip() or ", ".join(
		part for part in (facility.get("street"), facility.get("district"), facility.get("city")) if part
	)
	return {
		"name": doc.customer_name or doc.party_name or "",
		"address": " ".join(address.split()),
		"commercial_registration": documents.get("commercial_registration", ""),
		"national_id": documents.get("national_id", ""),
		"tax_id": party.get("tax_id") or documents.get("tax", ""),
		"phone": doc.contact_mobile or party.get("mobile_no") or party.get("phone") or "",
		"email": doc.contact_email or party.get("email_id") or "",
	}


def _second_party(doc, company) -> dict:
	"""The transporter: the Company, its documents (licenses), its address."""
	documents = _documents("Company", company.get("name"), with_expiry=True) if company else {}
	address = strip_html(doc.company_address_display or "").strip()
	return {
		"name": company.get("company_name") or doc.company or "",
		"address": " ".join(address.split()),
		"commercial_registration": documents.get("commercial_registration", ("", ""))[0],
		"tax_id": company.get("tax_id") or "",
		"email": company.get("email") or "",
		"phone": company.get("phone_no") or "",
		"mwan": documents.get("mwan", ("", "")),
		"municipal": documents.get("municipal", ("", "")),
		"qualification": documents.get("qualification", ("", "")),
	}


def _documents(parenttype: str, parent: str, with_expiry: bool = False) -> dict:
	"""A record's credentials by kind (DOCUMENTS): its number, or (number, expiry) `with_expiry`."""
	doctype = "Facility Credential" if parenttype == "Facility" else "Company Credential"
	out = {}
	for row in frappe.get_all(
		doctype,
		filters={"parenttype": parenttype, "parent": parent},
		fields=["document_type", "document_number", "expiry_date"],
		order_by="idx",
	):
		name = (row.document_type or "").lower()
		for kind, words in DOCUMENTS.items():
			if kind not in out and any(word in name for word in words):
				number = row.document_number or ""
				out[kind] = (number, _date(row.expiry_date)) if with_expiry else number
	return out


def _area(doc) -> str:
	"""The facility's size in its unit (e.g. 120 m²)."""
	if not doc.facility_uom:
		return ""
	unit = doc.default_uom or doc.facility_uom
	return f"{flt(doc.facility_measurement):,.0f} {frappe._(unit)}"


def _region_name(region: str | None, level: str) -> str:
	name = region and region_at_level(region, level)
	return frappe.db.get_value("Region", name, "region_name") if name else ""


def _date(value) -> str:
	return getdate(value).strftime("%d/%m/%Y") if value else ""


def _hijri(value) -> str:
	try:
		from hijridate import Gregorian
	except ImportError:
		return ""
	date = getdate(value)
	hijri = Gregorian(date.year, date.month, date.day).to_hijri()
	return f"{hijri.day:02d}/{hijri.month:02d}/{hijri.year}"


@cache
def _image_data(name: str) -> str:
	"""An image of the app's print assets as a data URI: it prints in the PDF without a request back to the
	site."""
	path = Path(frappe.get_app_path("ozone", "public", "images", "print", name))
	return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()
