# Naqel Page: Docs Index

`/naqel` (Arabic) and `/en/naqel` (English) present **the Naqel system**, which manages every
waste operation of the transporter Ozone is, exactly as Naqel's own site presents it: the home page of hawya's
website (`apps/hawya/frontend`, branch `naqel`), in Naqel's identity, between Ozone's header and
footer. The navbar calls it **نظام ناقل** / **Naqel system**. Naqel is developed by Quality Point;
the page's calls to action write to `erp@qp.sa`.

| File | Concern |
| --- | --- |
| [identity.md](identity.md) | How the page keeps Naqel's look inside Ozone's site: palette, tokens, fonts, icons |
| [routing.md](routing.md) | The address, the navbar entry, the server rule, SEO and sitemap |
| [porting.md](porting.md) | What came from hawya, where it lives here, and what differs on purpose |
| [contact.md](contact.md) | The calls to action (erp@qp.sa) and Quality Point's logo |

## Sections

hawya's home page, in its order: hero, platform, contracting, finance, calculator, operations,
governance, and the closing panel (`views/NaqelView.vue`).

## Status

Done 2026-10-19: every section, checked in both languages and themes at 320–1440 px against
hawya's page (same section heights, except the two differences in [porting.md](porting.md)).
