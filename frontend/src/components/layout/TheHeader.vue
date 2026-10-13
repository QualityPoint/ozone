<template>
  <header
    :class="[
      'sticky top-0 z-40 transition-all duration-300',
      scrolled || menuOpen ? 'bg-site-bg/80 shadow-header backdrop-blur-xl' : 'bg-transparent',
    ]"
  >
    <BrandStripe />
    <nav class="section flex h-20 items-center justify-between gap-4">
      <RouterLink :to="home" :aria-label="t('a11y.home')" class="shrink-0">
        <BrandLogo :height="48" />
      </RouterLink>

      <ul class="hidden items-center gap-1 lg:flex">
        <li v-for="item in navItems" :key="item.id">
          <NavLink
            :item="item"
            class="rounded-full px-4 py-2 text-caption font-bold text-site-heading transition hover:bg-site-hover"
          />
        </li>
      </ul>

      <div class="flex items-center gap-1 sm:gap-2">
        <!-- On phones it's in the menu: the row has no room left at 320 px. -->
        <AccountLink class="max-sm:hidden" />
        <ThemeToggle />
        <LanguageSwitcher />
        <button
          type="button"
          class="grid size-10 shrink-0 place-items-center rounded-full text-site-heading transition hover:bg-site-hover lg:hidden"
          :aria-expanded="menuOpen"
          aria-controls="mobile-menu"
          :aria-label="menuOpen ? t('a11y.closeMenu') : t('a11y.openMenu')"
          @click="menuOpen = !menuOpen"
        >
          <LucideX v-if="menuOpen" class="size-6" aria-hidden="true" />
          <LucideMenu v-else class="size-6" aria-hidden="true" />
        </button>
      </div>
    </nav>

    <div v-show="menuOpen" id="mobile-menu" class="section pb-6 lg:hidden">
      <ul class="space-y-1">
        <li v-for="item in navItems" :key="item.id">
          <NavLink :item="item" class="block rounded-2xl px-4 py-3 font-bold text-site-heading hover:bg-site-hover" />
        </li>
        <li class="border-t border-site-line pt-1 sm:hidden">
          <AccountLink labelled />
        </li>
      </ul>
    </div>
  </header>
</template>

<script lang="ts" setup>
import { onBeforeUnmount, onMounted, ref, watch } from "vue"
import { useI18n } from "vue-i18n"
import { useRoute } from "vue-router"
import LucideMenu from "~icons/lucide/menu"
import LucideX from "~icons/lucide/x"

import BrandLogo from "@/components/brand/BrandLogo.vue"
import BrandStripe from "@/components/brand/BrandStripe.vue"
import AccountLink from "@/components/layout/AccountLink.vue"
import LanguageSwitcher from "@/components/layout/LanguageSwitcher.vue"
import NavLink from "@/components/layout/NavLink.vue"
import ThemeToggle from "@/components/layout/ThemeToggle.vue"
import { useLocale } from "@/composables/useLocale"
import { navItems } from "@/config/site"

const { t } = useI18n()
const route = useRoute()
const { home } = useLocale()

const menuOpen = ref(false)
// Any navigation (a menu link, the logo, the language switch) closes the phone menu.
watch(
	() => route.fullPath,
	() => {
		menuOpen.value = false
	},
)

// The header turns solid once the page scrolls under it.
const scrolled = ref(false)
function onScroll() {
	scrolled.value = window.scrollY > 8
}
onMounted(() => {
	onScroll()
	window.addEventListener("scroll", onScroll, { passive: true })
})
onBeforeUnmount(() => window.removeEventListener("scroll", onScroll))
</script>
