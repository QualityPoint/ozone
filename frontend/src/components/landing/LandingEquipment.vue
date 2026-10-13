<template>
  <section id="equipment" class="bg-site-tint py-20">
    <div class="section">
      <BaseSectionHeading :tag="t('equipment.tag')" :title="t('equipment.title')" :intro="t('equipment.intro')" />

      <div v-for="group in GROUPS" :key="group" class="mt-14">
        <BasePill variant="solid">{{ t(`equipment.${group}`) }}</BasePill>
        <ul class="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <BaseReveal v-for="(item, i) in equipment[group]" :key="item.slug" as="li" :delay="i * 80">
            <BaseCard class="group h-full overflow-hidden p-3">
              <LandingPhoto
                :slug="item.slug"
                :alt="t(`equipment.items.${item.slug}.name`)"
                class="transition duration-500 motion-safe:group-hover:scale-[1.03]"
              />
              <div class="px-3 pb-3 pt-4">
                <h3 class="font-extrabold text-site-heading">{{ t(`equipment.items.${item.slug}.name`) }}</h3>
                <p class="mt-1.5 text-caption text-site-muted">{{ t(`equipment.items.${item.slug}.body`) }}</p>
              </div>
            </BaseCard>
          </BaseReveal>
        </ul>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"

import BaseCard from "@/components/base/BaseCard.vue"
import BasePill from "@/components/base/BasePill.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionHeading from "@/components/base/BaseSectionHeading.vue"
import { equipment } from "@/config/site"
import LandingPhoto from "./LandingPhoto.vue"

const GROUPS = ["fleet", "containers"] as const

const { t } = useI18n()
</script>
