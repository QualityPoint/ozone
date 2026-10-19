<template>
  <!-- Naqel's hero (hawya's LandingHero; the presentation, pp. 66-68): deep green-black, the title
       with its accent in the logo green, and an abstract picture of the platform. Ozone's header sits
       above it, not over it, so the top padding is hawya's less the header's 5rem. -->
  <section class="relative overflow-hidden bg-naqel-night pb-20 pt-12 text-white sm:pt-16 lg:pb-28">
    <!-- A soft green light behind the art, and the presentation's band along the foot. -->
    <div class="pointer-events-none absolute -end-40 top-10 size-[36rem] rounded-full bg-naqel-green/20 blur-3xl" aria-hidden="true" />
    <div class="section relative grid items-center gap-14 lg:grid-cols-[1fr_1.15fr]">
      <div>
        <!-- Naqel's logo in its white version, the brand sheet's for dark grounds (brand.pdf). -->
        <img :src="logo" :alt="t('naqel.name')" width="325" height="98" class="brand-art mb-8 h-14 w-auto sm:h-16" />
        <p class="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/5 px-3 py-1 text-caption">
          <span class="size-2 rounded-full bg-naqel-green" aria-hidden="true" />
          {{ t("naqel.hero.badge") }}
        </p>
        <!-- A step smaller on small phones and at lg, where the text column is narrowest, so each line of
             the title fits in both languages. -->
        <h1 class="mt-6 text-heading font-extrabold min-[400px]:text-heading-lg sm:text-display lg:text-heading-lg xl:text-display">
          {{ t("naqel.hero.title") }}
          <span class="block text-naqel-green">{{ t("naqel.hero.titleAccent") }}</span>
        </h1>
        <p class="mt-5 text-body-lg font-bold text-naqel-night-100">{{ t("naqel.tagline") }}</p>
        <p class="mt-3 max-w-xl text-naqel-night-200">{{ t("naqel.hero.intro") }}</p>
        <div class="mt-8 flex flex-wrap gap-3">
          <!-- Get started: an email to Naqel's developer (config/naqel.ts). -->
          <NaqelButton :href="naqelContactHref">
            {{ t("naqel.hero.start") }}
            <LucideArrowLeft class="size-4 ltr:-scale-x-100" aria-hidden="true" />
          </NaqelButton>
          <NaqelButton :to="{ hash: '#calculator' }" variant="ghost">{{ t("naqel.hero.calculator") }}</NaqelButton>
        </div>
      </div>

      <div class="relative">
        <NaqelPlatformArt />
        <!-- The mock's card over the art's corner: the app icon and "digital and smart". The art
             isn't mirrored, so the card sits on its left (over the bars) in both languages. -->
        <div class="absolute -bottom-6 left-6 flex items-center gap-3 rounded-2xl bg-site-bg px-4 py-3 shadow-naqel-card" aria-hidden="true">
          <img :src="appIcon" alt="" width="40" height="40" class="brand-art size-10" />
          <span class="leading-tight">
            <span class="block text-label text-site-muted">{{ t("naqel.hero.floating.label") }}</span>
            <span class="block font-extrabold text-site-heading">{{ t("naqel.hero.floating.value") }}</span>
          </span>
        </div>
      </div>
    </div>
    <NaqelBar class="absolute inset-x-0 bottom-0" />
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideArrowLeft from "~icons/lucide/arrow-left"

import appIcon from "@/assets/naqel/app-icon.svg"
import logo from "@/assets/naqel/logo-white.svg"
import NaqelButton from "@/components/naqel/base/NaqelButton.vue"
import NaqelBar from "@/components/naqel/brand/NaqelBar.vue"
import NaqelPlatformArt from "@/components/naqel/brand/NaqelPlatformArt.vue"
import { naqelContactHref } from "@/config/naqel"

const { t } = useI18n()
</script>
