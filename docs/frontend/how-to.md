# How To

Recipes for the changes most likely to come up. Each keeps one source per fact: texts in
`src/i18n/locales/{ar,en}/`, facts in `src/config/site.ts`, contact details in Ozone Settings.

## The landing page's sections

`src/views/LandingView.vue` composes them in order:

| Section | Component | Anchor | Texts | Facts |
| --- | --- | --- | --- | --- |
| Hero | `LandingHero` | | `hero.*`, `brand.*` | `hero-truck.webp`, a cut-out ([branding.md](branding.md#the-hero-trucks-cut-out)) |
| About | `LandingAbout` (+ `LandingStreams`) | `#about` | `about.*` | `wasteStreams` |
| Services | `LandingServices` | `#services` | `services.*` | `serviceIds` |
| Equipment | `LandingEquipment` | `#equipment` | `equipment.*` | `equipment` (photo slugs) |
| Industries | `LandingIndustries` | `#industries` | `industries.*` | `industryIds` |
| Why us | `LandingWhyUs` | `#why` | `why.*` | `stats` |
| Contact | `LandingContact` | `#contact` | `contact.*` | Ozone Settings |

Sections are built from shared parts: `BaseSectionHeading` (the red tag, title and intro),
`BaseCard`, `BaseReveal` (fade up in view), `BaseButton`, `BasePill`, `BaseStat`,
`BaseCheckList` (green checks), `BaseDotList` (red dots) and `LandingPhotoCard` (a product
photo with its name). A section adds only its own texts and layout.

## The capabilities page's sections

`/capabilities` (`src/views/CapabilitiesView.vue`) shows Ozone's capabilities from its
operation file, for publicity. All its texts are `capabilities.*`, with the operation file's
pages noted in `ar/capabilities.ts`.

| Section | Component | Anchor | Facts |
| --- | --- | --- | --- |
| Opening: the head office in photos, then the page's contents | `CapabilitiesHero` | | `capabilitySections` (the contents' order), `office/towers`, `office/entrance` |
| Methodology, the head office's reception, ways of working | `CapabilitiesMethod` | `#method` | `office/reception` |
| The protocol, a route per stream, Ramadan and Hajj | `CapabilitiesOperations` | `#operations` | `wasteStreams` (and `about.streams` names), `route-<stream>` photos |
| Live tracking and daily reports | `CapabilitiesTracking` | `#tracking` | |
| The operations camp | `CapabilitiesCamp` | `#camp` | |
| The organisation, field crews, safety gear, the teams' vehicles | `CapabilitiesTeams` | `#teams` | `supportFleet` (photo slugs), `safety-gear` |
| Maintenance, safety, follow-up, the risk plan | `CapabilitiesQuality` | `#quality` | |
| Contact | `LandingContact` (shared) | `#contact` | Ozone Settings |

A section's tag is its name in `capabilities.sections`, which the contents list too. A new
section needs its id in `capabilitySections`, a name there, and that id on its `<section>`.

The operation file states no achievements (completed projects, figures), so the page has none.
Add them only from a source Ozone confirms.

## Change a text

Edit the message in `src/i18n/locales/ar/<area>.ts` and the same key in `en/<area>.ts`. Arabic
is the source of truth. The locales test fails if the two differ in keys or list lengths, or
if a message uses `@ { } |`.

## Add an item to a list (a goal, a feature)

Add it to the array in both languages, in the same position. Lists with icons (`about.goals`,
`why.pillars`) take one icon per item in the component's `ICONS` array, in the same order.

## Add a service, a sector, a waste stream or a key figure

1. Add the id to `ServiceId` / `IndustryId` / `WasteStreamId` in `src/types/index.ts`, and to
   `serviceIds` / `industryIds` / `wasteStreams` (with its bins' colour) in `config/site.ts`.
   For a figure, add `{ id, value, prefix?, suffix? }` to `stats`.
2. Add its texts under `services.items.<id>`, `industries.items.<id>`,
   `about.streams.items.<id>` or `why.stats.<id>`, in both languages.
3. Services, sectors and streams take an icon in the component's `ICONS` record, which TypeScript
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

Add `{ id, section }` (a section of the landing page) or `{ id, page }` (a page of its own) to
`navItems` in `config/site.ts`, and `nav.<id>` in both languages. A section needs that `id` on its
`<section>`. A page entry is marked as the current page while it's open (`aria-current`).

## Change contact details or social links

In the Desk: Ozone → Settings → Ozone Settings ([server.md](server.md#ozone-settings)). The
footer and the contact section show what's filled in, and hide the rest.

## Change how the team logs in

In the Desk: System Settings (password, email link, username or mobile number, two-factor) and
Social Login Key (Google and others). The login page shows only what's enabled
([auth.md](auth.md#only-enabled-options-are-shown)). Email links and resets need an outgoing
Email Account.

## Check responsiveness

Open `http://ozone.local:8000` and `/en` at 320, 390 and 414 px wide and on desktop. There
should be no sideways scrolling and nothing cut off. Animations are off with reduced motion
(DevTools → Rendering → *prefers-reduced-motion*), which is also the way to take a full-page
screenshot without catching them half-way:

```bash
google-chrome --headless=new --force-prefers-reduced-motion --virtual-time-budget=8000 \
  --window-size=1366,5300 --screenshot=page.png http://ozone.local:8000/
```
