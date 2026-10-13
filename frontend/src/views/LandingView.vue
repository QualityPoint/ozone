<template>
  <!-- Placeholder hero until the landing sections land (step 4 of docs/frontend/README.md). -->
  <section class="section flex min-h-[70vh] flex-col items-start justify-center gap-6 py-20">
    <BaseSectionTag>{{ t("brand.name") }}</BaseSectionTag>
    <h1 class="max-w-3xl text-display font-extrabold text-site-heading sm:text-display-lg">
      {{ t("hero.title") }}
    </h1>
    <p class="max-w-2xl text-body-lg text-site-muted">{{ t("brand.about") }}</p>
    <BasePill>
      <BrandTagline />
    </BasePill>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"

import BasePill from "@/components/base/BasePill.vue"
import BaseSectionTag from "@/components/base/BaseSectionTag.vue"
import BrandTagline from "@/components/brand/BrandTagline.vue"

const { t } = useI18n()
</script>
