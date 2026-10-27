import meta from "@/i18n/locales/meta.json"
import {
	type EquipmentItem,
	type IndustryId,
	type LocaleCode,
	type NavItem,
	type PageKey,
	SUPPORTED_LOCALES,
	type ServiceId,
	type Stat,
	type WasteStream,
} from "@/types"

/**
 * Static site facts shared by the header and footer.
 * Translatable text lives in src/i18n/locales/, not here.
 */
export const site = {
	name: "Ozone",
}

/** The default language: its pages have no prefix ("/"); every other one does ("/en"). */
export const defaultLocale: LocaleCode = SUPPORTED_LOCALES[0]

/** Each public page's base address (meta.json, shared with ozone/www/frontend.py). */
export const pagePaths: Record<PageKey, string> = meta.paths

/**
 * The login pages' base addresses (website_route_rules in ozone/hooks.py). Not public pages:
 * they aren't in meta.json, so they stay out of the sitemap and aren't indexed.
 */
export const authPaths = {
	login: "/login",
	signup: "/signup",
	forgotPassword: "/forgot-password",
} as const

/**
 * The producer dashboard (website_route_rules in ozone/hooks.py: /dashboard and below). Private:
 * not in meta.json, so not indexed. Its pages in the menu's order, the overview then two groups.
 */
export const dashboardPath = "/dashboard"
export const dashboardPages = [
	{ id: "overview", path: "" },
	// The journey, in its order: a producer registers its facility, asks for services for it, answers
	// the quotation a request turns into, and pays and follows the contract that follows
	{ id: "facilities", path: "/facilities", group: "operations" },
	{ id: "requests", path: "/requests", group: "operations" },
	{ id: "quotations", path: "/quotations", group: "operations" },
	{ id: "contracts", path: "/contracts", group: "operations" },
	{ id: "profile", path: "/profile", group: "account" },
	{ id: "establishment", path: "/establishment", group: "account" },
] as const
export type DashboardPageId = (typeof dashboardPages)[number]["id"]

/**
 * A page's address in a language: the base path in the default language, under
 * "/<code>" in the others ("/" → "/en", "/x" → "/en/x"). The server applies the same
 * rule (frontend.py: localized_path).
 */
export function localePath(basePath: string, code: LocaleCode): string {
	if (code === defaultLocale) {
		return basePath
	}
	return basePath === "/" ? `/${code}` : `/${code}${basePath}`
}

/** The base address of any path: "/en/x" → "/x", "/en" → "/", "/x" → "/x". */
export function basePath(path: string): string {
	for (const code of SUPPORTED_LOCALES) {
		if (code === defaultLocale) continue
		if (path === `/${code}` || path.startsWith(`/${code}/`)) {
			return path.slice(code.length + 1) || "/"
		}
	}
	return path
}

/**
 * The site's languages as the language switch shows them: each language's own name
 * (never translated: a visitor looks for the name they read) and a short form for phones.
 */
export const languages: Record<LocaleCode, { native: string; short: string }> =
	{
		ar: { native: "العربية", short: "ع" },
		en: { native: "English", short: "EN" },
	}

/** Landing page of each language. */
export const localeHome = Object.fromEntries(
	SUPPORTED_LOCALES.map((code) => [code, localePath(pagePaths.landing, code)]),
) as Record<LocaleCode, string>

/** The navbar, in order: sections of the landing page and pages. Labels are `nav.<id>` messages. */
export const navItems: NavItem[] = [
	{ id: "about", section: "about" },
	{ id: "services", section: "services" },
	{ id: "capabilities", page: "capabilities" },
	{ id: "industries", section: "industries" },
	{ id: "naqel", page: "naqel" },
	{ id: "contact", section: "contact" },
]

export const serviceIds: ServiceId[] = ["collection", "sorting", "debris"]

/**
 * The operation file's three streams, in its order, with the colour of their bins, bags and
 * trucks (sampled from its photos).
 */
export const wasteStreams: WasteStream[] = [
	{ id: "organics", color: "#2f8a3c" },
	{ id: "recyclables", color: "#1f4fa3" },
	{ id: "residuals", color: "#2b2b2b" },
]

/**
 * The fleet and the containers, in the operation file's order. Each slug's photo is
 * src/assets/images/equipment/<slug>.webp (made by scripts/build-brand-assets.py).
 */
export const equipment: Record<"fleet" | "containers", EquipmentItem[]> = {
	fleet: [
		{ slug: "compactor-trucks" },
		{ slug: "hook-lift-truck" },
		{ slug: "skip-loader" },
		{ slug: "tipper-truck" },
	],
	containers: [
		{ slug: "indoor-bins" },
		{ slug: "outdoor-containers" },
		{ slug: "compactors" },
		{ slug: "debris-containers" },
	],
}

/** The capabilities page's sections, in order: their ids are the page's anchors (#camp). */
export const capabilitySections = [
	"method",
	"operations",
	"tracking",
	"camp",
	"teams",
	"quality",
] as const

/** The teams' vehicles on the capabilities page, in the operation file's order. */
export const supportFleet: EquipmentItem[] = [
	{ slug: "supervision-cars" },
	{ slug: "support-pickups" },
	{ slug: "mobile-workshop" },
	{ slug: "staff-bus" },
]

export const industryIds: IndustryId[] = [
	"complexes",
	"restaurants",
	"shops",
	"streets",
]

/**
 * Key figures of the operation plan, from Ozone's operation file: the sorting streams, the
 * compactor trucks' capacity (yards), the trackers' update interval (seconds). Numbers aren't
 * translated (the site uses Latin digits in both languages, as blinktech does); their labels
 * are `why.stats.<id>`.
 */
export const stats: Stat[] = [
	{ id: "streams", value: wasteStreams.length },
	{ id: "capacity", value: 22 },
	{ id: "tracking", value: 30 },
]
