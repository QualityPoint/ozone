import { type Component, computed } from "vue"
import { useI18n } from "vue-i18n"
import LucideMail from "~icons/lucide/mail"
import LucideMessageCircle from "~icons/lucide/message-circle"
import LucidePhone from "~icons/lucide/phone"

import { useSiteContact } from "@/composables/useSiteContact"

/**
 * The ways to reach the transporter, WhatsApp first: one per detail filled in (Hawya Website
 * Settings), each with its href, label (`contact.*`) and icon. The landing's contact section and
 * the dashboard's not-linked page show them.
 */
export function useContactActions() {
	const { t } = useI18n()
	const contact = useSiteContact()
	return computed(() =>
		(
			[
				[
					contact.value.whatsappHref,
					t("contact.whatsapp"),
					LucideMessageCircle,
				],
				[contact.value.phoneHref, t("contact.call"), LucidePhone],
				[contact.value.emailHref, t("contact.email"), LucideMail],
			] as [string | null, string, Component][]
		)
			.filter(([href]) => href)
			.map(([href, label, icon]) => ({ href: href as string, label, icon })),
	)
}
