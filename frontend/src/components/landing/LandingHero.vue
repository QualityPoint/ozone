<template>
  <section class="relative overflow-x-clip">
    <div class="section grid items-end gap-10 pt-10 lg:grid-cols-[1fr_1.1fr] lg:pt-16">
      <div class="lg:pb-16">
        <BaseSectionTag>{{ t("brand.name") }}</BaseSectionTag>
        <h1 class="mt-6 text-heading-lg font-extrabold text-site-heading sm:text-display">{{ t("hero.title") }}</h1>
        <p class="mt-5 max-w-xl text-body-lg text-site-muted">{{ t("brand.about") }}</p>
        <!-- On phones the items wrap (English needs two lines), so the pill becomes a rounded box. -->
        <BasePill class="mt-6 max-sm:rounded-2xl">
          <BrandTagline class="text-caption sm:text-body" />
        </BasePill>
        <div class="mt-8 flex flex-wrap gap-3">
          <BaseButton :to="sectionLink('contact')">{{ t("hero.primaryCta") }}</BaseButton>
          <BaseButton :to="sectionLink('services')" variant="outline">{{ t("hero.secondaryCta") }}</BaseButton>
        </div>
      </div>

      <!-- The truck, cut out of the operation file, parked on the band below: its wheels touch
           the band, over a soft contact shadow. -->
      <div class="relative lg:-me-4 xl:-me-16">
        <span class="absolute inset-x-[4%] -bottom-1.5 h-5 rounded-[50%] bg-black/25 blur-md" aria-hidden="true" />
        <img
          :src="heroTruck"
          :alt="t('hero.imageAlt')"
          width="1200"
          height="529"
          fetchpriority="high"
          class="brand-art relative w-full"
        />
      </div>
    </div>
    <BrandStripe edge="bottom" />
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"

import heroTruck from "@/assets/images/hero-truck.webp"
import BaseButton from "@/components/base/BaseButton.vue"
import BasePill from "@/components/base/BasePill.vue"
import BaseSectionTag from "@/components/base/BaseSectionTag.vue"
import BrandStripe from "@/components/brand/BrandStripe.vue"
import BrandTagline from "@/components/brand/BrandTagline.vue"
import { useLocale } from "@/composables/useLocale"

const { t } = useI18n()
const { sectionLink } = useLocale()
</script>
