# What a producer may read and write

This is ERPNext's portal pattern.

| Rule | How | Source |
| --- | --- | --- |
| **No DocType permissions** | The Customer role (ERPNext gives it to website users through Portal Users) may only read Service, a catalogue, and keep the Container Surveys it made (`if_owner`). Facility, Service Request, Service Quotation, Container and Waste Calculator grant it nothing, so `/api/resource` returns nothing of them; the dashboard reads through `ozone/portal/` | `website_list_for_contact.py: get_transaction_list` ("customers… do not have direct access to internal doctypes") |
| **Lists** | First the producer's records (`owned_names`), then read with `ignore_permissions` | The same function |
| **One record** | `owns(doctype, name, producer)` (`producer.py`). ozone answers Frappe's `has_website_permission` for Facility with it (`hooks.py` → `producer.facility_website_permission`; naqel's Facility is left as it is), which Frappe calls first | `frappe/__init__.py: has_website_permission` |
| **Writes** | Allowlisted fields only (`ozone/portal/`: `pick`). New records are linked to the producer's party on the server. The controller's validation still runs | `web_form.py: accept` (Web Forms) |
| **Unknown or foreign names** | The same `PermissionError` (`own_doc`), so nothing tells whether another producer's record exists | — |
| **The party** | Never taken from the client: `require_producer()` reads it from the session | — |

## Who owns what

`OWNER_FIELDS` in `ozone/producer.py`. To add a DocType to the dashboard, add a row here.

| DocType | Owner field(s) | ERPNext pattern | A Lead sees it |
| --- | --- | --- | --- |
| Address | `links` (Dynamic Link rows) | Frappe's own | Yes |
| Facility | `links` (Dynamic Link rows) | Address, Contact | Yes |
| Facility credential (from a request) | One of the requested service's Registration Documents: document type, number, uploaded file (their own), issue and expiry dates | The facility (the request's), the row's flags (from the document type) |
| Service Request | `request_from` + `party` | Quotation's `quotation_to` + `party_name` | Yes |
| Operation Order | `customer` | Sales Order | No: a Customer only |

Cancelled records of submittable DocTypes are left out.

## What a producer may change

| Record | Fields | Fixed by the server |
| --- | --- | --- |
| Their Contact | First and last name, primary mobile | The email (it is the login) |
| Address | Type, two lines, city, region, postcode | Country (the system default), title (the party), links |
| Their User | Picture (an image they uploaded) | Everything else |
| Establishment (their Lead or Customer) | Industry, market segment, website | Name, customer type and group, territory |
| Facility | Name, activity (a leaf of the ISIC tree), composite facility or annex, parent, location (a pasted value or a pin dropped on the map), address (street, building and secondary numbers, district, city, postcode, country), credentials (type, document type, number, file, dates) | Links, and the rating: the desk's own assessment, never read or set here (nor named in the waste report the producer sees). The parent must be one of the producer's **composite** facilities: Frappe's tree lets only a group have children (`nestedset.py: validate_ledger`) |

| Service Request (new, or one of their Drafts) | Facility (their own) and, for a composite facility, the annexes it covers (its own), service, unit and size, the wastes added to each waste type, start date, duration, license status, number and document; submitting it | `request_from` and `party` (their party), status (Draft until submitted, then Under Process), the end date, the Service Setup and the waste types' default wastes (always kept: naqel's `ServiceRequest.set_waste_types`), activity and region. A submitted request can't be changed |
| Comment (on their request or quotation) | The text, and files they uploaded for it (attached to the record, up to its DocType's Max Attachments; only files of their own not yet attached anywhere): on a request while it is in Require Clarification (sending it makes the request Clarified, the one status the producer sets after submitting). On a quotation only the reason of a rejection (no files); its comments are otherwise read only | Type *Comment*, the author (their user), the record. The text is escaped (`portal/comments.py`). They read all the record's comments, the team's without their authors' names |
| Service Contract (its Customer's, once issued: not Draft or Cancelled) | Nothing: read only | Everything |
| Service Quotation (one the team has sent: Open, Accepted, Rejected) | Accept or reject an Open one; a rejection needs a comment | Everything else. A Draft isn't visible: reading one is refused as for another producer's. The container type is shown only when the collection mechanism deploys a container; the waste report names none |

The party's own name and legal details stay with Ozone.

**Files** (avatars, credential and license documents) go through Frappe's `upload_file`. The server
accepts a file only if this user uploaded it (`File.owner`), or, for a credential, the row already had
it, so nobody can point a record at another user's file.

