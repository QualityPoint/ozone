<template>
  <section id="services" class="section py-20">
    <BaseSectionHeading :tag="t('nav.services')" :title="t('services.title')" :intro="t('services.intro')" />

    <ul class="mt-14 grid gap-6 md:grid-cols-3">
      <BaseReveal v-for="(id, i) in serviceIds" :key="id" as="li" :delay="i * 100">
        <BaseCard class="group h-full p-7 transition motion-safe:hover:-translate-y-1">
          <span class="grid size-14 place-items-center rounded-2xl bg-brand-green text-white transition group-hover:bg-brand-red">
            <component :is="ICONS[id]" class="size-7" aria-hidden="true" />
          </span>
          <h3 class="mt-5 text-title font-extrabold text-site-heading">{{ t(`services.items.${id}.title`) }}</h3>
          <ul class="mt-4 space-y-2.5 text-site-muted">
            <li v-for="point in list(`services.items.${id}.points`)" :key="point" class="flex gap-2.5">
              <span class="mt-2.5 size-1.5 shrink-0 rounded-full bg-brand-red" aria-hidden="true" />
              <span>{{ point }}</span>
            </li>
          </ul>
        </BaseCard>
      </BaseReveal>
    </ul>
  </section>
</template>

<script lang="ts" setup>
import type { Component } from "vue"
import { useI18n } from "vue-i18n"
import LucideClipboardCheck from "~icons/lucide/clipboard-check"
import LucideRecycle from "~icons/lucide/recycle"
import LucideTruck from "~icons/lucide/truck"

import BaseCard from "@/components/base/BaseCard.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionHeading from "@/components/base/BaseSectionHeading.vue"
import { useMessageList } from "@/composables/useMessageList"
import { serviceIds } from "@/config/site"
import type { ServiceId } from "@/types"

const ICONS: Record<ServiceId, Component> = {
	collection: LucideTruck,
	environmental: LucideClipboardCheck,
	recycling: LucideRecycle,
}

const { t } = useI18n()
const { list } = useMessageList()
</script>
