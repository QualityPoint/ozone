# Testing

## Automated

| Where | What |
| --- | --- |
| `frontend/src/components/auth/__tests__/authHelpers.test.ts` | Where a login goes, by user type and language. Safe redirects (hawya's tests) |
| `frontend/src/router/__tests__/routes.test.ts` | The routes in both languages, with their meta |

```bash
cd frontend && yarn type-check && npx biome check . && yarn test:run
```

**Server tests:** hawya's (`test_auth`, `test_producer`, `test_portal_*`, with the `producers.py` builders) are not
ported yet. ozone is installed only on naqel.local, a development site where `bench run-tests` must not run
(ERPNext's test bootstrap commits test companies and settings). They need a test site with naqel and ozone.

## Manual (2026-10-15)

The server flow was run in rolled-back transactions on naqel.local, and the pages in headless Chrome as a demo
producer (`demo.producer@example.com`, a Lead; left on the site with its facility and request).

| Check | Result |
| --- | --- |
| Sign-up's Lead | One Lead and one Contact with `user` set; `get_session_user` returns the Lead as the producer |
| Facility from the form (Arabic): name, activity search, pasted location | Saved; region الورود from the pin; no rating anywhere (the desk's own) |
| Composite facility + annex (rolled back) | The annex listed under it; the request form offers it; the request covers it |
| Request from the form: service, size, start, duration, license, an added waste | A Draft from the producer's Lead, Service Setup resolved, end date 2027-04-30, the Recyclable defaults kept with Clear Glass added |
| Edit a Draft from the list, Save as draft | The form opens on its values (size, dates, wastes); "Your draft is saved" |
| Send a Draft from the list (confirm) | Under Process; the row shows Comments instead of Edit and Send |
| A desk user asks for clarification | The row is outlined in red, its comments open with the question; the answer appears as "You" and in the Desk timeline |
| Clarified, then Create → Service Quotation in the Desk | The request is Quotation; deleting its only quotation brings it back to Under Process |
| Create → Service Quotation, set the collection mechanism and frequency, Calculate Service Price, save | The Service Setup and wastes come from the request; containers priced per rental period (4 ياردة at 650 SAR/month, twice a day → 1,300 × 3 months = 3,900) |
| Send to Client, then the request in the dashboard | The quotation opens under the request: amount, period, mechanism and "مرتان كل يوم", the report in Arabic without container types; with Container Deployment, the container type shows |
| Attach files to a comment (a PDF and a picture), remove one, send; send with files only | The comment shows its files as links that open; the Desk shows them in the record's attachments and linked in the timeline comment. A file-only comment is sent; an empty one is refused. On a request (Max Attachments 5, its documents included), Attach files goes once it is full, and more files are refused |
| Reject without a comment / with one; Send Again; Accept | Refused / Rejected with the comment in the Desk timeline / Open again / Accepted |
| A party or status sent by the client | Ignored |
| Another producer's facility | "Not permitted." |
| `/en/dashboard/requests` | English labels, the request listed |
| `/signup` with sign-up off | The "not available" notice |
| Staff on `/dashboard` | Sent to `/desk` |
