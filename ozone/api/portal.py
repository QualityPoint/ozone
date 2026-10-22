"""The producer dashboard's API: the only way a producer reads or changes data. Producers have no
DocType permissions (ERPNext's portal pattern), so every method starts with require_producer();
the rules are in ozone/portal/ (docs/producer_dashboard/access.md, api.md)."""

import frappe

from ozone.portal import contracts, establishment, facilities, profile, quotations, requests
from ozone.producer import owned_names, require_producer


@frappe.whitelist(methods=["GET"])
def get_overview() -> dict:
	"""The producer and how many of its records there are, for the dashboard's first page."""
	producer = require_producer()
	return {
		"producer": {"doctype": producer.doctype, "name": producer.name, "title": producer.title},
		"counts": {
			"facilities": len(owned_names("Facility", producer)),
			"service_requests": len(owned_names("Service Request", producer)),
			"quotations": quotations.count_quotations(producer),
			"contracts": contracts.count_contracts(producer),
		},
	}


@frappe.whitelist(methods=["GET"])
def get_profile() -> dict:
	return profile.get_profile(require_producer())


@frappe.whitelist(methods=["POST"])
def update_profile(data: dict | str) -> dict:
	return profile.update_profile(require_producer(), frappe.parse_json(data))


@frappe.whitelist(methods=["POST"])
def save_address(data: dict | str) -> dict:
	return profile.save_address(require_producer(), frappe.parse_json(data))


@frappe.whitelist(methods=["POST"])
def update_avatar(file_url: str | None = None) -> dict:
	return profile.update_avatar(require_producer(), file_url)


@frappe.whitelist(methods=["GET"])
def get_establishment() -> dict:
	return establishment.get_establishment(require_producer())


@frappe.whitelist(methods=["POST"])
def update_establishment(data: dict | str) -> dict:
	return establishment.update_establishment(require_producer(), frappe.parse_json(data))


@frappe.whitelist(methods=["GET"])
def get_facility_settings() -> dict:
	require_producer()
	return facilities.get_facility_settings()


@frappe.whitelist(methods=["GET"])
def get_facilities() -> list[dict]:
	return facilities.get_facilities(require_producer())


@frappe.whitelist(methods=["POST"])
def save_facility(data: dict | str) -> dict:
	return facilities.save_facility(require_producer(), frappe.parse_json(data))


@frappe.whitelist(methods=["GET"])
def search_regions(txt: str = "") -> list[dict]:
	require_producer()
	return facilities.search_regions(txt)


@frappe.whitelist(methods=["GET"])
def region_at(latitude: float, longitude: float) -> dict | None:
	require_producer()
	return facilities.region_at(latitude, longitude)


@frappe.whitelist(methods=["GET"])
def search_isic(txt: str = "") -> list[dict]:
	require_producer()
	return facilities.search_isic(txt)


@frappe.whitelist(methods=["GET"])
def get_service_requests(filters: dict | str | None = None) -> list[dict]:
	return requests.get_service_requests(require_producer(), frappe.parse_json(filters) if filters else None)


@frappe.whitelist(methods=["GET"])
def get_request_options() -> dict:
	return requests.get_request_options(require_producer())


@frappe.whitelist(methods=["GET"])
def get_request_form(facility: str, service_type: str, name: str | None = None) -> dict:
	return requests.get_request_form(require_producer(), facility, service_type, name)


@frappe.whitelist(methods=["POST"])
def save_service_request(data: dict | str) -> dict:
	return requests.save_service_request(require_producer(), frappe.parse_json(data))


@frappe.whitelist(methods=["GET"])
def get_service_request(name: str) -> dict:
	return requests.get_service_request(require_producer(), name)


@frappe.whitelist(methods=["POST"])
def submit_service_request(name: str) -> dict:
	return requests.submit_service_request(require_producer(), name)


@frappe.whitelist(methods=["POST"])
def add_request_comment(name: str, text: str, files: list[str] | None = None) -> list[dict]:
	return requests.add_request_comment(require_producer(), name, text, files)


@frappe.whitelist(methods=["GET"])
def get_facility_activity(facility: str) -> dict:
	return requests.get_facility_activity(require_producer(), facility)


@frappe.whitelist(methods=["GET"])
def get_contracts() -> list[dict]:
	return contracts.get_contracts(require_producer())


@frappe.whitelist(methods=["GET"])
def get_quotations() -> list[dict]:
	return quotations.get_quotations(require_producer())


@frappe.whitelist(methods=["GET"])
def get_quotation(name: str) -> dict:
	return quotations.get_quotation(require_producer(), name)


@frappe.whitelist(methods=["POST"])
def decide_quotation(name: str, decision: str, comment: str | None = None) -> dict:
	return quotations.decide_quotation(require_producer(), name, decision, comment)


@frappe.whitelist(methods=["GET"])
def get_quotation_thread(name: str) -> dict:
	return quotations.get_quotation_thread(require_producer(), name)


@frappe.whitelist(methods=["POST"])
def add_quotation_comment(name: str, text: str, files: list[str] | None = None) -> list[dict]:
	return quotations.add_quotation_comment(require_producer(), name, text, files)
