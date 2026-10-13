import type meta from "@/i18n/locales/meta.json"

/** The site's languages; the first is the default, served without a path prefix. */
export const SUPPORTED_LOCALES = ["ar", "en"] as const
export type LocaleCode = (typeof SUPPORTED_LOCALES)[number]

/** A public page with its own address in each language (keys of `paths` in meta.json). */
export type PageKey = keyof typeof meta.paths

/** One navbar entry: a section of the landing page. Its label is the `nav.<id>` message. */
export interface NavItem {
	id: string
	section: string
}
