# Notifications

What Ozone's team does on a producer's records tells the producer in its dashboard: a bell in the top bar
(`NotificationBell.vue`) with the unread count, each notification opening its page and marked read. Dashboard only:
nothing is e-mailed.

## What notifies

| Event | Hook (`ozone/notifications.py`) | Opens |
| --- | --- | --- |
| A quotation sent to the producer (Open), waiting for its answer | Service Quotation `on_update`: `quotation_sent` | Quotations |
| A Service Request it is asked to clarify | Service Request `on_update_after_submit`: `clarification_asked` | Requests |
| A contract awaiting its payment: its Sales Order submitted, its Service requiring an advance or a full payment | Sales Order `on_submit`: `contract_awaits_payment` | Contracts |
| A payment received against a contract's Sales Order | Payment Entry `on_submit`: `payment_received` | Contracts |
| A contract issued (submitted) | Service Contract `on_submit`: `contract_issued` | Contracts |
| A contract renewed (a new period, the previous one archived) | Service Contract `on_update_after_submit`: `contract_renewed` | Contracts |

## How

- Each is Frappe's **Notification Log** of type **Alert**, which Frappe never e-mails (`get_skip_email_types`), for each
  website user of the party the record belongs to: a Customer's Portal Users, a Lead's Contacts' users
  (`producer.party_users`, the reverse of `get_producer`).
- Its subject is written in that user's language (`User.language`, else the site's): Arabic or English, from
  `ozone/translations/ar.csv`.
- Its `link` is the dashboard section it opens in (`SECTIONS`: quotations, requests, contracts); the frontend makes
  the localized path.
- The API: `get_notifications` (the latest 30 and the unread count) and `mark_notifications_read` (some, or all),
  only the session user's own (`ozone/portal/notifications.py`). The bell loads them when the dashboard opens, every
  minute, and when it is opened.

## Checked on naqel.local (2026-10-27, rolled back)

A Website User with Arabic as its language, in a Customer's Portal Users: a quotation sent, a request asked to clarify,
the contract's Sales Order submitted (awaiting 1,800), a payment of 1,800 and the contract submitted each wrote one
Alert in Arabic, in its section; the API listed 5 unread, 4 after one was read, 0 after all; no e-mail queued.
