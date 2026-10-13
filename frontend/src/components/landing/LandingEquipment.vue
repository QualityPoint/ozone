<template>
  <section id="equipment" class="bg-site-tint py-20">
    <div class="section">
      <BaseSectionHeading :tag="t('equipment.tag')" :title="t('equipment.title')" :intro="t('equipment.intro')" />

      <div v-for="group in GROUPS" :key="group" class="mt-14">
        <BasePill variant="solid">{{ t(`equipment.${group}`) }}</BasePill>
        <ul class="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <BaseReveal v-for="(item, i) in equipment[group]" :key="item.slug" as="li" :delay="i * 80">
            <LandingPhotoCard
              :slug="item.slug"
              :name="t(`equipment.items.${item.slug}.name`)"
              :body="t(`equipment.items.${item.slug}.body`)"
            />
          </BaseReveal>
        </ul>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"

import BasePill from "@/components/base/BasePill.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionHeading from "@/components/base/BaseSectionHeading.vue"
import { equipment } from "@/config/site"
import LandingPhotoCard from "./LandingPhotoCard.vue"

const GROUPS = ["fleet", "containers"] as const

const { t } = useI18n()
</script>
