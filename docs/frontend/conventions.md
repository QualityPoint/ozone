# Conventions

These are blinktech's conventions (`apps/blinktech/docs/frontend/conventions.md`), applied
as-is. `frontend/src/` follows the standard Vue 3 layout and the
[Vue style guide](https://vuejs.org/style-guide/).

## Where code goes

| Folder | Put here | Don't put here |
| --- | --- | --- |
| `main.ts` | App bootstrap only: plugins, global components, mount | Business logic |
| `views/` | Route components (`*View.vue`) | Reusable UI |
| `layouts/` | Page shells chosen by `route.meta.layout` (`*Layout.vue`) | Page content |
| `components/base/` | Generic presentational blocks (`Base*`) | Data fetching, i18n keys (take translated text as props) |
| `components/brand/` | Logo, tagline and the brand's backgrounds and stripes (`Brand*`) | |
| `components/layout/` | Header and footer (`The*`) and the controls they share | |
| `components/<feature>/` | Components for one feature, named after it (`Landing*`) | |
| `composables/` | Reusable stateful logic (`use*`) | |
| `services/` | Clients for the server (`http.ts`) | |
| `utils/` | Pure functions with no Vue state, unit-tested | Anything that reads the locale or a store (pass it in) |
| `router/` | `routes.ts` (table and `RouteMeta` types), `index.ts` | |
| `i18n/` | vue-i18n setup and `locales/{ar,en}/` messages | Emails, URLs, phone numbers |
| `config/` | Static site constants: name, nav items, page paths | Contact details (they come from Ozone Settings, [server.md](server.md#ozone-settings)) |
| `types/` | Shared TS types | |
| `assets/` | `styles/` and generated images | Files that need a fixed URL (use `public/`) |

## Reuse

- **Entrances go through `BaseReveal` (or `useReveal`).** One place decides when something is
  in view, instead of an IntersectionObserver per section.

- **Before writing a second copy** of markup or logic, extract it: a `Base*` component for
  UI, a composable (`use*`) for stateful logic, a `utils/` function for pure logic. Then
  switch the first copy to it too.
- **One source per fact.** A text, path or setting the server also needs lives in one file
  that both sides read, such as `i18n/locales/meta.json`. It is not copied into Python.
- **Generalize, don't fork.** Name helpers by role, not by language: Arabic is the default
  here and English is in blinktech, so a rule like "the default language has no prefix" is
  written once, against `defaultLocale`.

## Naming

- Components use PascalCase and multi-word names (`LandingView`, not `Landing`).
- Prefixes:
  - `Base*` for shared UI;
  - `The*` for single-instance parts;
  - the feature name for feature components (`LandingHero`).
- Import with the `@/` alias, not `../../`.
- SFCs use `<script setup lang="ts">`.
- On public pages, colour text and surfaces with the `site-*` tokens, not `bg-white` or
  `text-brand-green`, so dark mode works with no extra classes ([branding.md](branding.md#light-and-dark)).
- Give every logo `<img>` the `brand-art` class.
- Use logical utilities (`ps-`, `start-`, `text-start`): Arabic is the default ([styling.md](styling.md#right-to-left)).

## Routes

- Public pages come in pairs: add both with `localizedRoutes(page, name, component)` ([i18n.md](i18n.md#adding-a-page-in-both-languages)).
- Link inside the site with `useLocale()`: `sectionLink("about")`, `twin(code)`. Never a bare `href="#id"`.
- Every route sets `meta.layout`.
- A new top-level path needs a `website_route_rules` entry in `ozone/hooks.py`, or Frappe
  returns 404 on a full page load.

## Tests

Tests live next to the code they cover, in `__tests__/*.test.ts`:

| File | Checks |
| --- | --- |
| `router/__tests__/routes.test.ts` | `/` (Arabic) and `/en` resolve with their locale and page; unknown paths redirect to their language's landing page; every page has a layout |
| `config/__tests__/site.test.ts` | Arabic has no prefix, English is under `/en` and back (`localePath`, `basePath`), language homes, unique nav ids, a photo for every equipment slug |
| `utils/__tests__/format.test.ts` | Thousands separators, Latin digits |
| `i18n/__tests__/locales.test.ts` | `en` has exactly the same keys and list lengths as `ar`, no empty messages, no `@ { } \|` |
| `composables/__tests__/useTheme.test.ts` | Theme toggle, storage key, `theme-color` |
| `composables/__tests__/useSiteContact.test.ts` | Phone formatting, `wa.me` link, filtering of boot data (unknown platforms, non-https links, empty addresses) |
| `ozone/tests/test_frontend.py` (server) | `localized_path`, `resolve_page`, SEO per language, `noindex` for unknown pages |
| `ozone/tests/test_site_contact.py` (server) | Filled details shown, empty ones `None`, only published socials |
| `ozone/ozone/doctype/ozone_settings/test_ozone_settings.py` (server) | https-only links, one row per platform, one address per language, trimmed links |

Run the server's with `bench --site ozone.local run-tests --app ozone`.

`vitest.config.ts` is standalone and uses the Node environment, so tests resolve routes rather
than load `.vue` views.

## Checking a change

Run in `frontend/`:

```bash
yarn type-check && npx biome check . && yarn test:run && yarn build
```

Then open `http://ozone.local:8000` and `/en`, where the build is served directly, at phone
width and on desktop, in light and dark mode.
