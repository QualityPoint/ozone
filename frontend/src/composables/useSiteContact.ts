import { computed, ref } from "vue"
import { useI18n } from "vue-i18n"

import { getMethod } from "@/services/http"
import { SOCIAL_PLATFORMS, type SiteContact } from "@/types"

/**
 * Display form of a stored phone number: Saudi mobiles as "+966 54 690 6900",
 * anything else unchanged.
 */
export function formatPhone(phone: string): string {
	const digits = phone.replace(/[^\d+]/g, "")
	const saudi = digits.match(/^\+966(\d{2})(\d{3})(\d{4})$/)
	return saudi ? `+966 ${saudi[1]} ${saudi[2]} ${saudi[3]}` : phone
}

/** wa.me wants the number in international form with digits only. */
export function whatsappHref(number: string): string {
	return `https://wa.me/${number.replace(/\D/g, "")}`
}

const text = (v: unknown) =>
	typeof v === "string" && v.trim() ? v.trim() : null
const httpsLink = (v: unknown) => {
	const link = text(v)
	return link?.startsWith("https://") ? link : null
}

/** Drops anything the page can't show safely: unknown platforms and non-https links. */
export function sanitizeContact(raw: unknown): SiteContact {
	const value = (
		raw && typeof raw === "object" ? raw : {}
	) as Partial<SiteContact>
	return {
		email: text(value.email),
		phone: text(value.phone),
		whatsapp: text(value.whatsapp),
		address: Object.fromEntries(
			Object.entries(
				value.address && typeof value.address === "object" ? value.address : {},
			)
				.map(([code, address]) => [code, text(address)])
				.filter(([, address]) => address),
		),
		map: httpsLink(value.map),
		socials: (Array.isArray(value.socials) ? value.socials : []).filter(
			(s) => SOCIAL_PLATFORMS.includes(s?.platform) && httpsLink(s.url),
		),
	}
}

const contact = ref<SiteContact>(sanitizeContact(null))
let loaded = false

function load() {
	if (loaded) return
	loaded = true
	// Production: in the page's boot data. Dev server: no boot data, so ask the API.
	if (window.site_contact && typeof window.site_contact === "object") {
		contact.value = sanitizeContact(window.site_contact)
		return
	}
	getMethod<SiteContact>("ozone.api.site.get_site_contact")
		.then((message) => {
			contact.value = sanitizeContact(message)
		})
		.catch(() => {
			// Leave everything empty: the page hides missing details.
		})
}

/**
 * Contact details from Ozone Settings, with ready-to-use hrefs and the address in the current
 * language. A detail left empty in the settings is null, and the page hides it.
 */
export function useSiteContact() {
	load()
	const { locale } = useI18n()
	return computed(() => {
		const { email, phone, whatsapp, address, map, socials } = contact.value
		return {
			email,
			emailHref: email ? `mailto:${email}` : null,
			phone: phone ? formatPhone(phone) : null,
			phoneHref: phone ? `tel:${phone.replace(/[^\d+]/g, "")}` : null,
			whatsappHref: whatsapp ? whatsappHref(whatsapp) : null,
			address: address[locale.value] ?? null,
			map,
			socials,
		}
	})
}
