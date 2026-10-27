/**
 * The producer dashboard's API (ozone/api/portal.py). The server scopes every answer to the
 * logged-in producer: nothing here names a party (docs/producer_dashboard/api.md).
 */
import type { Producer } from "@/services/auth"
import { getMethod, postMethod } from "@/services/http"
import type { DurationUom } from "@/utils/duration"

export interface Overview {
	producer: Producer
	counts: {
		facilities: number
		service_requests: number
		quotations: number
		contracts: number
	}
}

export interface Address {
	name: string
	address_type: string
	address_line1: string
	address_line2: string | null
	city: string
	state: string | null
	pincode: string | null
	country: string
}

/** An address as the form edits it: a new one has no name. */
export type AddressInput = Partial<
	Record<Exclude<keyof Address, "country">, string>
>

export interface Profile {
	/** The login: shown, never changed here. */
	email: string
	/** The user's picture (ozone/portal/profile.py: update_avatar). */
	user_image: string | null
	first_name: string
	last_name: string | null
	mobile_no: string | null
	party: Pick<Producer, "doctype" | "title">
	addresses: Address[]
	/** The address types to pick from (Frappe's Address options the dashboard offers). */
	address_types: string[]
}

export type ProfileInput = Pick<
	Profile,
	"first_name" | "last_name" | "mobile_no"
>

/** One of the facility's credentials (commercial registration, licenses). */
export interface Credential {
	credential_type: "Government ID" | "Service License"
	document_type: string
	document_number: string
	/** The uploaded document's URL. */
	credential: string | null
	issue_date: string | null
	expiry_date: string | null
	/** From the document type, set by the server. */
	has_expiry_date?: 0 | 1
	eligible_for_multiple_facility_branches?: 0 | 1
}

/** The facility's own address: hawya requires a street, city and country. */
export interface FacilityAddress {
	street: string
	building_no: string
	secondary_no: string
	district: string
	city: string
	pincode: string
	country: string
}

export interface Facility
	extends Partial<Record<keyof FacilityAddress, string | null>> {
	name: string
	facility_name: string
	parent_facility: string | null
	/** A main facility, which can have branches. */
	is_group: 0 | 1
	isic_classification: string
	isic_title: string | null
	/** The region it is in (Naqel Settings' division or below), and its name. */
	region: string | null
	region_title: string | null
	latitude: number | null
	longitude: number | null
	google_maps_location: string | null
	credentials: Credential[]
}

export interface FacilityInput extends FacilityAddress {
	name?: string
	facility_name: string
	isic_classification: string
	parent_facility: string | null
	is_group: 0 | 1
	/** Picked from search_regions when Naqel Settings requires a region. */
	region: string
	google_maps_location: string
	/** A pin dropped on the form's map (used when no Google Maps value is pasted). */
	latitude?: number | null
	longitude?: number | null
	credentials: Credential[]
}

/** A region the facility may be in: its name, the regions above it (nearest first) and the address parts it fills. */
export interface RegionOption {
	value: string
	label: string
	within: string[]
	city?: string
	district?: string
}

/** A credential document type the producer may pick (its flags come from the server). */
export interface DocumentType {
	credential_type: Credential["credential_type"]
	document_type: string
	label: string
	has_expiry_date: 0 | 1
	eligible_for_multiple_facility_branches: 0 | 1
}

export interface FacilitySettings {
	/** The documents a composite facility may share with its annexes (one is required for it). The others come
	 * with the services requested (RequestForm.documents). */
	shared_document_types: DocumentType[]
	requires_region: boolean
	/** The level the region is picked at (Region Division level: District, City…), or null. */
	region_level: string | null
	requires_pin: boolean
	map: { latitude: number; longitude: number; zoom: number }
	country: string | null
}

export interface Option {
	value: string
	label: string
}

export interface Establishment {
	doctype: "Lead" | "Customer"
	title: string
	/** Read-only: kept by the transporter. */
	company_name?: string | null
	customer_type?: string | null
	customer_group?: string | null
	territory: string | null
	/** What the producer may change. */
	industry: string | null
	market_segment: string | null
	website: string | null
	options: { industry: Option[]; market_segment: Option[] }
}

