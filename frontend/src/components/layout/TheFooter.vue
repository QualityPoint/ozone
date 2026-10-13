<template>
  <footer class="bg-brand-green-800 text-brand-silver-200 dark:border-t dark:border-white/10">
    <div class="section grid gap-10 py-14 md:grid-cols-3">
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
import { useI18n } from "vue-i18n"

import BrandLogo from "@/components/brand/BrandLogo.vue"
import BrandStripe from "@/components/brand/BrandStripe.vue"
import BrandTagline from "@/components/brand/BrandTagline.vue"
import NavLink from "@/components/layout/NavLink.vue"
import { navItems } from "@/config/site"

const { t } = useI18n()
const year = new Date().getFullYear()
</script>
