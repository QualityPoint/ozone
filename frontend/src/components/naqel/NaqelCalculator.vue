<template>
  <section id="calculator" class="overflow-x-clip py-16 sm:py-20">
    <NaqelSectionHeading :title="t('naqel.calculator.title')" :intro="t('naqel.calculator.intro')" />

    <div class="section mt-10 grid gap-6 lg:grid-cols-2">
      <!-- ISIC: its five levels, broadest first. -->
      <NaqelCard as="article" class="p-6">
        <h3 class="text-title font-extrabold text-site-heading">{{ t("naqel.calculator.isic.title") }}</h3>
        <p class="mt-2 text-site-muted">{{ t("naqel.calculator.isic.body") }}</p>
        <!-- ISIC's five levels, broadest first, deepening to the logo green at the activity. From sm
             up, one arrow bar of equal segments that fill the card, so it stays on one line in both
             languages, pointing the reading way; on phones, a staircase of bars (styles below). -->
        <ol class="isic mt-5 grid gap-1.5 sm:grid-cols-5 sm:gap-0">
          <li
            v-for="(level, i) in list('naqel.calculator.isic.levels')"
            :key="level"
            :style="{ '--i': i }"
            :class="['isic-step grid min-h-10 place-items-center text-center text-label font-extrabold sm:text-caption', i >= 3 ? 'text-white' : 'text-naqel-night']"
          >
            {{ level }}
          </li>
        </ol>
      </NaqelCard>

      <!-- Fair evaluation: the factors of the facility's own rating, one star to five. -->
      <NaqelCard as="article" class="p-6">
        <h3 class="text-title font-extrabold text-site-heading">{{ t("naqel.calculator.rating.title") }}</h3>
        <p class="mt-2 text-site-muted">{{ t("naqel.calculator.rating.body") }}</p>
        <ol class="mt-5 grid grid-cols-5 items-end gap-2">
          <li v-for="(factor, i) in ratingFactors" :key="factor" class="flex flex-col items-center gap-1.5">
            <span class="text-caption font-extrabold text-site-heading" dir="ltr">×{{ factor.toFixed(1) }}</span>
            <span class="w-full rounded-t-lg bg-naqel-green" :style="{ height: `${factor * 34}px`, opacity: 0.45 + i * 0.13 }" aria-hidden="true" />
            <span class="flex text-naqel-green" :aria-label="`${i + 1} ★`">
              <LucideStar v-for="n in i + 1" :key="n" class="size-2.5 fill-current" aria-hidden="true" />
            </span>
          </li>
        </ol>
      </NaqelCard>

      <!-- The containers it infers, at their capacity: the presentation's chart. -->
      <NaqelCard as="article" class="grid gap-8 p-6 lg:col-span-2 lg:grid-cols-[minmax(0,1fr)_minmax(0,2fr)] lg:items-center">
        <div>
          <h3 class="text-title font-extrabold text-site-heading">{{ t("naqel.calculator.containers.title") }}</h3>
          <p class="mt-2 text-site-muted">{{ t("naqel.calculator.containers.body") }}</p>
        </div>
        <NaqelContainerChart />
      </NaqelCard>

      <NaqelCard as="article" class="p-6">
        <h3 class="text-title font-extrabold text-site-heading">{{ t("naqel.calculator.rate.title") }}</h3>
        <p class="mt-2 text-site-muted">{{ t("naqel.calculator.rate.body") }}</p>
        <h3 class="mt-6 text-title font-extrabold text-site-heading">{{ t("naqel.calculator.tree.title") }}</h3>
        <p class="mt-2 text-site-muted">{{ t("naqel.calculator.tree.body") }}</p>
      </NaqelCard>

      <!-- Geographic estimation: the Kingdom's administrative levels, broadest first. -->
      <NaqelCard as="article" class="p-6">
        <h3 class="text-title font-extrabold text-site-heading">{{ t("naqel.calculator.geo.title") }}</h3>
        <p class="mt-2 text-site-muted">{{ t("naqel.calculator.geo.body") }}</p>
        <ol class="mt-5 space-y-2">
          <li v-for="(level, i) in list('naqel.calculator.geo.levels')" :key="level" class="flex items-center gap-3" :style="{ paddingInlineStart: `${i * 1.25}rem` }">
            <LucideMapPin class="size-4 shrink-0 text-naqel-green" aria-hidden="true" />
            <span class="font-bold text-site-heading">{{ level }}</span>
          </li>
        </ol>
      </NaqelCard>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideMapPin from "~icons/lucide/map-pin"
import LucideStar from "~icons/lucide/star"

import NaqelCard from "@/components/naqel/base/NaqelCard.vue"
import NaqelSectionHeading from "@/components/naqel/base/NaqelSectionHeading.vue"
import { useMessageList } from "@/composables/useMessageList"
import { ratingFactors } from "@/config/naqel"
import NaqelContainerChart from "./NaqelContainerChart.vue"

const { t } = useI18n()
const { list } = useMessageList()
</script>

<style scoped>
/* The ISIC bar: the brand green's steps, light to the logo green at the activity. */
.isic-step:nth-child(1) {
	background-color: theme("colors.naqel.green.100");
}
.isic-step:nth-child(2) {
	background-color: theme("colors.naqel.green.200");
}
.isic-step:nth-child(3) {
	background-color: theme("colors.naqel.green.300");
}
.isic-step:nth-child(4) {
	background-color: theme("colors.naqel.green.600");
}
.isic-step:nth-child(5) {
	background-color: theme("colors.naqel.green.DEFAULT");
}
/* Phones: a staircase, each level indented a step further than the one above it. */
.isic-step {
	border-radius: 8px;
	margin-inline-start: calc(var(--i) * 14px);
	padding-inline: 12px;
}

/* From sm up: each segment an arrow pointing the reading way, overlapping the next by its tip; the
   first has a straight back. Drawn for English (pointing right), mirrored in Arabic. */
@media (min-width: 640px) {
	.isic-step {
		border-radius: 0;
		margin-inline-start: 0;
		margin-inline-end: -8px;
		padding-inline: 14px;
		clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 50%, calc(100% - 10px) 100%, 0 100%, 10px 50%);
	}
	.isic-step:first-child {
		clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 50%, calc(100% - 10px) 100%, 0 100%);
	}
	.isic-step:last-child {
		margin-inline-end: 0;
	}
	:dir(rtl) .isic-step {
		clip-path: polygon(10px 0, 100% 0, calc(100% - 10px) 50%, 100% 100%, 10px 100%, 0 50%);
	}
	:dir(rtl) .isic-step:first-child {
		clip-path: polygon(10px 0, 100% 0, 100% 100%, 10px 100%, 0 50%);
	}
}
</style>
