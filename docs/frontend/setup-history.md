# Setup History

## Environment

Node 24.13, Yarn 1.22.22, Python 3.14, Frappe v16.51, and the doppio app (provides the
`bench add-*` commands).

## 1. Scaffold: `bench add-frappe-ui` (2026-10-13)

```bash
cd ~/frappe-bench
bench add-frappe-ui --app ozone --name frontend
```

This command:

- copies [doppio_frappeui_starter](https://github.com/NagariaHussain/doppio_frappeui_starter)
  with `degit`, then runs `yarn`;
- creates the app-root `package.json` with `postinstall`, `build` and `dev` scripts that `cd`
  into `frontend`;
- adds a `website_route_rules` entry for `/frontend/<path>` to `hooks.py`.

doppio's other command, `bench add-spa`, was not used. blinktech's first attempt with it
failed, as its `setup-history.md` records.

## 2. Aligned with blinktech

The starter has the same problems blinktech fixed, so Ozone took blinktech's finished setup
instead of fixing them again:

- TypeScript;
- Biome without the `<app-name>` placeholder;
- `optimizeDeps` without `showdown`, and with `frappe-ui` excluded;
- the frappe-ui import paths;
- `www/frontend.py` boot data;
- the gitignored build output.

The details are in [changes-from-starter.md](changes-from-starter.md).

## 3. Milestones

| Date | Milestone |
| --- | --- |
| 2026-10-13 | Step 1: scaffold, build and serving. A placeholder landing page at `/` on ozone.local |
| 2026-10-13 | Step 2: brand palette and the documents' motifs, header and footer, Arabic at `/` and English at `/en`, server-side SEO, light and dark themes, favicons and social image |
| 2026-10-13 | Step 3: Ozone Settings (contact details, an address per language, map link, social links) feeding the footer; Desk sidebar link |
| 2026-10-13 | Step 4: the landing sections (hero, about with the waste hierarchy, services, equipment with photos from the operation file, industries, why us with impact figures, contact), in Arabic and English |
| 2026-10-13 | Step 5: polish. No sideways scrolling at 320–1366 px in either language, one `h1`, alt text and names everywhere; unused font weights dropped; the hero shows a compactor truck cut out of the operation file, standing on the brand band, with no motion; a clean clone installs and builds; CI gained a Frontend job |
| 2026-10-13 | Content corrected against the operation file: Ozone collects, transports and sorts at source, and doesn't recycle. The 25-page technical offer's claims removed (recycling services, 90%, +50,000 t, +200 clients, ISO 14001, consulting); the waste hierarchy replaced by the three sorting streams |
