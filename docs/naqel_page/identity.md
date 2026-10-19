# Identity

The page must look exactly like Naqel's site, while Ozone's header and footer stay Ozone's. Both
sites are built the same way (blinktech's design system: Tailwind `site-*` tokens, Base and Brand
components), but with different values, so the page re-points the shared names and gives Naqel's
own colours a name of their own.

## Colours

`tailwind.config.ts` has a `naqel` palette beside Ozone's `brand`: `naqel-green` (#3dba6b),
`naqel-mint`, `naqel-night`, `naqel-ink`, hawya's values. Their shades use **Naqel's steps**
(`NAQEL_STEPS`): `scale()` takes the steps as an argument, because the two sites mix their tints
and shades by different amounts (100 is 88% white in Naqel, 90% in Ozone). Also from hawya:
`bg-naqel-band` (the title bands' gradient) and `shadow-naqel-card`.

## The `.naqel` scope

`views/NaqelView.vue` wraps the page in `<div class="naqel">`. `assets/styles/naqel.css` sets, inside
it, hawya's values for:

- the `site-*` tokens, light and dark (`[data-theme="dark"] .naqel`), so the components keep their
  `bg-site-bg`, `text-site-heading`… classes;
- the fonts: **Inter** for Latin (`font-naqel`, frappe-ui's InterVar, already loaded) and Almarai
  first on Arabic pages (`font-naqel-arabic`); Ozone's header keeps Montserrat;
- `--band-to`, the side the bands' gradient points to (the start side);
- the page's background, which covers Ozone's silver background geometry.

## Icons

The icons are **naqel's Desk icons**, from the naqel app's sprite
(`/assets/naqel/icons/module-icons.svg`; naqel is a required app, so every Ozone site serves it).
`components/naqel/brand/naqelSprite.ts` inserts it into the page once, as hawya's `deskSprite.ts` does
with hawya's copy. The icons the page uses are identical in both sprites (checked symbol by symbol,
2026-10-19); naqel's stylesheet only adds two animations for icons the page doesn't use. The page
passes Frappe's `build_version` (boot data, `www/frontend.py`) to bust the browser's cache when
the sprite changes.

The app icon in the hero's floating card is hawya's `public/favicon.svg`, copied to
`src/assets/naqel/app-icon.svg`.

## Logo

The hero opens with Naqel's logo in its **white version**, the one the brand sheet
(`~/Projects/naqel/brand.pdf`) shows on its black and green panels: the hero's ground is Naqel's
night green, where the primary lockup's black "نَاقل" would vanish. The file is hawya's
`src/assets/brand/logo-white.svg` (vector, cut from `brand.pdf` by hawya's
`scripts/build-brand-assets.py`), copied to `src/assets/naqel/logo-white.svg`. Its alternative text
is `naqel.name`.
