<template>
  <section id="teams" class="bg-site-tint py-20">
    <div class="section">
      <BaseSectionHeading
        :tag="t('capabilities.sections.teams')"
        :title="t('capabilities.teams.title')"
        :intro="t('capabilities.teams.intro')"
      />

      <div class="mt-14 grid items-start gap-10 lg:grid-cols-[1.4fr_1fr]">
        <!-- The camp's organisation chart, as in the operation file: the administrative manager,
             then the camp manager and the maintenance supervisor, then the specialists. -->
        <figure>
          <figcaption class="mb-5 text-title font-extrabold text-site-heading">{{ t("capabilities.teams.structureTitle") }}</figcaption>
          <ol class="space-y-4">
            <li v-for="(tier, level) in TIERS" :key="level" :class="['grid gap-4', COLUMNS[tier.length]]">
              <BaseReveal v-for="id in tier" :key="id" :delay="level * 120" :class="['rounded-2xl p-4', LEVEL_STYLES[level]]">
                <p class="font-extrabold">{{ t(`capabilities.teams.roles.${id}.title`) }}</p>
                <p class="mt-1 text-caption opacity-90">{{ t(`capabilities.teams.roles.${id}.body`) }}</p>
              </BaseReveal>
            </li>
          </ol>
        </figure>

        <div class="space-y-6">
          <BaseCard class="p-6">
            <h3 class="text-title font-extrabold text-site-heading">{{ t("capabilities.teams.fieldTitle") }}</h3>
            <BaseCheckList :items="list('capabilities.teams.field')" class="mt-5 text-site-text" />
          </BaseCard>
          <BaseCard as="figure" class="overflow-hidden p-3">
            <LandingPhoto slug="safety-gear" :alt="t('capabilities.teams.gear')" />
            <figcaption class="px-3 pb-2 pt-3 text-caption font-bold text-site-heading">{{ t("capabilities.teams.gear") }}</figcaption>
          </BaseCard>
        </div>
      </div>

      <BasePill variant="solid" class="mt-16">{{ t("capabilities.teams.vehiclesTitle") }}</BasePill>
      <ul class="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <BaseReveal v-for="(item, i) in supportFleet" :key="item.slug" as="li" :delay="i * 80">
          <LandingPhotoCard
            :slug="item.slug"
            :name="t(`capabilities.teams.vehicles.${item.slug}.name`)"
            :body="t(`capabilities.teams.vehicles.${item.slug}.body`)"
          />
        </BaseReveal>
      </ul>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"

import BaseCard from "@/components/base/BaseCard.vue"
import BaseCheckList from "@/components/base/BaseCheckList.vue"
import BasePill from "@/components/base/BasePill.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionHeading from "@/components/base/BaseSectionHeading.vue"
import LandingPhoto from "@/components/landing/LandingPhoto.vue"
import LandingPhotoCard from "@/components/landing/LandingPhotoCard.vue"
import { useMessageList } from "@/composables/useMessageList"
import { supportFleet } from "@/config/site"

/** The chart's levels, top down (capabilities.teams.roles). */
const TIERS = [
	["admin"],
	["camp", "maintenance"],
	["stores", "vehicleTechs", "containerTechs"],
] as const

/** Each level a step lighter, as the operation file's chart: deep green, leaf green, then outlined. */
const LEVEL_STYLES = [
	"bg-brand-green text-white",
	"bg-brand-leaf-700 text-white",
	"border-2 border-brand-green/30 bg-site-bg text-site-heading dark:border-brand-leaf/30",
]

/** The grid for a level with 1, 2 or 3 roles. */
const COLUMNS: Record<number, string> = {
	1: "grid-cols-1",
	2: "sm:grid-cols-2",
	3: "sm:grid-cols-3",
}

const { t } = useI18n()
const { list } = useMessageList()
</script>
