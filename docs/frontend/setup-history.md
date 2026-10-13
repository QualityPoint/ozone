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
