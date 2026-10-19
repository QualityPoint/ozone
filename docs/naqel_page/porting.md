# Porting from hawya

The source is hawya's website on branch `naqel` (`apps/hawya/frontend`, 2026-10-14, fe14fe8). Its
files were carried over by exact text replacement, so they can be compared with hawya's line by
line.

| hawya | ozone |
| --- | --- |
| `components/landing/Landing*.vue` | `components/naqel/Naqel*.vue` |
| `components/base/Base*.vue` | `components/naqel/base/Naqel*.vue` |
| `components/brand/Brand*.vue`, `deskSprite.ts` | `components/naqel/brand/Naqel*.vue`, `naqelSprite.ts` |
| `i18n/locales/<code>/<section>.ts` | `i18n/locales/<code>/naqel/<section>.ts`, messages under `naqel.` |
| `brand.tagline` | `naqel.tagline` |
| `config/site.ts` (Naqel's facts) | `config/naqel.ts` |
| `utils/calibration.ts` and its test | the same paths |
| `utils/format.ts` `formatNumber(value, code, digits)`, `formatMonth` | Ozone's `formatNumber(value, digits)` (the same text in both languages), `formatMonth` added |

Code names stay hawya's (`NaqelPlatform`, `platformModules`, the `platform` messages): only
the visible text says "system". Renamed in every file: the `brand-*` colours to `naqel-*`, `shadow-card` to `shadow-naqel-card`,
`bg-brand-band` to `bg-naqel-band`. Shared helpers that both apps already have are reused
(`base/nativeTag.ts`, `useMessageList`, `useReveal` with Naqel's threshold, `naqelRevealThreshold`).
The port was a script of exact replacements that stopped on any leftover hawya name; the
sections' diffs against hawya show only those renames.

## Differences on purpose

| What | hawya | Here | Why |
| --- | --- | --- | --- |
| Hero top padding | `pt-32 sm:pt-36` | `pt-12 sm:pt-16` | hawya's header lies over the hero; Ozone's sits above it (5rem) |
| "Get started" | Naqel's login page | `mailto:erp@qp.sa` (`config/naqel.ts`) | Visitors write to the developer, Quality Point |
| "Waste calculator" | A section link from any page | `#calculator` on this page | The page is not the home page |
| Floating card | `site-surface` class | Dropped | Ozone's site doesn't re-point tokens over the hero |
| Calculator section | Ends with "Try the waste calculator" | No button (87 px shorter) | The calculator page isn't part of Ozone's site |
| Closing panel | WhatsApp, call and email buttons from Naqel Website Settings | One "Email us" button and Quality Point's logo ([contact.md](contact.md)) | Visitors write to the developer |
| Operations | Imports `BaseCheckList` without using it | Not imported | Dead import in hawya |
| Section offsets | — | 8 px lower | Ozone's header is 88 px (its 8 px brand stripe) |
| "Platform" / "منصة" | Naqel is called a platform | A **system** / **نظام** everywhere on the page, the Arabic agreeing (نظام رقمي ذكي، يربط، مبني) | Naqel manages all of the waste operations; it is a system, not a platform |
| Hero badge | "منصة رقمية ذكية لإدارة النفايات" | "نظام متكامل لإدارة عمليات النفايات" / "An integrated waste operations management system" | "نظام رقمي ذكي…" would repeat the line under the title |
| Hero | No logo (it is in hawya's header) | Naqel's white logo above the badge ([identity.md](identity.md#logo)) | Ozone's header carries Ozone's logo |
