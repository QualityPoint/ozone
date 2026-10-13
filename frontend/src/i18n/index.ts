import { createI18n } from "vue-i18n"

import { defaultLocale } from "@/config/site"
import type { LocaleCode } from "@/types"

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

/** The message of the page on screen's title, which the browser tab shows. */
let currentTitle = "meta.landing.title"

/**
 * Sets the browser tab's title to a message in the active language: a public page's
 * (`meta.<page>.title`, as the server does in ozone/www/frontend.py) or a route's own
 * (`meta.title`). Called with no arguments, it re-translates.
 */
export function setPageTitle(title: string = currentTitle): void {
	currentTitle = title
	document.title = i18n.global.t(title)
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
