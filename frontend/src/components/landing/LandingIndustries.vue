<template>
  <section id="industries" class="section py-20">
    <BaseSectionHeading :tag="t('nav.industries')" :title="t('industries.title')" :intro="t('industries.intro')" />

    <ul class="mt-14 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
      <BaseReveal v-for="(id, i) in industryIds" :key="id" as="li" :delay="i * 90">
        <BaseCard class="group h-full p-6 text-center transition motion-safe:hover:-translate-y-1">
          <span class="mx-auto grid size-16 place-items-center rounded-full border-2 border-brand-green text-brand-green transition group-hover:border-brand-red group-hover:text-brand-red dark:border-brand-leaf dark:text-brand-leaf">
            <component :is="ICONS[id]" class="size-7" aria-hidden="true" />
          </span>
          <h3 class="mt-4 font-extrabold text-site-heading">{{ t(`industries.items.${id}.title`) }}</h3>
          <p class="mt-2 text-caption text-site-muted">{{ t(`industries.items.${id}.body`) }}</p>
        </BaseCard>
      </BaseReveal>
    </ul>
  </section>
</template>

<script lang="ts" setup>
import type { Component } from "vue"
import { useI18n } from "vue-i18n"
import LucideFactory from "~icons/lucide/factory"
import LucideHouse from "~icons/lucide/house"
import LucideLandmark from "~icons/lucide/landmark"
import LucideStore from "~icons/lucide/store"

import BaseCard from "@/components/base/BaseCard.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionHeading from "@/components/base/BaseSectionHeading.vue"
import { industryIds } from "@/config/site"
import type { IndustryId } from "@/types"

const ICONS: Record<IndustryId, Component> = {
	commercial: LucideStore,
	industrial: LucideFactory,
	government: LucideLandmark,
	residential: LucideHouse,
}

const { t } = useI18n()
</script>
