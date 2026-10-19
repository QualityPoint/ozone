# Routing

| Piece | Where |
| --- | --- |
| Address | `meta.json` `paths.naqel = "/naqel"`; `/en/naqel` by the usual prefix rule |
| SPA routes | `router/routes.ts`: `localizedRoutes("naqel", "Naqel", …)`, names `Naqel` / `NaqelEn` |
| Server rule | `hooks.py` `website_route_rules`: `/naqel` → `frontend` (`/en/…` is already covered) |
| Navbar and footer | `config/site.ts` `navItems`: `{ id: "naqel", page: "naqel" }`, just before Contact; label `nav.naqel` |
| Title and description | `meta.json` `ar.naqel` / `en.naqel`, shared by the SPA and `www/frontend.py` |
| Sitemap | Listed in both languages with hreflang, from `meta.json` (`www/sitemap.py`) |

The hero's "Waste calculator" button goes to the calculator section on this page (`#calculator`);
Naqel's calculator page itself isn't part of Ozone's site.

Frappe caches the route rules: `bench migrate` clears the cache; after a code pull alone, run
`bench --site <site> clear-cache`, or a full page load of `/naqel` keeps returning Frappe's 404.

Tests: `router/__tests__/routes.test.ts` (both routes and their meta), `ozone/tests/test_frontend.py`
(`resolve_page` and the sitemap).
