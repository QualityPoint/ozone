# API

Thin methods. The rules live in `ozone/producer.py` and `ozone/auth.py`.

## `ozone.api.auth` (open to guests)

| Method | Returns | Rule |
| --- | --- | --- |
| `get_session_user` | `{name, full_name, user_type, producer}`. `producer` is `{doctype, name, title, facilities}` or null | [identity.md](identity.md) |
| `start_producer` (POST) | The same answer, after making an unlinked Website User a producer of its own: its Lead, linked through its Contact, as a sign-up does (`create_signup_lead`, with no Lead Owner). The SPA's user store calls it whenever a Website User has no party, so an account made in the Desk or by a social login goes straight to registering its facility. An email on a Customer's contact stays unlinked (Portal Users) | [accounts.md](accounts.md) |
| `get_login_options` | The sign-in methods enabled on the site, including `signup` | Frappe's System and Website Settings |
| `sign_up` (POST) | Frappe's `(status, message)`: 0 already registered, 1 check email, 2 pending approval | [accounts.md](accounts.md) |
| `social_login` (GET) | A redirect to the provider | Enabled, fully configured providers only |

## `ozone.api.portal` (logged-in producers)

Each method starts with `require_producer()`. Anyone else gets `PermissionError`.

Every `status_label` comes with `status_color`: the status's colour in its DocType's states (`portal.status_color`, gray without one), the colour the Desk shows it in. The dashboard draws its badges with it (`utils/status.ts`), never colours of its own.

