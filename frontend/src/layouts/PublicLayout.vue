<template>
  <div class="relative isolate flex min-h-screen flex-col">
    <a
      href="#main"
      class="sr-only focus:not-sr-only focus:fixed focus:start-4 focus:top-4 focus:z-50 focus:rounded-full focus:bg-site-bg focus:px-4 focus:py-2 focus:font-bold focus:text-site-heading focus:shadow-card"
    >
      {{ t("a11y.skipToContent") }}
    </a>
    <BrandSilverBackground />
    <TheHeader />
    <main id="main" class="flex-1">
      <slot />
    </main>
    <TheFooter />
  </div>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"

import BrandSilverBackground from "@/components/brand/BrandSilverBackground.vue"
import TheFooter from "@/components/layout/TheFooter.vue"
import TheHeader from "@/components/layout/TheHeader.vue"

const { t } = useI18n()
</script>
