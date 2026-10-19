<template>
  <section id="operations" class="overflow-x-clip bg-site-tint py-16 sm:py-20">
    <NaqelSectionHeading :title="t('naqel.operations.title')" :intro="t('naqel.operations.intro')" />

    <div class="section mt-10">
      <ul class="grid gap-6 md:grid-cols-3">
        <li v-for="(icon, id) in IOT" :key="id">
          <NaqelHeaderCard as="article" :title="t(`naqel.operations.iot.${id}.title`)" class="h-full">
            <template #icon>
              <component :is="icon" class="size-6" aria-hidden="true" />
            </template>
            <span class="font-normal text-site-text">{{ t(`naqel.operations.iot.${id}.body`) }}</span>
          </NaqelHeaderCard>
        </li>
      </ul>

      <!-- The devices on every compactor, around the truck as in the presentation. -->
      <h3 class="mt-14 flex items-center gap-2 text-title-lg font-extrabold text-site-heading">
        <NaqelCorner class="size-5 text-naqel-green" />
        {{ t("naqel.operations.devicesTitle") }}
      </h3>
      <NaqelCompactorDiagram class="mt-8" />

      <!-- Two columns of the same height: each a pill heading over a card that fills the rest. -->
      <div class="mt-14 grid gap-10 lg:grid-cols-2">
        <div class="flex flex-col">
          <NaqelPillHeading>{{ t("naqel.operations.dashboardTitle") }}</NaqelPillHeading>
          <!-- What the operations dashboard shows, each with its icon: equal rows that fill the card,
               divided by thin lines. -->
          <NaqelCard class="mt-5 flex-1 p-5">
            <ul class="flex h-full flex-col divide-y divide-site-line">
              <li v-for="(item, i) in list('naqel.operations.dashboard')" :key="item" class="flex flex-1 items-center gap-4 py-3 first:pt-0 last:pb-0">
                <span class="grid size-12 shrink-0 place-items-center rounded-xl bg-site-hover text-naqel-green-700 dark:text-naqel-green-300">
                  <component :is="DASHBOARD_ICONS[i]" class="size-6" aria-hidden="true" />
                </span>
                <span class="text-site-text">{{ item }}</span>
              </li>
            </ul>
          </NaqelCard>
        </div>

        <!-- AI calibration: its story as a chart (NaqelCalibrationChart). -->
        <div class="flex flex-col">
          <NaqelPillHeading tone="ink">{{ t("naqel.operations.ai.title") }}</NaqelPillHeading>
          <NaqelCard class="mt-5 flex-1 p-5">
            <p class="text-site-text">{{ t("naqel.operations.ai.body") }}</p>
            <NaqelCalibrationChart class="mt-5" />
          </NaqelCard>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideBellRing from "~icons/lucide/bell-ring"
import LucideContainer from "~icons/lucide/container"
import LucideLink from "~icons/lucide/link"
import LucideMap from "~icons/lucide/map"
import LucideMapPinned from "~icons/lucide/map-pinned"
import LucideRoute from "~icons/lucide/route"
import LucideUsers from "~icons/lucide/users"
import LucideWeight from "~icons/lucide/weight"

import NaqelCard from "@/components/naqel/base/NaqelCard.vue"
import NaqelHeaderCard from "@/components/naqel/base/NaqelHeaderCard.vue"
import NaqelPillHeading from "@/components/naqel/base/NaqelPillHeading.vue"
import NaqelSectionHeading from "@/components/naqel/base/NaqelSectionHeading.vue"
import NaqelCorner from "@/components/naqel/brand/NaqelCorner.vue"
import { useMessageList } from "@/composables/useMessageList"
import NaqelCalibrationChart from "./NaqelCalibrationChart.vue"
import NaqelCompactorDiagram from "./NaqelCompactorDiagram.vue"

/** The three IoT capabilities (operations.iot), as in the presentation. */
const IOT = {
	gps: LucideMapPinned,
	weighing: LucideWeight,
	attribution: LucideLink,
}

/** One icon per item in operations.dashboard, same order: vehicles, routes, containers, drivers, reports. */
const DASHBOARD_ICONS = [
	LucideMap,
	LucideRoute,
	LucideContainer,
	LucideUsers,
	LucideBellRing,
]

const { t } = useI18n()
const { list } = useMessageList()
</script>