| Method | Returns |
| --- | --- |
| `get_overview` (GET) | `{producer, counts: {facilities, service_requests}}` |
| `get_profile` (GET) | `{email, first_name, last_name, mobile_no, user_image, party: {doctype, title}, addresses, address_types}` |
| `update_avatar` (POST `file_url`) | The profile. The image must be one the user uploaded (Frappe's `upload_file`); none removes it |
| `get_establishment` (GET) | The producer's Lead or Customer: name, type, group and territory (read-only), industry, market segment and website, and the `options` to pick them from |
| `update_establishment` (POST `data`) | The establishment, after setting industry, market segment and website (nothing else) |
| `get_facility_settings` (GET) | `shared_document_types`: the documents a composite facility may share with its annexes (`{credential_type, document_type, label, has_expiry_date, eligible_for_multiple_facility_branches}`); whether a region or a pin is required, the map's default centre, the default country |
| `update_profile` (POST `data`) | The profile, after saving the user's Contact |
| `save_address` (POST `data`, with `name` to edit) | `{name, addresses}` |
| `get_facilities` (GET) | The producer's facilities in tree order: name, parent, `is_group`, activity and region titles (not the rating: the desk's own), pin, address, credentials |
| `get_facility_settings` (GET) | `shared_document_types`, `requires_region` and `region_level` (Naqel Settings: a region is required, picked at the assigned Region Division's level, e.g. District), `requires_pin`, the map's start and the country |
| `search_regions` (GET `txt`) | Regions at the assigned division or below matching a name or alias: `{value, label, within (the regions above, nearest first), city, district}` |
| `region_at` (GET `latitude`, `longitude`) | The allowed region a dropped pin falls in, or null |
| `save_facility` (POST `data`, with `name` to edit) | `{name, facilities}`. `region` must be one `search_regions` offers; naqel's Facility then sets the city (its City-level region) and, for a District, the district, and a region picked by hand wins over the pin's. The rating isn't taken (the desk sets it). `google_maps_location` is resolved to a pin on the server (`map_location.resolve_map_location`), and the controller sets the region. `credentials`, for a composite facility only: its shared documents (number and uploaded file each), added or updated by document type; an annex takes its parent's shared documents. Other documents come with requests. The country defaults to the system's |
| `search_isic` (GET `txt`) | Up to 20 ISIC activities (leaves) matching a code or name |
| `get_service_requests` (GET `filters`: facility, service_type, status) | The producer's requests, newest first (not those that moved on: Quotation, Contract Quotation, Contract), with service, facility and status labels, and `quotations` (`[{name, status, status_label, grand_total, currency}]`: the ones the team has sent) |
| `get_request_options` (GET) | The services, the producer's facilities, and the statuses |
| `get_request_form` (GET `facility`, `service_type`, `name`: the Draft being changed) | Refused while the facility has another open request for the service (naqel's `open_request`: one that isn't cancelled, a Draft included). How a request for that service at that facility is measured: the Service Setup the request will resolve (`service_setup`), its units (a composite unit with its `parts`), its `waste_types` (each with its share, its `defaults` and the `wastes` that may be added), the composite facility's `annexes`, `documents` (`required`: the service's Registration Documents; `on_file`: the facility's one that answers them), whether the service has an end date (`has_end_date`: not for a Milestone-Based service) and a Duration-Based service's `minimum_period` (`{count, uom}`, or null), which the form's end date defaults to, the duration units, whether it grants a license. Refused when no Service Setup exists for the facility's activity |
| `get_service_request` (GET `name`) | One of the producer's requests: `status`, `can_edit` (a Draft), `can_reply` (Require Clarification), `values` (as `save_service_request` takes them; `waste_types` lists only the added wastes), `attachments_left` (how many more files its DocType's Max Attachments allows; null without a limit) and `comments` (`[{name, text, from_team, creation, attachments}]`, oldest first, as plain text; `attachments` (`[{name, url}]`) are the files a comment links to that are attached to the record and that the producer may open: its own, not the team's private ones) |
| `submit_service_request` (POST `name`) | `{name, requests}`. Submits one of the producer's Drafts (naqel's checks run again): Under Process, no longer changeable |
| `clarify_request` (POST `name`, `text`, `files`) | The producer's answer to the team's clarification, which makes the request Clarified (naqel's `ServiceRequest.clarify`); returns the request as `get_service_request` does. Only while it is in Require Clarification; up to 4000 characters, escaped. `files`: URLs of files the producer uploaded (Frappe's `upload_file`, private) and hasn't attached yet; they are attached to the request and linked in the comment, as many as its DocType's Max Attachments still allows (counting every file attached to it; Frappe checks it only for a file inserted attached). Text or a file is needed |
| `get_contracts` (GET) | The producer's Service Contracts (its Customer's; not Draft or Cancelled), newest first: status, dates, duration, net total and currency, with the service and facility of the quotation each follows, or of the request it follows straight away (listed "being prepared" from the contract's draft on; `document_type` / `document_name`). Read only |
| `get_quotations` (GET) | The producer's requests that have turned into a quotation (status Quotation), newest first, each with `quotations` (those sent; none while the team prepares it). `get_service_requests` leaves them out |
| `get_quotation` (GET `name`) | A quotation the team has sent (Open, Accepted, Rejected): `amounts` (net, taxes, discount (0: naqel applies none yet), grand and rounded total, currency), `period`, `collections` (one per container line: its `waste_type`, `mechanism`, its `description`, `count` times every `period_count` `period_uom`, and `container` (`{container_type, count, image}`: the collection container) only when the line's mechanism deploys one), `report` (naqel's `client_waste_report`, rendered now in the producer's language, naming no container type), `can_decide`, `can_reply` (false: the producer doesn't write on a quotation), `comments` |
| `decide_quotation` (POST `name`, `decision`: Accepted or Rejected, `comment`) | The quotation, answered. Only an Open one; a rejection needs the comment (its reason), which goes into its comments; an acceptance carries none |
| `get_quotation_thread` (GET `name`) | `{status, can_reply, comments}`: what the quotation's conversation refreshes, without rendering the report |
| `save_service_request` (POST `data`; `name` to change a Draft, `submit` to submit it once saved) | `{name, requests}`. `waste_types` (`[{waste_type, wastes}]`) carries each waste type's whole selection, defaults included; naqel keeps the defaults unless the Service allows removing them (`get_request_form` says so in `defaults_locked`), and each type needs one waste. A Draft from the producer's party: facility (its own), service, unit and size (or `facility_uoms` for a composite unit), `waste_types` (`[{waste_type, wastes}]`: the wastes added; the defaults are kept by naqel), `annexes` (a composite facility's own, which the request covers), `document` (`{credential_type, document_type, document_number, credential, issue_date, expiry_date}`: one of the service's Registration Documents with its uploaded file, required when the facility holds none; saved in the **Facility's** credentials), start date and, when the service has one, end date (naqel keeps them to the service's term, an end at its minimum period at the earliest, and works out the duration and its unit from them: `service_term.set_term_dates`, `party.duration_between`), license status, number and document when the service grants a license |
| `get_facility_activity` (GET `facility`) | The facility's requests, quotations, contracts and operation orders, only the producer's own |

The rules behind them are in `ozone/portal/`: `profile.py`, `establishment.py`, `facilities.py`, `requests.py`, and the shared
`pick` and `own_doc` in `__init__.py`.
