# Server Side (Frappe App)

What the `ozone` Frappe app does for the website. The SPA itself is in
[architecture.md](architecture.md).

## Files

| File | Role |
| --- | --- |
| `ozone/hooks.py` | `home_page = "frontend"`, `website_route_rules` for `/en` and `/en/<path>` |
| `ozone/www/frontend.py` | Renders the SPA shell: SEO values (`context.seo`) and boot data (`context.boot`). `resolve_page` maps the path to a page and language with the SPA's `meta.json`, which also gives the title and description. Known pages get a canonical and hreflang links; other paths are `noindex`. `no_cache = 1` |
| `ozone/www/frontend.html` | Build output (git-ignored): the Jinja shell made by `yarn build` |
| `ozone/api/` | Every whitelisted method, one module per area (`ozone.api.<area>.<method>`): thin, they call the modules below |
| `ozone/site_contact.py` | Contact details and social links from Ozone Settings |
| `ozone/locales.py` | Shared: `shared_json` reads the SPA's `meta.json`; `SUPPORTED_LOCALES`, `DEFAULT_LOCALE` |
| `ozone/tests/` | Python tests: `test_frontend.py` (addresses, SEO per language), `test_site_contact.py` (what the site shows) |
| `ozone/ozone/doctype/` | `Ozone Settings` (with its validation tests) and its child tables `Localized Address`, `Social Media Link` |

## Endpoints

All under `/api/method/`. Guest endpoints are public, so they return only what the website
shows anyway.

| Method | Access | Returns |
| --- | --- | --- |
| `ozone.api.site.get_site_contact` (GET) | guest | Same data as `window.site_contact`. Used by the dev server, which has no boot data |

## Boot data

`www/frontend.py` puts these keys in `context.boot`. frappe-ui's `jinjaBootData` copies each
onto `window` (typed in `frontend/src/env.d.ts`):

| Key | Content | Used by |
| --- | --- | --- |
| `csrf_token` | Session CSRF token (committed during the GET so it persists) | Forms, when there are any |
| `site_name` | Site name | |
| `site_contact` | `{ email, phone, whatsapp, address: { <language code>: text }, map, socials: [{ platform, url }] }` | `useSiteContact()` |

On the dev server (`yarn dev`, port 8080) the page isn't rendered by Frappe, so none of
these exist. `useSiteContact()` calls the API instead, through `services/http.ts`
`getMethod`.

## Ozone Settings

A single DocType in module Ozone. Edit it in the Desk: Ozone sidebar → Settings → Ozone
Settings (`/desk/ozone-settings`). Permission: **Website Manager** (and Administrator).

| Field | Type | Shown on the website |
| --- | --- | --- |
| `email` | Data (Email) | Footer |
| `contact_phone` | Data (Phone) | Footer; Saudi numbers formatted `+966 50 000 0000`, left to right on Arabic pages too |
| `whatsapp` | Data | Footer link "WhatsApp" (`wa.me/<digits>`) |
| `addresses` | Table → **Localized Address** | Footer: the row in the page's language; line breaks are kept. No row for that language, no address |
| `map_link` | Data (URL) | Footer link "Find us on the map" |
| `social_media_links` | Table → **Social Media Link** | Footer icons, in the table's order |

**Localized Address** (child table): one address per language, so a new language needs a row, not a new field.

| Field | Type | Notes |
| --- | --- | --- |
| `language` | Link → Language, required | Frappe's Language records are named by code (`ar`, `en`, `fr`), the codes the site uses |
| `address` | Small Text, required | The address as it should read in that language |

**Social Media Link** (child table, as in blinktech):

| Field | Type | Notes |
| --- | --- | --- |
| `platform` | Select, required | Facebook, Snapchat, Instagram, Threads, X, TikTok, LinkedIn, YouTube, Telegram, Linktree |
| `link` | Data (URL), required | A full URL starting with `https://` |
| `published` | Check | Unpublished rows stay in the table but aren't shown |

**Validation** (`OzoneSettings.validate`):

- each language may have only one address, and each platform only one link: a field in a child
  table can't be made unique, so one helper, `unique_rows`, checks both tables;
- every link (the map link and each social link) must be a full `https://` URL. One helper,
  `https_link`, checks them all and trims surrounding spaces.

**Rules:**

- **No fallbacks.** Nothing about contact details is hard-coded in the frontend. A field left
  empty hides that detail on the site, and with nothing filled in, the footer's contact column
  is hidden.
- **Changes show on the next page load.** `site_contact()` reads `frappe.get_cached_doc`, which
  Frappe clears on save, and the page is `no_cache`.
- The frontend also filters what it receives (`sanitizeContact`): unknown platforms and
  non-`https://` links are dropped, so bad data can't produce a broken or unsafe link.

## Changing a DocType

1. Edit it in the Desk (developer mode) or edit the JSON. If you edit the JSON by hand, keep
   Frappe's format (sorted keys, 1-space indent) and bump `modified`, or `bench migrate`
   skips it.
2. Apply it: `bench --site ozone.local migrate`.
3. Adding a Platform option also needs `SOCIAL_PLATFORMS` (`src/types/index.ts`) and an icon
   path (`src/components/icons/socialIconPaths.ts`).

## Tests

```bash
bench --site ozone.local run-tests --app ozone
```

`test_site_contact.py` saves Ozone Settings, then rolls back and clears the cached copy in
`tearDown`, so the site's real settings come back.
