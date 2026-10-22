# Producer Dashboard

Ozone's website has two kinds of user, as in ERPNext:

| User | Frappe user type | Works in |
| --- | --- | --- |
| **Ozone's team** (the Company and its employees) | System User | The Desk (`/desk`) |
| **Producer**: the client, as a Lead or a Customer | Website User | This dashboard (`/dashboard`, `/en/dashboard`) |

The dashboard works like **ERPNext's customer portal**. Producers have no DocType permissions.
ozone's own API scopes every answer to the producer's records. It works on **naqel**'s doctypes
(Facility, Service Request, Service, Service Setup, ISIC Classification), so ozone requires the
naqel app (`required_apps` in `hooks.py`).

Ported from hawya's `naqel` branch (`apps/hawya`, its `docs/producer_dashboard/`), adapted to
today's naqel:

| hawya | ozone, on naqel |
| --- | --- |
| Service Type, License Type, Identification Number | Service, Service License, Government ID |
| Service Settings | Naqel Settings (Services tab) |
| Main facility and branches | Composite facility (`is_group`) and its annexes |
| The request's waste configuration (regional or not), conversion factor | The Service Setup only (service + the facility's activity): it decides the units and the waste types |
| — | The request's **waste types**: each type's default wastes stay, the producer adds others of the type |
| — | A composite facility's request lists the **annexes** it covers |
| `Facility.has_website_permission` | A `has_website_permission` hook in ozone |

## Status

| Part | Covers | State |
| --- | --- | --- |
| Server | Who a producer is, access rules, the `ozone.api.auth`, `ozone.api.portal` and `ozone.api.site` endpoints, the Lead → Customer carry-over | Done |
| SPA | Sign-up, the login pages' redirects, the dashboard frame, Overview, My details (with a picture), Establishment, Facilities (address, map, credentials, activity), Service requests (with waste types and annexes; drafts edited and submitted; the clarification comments) | Done |
| Next | Quotations and contracts pages (listed as "soon"); server tests (below) | |

## Before producers can sign up and add facilities

- **Sign-up:** Website Settings → *Disable Signup* must be off (it is on, on naqel.local), and an
  outgoing Email Account must exist for the welcome email. Portal Settings → *Default Role* may give
  new accounts a role.
- **Facilities:** an ISIC activity (a leaf of the ISIC Classification tree), a street, city and
  country. For a composite facility with annexes, a credential whose document type is *Eligible For
  Multi-branched Facility*: on naqel.local no Government ID is, so mark one (Commercial Registration)
  first.
- **Requests:** a Service Setup for the service and the facility's activity, with default wastes for
  each waste type (naqel requires them).
- **Request lifecycle:** a request is a Draft the producer can change until it submits it; then it is Under
  Process. A desk user who may write Service Requests asks for clarification when needed (Require
  Clarification, with the question added to the comments), the producer answers in the dashboard, the desk
  marks it Clarified and makes the Service Quotation (the request becomes Quotation). The desk calculates and
  prices it, then sends it to the client (Open), who accepts or rejects it (a rejection's reason goes into its comments; the client only reads them otherwise). See naqel's
  `docs/modules/naqel_contracting/service_request.md`.
- **Documents:** each Service lists the documents it requires (Service → Registration Documents). The
  first request for a facility asks for one of them, with its number and uploaded file, and saves it in the
  **Facility's** credentials; later requests show it as on file. Naqel Settings no longer has a facility-credential
  policy.

## Docs

Each file covers one concern.

| File | Concern |
| --- | --- |
| [identity.md](identity.md) | Who a producer is, and which records are theirs |
| [accounts.md](accounts.md) | How a producer's account comes to exist |
| [access.md](access.md) | What a producer may read and write, and how the server enforces it |
| [routing.md](routing.md) | Where a login goes, for staff and for producers |
| [api.md](api.md) | Each server method the dashboard calls |
| [frontend.md](frontend.md) | The dashboard's routes, guard, layout and pages |
| [testing.md](testing.md) | The automated tests and the manual check |

The login pages themselves are in [../frontend/auth.md](../frontend/auth.md).