export type EstablishmentInput = Pick<
	Establishment,
	"industry" | "market_segment" | "website"
>

/** A request's life: Draft (the producer's to change), then Ozone's team's. */
export type RequestStatus =
	| "Draft"
	| "Under Process"
	| "Require Clarification"
	| "Clarified"
	| "Quotation"
	| "Contract Quotation"
	| "Contract"
	| "Cancelled"

/** A quotation Ozone's team has sent: Open (waiting for the producer's answer), Accepted or Rejected; Contract once its
 *  contract is submitted. */
export type QuotationStatus = "Open" | "Accepted" | "Rejected" | "Contract"

export interface QuotationSummary {
	name: string
	status: QuotationStatus
	status_label: string
	/** The status's colour in its DocType's states (utils/status: statusBadge). */
	status_color: string
	grand_total: number
	currency: string
}

export interface QuotationCollection {
	waste_type: string
	mechanism: string
	description: string
	count: number
	period_count: number
	period_uom: "Day" | "Week" | "Month" | "Year"
	/** Only when the collection deploys a container at the facility. */
	container: {
		container_type: string
		count: number
		image: string | null
	} | null
}

export interface QuotationDetail {
	name: string
	status: QuotationStatus
	status_label: string
	/** The status's colour in its DocType's states (utils/status: statusBadge). */
	status_color: string
	service_request: string
	service_title: string
	facility_title: string
	transaction_date: string
	valid_till: string | null
	period: {
		start_date: string | null
		end_date: string | null
		duration: number | null
		duration_uom: string | null
	}
	/** How each container line is collected. */
	collections: QuotationCollection[]
	amounts: {
		currency: string
		net_total: number
		taxes: { description: string; amount: number }[]
		discount: number
		grand_total: number
		rounded_total: number
		in_words: string | null
	}
	/** The waste calculation report (HTML, from naqel's template). */
	report: string
	can_decide: boolean
	/** Always false: the producer reads a quotation's comments, its rejection reason aside. */
	can_reply: boolean
	comments: RequestComment[]
}

export interface ServiceRequest {
	name: string
	service_type: string
	service_title: string
	facility: string
	facility_title: string
	status: RequestStatus
	status_label: string
	/** The status's colour in its DocType's states (utils/status: statusBadge). */
	status_color: string
	start_date: string | null
	creation: string
	/** The quotations Ozone's team has sent for it, newest first. */
	quotations: QuotationSummary[]
}

export interface RequestOptions {
	service_types: (Option & { image: string | null })[]
	facilities: Option[]
	statuses: Option[]
}

/** A unit a request is measured in; a composite one is measured part by part. */
export interface MeasureUnit extends Option {
	whole_number: 0 | 1
	composite: 0 | 1
	parts: (Option & { whole_number: 0 | 1 })[]
}

/** A waste type of the request's Service Setup: its default wastes stay on the request (the
 * server keeps them); the producer may add others of the type. */
export interface RequestWasteType {
	waste_type: string
	label: string
	percentage: number
	defaults: Option[]
	wastes: Option[]
}

export interface RequestForm {
	/** The Service Setup the request resolves (the service and the facility's activity). */
	service_setup: string
	/** The default wastes stay (the Service doesn't allow removing them); else they can be removed. */
	defaults_locked: boolean
	uoms: MeasureUnit[]
	waste_types: RequestWasteType[]
	/** A composite facility's annexes, which the request may cover; empty otherwise. */
	annexes: Option[]
	/** The documents the service requires (one of them), and the facility's one already on file. */
	documents: {
		required: DocumentType[]
		on_file: {
			credential_type: string
			document_type: string
			label: string
			document_number: string
			expiry_date: string | null
		} | null
	}
	/** Not for a Milestone-Based service (naqel.utils.service_term). */
	has_end_date: 0 | 1
	/** A Duration-Based service's minimum period: the end date defaults to it, and can't come before it. */
	minimum_period: { count: number; uom: DurationUom } | null
	duration_uoms: Option[]
	grants_license: 0 | 1
	license_statuses: Option[]
}

