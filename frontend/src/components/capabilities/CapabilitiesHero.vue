<template>
  <!-- The page's opening: the head office in photos beside the title, then the page's contents
       laid out like the operation file's index page. Still: no motion. -->
  <section class="section pb-16 pt-10 lg:pt-16">
    <div class="grid items-center gap-12 lg:grid-cols-[1fr_1.05fr]">
      <div>
        <BaseSectionTag>{{ t("capabilities.hero.tag") }}</BaseSectionTag>
        <h1 class="mt-6 text-heading-lg font-extrabold text-site-heading sm:text-display">{{ t("capabilities.hero.title") }}</h1>
        <p class="mt-5 max-w-xl text-body-lg text-site-muted">{{ t("capabilities.hero.intro") }}</p>
        <BasePill class="mt-6 max-sm:rounded-2xl">
          <BrandTagline class="text-caption sm:text-body" />
        </BasePill>
      </div>

      <!-- The tower block, its caption in the top corner, with the office's entrance (its Ozone
           sign) over the lower corner. -->
      <figure class="relative pb-16 sm:pb-20">
        <img
          :src="towers"
          :alt="t('capabilities.hero.towersAlt')"
          width="680"
          height="310"
          fetchpriority="high"
          class="brand-art aspect-[16/10] w-full rounded-4xl object-cover shadow-card"
        />
        <img
          :src="entrance"
          :alt="t('capabilities.hero.entranceAlt')"
          width="1068"
          height="755"
          class="brand-art absolute bottom-0 end-4 aspect-[4/3] w-[46%] rounded-3xl object-cover shadow-card ring-8 ring-site-bg"
        />
        <figcaption class="absolute start-4 top-4">
          <BasePill variant="accent" size="sm">{{ t("capabilities.hero.photoCaption") }}</BasePill>
        </figcaption>
      </figure>
    </div>

    <nav :aria-label="t('capabilities.hero.contents')" class="mt-14">
      <BaseCard class="p-6 sm:p-8">
        <BasePill variant="accent" size="sm">{{ t("capabilities.hero.contents") }}</BasePill>
        <ol class="mt-4 grid gap-x-8 sm:grid-cols-2 lg:grid-cols-3">
          <li v-for="(id, i) in capabilitySections" :key="id" class="border-b border-site-line">
            <RouterLink :to="{ hash: `#${id}` }" class="group flex items-center gap-4 py-3 font-bold text-site-heading">
              <span class="w-8 text-title font-extrabold text-brand-red" dir="ltr">{{ String(i + 1).padStart(2, "0") }}</span>
              <span class="flex-1 transition group-hover:text-brand-red">{{ t(`capabilities.sections.${id}`) }}</span>
              <LucideArrowLeft class="size-4 text-site-muted ltr:-scale-x-100" aria-hidden="true" />
            </RouterLink>
          </li>
        </ol>
      </BaseCard>
    </nav>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideArrowLeft from "~icons/lucide/arrow-left"

// Photos from the operation file (scripts/build-brand-assets.py: EMBEDDED_PHOTOS).
import entrance from "@/assets/images/office/entrance.webp"
import towers from "@/assets/images/office/towers.webp"
import BaseCard from "@/components/base/BaseCard.vue"
import BasePill from "@/components/base/BasePill.vue"
import BaseSectionTag from "@/components/base/BaseSectionTag.vue"
import BrandTagline from "@/components/brand/BrandTagline.vue"
import { capabilitySections } from "@/config/site"

const { t } = useI18n()
</script>
