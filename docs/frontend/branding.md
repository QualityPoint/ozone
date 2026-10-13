# Branding

The site takes its look from Ozone's own documents (`~/Projects/Ozone/References`: the
operation files and the waste-sorting file): white pages, soft silver geometry, a green
and red band framing each page, red slanted section tags and green outline pills. Colours
were sampled from those pages and match the official logo.

## Palette

`tailwind.config.ts` defines each official colour once. `scale()` derives its steps: lighter
ones mix it with white and darker ones with black, so every colour steps the same way.

| Class | Official value | Role |
| --- | --- | --- |
| `brand-green` | `#11532a` (logo; prints as `#194c26` in the documents) | Headings, bands, outlines, buttons |
| `brand-red` | `#af2625` (logo; prints as `#ad212c`) | Section tags, small labels, accents |
| `brand-leaf` | `#61be51` | Highlights, focus rings, the bottom band's line |
| `brand-silver` | `#d8deda` | Background geometry, borders |
| `brand-ink` | `#231f20` | Body text on light pages |

## Light and dark

Public pages colour text and surfaces with the `site-*` tokens: `text-site-heading`,
`bg-site-bg`, `border-site-line`… They are RGB channels in `src/assets/styles/main.css` that
swap under `[data-theme="dark"]`, so components need no `dark:` classes for them.

| Token | Light | Dark |
| --- | --- | --- |
| `site-bg` | white | deep green |
| `site-tint` | off-white wash | a step lighter |
| `site-heading` | brand green | white |
| `site-text` | brand ink | pale green-grey |
| `site-muted` | grey | muted green-grey |
| `site-hover` | pale green | dark green |
| `site-line`, `site-silver` | brand silver | dark green |

The theme follows the system until the visitor picks one with the toggle (`useTheme`,
stored under `ozone-theme`). `index.html` applies it before the first paint.

## Fonts

Almarai for Arabic, the default (close to the documents' bold geometric Arabic, and already
Ozone's desk font), and Montserrat for Latin. Both are self-hosted with `@fontsource`.
`html:lang(ar)` puts Almarai first.

The type scale (`text-body`, `text-heading`, `text-display`…) is blinktech's. frappe-ui's
`text-xs…3xl` also set letter-spacing, which breaks Arabic letter joins, so public pages
don't use them.

## Motifs

Each motif is one component, used wherever it appears:

| Component | The documents' motif |
| --- | --- |
| `brand/BrandStripe` | The band framing each page: green with a slanted red segment at the start (`edge="top"`), or green over a leaf line (`edge="bottom"`). It sits on the header's top edge and at the footer's base |
| `brand/BrandSilverBackground` | White pages with soft diagonal silver shards and faint dots: CSS only, theme-aware |
| `base/BaseSectionTag` | A section's label: white on a slanted red tag with a darker edge, mirrored in English |
| `base/BasePill` | Rounded titles: `outline` (green border), `solid` (green), `accent` (small red label) |
| `brand/BrandTagline` | The logo's slogan "صيانة - نظافة - مقاولات عامة", its items with red dots between |
| `base/BaseCard` | The documents' white panels with a soft green-tinted ground shadow |
| `base/BaseStat` | An impact figure over the documents' green underline bar, counting up in view |
| `base/BaseCheckList` | The "features" page's green check badges |
| `landing/LandingPhoto` | A product photo on white, as the documents show the fleet and containers. It stays white in dark mode; `mix-blend-multiply` removes the photo's off-white page |
| `landing/LandingHierarchy` | The waste-sorting file's inverted triangle, brand green to leaf green |
| `brand/BrandLogo` | The official logo. `auto` shows the official inks in light mode and the white variant in dark mode; `white` on the green footer |

## Logo and icon files

`scripts/build-brand-assets.py` makes every brand file from the official logo in
`~/Projects/Ozone`:

```bash
cd frontend
~/frappe-bench/env/bin/python scripts/build-brand-assets.py   # needs Pillow
```

| Output | From |
| --- | --- |
| `src/assets/brand/logo-color.svg` | `logo.svg`, cleaned |
| `src/assets/brand/logo-white.svg` | The same with the green ink white, for dark backgrounds |
| `public/favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` | The logo's red "O" and its location pin, cut from `logo.png` |
| `public/og-image.png` | The logo between the brand bands, 1200×630 |
| `src/assets/images/equipment/<slug>.webp` | Fleet and container photos cropped from the operation file's pages (`PHOTOS` in the script) |

Give every logo `<img>` the `brand-art` class, or frappe-ui dims it in dark mode.
