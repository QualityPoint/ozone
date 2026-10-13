<template>
  <section id="camp" class="section py-20">
    <BaseSectionHeading
      :tag="t('capabilities.sections.camp')"
      :title="t('capabilities.camp.title')"
      :intro="t('capabilities.camp.intro')"
    />

    <ul class="mt-14 grid gap-5 sm:grid-cols-2 lg:grid-cols-5">
      <BaseReveal v-for="(id, i) in FACILITIES" :key="id" as="li" :delay="(i % 5) * 70">
        <BaseCard class="h-full p-5">
          <span class="grid size-11 place-items-center rounded-xl bg-site-tint text-brand-green dark:text-brand-leaf">
            <component :is="ICONS[id]" class="size-6" aria-hidden="true" />
          </span>
          <h3 class="mt-4 font-extrabold text-site-heading">{{ t(`capabilities.camp.items.${id}.title`) }}</h3>
          <p class="mt-1.5 text-caption text-site-muted">{{ t(`capabilities.camp.items.${id}.body`) }}</p>
        </BaseCard>
      </BaseReveal>
    </ul>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideBuilding from "~icons/lucide/building"
import LucideContainer from "~icons/lucide/container"
import LucideDroplets from "~icons/lucide/droplets"
import LucideFence from "~icons/lucide/fence"
import LucideHammer from "~icons/lucide/hammer"
import LucideMoonStar from "~icons/lucide/moon-star"
import LucidePackage from "~icons/lucide/package"
import LucideShield from "~icons/lucide/shield"
import LucideSquareParking from "~icons/lucide/square-parking"
import LucideWrench from "~icons/lucide/wrench"

import BaseCard from "@/components/base/BaseCard.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionHeading from "@/components/base/BaseSectionHeading.vue"

/** The camp's facilities (capabilities.camp.items), the working ones first. */
const FACILITIES = [
	"workshop",
	"smithy",
	"wash",
	"containers",
	"parking",
	"store",
	"offices",
	"security",
	"mosque",
	"fence",
] as const

const ICONS = {
	workshop: LucideWrench,
	smithy: LucideHammer,
	wash: LucideDroplets,
	containers: LucideContainer,
	parking: LucideSquareParking,
	store: LucidePackage,
	offices: LucideBuilding,
	security: LucideShield,
	mosque: LucideMoonStar,
	fence: LucideFence,
} satisfies Record<(typeof FACILITIES)[number], unknown>

const { t } = useI18n()
</script>
