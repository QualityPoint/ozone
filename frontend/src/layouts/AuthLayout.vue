<template>
  <!-- One of the documents' pages: white with silver shards between the green and red top band
       and the green bottom band. The form sits on the start side; on desktop, the website's
       slogan and its truck, parked on the bottom band, fill the other. -->
  <div class="relative isolate flex min-h-screen flex-col">
    <a
      href="#main"
      class="sr-only focus:not-sr-only focus:fixed focus:start-4 focus:top-4 focus:z-50 focus:rounded-full focus:bg-site-bg focus:px-4 focus:py-2 focus:font-bold focus:text-site-heading focus:shadow-card"
    >
      {{ t("a11y.skipToContent") }}
    </a>
    <BrandSilverBackground />
    <BrandStripe />
    <header class="section flex h-20 items-center justify-between gap-4">
      <RouterLink :to="home" :aria-label="t('a11y.home')" class="shrink-0">
        <BrandLogo :height="44" />
      </RouterLink>
      <div class="flex items-center gap-1 sm:gap-2">
        <RouterLink
          :to="home"
          class="hidden items-center gap-2 rounded-full px-3 py-2 text-caption font-bold text-site-heading transition hover:bg-site-hover sm:inline-flex"
        >
          <LucideArrowLeft class="size-4 rtl:-scale-x-100" aria-hidden="true" />
          {{ t("auth.backToSite") }}
        </RouterLink>
        <ThemeToggle />
        <LanguageSwitcher />
      </div>
    </header>

    <main id="main" class="section grid flex-1 gap-12 lg:grid-cols-[minmax(0,28rem)_minmax(0,1fr)] lg:gap-16">
      <div class="mx-auto w-full max-w-md self-center py-8 lg:mx-0">
        <slot />
      </div>
      <div class="hidden flex-col justify-end pt-12 lg:flex" aria-hidden="true">
        <p class="text-heading-lg font-extrabold text-site-heading">{{ t("hero.title") }}</p>
        <p class="mt-4 max-w-md text-body-lg text-site-muted">{{ t("auth.panel") }}</p>
        <BasePill class="mt-6 self-start">
          <BrandTagline />
        </BasePill>
        <BrandTruck class="mt-10 xl:-me-16" />
      </div>
    </main>
    <BrandStripe edge="bottom" />
  </div>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideArrowLeft from "~icons/lucide/arrow-left"

import BasePill from "@/components/base/BasePill.vue"
import BrandLogo from "@/components/brand/BrandLogo.vue"
import BrandSilverBackground from "@/components/brand/BrandSilverBackground.vue"
import BrandStripe from "@/components/brand/BrandStripe.vue"
import BrandTagline from "@/components/brand/BrandTagline.vue"
import BrandTruck from "@/components/brand/BrandTruck.vue"
import LanguageSwitcher from "@/components/layout/LanguageSwitcher.vue"
import ThemeToggle from "@/components/layout/ThemeToggle.vue"
import { useLocale } from "@/composables/useLocale"

const { t } = useI18n()
const { home } = useLocale()
</script>
