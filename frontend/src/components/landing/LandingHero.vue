<template>
  <section class="section grid items-center gap-12 pb-20 pt-10 lg:grid-cols-[1.05fr_1fr] lg:pt-16">
    <div class="motion-safe:animate-fade-up">
      <BaseSectionTag>{{ t("brand.name") }}</BaseSectionTag>
      <h1 class="mt-6 text-heading-lg font-extrabold text-site-heading sm:text-display">{{ t("hero.title") }}</h1>
      <p class="mt-5 max-w-xl text-body-lg text-site-muted">{{ t("brand.about") }}</p>
      <BasePill class="mt-6">
        <BrandTagline />
      </BasePill>
      <div class="mt-8 flex flex-wrap gap-3">
        <BaseButton :to="sectionLink('contact')">{{ t("hero.primaryCta") }}</BaseButton>
        <BaseButton :to="sectionLink('services')" variant="outline">{{ t("hero.secondaryCta") }}</BaseButton>
      </div>
    </div>

    <div class="float-layer motion-safe:animate-float">
      <LandingPhoto slug="compactor-trucks" :alt="t('hero.imageAlt')" class="shadow-card ring-1 ring-site-line/70" />
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"

import BaseButton from "@/components/base/BaseButton.vue"
import BasePill from "@/components/base/BasePill.vue"
import BaseSectionTag from "@/components/base/BaseSectionTag.vue"
import BrandTagline from "@/components/brand/BrandTagline.vue"
import { useLocale } from "@/composables/useLocale"
import LandingPhoto from "./LandingPhoto.vue"

const { t } = useI18n()
const { sectionLink } = useLocale()
</script>
