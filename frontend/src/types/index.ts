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

/** The Platform options of the Social Media Link doctype (Ozone Settings). */
export const SOCIAL_PLATFORMS = [
	"Facebook",
	"Snapchat",
	"Instagram",
	"Threads",
	"X",
	"TikTok",
	"LinkedIn",
	"YouTube",
	"Telegram",
	"Linktree",
] as const
export type SocialPlatform = (typeof SOCIAL_PLATFORMS)[number]

/** Public contact details from Ozone Settings (ozone/site_contact.py). */
export interface SiteContact {
	email: string | null
	phone: string | null
	whatsapp: string | null
	/** The postal address in each language it was written in ({ ar: "…" }); any language code. */
	address: Partial<Record<string, string>>
	/** A map link (https), e.g. Google Maps. */
	map: string | null
	socials: { platform: SocialPlatform; url: string }[]
}
