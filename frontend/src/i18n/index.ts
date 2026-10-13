import { createI18n } from "vue-i18n"

import { defaultLocale } from "@/config/site"
import type { LocaleCode, PageKey } from "@/types"

import ar, { type MessageSchema } from "./locales/ar"
import en from "./locales/en"

export const i18n = createI18n<[MessageSchema], LocaleCode, false>({
	legacy: false,
	locale: defaultLocale,
	fallbackLocale: defaultLocale,
	messages: { ar, en },
})

export function isRtl(locale: LocaleCode): boolean {
	return locale === "ar"
}

/** The public page on screen, whose title the browser tab shows. */
let currentPage: PageKey = "landing"

/**
 * Sets the browser tab's title to `page`'s, in the active language (meta.json), as the
 * server does (ozone/www/frontend.py). Called with no arguments, it re-translates.
 */
export function setPageTitle(page: PageKey = currentPage): void {
	currentPage = page
	document.title = i18n.global.t(`meta.${page}.title`)
}

/**
 * Switches the active language and updates <html lang/dir> and the page title. Every page
 * carries its language in its address, so the router calls this on each navigation.
 */
export function setLocale(locale: LocaleCode): void {
	i18n.global.locale.value = locale
	const html = document.documentElement
	html.lang = locale
	html.dir = isRtl(locale) ? "rtl" : "ltr"
	setPageTitle()
}