export interface RequestInput {
	/** The Draft being changed; none for a new request. */
	name?: string
	/** Send it to Ozone's team once saved (it can't be changed then). */
	submit?: boolean
	facility: string
	service_type: string
	facility_uom: string
	facility_measurement?: number | null
	facility_uoms?: { uom: string; uom_value: number }[]
	start_date: string
	/** When the service has one; naqel works out the duration and its unit from the dates. */
	end_date?: string | null
	license_status?: string
	license_no?: string
	license_document?: string | null
	/** The wastes added to each waste type (its defaults are kept by the server). */
	waste_types?: { waste_type: string; wastes: string[] }[]
	/** The annexes covered, for a composite facility. */
	annexes?: string[]
	/** The required document, when the facility has none on file: saved with the facility. */
	document?: Credential
}

export interface RequestComment {
	name: string
	text: string
	/** Written by Ozone's team (else by the producer). */
	from_team: boolean
	creation: string
	/** The files it carries that the producer may open. */
	attachments: { name: string; url: string }[]
}

export interface RequestDetail {
	name: string
	status: RequestStatus
	status_label: string
	/** The status's colour in its DocType's states (utils/status: statusBadge). */
	status_color: string
	service_title: string
	facility_title: string
	can_edit: boolean
	can_reply: boolean
	values: {
		facility: string
		service_type: string
		facility_uom: string | null
		facility_measurement: number | null
		facility_uoms: { uom: string; uom_value: number }[]
		start_date: string | null
		end_date: string | null
		license_status: string | null
		license_no: string | null
		license_document: string | null
		waste_types: { waste_type: string; wastes: string[] }[]
		annexes: string[]
	}
	comments: RequestComment[]
	/** How many more files the record takes (its DocType's Max Attachments); null: no limit. */
	attachments_left: number | null
}

export interface ActivityRecord {
	name: string
	status: string
	status_label: string
	/** The status's colour in its DocType's states (utils/status: statusBadge). */
	status_color: string
}

export interface FacilityActivity {
	requests: ServiceRequest[]
	quotations: (ActivityRecord & {
		transaction_date: string
		grand_total: number
		currency: string
	})[]
	contracts: (ActivityRecord & { contract_date: string })[]
	operation_orders: (ActivityRecord & { service_type: string })[]
}

export interface Activity {
	name: string
	code: string
	title: string
}

const API = "ozone.api.portal"

export function getOverview(): Promise<Overview> {
	return getMethod(`${API}.get_overview`)
}

export function getProfile(): Promise<Profile> {
	return getMethod(`${API}.get_profile`)
}

export function updateProfile(data: ProfileInput): Promise<Profile> {
	return postMethod(`${API}.update_profile`, { data })
}

export function saveAddress(
	data: AddressInput,
): Promise<{ name: string; addresses: Address[] }> {
	return postMethod(`${API}.save_address`, { data })
}

export function getFacilities(): Promise<Facility[]> {
	return getMethod(`${API}.get_facilities`)
}

export function saveFacility(
	data: FacilityInput,
): Promise<{ name: string; facilities: Facility[] }> {
	return postMethod(`${API}.save_facility`, { data })
}

export function searchRegions(txt: string): Promise<RegionOption[]> {
	return getMethod(`${API}.search_regions`, { txt })
}

/** The region a pin falls in, if the facility may be in it. */
export function regionAt(
	latitude: number,
	longitude: number,
): Promise<RegionOption | null> {
	return getMethod(`${API}.region_at`, {
		latitude: String(latitude),
		longitude: String(longitude),
	})
}

export function searchIsic(txt: string): Promise<Activity[]> {
	return getMethod(`${API}.search_isic`, { txt })
}

