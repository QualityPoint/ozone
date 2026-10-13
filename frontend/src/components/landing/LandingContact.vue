<template>
  <section id="contact" class="section py-20">
    <BaseReveal class="relative overflow-hidden rounded-4xl bg-brand-green-800 px-6 py-14 text-center text-white sm:px-12">
      <!-- BrandStripe positions itself (relative), so a wrapper places it on the card's top edge. -->
      <div class="absolute inset-x-0 top-0"><BrandStripe /></div>
      <BaseSectionTag>{{ t("nav.contact") }}</BaseSectionTag>
      <h2 class="mx-auto mt-5 max-w-2xl text-heading font-extrabold sm:text-heading-lg">{{ t("contact.title") }}</h2>
      <p class="mx-auto mt-4 max-w-xl text-body-lg text-brand-silver-200">{{ t("contact.text") }}</p>
      <!-- From Ozone Settings: each channel shows only when it is filled in. -->
      <div v-if="actions.length" class="mt-8 flex flex-wrap justify-center gap-3">
        <BaseButton v-for="action in actions" :key="action.href" :href="action.href" :variant="action.variant">
          <component :is="action.icon" class="size-4" aria-hidden="true" />
          {{ action.label }}
        </BaseButton>
      </div>
    </BaseReveal>
  </section>
</template>

<script lang="ts" setup>
import { type Component, computed } from "vue"
import { useI18n } from "vue-i18n"
import LucideMail from "~icons/lucide/mail"
import LucideMessageCircle from "~icons/lucide/message-circle"
import LucidePhone from "~icons/lucide/phone"

import BaseButton from "@/components/base/BaseButton.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionTag from "@/components/base/BaseSectionTag.vue"
import BrandStripe from "@/components/brand/BrandStripe.vue"
import { useSiteContact } from "@/composables/useSiteContact"

const { t } = useI18n()
const contact = useSiteContact()

interface Action {
	href: string
	label: string
	icon: Component
	variant: "accent" | "light"
}

const actions = computed(() => {
	const c = contact.value
	const all: (Action | null)[] = [
		c.whatsappHref
			? {
					href: c.whatsappHref,
					label: t("contact.whatsapp"),
					icon: LucideMessageCircle,
					variant: "accent",
				}
			: null,
		c.phoneHref
			? {
					href: c.phoneHref,
					label: t("contact.call"),
					icon: LucidePhone,
					variant: "light",
				}
			: null,
		c.emailHref
			? {
					href: c.emailHref,
					label: t("contact.email"),
					icon: LucideMail,
					variant: "light",
				}
			: null,
	]
	return all.filter((action): action is Action => !!action)
})
</script>
