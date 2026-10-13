# Changes From the Starter Template

Everything that differs from what `bench add-frappe-ui` generated. Each change matches
blinktech's (`apps/blinktech/docs/frontend/changes-from-starter.md`), where the reasons are
explained in full.

## Fixes (the starter was broken)

| File | Change | Why |
| --- | --- | --- |
| `src/index.css` → `src/assets/styles/main.css` | Imports `frappe-ui/style.css` | The only path frappe-ui ≥0.1.2xx exports (blinktech found the starter's old path broke the build) |
| `tailwind.config.ts` | Preset from `frappe-ui/tailwind` | The exported preset path, as in blinktech |
| `biome.json` | `../<app-name>/**` → `../ozone/**`; also ignores `auto-imports.d.ts` and `components.d.ts` | doppio never replaces the placeholder; those two files are generated |
| `vite.config.ts` `optimizeDeps` | `exclude: ["frappe-ui"]`; removed `showdown`; pre-bundles `frappe-ui > reka-ui / echarts / lowlight / @popperjs/core` | frappe-ui's `~icons/lucide/*` imports only resolve through its plugin; `showdown` isn't installed |
| `ozone/www/frontend.py` (new) | `context.boot` with `csrf_token` and `site_name` | Without it, the production page sets nothing on `window` |
| `ozone/hooks.py` | Dropped the `/frontend/<path>` rule; `home_page = "frontend"` | The site lives at `/`, not `/frontend` |

## TypeScript

| Before | After |
| --- | --- |
| `src/main.js`, `router.js` | `src/main.ts`, `src/router/{index,routes}.ts` |
| `vite.config.js`, `tailwind.config.js` | `.ts` (Tailwind uses `satisfies Config`) |
| `index.html` → `/src/main.js` | → `/src/main.ts` |

Added: `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`, `src/env.d.ts`,
`types/frappe-ui-config.d.ts`, `scripts/type-check.mjs` and `vitest.config.ts`, all copied
from blinktech.

## Removed (not used by a public landing page)

| Starter file | Why |
| --- | --- |
| `src/pages/Login.vue`, `Home.vue` | No login or dashboard; the landing page is `src/views/LandingView.vue` |
| `src/data/session.js`, `user.js` | No session or user state |
| `src/socket.js`, `socket.io-client` | No realtime |
| `src/assets/Inter/`, `public/favicon.png` | Brand fonts and favicons come in step 2 |

## Restructure

| Before | After |
| --- | --- |
| Plain `<router-view>` in `App.vue` | Layout chosen per route (`src/layouts/`) |
| `frontend/README.md` (the starter's) | A short pointer to these docs |
