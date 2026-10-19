<template>
  <section id="governance" class="overflow-x-clip py-16 sm:py-20">
    <NaqelSectionHeading :title="t('naqel.governance.title')" :intro="t('naqel.governance.intro')" />

    <div class="section mt-10 grid gap-10 lg:grid-cols-[1.15fr_1fr]">
      <!-- The municipality's controls, numbered as in the presentation. -->
      <ol class="space-y-4">
        <li v-for="(control, i) in controls" :key="control.title" class="flex gap-4">
          <span class="grid w-14 shrink-0 place-items-center rounded-xl border-2 border-naqel-green text-display font-extrabold leading-none text-naqel-green" dir="ltr">{{ i + 1 }}</span>
          <div class="flex-1 rounded-xl bg-site-tint px-5 py-4">
            <h3 class="font-extrabold text-site-heading">{{ control.title }}</h3>
            <p class="mt-1 text-caption text-site-text">{{ control.body }}</p>
          </div>
        </li>
      </ol>

      <ul class="space-y-5">
        <li v-for="(icon, id) in FEATURES" :key="id">
          <NaqelCard as="article" class="flex gap-4 p-5">
            <span class="grid size-11 shrink-0 place-items-center rounded-xl bg-naqel-green text-white">
              <component :is="icon" class="size-5" aria-hidden="true" />
            </span>
            <div>
              <h3 class="font-extrabold text-site-heading">{{ t(`naqel.governance.${id}.title`) }}</h3>
              <p class="mt-1 text-caption text-site-muted">{{ t(`naqel.governance.${id}.body`) }}</p>
            </div>
          </NaqelCard>
        </li>
      </ul>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { computed } from "vue"
import { useI18n } from "vue-i18n"
import LucideChartColumn from "~icons/lucide/chart-column"
import LucideHeadset from "~icons/lucide/headset"
import LucideSmartphone from "~icons/lucide/smartphone"

import NaqelCard from "@/components/naqel/base/NaqelCard.vue"
import NaqelSectionHeading from "@/components/naqel/base/NaqelSectionHeading.vue"
import { useMessageList } from "@/composables/useMessageList"

const FEATURES = {
	reports: LucideChartColumn,
	support: LucideHeadset,
	app: LucideSmartphone,
}

const { t } = useI18n()
const { list } = useMessageList()
const controls = computed(() => {
	const bodies = list("naqel.governance.controls", "body")
	return list("naqel.governance.controls", "title").map((title, i) => ({
		title,
		body: bodies[i],
	}))
})
</script>
