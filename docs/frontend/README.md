# Ozone Frontend: Docs Index

A Vue 3 + TypeScript single-page app in `apps/ozone/frontend/`, built on the
[frappe-ui](https://ui.frappe.io) starter. It is Ozone Environmental Services' public website:
Arabic at `/` (the default) and English at `/en`. The project is organized like blinktech's
(`apps/blinktech/frontend`, `apps/blinktech/docs/frontend`), and its docs follow the same
layout.

## At a glance

| | |
| --- | --- |
| Stack | Vue 3.5, TypeScript, vue-router 4, vue-i18n 11, frappe-ui 0.1.278, Tailwind 3.4, Vite 5 |
| Served by | Frappe: `home_page = "frontend"` and `/en` route rules render `ozone/www/frontend.html`, with boot data and server-side SEO from `www/frontend.py` ([architecture.md](architecture.md#production)) |
| Languages | Arabic (default, `/`, RTL) and English (`/en`) ([i18n.md](i18n.md)) |
| Themes | Light and dark, following the system until the visitor picks one ([branding.md](branding.md#light-and-dark)) |
| Editable in the Desk | Phone, email, WhatsApp, address, map link and social links: **Ozone Settings** ([server.md](server.md#ozone-settings)) |
| Local site | `ozone.local` on `:8000` (production build), `:8080` with `yarn dev` |

## Status

| Step | State |
| --- | --- |
| 1. Scaffold, build and serving | Done |
| 2. Brand, layout, Arabic/English, SEO | Done: header, footer, brand motifs, a placeholder hero |
| 3. Ozone Settings (contact details) | Done: the footer's contact column, the Desk link |
| 4. Landing sections | Done: hero, about, services, equipment, industries, why us, contact |
| 5. Polish | Next |

## To confirm before publishing

The landing page's content comes from Ozone's operation files (`~/Projects/Ozone/References`). These claims come from a proposal document, so confirm them with Ozone before the site goes public:

| Claim | Where |
| --- | --- |
| +50,000 tonnes recycled a year, +200 clients | `stats` in `src/config/site.ts`, `why.stats` |
| Working to ISO 14001 | `why.pillars` (environmental commitment) |
| Recycling 90% of collected waste (stated as a goal) | `about.goals`, `stats` |

Also fill in Ozone Settings: the contact section shows no buttons until it is.

## Docs

| File | What it covers |
| --- | --- |
| [architecture.md](architecture.md) | Folder layout, routing, dev vs production serving |
| [conventions.md](conventions.md) | Where new code goes, naming, routes, tests, the checks to run |
| [i18n.md](i18n.md) | Arabic and English: addresses, messages, `meta.json`, adding a page |
| [branding.md](branding.md) | Palette, light and dark, fonts, the documents' motifs, logo and icon files |
| [styling.md](styling.md) | Tailwind and the frappe-ui preset, shared classes, right to left, motion |
| [how-to.md](how-to.md) | Recipes: texts, list items, services and sectors, figures, equipment photos, nav, contact details, responsive checks |
| [server.md](server.md) | The Frappe side: hooks, boot data, endpoints, Ozone Settings and its validation, tests |
| [setup-history.md](setup-history.md) | How the project was scaffolded |
| [changes-from-starter.md](changes-from-starter.md) | Every edit made on top of the starter template, and why |

## Commands (run in `apps/ozone/frontend/`)

| Command | Does |
| --- | --- |
| `yarn dev` | Vite dev server on port 8080, proxying the backend on `:8000` |
| `yarn build` | Production build into `ozone/public/frontend/`, plus `ozone/www/frontend.html` |
| `yarn type-check` | vue-tsc on project files only |
| `yarn test:run` | Vitest unit tests |
| `yarn lint` | Biome check and autofix |
| `~/frappe-bench/env/bin/python scripts/build-brand-assets.py` | Regenerate logos, favicons and the social image from `~/Projects/Ozone` ([branding.md](branding.md#logo-and-icon-files)) |
