<template>
  <section id="method" class="section py-20">
    <BaseSectionHeading :tag="t('capabilities.sections.method')" :title="t('capabilities.method.title')" />

    <!-- The two phases, as the operation file pairs them: building (green), then operating (red). -->
    <ol class="mt-14 grid gap-6 md:grid-cols-2">
      <BaseReveal v-for="(phase, i) in PHASES" :key="phase.id" as="li" :delay="i * 100">
        <BaseCard class="flex h-full gap-5 p-7">
          <span :class="['grid size-14 shrink-0 place-items-center rounded-2xl text-white', phase.color]">
            <component :is="phase.icon" class="size-7" aria-hidden="true" />
          </span>
          <div>
            <h3 class="text-title font-extrabold text-site-heading">{{ t(`capabilities.method.phases.${phase.id}.title`) }}</h3>
            <p class="mt-2 text-site-muted">{{ t(`capabilities.method.phases.${phase.id}.body`) }}</p>
          </div>
        </BaseCard>
      </BaseReveal>
    </ol>

    <!-- Where the work is run from: the head office's reception, as a wide banner. -->
    <BaseReveal as="figure" class="relative mt-10 overflow-hidden rounded-4xl shadow-card">
      <img
        :src="reception"
        :alt="t('capabilities.method.receptionCaption')"
        width="1100"
        height="423"
        loading="lazy"
        decoding="async"
        class="brand-art aspect-[21/9] w-full object-cover sm:aspect-[26/10]"
      />
      <figcaption class="absolute bottom-4 start-4">
        <BasePill variant="accent" size="sm">{{ t("capabilities.method.receptionCaption") }}</BasePill>
      </figcaption>
    </BaseReveal>

    <h3 class="mt-16 text-center text-title-lg font-extrabold text-site-heading">{{ t("capabilities.method.strategiesTitle") }}</h3>
    <ul class="mt-8 grid gap-6 md:grid-cols-3">
      <BaseReveal v-for="(id, i) in STRATEGIES" :key="id" as="li" :delay="i * 100">
        <div class="h-full rounded-3xl bg-site-tint p-7">
          <component :is="STRATEGY_ICONS[id]" class="size-8 text-brand-red" aria-hidden="true" />
          <h4 class="mt-4 font-extrabold text-site-heading">{{ t(`capabilities.method.strategies.${id}.title`) }}</h4>
          <BaseDotList :items="list(`capabilities.method.strategies.${id}.points`)" class="mt-3 text-caption text-site-muted" />
        </div>
      </BaseReveal>
    </ul>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideChartLine from "~icons/lucide/chart-line"
import LucideConstruction from "~icons/lucide/construction"
import LucideCpu from "~icons/lucide/cpu"
import LucideSettings from "~icons/lucide/settings"
import LucideUsers from "~icons/lucide/users"

import reception from "@/assets/images/office/reception.webp"
import BaseCard from "@/components/base/BaseCard.vue"
import BaseDotList from "@/components/base/BaseDotList.vue"
import BasePill from "@/components/base/BasePill.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionHeading from "@/components/base/BaseSectionHeading.vue"
import { useMessageList } from "@/composables/useMessageList"

const PHASES = [
	{ id: "build", icon: LucideConstruction, color: "bg-brand-green" },
	{ id: "operate", icon: LucideSettings, color: "bg-brand-red" },
] as const

const STRATEGIES = ["analysis", "team", "technology"] as const
const STRATEGY_ICONS = {
	analysis: LucideChartLine,
	team: LucideUsers,
	technology: LucideCpu,
} satisfies Record<(typeof STRATEGIES)[number], unknown>

const { t } = useI18n()
const { list } = useMessageList()
</script>
