# How To

Recipes for the changes most likely to come up. Each keeps one source per fact: texts in
`src/i18n/locales/{ar,en}/`, facts in `src/config/site.ts`, contact details in Ozone Settings.

## The landing page's sections

`src/views/LandingView.vue` composes them in order:

| Section | Component | Anchor | Texts | Facts |
| --- | --- | --- | --- | --- |
| Hero | `LandingHero` | | `hero.*`, `brand.*` | the compactor-trucks photo |
| About | `LandingAbout` (+ `LandingHierarchy`) | `#about` | `about.*` | |
| Services | `LandingServices` | `#services` | `services.*` | `serviceIds` |
| Equipment | `LandingEquipment` | `#equipment` | `equipment.*` | `equipment` (photo slugs) |
| Industries | `LandingIndustries` | `#industries` | `industries.*` | `industryIds` |
| Why us | `LandingWhyUs` | `#why` | `why.*` | `stats` |
| Contact | `LandingContact` | `#contact` | `contact.*` | Ozone Settings |

Sections are built from shared parts: `BaseSectionHeading` (the red tag, title and intro),
`BaseCard`, `BaseReveal` (fade up in view), `BaseButton`, `BasePill`, `BaseStat` and
`BaseCheckList`. A section adds only its own texts and layout.

## Change a text

Edit the message in `src/i18n/locales/ar/<area>.ts` and the same key in `en/<area>.ts`. Arabic
is the source of truth. The locales test fails if the two differ in keys or list lengths, or
if a message uses `@ { } |`.

## Add an item to a list (a goal, a feature, a hierarchy tier)

Add it to the array in both languages, in the same position. Lists with icons (`about.goals`,
`why.pillars`) take one icon per item in the component's `ICONS` array, in the same order.

## Add a service, a sector or an impact figure

1. Add the id to `ServiceId` / `IndustryId` in `src/types/index.ts`, and to `serviceIds` /
   `industryIds` in `config/site.ts`. For a figure, add `{ id, value, prefix?, suffix? }` to
   `stats`.
2. Add its texts under `services.items.<id>`, `industries.items.<id>` or `why.stats.<id>`, in
   both languages.
3. Services and sectors take an icon in the component's `ICONS` record, which TypeScript
   requires for every id.

## Add an equipment photo

1. Find the photo's page in the operation file, and its crop box at 150 dpi
   (`pdftoppm -r 150 -png -f <page> -l <page> <file> page`).
2. Add `"<slug>": (<page>, (left, top, right, bottom))` to `PHOTOS` in
   `scripts/build-brand-assets.py`, and run it:
   `~/frappe-bench/env/bin/python scripts/build-brand-assets.py`.
3. Add `{ slug: "<slug>" }` to `equipment.fleet` or `equipment.containers` in
   `config/site.ts`, and `equipment.items.<slug>.{name, body}` in both languages.

The site test checks that every listed slug has its photo. Photos are shown on white
(`LandingPhoto`), whose `mix-blend-multiply` blends away the documents' off-white page.

## Add a navbar entry

Add `{ id, section }` to `navItems` in `config/site.ts` and `nav.<id>` in both languages. The
section needs that `id` on its `<section>`.

## Change contact details or social links

In the Desk: Ozone → Settings → Ozone Settings ([server.md](server.md#ozone-settings)). The
footer and the contact section show what's filled in, and hide the rest.

## Check responsiveness

Open `http://ozone.local:8000` and `/en` at 320, 390 and 414 px wide and on desktop. There
should be no sideways scrolling and nothing cut off. Animations are off with reduced motion
(DevTools → Rendering → *prefers-reduced-motion*), which is also the way to take a full-page
screenshot without catching them half-way:

```bash
google-chrome --headless=new --force-prefers-reduced-motion --virtual-time-budget=8000 \
  --window-size=1366,5300 --screenshot=page.png http://ozone.local:8000/
```
