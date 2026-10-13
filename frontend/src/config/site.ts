import meta from "@/i18n/locales/meta.json"
import {
	type LocaleCode,
	type NavItem,
	type PageKey,
	SUPPORTED_LOCALES,
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

/** The navbar, in order: sections of the landing page. Labels are `nav.<id>` messages. */
export const navItems: NavItem[] = [
	{ id: "about", section: "about" },
	{ id: "services", section: "services" },
	{ id: "industries", section: "industries" },
	{ id: "contact", section: "contact" },
]
