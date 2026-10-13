<template>
  <!-- The green band, like the documents' "why us" pages. -->
  <section id="why" class="relative overflow-hidden bg-brand-green py-20 text-white dark:border-y dark:border-white/10">
    <div class="section">
      <div class="mx-auto max-w-3xl text-center">
        <BaseSectionTag>{{ t("why.tag") }}</BaseSectionTag>
        <h2 class="mt-5 text-heading font-extrabold sm:text-heading-lg">{{ t("why.title") }}</h2>
      </div>

      <ul class="mt-14 grid gap-5 md:grid-cols-3">
        <BaseReveal
          v-for="(pillar, i) in pillars"
          :key="pillar.title"
          as="li"
          :delay="i * 100"
          class="rounded-3xl border border-white/15 bg-white/5 p-7"
        >
          <component :is="ICONS[i]" class="size-8 text-brand-leaf" aria-hidden="true" />
          <h3 class="mt-4 text-title font-extrabold">{{ pillar.title }}</h3>
          <p class="mt-2 text-brand-silver-200">{{ pillar.body }}</p>
        </BaseReveal>
      </ul>

      <ul class="mt-16 grid gap-10 text-center sm:grid-cols-3">
        <li v-for="stat in stats" :key="stat.id">
          <BaseStat
            :value="stat.value"
            :prefix="stat.prefix"
            :suffix="stat.suffix"
            :label="t(`why.stats.${stat.id}`)"
            class="flex flex-col items-center text-brand-silver-100"
          />
        </li>
      </ul>

      <BaseReveal class="mx-auto mt-16 max-w-3xl rounded-3xl bg-white p-7 text-brand-ink">
        <h3 class="text-title font-extrabold text-brand-green">{{ t("why.featuresTitle") }}</h3>
        <BaseCheckList :items="list('why.features')" class="mt-5" />
      </BaseReveal>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { computed } from "vue"
import { useI18n } from "vue-i18n"
import LucideMapPin from "~icons/lucide/map-pin"
import LucideShieldCheck from "~icons/lucide/shield-check"
import LucideSprayCan from "~icons/lucide/spray-can"

import BaseCheckList from "@/components/base/BaseCheckList.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionTag from "@/components/base/BaseSectionTag.vue"
import BaseStat from "@/components/base/BaseStat.vue"
import { useMessageList } from "@/composables/useMessageList"
import { stats } from "@/config/site"

/** One icon per pillar in why.pillars, same order. */
const ICONS = [LucideMapPin, LucideShieldCheck, LucideSprayCan]

const { t } = useI18n()
const { list } = useMessageList()
const pillars = computed(() => {
	const bodies = list("why.pillars", "body")
	return list("why.pillars", "title").map((title, i) => ({
		title,
		body: bodies[i],
	}))
})
</script>
