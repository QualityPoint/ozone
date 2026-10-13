<template>
  <section id="quality" class="section py-20">
    <BaseSectionHeading
      :tag="t('capabilities.sections.quality')"
      :title="t('capabilities.quality.title')"
      :intro="t('capabilities.quality.intro')"
    />

    <ul class="mt-14 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <BaseReveal v-for="(id, i) in CARDS" :key="id" as="li" :delay="(i % 3) * 100">
        <BaseCard class="h-full p-7">
          <component :is="ICONS[id]" class="size-8 text-brand-red" aria-hidden="true" />
          <h3 class="mt-4 text-title font-extrabold text-site-heading">{{ t(`capabilities.quality.cards.${id}.title`) }}</h3>
          <BaseDotList :items="list(`capabilities.quality.cards.${id}.points`)" class="mt-4 text-caption text-site-muted" />
        </BaseCard>
      </BaseReveal>
    </ul>

    <!-- The operation file's risk plan: each risk, its mitigation, and the department that owns it. -->
    <div class="mt-20">
      <h3 class="text-center text-title-lg font-extrabold text-site-heading">{{ t("capabilities.quality.risksTitle") }}</h3>
      <p class="mt-2 text-center text-site-muted">{{ t("capabilities.quality.risksIntro") }}</p>
      <ol class="mt-8 space-y-4">
        <BaseReveal
          v-for="(risk, i) in risks"
          :key="risk.risk"
          as="li"
          :delay="i * 60"
          class="grid gap-3 rounded-3xl border border-site-line bg-site-bg p-5 shadow-card md:grid-cols-[minmax(0,14rem)_1fr_auto] md:items-center md:gap-6"
        >
          <p class="flex items-center gap-3 font-extrabold text-site-heading">
            <span class="grid size-8 shrink-0 place-items-center rounded-full bg-brand-red text-caption text-white" dir="ltr">{{ i + 1 }}</span>
            {{ risk.risk }}
          </p>
          <p class="text-caption text-site-text">
            <span class="sr-only">{{ t("capabilities.quality.plan") }}: </span>{{ risk.plan }}
          </p>
          <BasePill size="sm" class="justify-self-start md:justify-self-end">
            <span class="sr-only">{{ t("capabilities.quality.owner") }}: </span>{{ risk.owner }}
          </BasePill>
        </BaseReveal>
      </ol>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { computed } from "vue"
import { useI18n } from "vue-i18n"
import LucideClipboardCheck from "~icons/lucide/clipboard-check"
import LucideContainer from "~icons/lucide/container"
import LucideRefreshCw from "~icons/lucide/refresh-cw"
import LucideShieldCheck from "~icons/lucide/shield-check"
import LucideTruck from "~icons/lucide/truck"
import LucideWarehouse from "~icons/lucide/warehouse"

import BaseCard from "@/components/base/BaseCard.vue"
import BaseDotList from "@/components/base/BaseDotList.vue"
import BasePill from "@/components/base/BasePill.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionHeading from "@/components/base/BaseSectionHeading.vue"
import { useMessageList } from "@/composables/useMessageList"

const CARDS = [
	"vehicles",
	"containers",
	"stores",
	"safety",
	"continuity",
	"followup",
] as const

const ICONS = {
	vehicles: LucideTruck,
	containers: LucideContainer,
	stores: LucideWarehouse,
	safety: LucideShieldCheck,
	continuity: LucideRefreshCw,
	followup: LucideClipboardCheck,
} satisfies Record<(typeof CARDS)[number], unknown>

const { t } = useI18n()
const { list } = useMessageList()
const risks = computed(() => {
	const key = "capabilities.quality.risks"
	const plans = list(key, "plan")
	const owners = list(key, "owner")
	return list(key, "risk").map((risk, i) => ({
		risk,
		plan: plans[i],
		owner: owners[i],
	}))
})
</script>
