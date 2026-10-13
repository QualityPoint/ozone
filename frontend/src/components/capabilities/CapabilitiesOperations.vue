<template>
  <section id="operations" class="bg-site-tint py-20">
    <div class="section">
      <BaseSectionHeading
        :tag="t('capabilities.sections.operations')"
        :title="t('capabilities.operations.title')"
        :intro="t('capabilities.operations.intro')"
      />

      <!-- The operation file's protocol: three numbered stages, joined by a line on desktop. -->
      <ol class="relative mt-14 grid gap-6 md:grid-cols-3">
        <span class="absolute inset-x-[16%] top-8 hidden h-0.5 bg-site-line md:block" aria-hidden="true" />
        <BaseReveal v-for="(step, i) in steps" :key="step.title" as="li" :delay="i * 100" class="relative text-center">
          <span class="relative mx-auto grid size-16 place-items-center rounded-full border-2 border-brand-green bg-site-bg text-brand-green dark:border-brand-leaf dark:text-brand-leaf">
            <component :is="STEP_ICONS[i]" class="size-7" aria-hidden="true" />
          </span>
          <h3 class="mt-4 text-title font-extrabold text-site-heading">
            <span class="text-brand-red" dir="ltr">{{ i + 1 }}.</span> {{ step.title }}
          </h3>
          <p class="mx-auto mt-2 max-w-xs text-site-muted">{{ step.body }}</p>
        </BaseReveal>
      </ol>

      <h3 class="mt-20 text-center text-title-lg font-extrabold text-site-heading">{{ t("capabilities.operations.routesTitle") }}</h3>
      <ul class="mt-8 grid gap-6 md:grid-cols-3">
        <BaseReveal v-for="(stream, i) in wasteStreams" :key="stream.id" as="li" :delay="i * 100">
          <BaseCard class="h-full overflow-hidden">
            <span class="block h-2" :style="{ backgroundColor: stream.color }" aria-hidden="true" />
            <!-- The stream's own truck, in its colour (operation file pp. 48–50). -->
            <div class="px-3 pt-3">
              <LandingPhoto
                :slug="`route-${stream.id}`"
                :alt="`${t('capabilities.operations.routeTruck')} ${t(`about.streams.items.${stream.id}.name`)}`"
              />
            </div>
            <div class="p-6 pt-4">
              <h4 class="font-extrabold text-site-heading">{{ t(`about.streams.items.${stream.id}.name`) }}</h4>
              <p class="mt-2 text-caption text-site-muted">{{ t(`about.streams.items.${stream.id}.examples`) }}</p>
              <ul class="mt-5 space-y-2 border-t border-site-line pt-4 text-caption text-site-text">
                <li class="flex items-center gap-2">
                  <LucideTruck class="size-4 shrink-0" :style="{ color: stream.color }" aria-hidden="true" />
                  {{ t("capabilities.operations.routeCrew") }}
                </li>
                <li class="flex items-center gap-2">
                  <LucideClock class="size-4 shrink-0" :style="{ color: stream.color }" aria-hidden="true" />
                  {{ t("capabilities.operations.routeHours") }}
                </li>
              </ul>
            </div>
          </BaseCard>
        </BaseReveal>
      </ul>

      <BaseReveal class="mt-8 flex gap-4 rounded-3xl border-s-4 border-brand-red bg-site-bg p-6 shadow-card">
        <LucideMoonStar class="mt-1 size-7 shrink-0 text-brand-red" aria-hidden="true" />
        <div>
          <h4 class="font-extrabold text-site-heading">{{ t("capabilities.operations.seasonal.title") }}</h4>
          <p class="mt-1.5 text-site-muted">{{ t("capabilities.operations.seasonal.body") }}</p>
        </div>
      </BaseReveal>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { computed } from "vue"
import { useI18n } from "vue-i18n"
import LucideClock from "~icons/lucide/clock"
import LucideCpu from "~icons/lucide/cpu"
import LucideMoonStar from "~icons/lucide/moon-star"
import LucideTrash2 from "~icons/lucide/trash-2"
import LucideTruck from "~icons/lucide/truck"

import BaseCard from "@/components/base/BaseCard.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionHeading from "@/components/base/BaseSectionHeading.vue"
import LandingPhoto from "@/components/landing/LandingPhoto.vue"
import { useMessageList } from "@/composables/useMessageList"
import { wasteStreams } from "@/config/site"

/** One icon per stage in capabilities.operations.steps, as on the operation file's page. */
const STEP_ICONS = [LucideTrash2, LucideTruck, LucideCpu]

const { t } = useI18n()
const { list } = useMessageList()
const steps = computed(() => {
	const bodies = list("capabilities.operations.steps", "body")
	return list("capabilities.operations.steps", "title").map((title, i) => ({
		title,
		body: bodies[i],
	}))
})
</script>
