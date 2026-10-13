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
| `config/` | Static site constants: name, nav items, page paths | Contact details (they come from Ozone Settings) |
| `types/` | Shared TS types | |
| `assets/` | `styles/` and generated images | Files that need a fixed URL (use `public/`) |

## Reuse

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

## Routes

- Every route sets `meta.layout`.
- A new top-level path needs a `website_route_rules` entry in `ozone/hooks.py`, or Frappe
  returns 404 on a full page load.

## Tests

Tests live next to the code they cover, in `__tests__/*.test.ts`:

| File | Checks |
| --- | --- |
| `router/__tests__/routes.test.ts` | `/` is the landing page, unknown paths redirect to it, every page has a layout |

`vitest.config.ts` is standalone and uses the Node environment, so tests resolve routes rather
than load `.vue` views.

## Checking a change

Run in `frontend/`:

```bash
yarn type-check && npx biome check . && yarn test:run && yarn build
```

Then open `http://ozone.local:8000`, where the build is served directly.
