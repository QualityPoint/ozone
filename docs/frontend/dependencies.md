# Dependencies

Versions are what `yarn.lock` resolved, checked on 2026-10-13. Ranges are in
`frontend/package.json`. The same choices as blinktech, minus what a public landing page
doesn't use (Pinia, socket.io).

## Runtime

| Package | Version | Purpose |
| --- | --- | --- |
| `vue` | 3.5.44 | UI framework |
| `vue-router` | 4.6.4 | Client routing (`src/router/`) |
| `frappe-ui` | 0.1.278 | Vite plugin (dev proxy, boot data, Lucide icons), Tailwind preset, styles |
| `@vueuse/core` | 10.11.1 | `useDark`/`useToggle` (theme), `useIntersectionObserver` (`useReveal`), `useTransition` (`useCountUp`). The version frappe-ui uses |
| `vue-i18n` | 11.4.14 | Arabic and English messages ([i18n.md](i18n.md)) |
| `@fontsource/almarai`, `@fontsource/montserrat` | 5.3.0 | Self-hosted brand fonts: weights 400, 700, 800 only |
| `feather-icons` | 4.29.2 | Needed by frappe-ui |

## Build and tooling

| Package | Version | Purpose | Added by |
| --- | --- | --- | --- |
| `vite` | 5.4.21 | Dev server and bundler | starter |
| `@vitejs/plugin-vue` | 5.2.4 | `.vue` support | starter |
| `tailwindcss` | 3.4.19 | Styling (stay on v3, as frappe-ui's preset) | starter |
| `postcss` / `autoprefixer` | 8.5.30 / 10.6.1 | CSS pipeline | starter |
| `@biomejs/biome` | 1.9.4 (pinned) | Lint and format (`yarn lint`) | starter |
| `vitest`, `@vitest/coverage-v8`, `jsdom` | 2.1.9 / 2.1.9 / 25.0.1 | Unit tests; jsdom for `useTheme`'s test | starter |
| `typescript` | 5.9.3 (`~5.9`) | Compiler, matching frappe-ui's TS 5 | blinktech's setup |
| `vue-tsc` | 3.3.13 | Type-checks `.vue` files | blinktech's setup |
| `@types/node` | 22.20.5 | Types for the config files | blinktech's setup |

## Outside yarn

| Tool | Used by | Notes |
| --- | --- | --- |
| Python with Pillow (12.3, the bench's `env`) | `scripts/build-brand-assets.py` | Logos, favicons, the social image, equipment photos |
| OpenCV (`opencv-python-headless` 4.13) and NumPy (2.4), in the bench's `env` | the same script, for the hero truck | The cut-out ([branding.md](branding.md#the-hero-trucks-cut-out)). Already in the bench's env; otherwise `pip install opencv-python-headless` |
| poppler's `pdftoppm` and `pdfimages` (26.01) | the same script, for the photos | `apt install poppler-utils` |

None of them is needed to build or deploy: the script's output is committed. It's only needed to
regenerate it.

## Notes

- `frappe-ui` uses the range `^0.1.192`, which allows any 0.1.x. It has changed export paths
  within that range before (blinktech's `changes-from-starter.md`). Check the build after
  `yarn upgrade`.
- Social brand icons are Simple Icons (CC0), copied from blinktech into
  `src/components/icons/socialIconPaths.ts`. The package isn't installed.
- Use **Yarn 1**, not npm, to keep `yarn.lock` consistent. The root `postinstall` runs
  `yarn install` in `frontend/`. A root `yarn.lock`, which `yarn install` may write at the app
  root, is gitignored, as in blinktech.
- The frontend does not depend on the doppio app. doppio is only needed for the
  `bench add-*` scaffolding commands.
