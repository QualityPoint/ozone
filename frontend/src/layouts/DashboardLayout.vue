<template>
  <!-- The producer's dashboard (docs/producer_dashboard/frontend.md): a top bar with the logo, the
       producer's name and the controls; the pages menu at the side on desktop and as a scrolling
       row under the top bar on phones; the page on the site's tint. -->
  <div class="flex min-h-screen flex-col bg-site-tint">
    <a
      href="#main"
      class="sr-only focus:not-sr-only focus:fixed focus:start-4 focus:top-4 focus:z-50 focus:rounded-full focus:bg-site-bg focus:px-4 focus:py-2 focus:font-bold focus:text-site-heading focus:shadow-card"
    >
      {{ t("a11y.skipToContent") }}
    </a>
    <header class="sticky top-0 z-40 border-b border-site-line bg-site-bg/90 backdrop-blur-xl">
      <BrandStripe />
      <div class="flex h-16 items-center justify-between gap-2 px-4 sm:px-6">
        <div class="flex min-w-0 items-center gap-3">
          <RouterLink :to="home" :aria-label="t('a11y.home')" class="block w-24 shrink-0 sm:w-28">
            <BrandLogo :height="40" />
          </RouterLink>
          <p v-if="producer" class="hidden min-w-0 truncate border-s border-site-line ps-3 text-caption font-bold text-site-heading sm:block">
            {{ producer.title }}
          </p>
        </div>
        <div class="flex items-center gap-1">
          <ThemeToggle />
          <LanguageSwitcher />
          <button
            type="button"
            class="grid size-10 place-items-center rounded-full text-site-heading transition hover:bg-site-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
            :aria-label="t('dashboard.logout')"
            :title="t('dashboard.logout')"
            @click="logOut"
          >
            <LucideLogOut class="size-5 rtl:-scale-x-100" aria-hidden="true" />
          </button>
        </div>
      </div>
      <DashboardNav v-if="producer" class="overflow-x-auto px-4 pb-3 lg:hidden" horizontal />
    </header>

    <div class="flex flex-1">
      <!-- An account nobody has linked yet has no pages to go to. -->
      <aside v-if="producer" class="hidden w-64 shrink-0 border-e border-site-line bg-site-bg lg:block">
        <DashboardNav class="sticky top-[4.5rem] p-4" />
      </aside>
      <main id="main" class="min-w-0 flex-1 px-4 py-8 sm:px-8">
        <div class="mx-auto max-w-5xl">
          <slot />
        </div>
      </main>
    </div>
    <BrandStripe edge="bottom" />
  </div>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideLogOut from "~icons/lucide/log-out"

import BrandLogo from "@/components/brand/BrandLogo.vue"
import BrandStripe from "@/components/brand/BrandStripe.vue"
import DashboardNav from "@/components/dashboard/DashboardNav.vue"
import LanguageSwitcher from "@/components/layout/LanguageSwitcher.vue"
import ThemeToggle from "@/components/layout/ThemeToggle.vue"
import { useLocale } from "@/composables/useLocale"
import { useSessionStore } from "@/stores/session"
import { useUserStore } from "@/stores/user"
import { storeToRefs } from "pinia"

const { t } = useI18n()
const { home } = useLocale()
const session = useSessionStore()
const { producer } = storeToRefs(useUserStore())

async function logOut() {
	await session.logout().catch(() => {})
	// A full load: the next visitor starts from a clean page (and a fresh CSRF token).
	window.location.assign(home.value)
}
</script>
