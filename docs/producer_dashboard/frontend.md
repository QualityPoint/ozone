# Frontend

## Routes

Each route exists in both languages: `/dashboard` and `/en/dashboard`.

| Path | Name | Meta |
| --- | --- | --- |
| `/dashboard` | `Dashboard` (Overview) | `requiresAuth`, `producerOnly` |
| `/dashboard/profile` | `DashboardProfile` | `requiresAuth`, `producerOnly` |
| `/dashboard/establishment` | `DashboardEstablishment` | `requiresAuth`, `producerOnly` |
| `/dashboard/facilities` | `DashboardFacilities` | `requiresAuth`, `producerOnly` |
| `/dashboard/requests` (`?facility=` opens the form on it) | `DashboardRequests` | `requiresAuth`, `producerOnly` |
| `/dashboard/quotations` | `DashboardQuotations` | `requiresAuth`, `producerOnly` |
| `/dashboard/contracts` | `DashboardContracts` | `requiresAuth`, `producerOnly` |
| `/dashboard/not-linked` | `DashboardNotLinked` | `requiresAuth` |

The pages are listed in `dashboardPages` (`config/site.ts`). Pages still to come show in the menu
with a "soon" tag.

## Guard (`router/guards.ts: installAuthGuard`)

It only picks the page. Data access is the server's job.

1. The cookie answers for guests. For anyone else, the server confirms
   (`stores/user.ts` → `get_session_user`).
2. A guest is sent to Login with `redirect-to`.
3. Staff are sent to the Desk.
4. A `producerOnly` page without a producer goes to the not-linked page.
5. Once linked, the not-linked page goes to the dashboard.

## Files

| File | Role |
| --- | --- |
| `layouts/DashboardLayout.vue` | Top bar (logo, producer, theme, language, logout), and the menu: at the side from `lg`, a scrolling row on phones |
| `components/dashboard/DashboardNav.vue` | The menu, from `dashboardPages` |
| `views/dashboard/OverviewView.vue` | The producer's stage (Lead or Customer), name and counts |
| `views/dashboard/ProfileView.vue` | My account (name, mobile), the party (read-only), addresses (add, edit) |
| `views/dashboard/EstablishmentView.vue` | The establishment: read-only details, and industry, market segment, website |
| `views/dashboard/FacilitiesView.vue` | The facility tree (annexes under their composite facility) with each one's activity and a link to request a service, and the form: details, address, location (pasted or on the map), credentials |
| `views/dashboard/ContractsView.vue` | The Contracts page: the producer's contracts, read only, or a pointer to Quotations while there are none |
| `views/dashboard/QuotationsView.vue` | The Quotations page: the requests that have turned into a quotation, each with its sent quotations (QuotationPanel; one awaiting the answer opens by itself) or "being prepared" |
| `views/dashboard/RequestsView.vue` | The requests with filters, and the form to raise one or change a Draft (saved as a Draft, or sent). A Draft row offers Edit and Send (after a confirmation); a sent row its comments, where Send clarification answers the team (`clarifyRequest`): the row turns Clarified at once and its thread stays open on the answer |
| `components/dashboard/CommentThread.vue` | A record's comments with Ozone's team and the answer box (`load` and `send` props), with its files (Attach files: as many as the record's `attachments_left`, uploaded as picked, private; the types website users may upload): a request's (open by default while it requires clarification), a quotation's. It reads them again every 15 seconds while the tab is visible and when the producer returns to the tab, so the team's answers appear without a reload (a quotation's status changed meanwhile reloads its panel, which stays open) |
| `components/dashboard/QuotationPanel.vue` | A sent quotation under its request (open by default while it awaits the answer): the amount, the period, each set's collection (a waste type's, or the whole facility's; its waste type when there are several; the container only when deployed), the waste report, Accept / Reject (a rejection needs its reason, sent only with it; both confirm) and the conversation, read only. Counts use `utils/format.counted` with plural forms in the messages (no vue-i18n placeholders) |
| `components/dashboard/FacilityMap.vue` | Leaflet map: click to drop the pin, drag to move it |
| `components/dashboard/FileField.vue` | Uploads a document (`services/http.ts: uploadFile`) and holds its URL |
| `utils/status.ts` | `statusBadge`: a status badge (requests, quotations, contracts, a facility's activity) in its DocType state's colour, as the server sends it (`status_color`), styled like the Desk's indicator pills |
| `components/dashboard/DashboardHeading.vue` | A page's corner-marked title, intro and main action |
| `components/dashboard/IsicPicker.vue` | Search and pick an ISIC activity |
| `components/base/BaseSelect.vue` | A select in BaseInput's look |
| `composables/useFormSubmit.ts` | How a form sends: errors after the first try, the server's own refusal text |
| `views/dashboard/NotLinkedView.vue` | "Being linked", with Ozone's contact buttons (`useContactActions`). Only for an account whose email is on a Customer's contact: any other is linked on arrival (`stores/user.ts` → `start_producer`) |
| `services/portal.ts` | Calls `ozone.api.portal` |
| `stores/user.ts` | `isStaff`, `producer` |
| `components/layout/AccountLink.vue` | The header's account link: Login, the dashboard, or the Desk |

Texts: `dashboard.*` in `i18n/locales/{ar,en}/dashboard.ts`.

## The first step: the facility

A producer starts by registering its facility; everything else (requests, then quotations and contracts) is
for one. `get_session_user` returns the producer's `facilities` count, and while it is 0:

- the guard sends the overview (`/dashboard`, where every login lands) to the Facilities page;
- the Facilities page opens the new-facility form with a "start here" notice;
- once the first facility is saved, it offers the next step, a service request for it
  (`/dashboard/requests?facility=…`), and reloads the session so the overview opens again.

The menu follows the same order: Overview, Facilities, Service requests, then My details and Establishment.
