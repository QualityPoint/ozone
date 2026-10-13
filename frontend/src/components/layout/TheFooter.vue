<template>
  <footer class="bg-brand-green-800 text-brand-silver-200 dark:border-t dark:border-white/10">
    <div class="section grid gap-10 py-14 md:grid-cols-4">
      <div class="md:col-span-2">
        <BrandLogo variant="white" :height="56" />
        <p class="mt-5 max-w-md">{{ t("brand.about") }}</p>
        <BrandTagline class="mt-4 text-white" />
      </div>

      <nav :aria-label="t('footer.explore')">
        <h2 class="font-bold text-white">{{ t("footer.explore") }}</h2>
        <ul class="mt-4 space-y-2.5">
          <li v-for="item in navItems" :key="item.id">
            <NavLink :item="item" class="transition hover:text-white" />
          </li>
        </ul>
      </nav>

      <!-- From Ozone Settings; details left empty there are hidden, and so is the column. -->
      <div v-if="hasContact">
        <h2 class="font-bold text-white">{{ t("footer.contact") }}</h2>
        <ul class="mt-4 space-y-2.5">
          <li v-for="line in lines" :key="line.href ?? line.text" class="flex items-start gap-2.5">
            <component :is="line.icon" class="mt-1 size-4 shrink-0 text-brand-leaf" aria-hidden="true" />
            <a v-if="line.href" :href="line.href" :dir="line.dir" v-bind="line.external ? EXTERNAL : {}" class="transition hover:text-white">
              {{ line.text }}
            </a>
            <span v-else class="whitespace-pre-line">{{ line.text }}</span>
          </li>
        </ul>
        <template v-if="contact.socials.length">
          <h3 class="sr-only">{{ t("footer.follow") }}</h3>
          <ul class="mt-5 flex flex-wrap gap-2">
            <li v-for="social in contact.socials" :key="social.url">
              <a
                :href="social.url"
                v-bind="EXTERNAL"
                :aria-label="`${t('footer.socialLabel')} ${social.platform}`"
                :title="social.platform"
                class="grid size-9 place-items-center rounded-full bg-white/10 text-white transition hover:bg-brand-red motion-safe:hover:-translate-y-0.5"
              >
                <IconSocial :platform="social.platform" class="size-4" />
              </a>
            </li>
          </ul>
        </template>
      </div>
    </div>

    <div class="border-t border-white/10">
      <p class="section py-5 text-caption text-brand-silver-300">
        © {{ year }} {{ t("brand.name") }}. {{ t("footer.rights") }}
      </p>
    </div>
    <BrandStripe edge="bottom" />
  </footer>
</template>

<script lang="ts" setup>
import { type Component, computed } from "vue"
import { useI18n } from "vue-i18n"
import LucideMail from "~icons/lucide/mail"
import LucideMapPin from "~icons/lucide/map-pin"
import LucideMessageCircle from "~icons/lucide/message-circle"
import LucidePhone from "~icons/lucide/phone"

import BrandLogo from "@/components/brand/BrandLogo.vue"
import BrandStripe from "@/components/brand/BrandStripe.vue"
import BrandTagline from "@/components/brand/BrandTagline.vue"
import IconSocial from "@/components/icons/IconSocial.vue"
import NavLink from "@/components/layout/NavLink.vue"
import { useSiteContact } from "@/composables/useSiteContact"
import { navItems } from "@/config/site"

const EXTERNAL = { target: "_blank", rel: "noopener" }

const { t } = useI18n()
const contact = useSiteContact()
const year = new Date().getFullYear()

interface Line {
	icon: Component
	text: string
	href?: string
	/** Phone numbers read left to right on Arabic pages too. */
	dir?: "ltr"
	external?: boolean
}

/** The contact details that are filled in, in display order. */
const lines = computed(() => {
	const c = contact.value
	const all: (Line | null)[] = [
		c.phone && c.phoneHref
			? { icon: LucidePhone, text: c.phone, href: c.phoneHref, dir: "ltr" }
			: null,
		c.email && c.emailHref
			? { icon: LucideMail, text: c.email, href: c.emailHref }
			: null,
		c.whatsappHref
			? {
					icon: LucideMessageCircle,
					text: t("footer.whatsapp"),
					href: c.whatsappHref,
					external: true,
				}
			: null,
		c.address ? { icon: LucideMapPin, text: c.address } : null,
		c.map
			? {
					icon: LucideMapPin,
					text: t("footer.map"),
					href: c.map,
					external: true,
				}
			: null,
	]
	return all.filter((line): line is Line => !!line)
})

const hasContact = computed(
	() => lines.value.length > 0 || contact.value.socials.length > 0,
)
</script>
