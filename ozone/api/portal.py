"""The producer dashboard's API: the only way a producer reads or changes data. Producers have no
DocType permissions (ERPNext's portal pattern), so every method starts with require_producer();
the rules are in ozone/portal/ (docs/producer_dashboard/access.md, api.md)."""

import frappe

from ozone.portal import (
	contracts,
	establishment,
	facilities,
	notifications,
	overview,
	profile,
	quotations,
	requests,
)
from ozone.producer import (
	owned_names,
	require_producer,
)


@frappe.whitelist(methods=["GET"])
def get_overview() -> dict:
	return overview.get_overview(require_producer())


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
def clarify_request(name: str, text: str, files: list[str] | None = None) -> dict:
	return requests.clarify_request(require_producer(), name, text, files)


@frappe.whitelist(methods=["GET"])
def get_facility_activity(facility: str) -> dict:
	return requests.get_facility_activity(require_producer(), facility)


@frappe.whitelist(methods=["GET"])
def get_contracts() -> list[dict]:
	return contracts.get_contracts(require_producer())


@frappe.whitelist(methods=["POST"])
def pay_contract(name: str) -> dict:
	"""The checkout to pay what the contract requires before it is issued: `{url}`."""
	return contracts.pay_contract(require_producer(), name)


@frappe.whitelist(methods=["GET"])
def get_contract_print(name: str) -> dict:
	"""The contract as it prints: `{html}`."""
	return contracts.get_contract_print(require_producer(), name)


@frappe.whitelist(methods=["POST"])
def sign_contract(name: str, signee: str, signature: str) -> list[dict]:
	"""Sign an issued contract: its drawn signature (a PNG data URL) and the signee's name; the contracts again."""
	return contracts.sign_contract(require_producer(), name, signee, signature)


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


@frappe.whitelist(methods=["GET"])
def get_notifications() -> dict:
	"""The producer's latest notifications and how many are unread."""
	return notifications.get_notifications(require_producer())


@frappe.whitelist(methods=["POST"])
def mark_notifications_read(names: list[str] | str | None = None) -> dict:
	"""Mark the given notifications read (all of them without names)."""
	return notifications.mark_read(require_producer(), frappe.parse_json(names) if isinstance(names, str) else names)
