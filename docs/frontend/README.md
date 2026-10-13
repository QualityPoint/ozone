# Ozone Frontend: Docs Index

A Vue 3 + TypeScript single-page app in `apps/ozone/frontend/`, built on the
[frappe-ui](https://ui.frappe.io) starter. It is Ozone Environmental Services' public website:
Arabic at `/` (the default) and English at `/en`. The project is organized like blinktech's
(`apps/blinktech/frontend`, `apps/blinktech/docs/frontend`), and its docs follow the same
layout.

## At a glance

| | |
| --- | --- |
| Stack | Vue 3.5, TypeScript, vue-router 4, frappe-ui 0.1.278, Tailwind 3.4, Vite 5 |
| Served by | Frappe: `home_page = "frontend"` renders `ozone/www/frontend.html` with the boot data from `www/frontend.py` ([architecture.md](architecture.md#production)) |
| Languages | Arabic (default, `/`) and English (`/en`), from the next step on |
| Local site | `ozone.local` on `:8000` (production build), `:8080` with `yarn dev` |

## Status

| Step | State |
| --- | --- |
| 1. Scaffold, build and serving | Done: placeholder landing page at `/` |
| 2. Brand, layout, Arabic/English, SEO | Next |
| 3. Ozone Settings (contact details) | |
| 4. Landing sections | |
| 5. Polish | |

## Docs

| File | What it covers |
| --- | --- |
| [architecture.md](architecture.md) | Folder layout, routing, dev vs production serving |
| [conventions.md](conventions.md) | Where new code goes, naming, routes, tests, the checks to run |
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