export function updateAvatar(fileUrl: string | null): Promise<Profile> {
	return postMethod(`${API}.update_avatar`, { file_url: fileUrl })
}

export function getEstablishment(): Promise<Establishment> {
	return getMethod(`${API}.get_establishment`)
}

export function updateEstablishment(
	data: EstablishmentInput,
): Promise<Establishment> {
	return postMethod(`${API}.update_establishment`, { data })
}

export function getFacilitySettings(): Promise<FacilitySettings> {
	return getMethod(`${API}.get_facility_settings`)
}

export function getServiceRequests(
	filters: Partial<Record<"facility" | "service_type" | "status", string>> = {},
): Promise<ServiceRequest[]> {
	return getMethod(`${API}.get_service_requests`, {
		filters: JSON.stringify(filters),
	})
}

export function getRequestOptions(): Promise<RequestOptions> {
	return getMethod(`${API}.get_request_options`)
}

/** `name`: the Draft being changed (it doesn't count as the facility's open request for the service). */
export function getRequestForm(
	facility: string,
	serviceType: string,
	name?: string | null,
): Promise<RequestForm> {
	return getMethod(`${API}.get_request_form`, {
		facility,
		service_type: serviceType,
		...(name ? { name } : {}),
	})
}

/** A new Draft, or a change to one (`name`); with `submit`, it is sent to Ozone's team. */
export function saveServiceRequest(
	data: RequestInput,
): Promise<{ name: string; requests: ServiceRequest[] }> {
	return postMethod(`${API}.save_service_request`, { data })
}

export function getServiceRequest(name: string): Promise<RequestDetail> {
	return getMethod(`${API}.get_service_request`, { name })
}

export function submitServiceRequest(
	name: string,
): Promise<{ name: string; requests: ServiceRequest[] }> {
	return postMethod(`${API}.submit_service_request`, { name })
}

/** The producer's answer to the team's clarification, which makes the request Clarified; `files`: the
 *  URLs of files the producer uploaded for it (uploadFile). The request as it is then. */
export function clarifyRequest(
	name: string,
	text: string,
	files: string[] = [],
): Promise<RequestDetail> {
	return postMethod(`${API}.clarify_request`, { name, text, files })
}

export function getFacilityActivity(
	facility: string,
): Promise<FacilityActivity> {
	return getMethod(`${API}.get_facility_activity`, { facility })
}

/** A submitted quotation and the contract that follows it (none while the team prepares it), or a contract of
 *  the Customer's made without one of its quotations (`quotation` null). */
export interface ContractEntry {
	quotation: string | null
	service_title: string
	facility_title: string
	amount: number
	currency: string
	start_date: string | null
	/** None for a service without one. */
	end_date: string | null
	contract: {
		name: string
		status: string
		status_label: string
		/** The status's colour in its DocType's states (utils/status: statusBadge). */
		status_color: string
		contract_date: string | null
	} | null
}

/** The submitted quotations and the contracts that follow them (not Draft or Cancelled ones). */
export function getContracts(): Promise<ContractEntry[]> {
	return getMethod(`${API}.get_contracts`)
}

/** The requests that have turned into a quotation, each with the quotations sent for it. */
export function getQuotations(): Promise<ServiceRequest[]> {
	return getMethod(`${API}.get_quotations`)
}

export function getQuotation(name: string): Promise<QuotationDetail> {
	return getMethod(`${API}.get_quotation`, { name })
}

/** Accept or reject an Open quotation; a rejection says why. */
export function decideQuotation(
	name: string,
	decision: "Accepted" | "Rejected",
	comment: string,
): Promise<QuotationDetail> {
	return postMethod(`${API}.decide_quotation`, { name, decision, comment })
}

/** A quotation's conversation and status, as its panel refreshes them. */
export interface QuotationThread {
	status: QuotationStatus
	can_reply: boolean
	comments: RequestComment[]
}

export function getQuotationThread(name: string): Promise<QuotationThread> {
	return getMethod(`${API}.get_quotation_thread`, { name })
}
