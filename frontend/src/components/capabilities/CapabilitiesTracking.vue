<template>
  <!-- The green band, as on the landing page's "why us". -->
  <section id="tracking" class="bg-brand-green py-20 text-white dark:border-y dark:border-white/10">
    <div class="section grid items-start gap-12 lg:grid-cols-[1fr_1.1fr]">
      <div>
        <BaseSectionTag>{{ t("capabilities.sections.tracking") }}</BaseSectionTag>
        <h2 class="mt-5 text-heading font-extrabold sm:text-heading-lg">{{ t("capabilities.tracking.title") }}</h2>
        <p class="mt-4 text-body-lg text-brand-silver-200">{{ t("capabilities.tracking.intro") }}</p>
        <BaseReveal class="mt-8 flex gap-4 rounded-3xl border border-white/15 bg-white/5 p-6">
          <LucideClipboardList class="mt-1 size-7 shrink-0 text-brand-leaf" aria-hidden="true" />
          <div>
            <h3 class="font-extrabold">{{ t("capabilities.tracking.reports.title") }}</h3>
            <p class="mt-1.5 text-brand-silver-200">{{ t("capabilities.tracking.reports.body") }}</p>
          </div>
        </BaseReveal>
      </div>
      <BaseReveal :delay="120" class="rounded-3xl bg-white p-7 text-brand-ink">
        <span class="flex items-center gap-3 font-extrabold text-brand-green">
          <LucideSatellite class="size-6" aria-hidden="true" />
          GPS
        </span>
        <BaseCheckList :items="list('capabilities.tracking.features')" class="mt-5" />
      </BaseReveal>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideClipboardList from "~icons/lucide/clipboard-list"
import LucideSatellite from "~icons/lucide/satellite"

import BaseCheckList from "@/components/base/BaseCheckList.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionTag from "@/components/base/BaseSectionTag.vue"
import { useMessageList } from "@/composables/useMessageList"

const { t } = useI18n()
const { list } = useMessageList()
</script>
