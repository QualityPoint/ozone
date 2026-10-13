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

/** The services on the landing page; texts are `services.items.<id>`. */
export type ServiceId = "collection" | "sorting" | "debris"

/** The kinds of establishment Ozone serves; texts are `industries.items.<id>`. */
export type IndustryId = "complexes" | "restaurants" | "shops" | "streets"

/** The waste streams sorted at source; texts are `about.streams.items.<id>`. */
export type WasteStreamId = "organics" | "recyclables" | "residuals"

/** A waste stream and the colour of its bins, bags and truck. */
export interface WasteStream {
	id: WasteStreamId
	color: string
}

/** One piece of equipment: its photo in assets/images/equipment/<slug>.webp, texts `equipment.items.<slug>`. */
export interface EquipmentItem {
	slug: string
}

/** A key figure: the number is a fact (here), its label a message (`why.stats.<id>`). */
export interface Stat {
	id: string
	value: number
	prefix?: string
	suffix?: string
}
