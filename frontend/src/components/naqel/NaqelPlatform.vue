<template>
  <section id="platform" class="overflow-x-clip py-16 sm:py-20">
    <NaqelSectionHeading :title="t('naqel.platform.title')" :intro="t('naqel.platform.intro')" />

    <div class="section mt-10">
      <!-- The two parties, the transporter on the start side and the producer on the end side, and
           what passes between them in the middle: arrows point the way each exchange goes (sideways,
           mirrored in Arabic; up and down on phones, where the cards stack). -->
      <div class="grid gap-4 md:grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] md:gap-6">
        <NaqelHeaderCard
          v-for="(side, s) in SIDES"
          :key="side.id"
          as="article"
          :title="t(`naqel.platform.sides.${side.id}.title`)"
          :term="current === 'en' ? undefined : t(`naqel.platform.sides.${side.id}.term`)"
          :tone="s ? 'ink' : 'green'"
          :class="s ? 'order-3' : 'order-1'"
        >
          <template #icon>
            <component :is="side.icon" class="size-6" aria-hidden="true" />
          </template>
          <div class="text-start font-normal">
            <p class="font-bold text-site-heading">{{ t(`naqel.platform.sides.${side.id}.who`) }}</p>
            <NaqelCheckList :items="list(`naqel.platform.sides.${side.id}.points`)" class="mt-4 text-caption text-site-text" />
          </div>
        </NaqelHeaderCard>

        <ol class="order-2 grid grid-cols-2 gap-3 md:flex md:flex-col md:justify-center">
          <li v-for="item in EXCHANGE" :key="item.id" class="flex flex-col items-center gap-1 text-center">
            <span class="text-caption font-extrabold text-site-heading">{{ t(`naqel.platform.exchange.${item.id}`) }}</span>
            <span class="grid h-8 w-24 place-items-center rounded-full bg-site-hover text-naqel-green-700 dark:text-naqel-green-300">
              <component :is="ARROWS[item.to].wide" class="hidden size-5 rtl:-scale-x-100 md:block" aria-hidden="true" />
              <component :is="ARROWS[item.to].stacked" class="size-5 md:hidden" aria-hidden="true" />
            </span>
          </li>
        </ol>
      </div>

      <div class="mt-16 grid items-center gap-10 lg:grid-cols-[1.2fr_1fr]">
        <div>
          <h3 class="flex items-center gap-2 text-title-lg font-extrabold text-site-heading">
            <NaqelCorner class="size-5 text-naqel-green" />
            {{ t("naqel.platform.foundationTitle") }}
          </h3>
          <ul class="mt-6 grid gap-5 sm:grid-cols-2">
            <li v-for="(icon, id) in FOUNDATION" :key="id" class="flex gap-4">
              <span class="grid size-11 shrink-0 place-items-center rounded-xl bg-site-hover text-naqel-green-700 dark:text-naqel-green-300">
                <component :is="icon" class="size-5" aria-hidden="true" />
              </span>
              <div>
                <h4 class="font-extrabold text-site-heading">{{ t(`naqel.platform.foundation.${id}.title`) }}</h4>
                <p class="mt-1 text-caption text-site-muted">{{ t(`naqel.platform.foundation.${id}.body`) }}</p>
              </div>
            </li>
          </ul>
        </div>
        <!-- The platform's apps, as its apps screen shows them: naqel's own Desk icons. -->
        <NaqelCard class="p-6">
          <h3 class="text-center font-extrabold text-site-heading">{{ t("naqel.platform.modulesTitle") }}</h3>
          <ul class="mt-5 grid grid-cols-3 gap-3">
            <li v-for="module in platformModules" :key="module.id" class="flex flex-col items-center gap-2 rounded-xl bg-site-tint px-2 py-4 text-center">
              <span class="grid size-12 place-items-center rounded-xl bg-site-bg shadow-naqel-card">
                <NaqelIcon :name="module.icon" class="size-7" />
              </span>
              <span class="text-caption font-bold text-site-heading">{{ t(`naqel.platform.modules.${module.id}`) }}</span>
            </li>
          </ul>
        </NaqelCard>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideArrowDown from "~icons/lucide/arrow-down"
import LucideArrowLeft from "~icons/lucide/arrow-left"
import LucideArrowLeftRight from "~icons/lucide/arrow-left-right"
import LucideArrowRight from "~icons/lucide/arrow-right"
import LucideArrowUp from "~icons/lucide/arrow-up"
import LucideArrowUpDown from "~icons/lucide/arrow-up-down"
import LucideBlocks from "~icons/lucide/blocks"
import LucideBrainCircuit from "~icons/lucide/brain-circuit"
import LucideBuilding2 from "~icons/lucide/building-2"
import LucideCable from "~icons/lucide/cable"
import LucideMegaphone from "~icons/lucide/megaphone"
import LucideShieldCheck from "~icons/lucide/shield-check"
import LucideTruck from "~icons/lucide/truck"

import NaqelCard from "@/components/naqel/base/NaqelCard.vue"
import NaqelCheckList from "@/components/naqel/base/NaqelCheckList.vue"
import NaqelHeaderCard from "@/components/naqel/base/NaqelHeaderCard.vue"
import NaqelSectionHeading from "@/components/naqel/base/NaqelSectionHeading.vue"
import NaqelCorner from "@/components/naqel/brand/NaqelCorner.vue"
import NaqelIcon from "@/components/naqel/brand/NaqelIcon.vue"
import { useLocale } from "@/composables/useLocale"
import { useMessageList } from "@/composables/useMessageList"
import { platformModules } from "@/config/naqel"

/** The platform's two parties (platform.sides): the transporter, then the producer. */
const SIDES = [
	{ id: "transporter", icon: LucideTruck },
	{ id: "producer", icon: LucideBuilding2 },
] as const

/** What passes between them (platform.exchange), and which way it goes. */
const EXCHANGE = [
	{ id: "request", to: "transporter" },
	{ id: "quotation", to: "producer" },
	{ id: "contract", to: "both" },
	{ id: "service", to: "producer" },
] as const

/**
 * The arrow for each way, side by side (the transporter on the start side: in English, the
 * left; the icons mirror in Arabic) and stacked on phones (the transporter above).
 */
const ARROWS = {
	producer: { wide: LucideArrowRight, stacked: LucideArrowDown },
	transporter: { wide: LucideArrowLeft, stacked: LucideArrowUp },
	both: { wide: LucideArrowLeftRight, stacked: LucideArrowUpDown },
}

/** The platform's foundations (platform.foundation), with their icons. */
const FOUNDATION = {
	framework: LucideShieldCheck,
	integration: LucideCable,
	ai: LucideBrainCircuit,
	saas: LucideBlocks,
	awareness: LucideMegaphone,
}

const { t } = useI18n()
const { current } = useLocale()
const { list } = useMessageList()
</script>
