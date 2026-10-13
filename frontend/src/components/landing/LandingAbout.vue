<template>
  <section id="about" class="section py-20">
    <BaseSectionHeading :tag="t('nav.about')" :title="t('about.title')" :intro="t('about.intro')" />

    <div class="mt-14 grid items-start gap-10 lg:grid-cols-[1.4fr_1fr]">
      <div>
        <h3 class="text-title-lg font-extrabold text-site-heading">{{ t("about.goalsTitle") }}</h3>
        <ul class="mt-6 grid gap-4 sm:grid-cols-3">
          <BaseReveal v-for="(goal, i) in goals" :key="goal.title" as="li" :delay="i * 100">
            <BaseCard class="h-full p-6">
              <component :is="ICONS[i]" class="size-8 text-brand-red" aria-hidden="true" />
              <h4 class="mt-4 font-extrabold text-site-heading">{{ goal.title }}</h4>
              <p class="mt-2 text-caption text-site-muted">{{ goal.body }}</p>
            </BaseCard>
          </BaseReveal>
        </ul>

        <BaseReveal class="mt-8 rounded-3xl bg-site-tint p-6">
          <BasePill variant="accent" size="sm">{{ t("about.visionTitle") }}</BasePill>
          <p class="mt-4 text-title font-bold text-site-heading">«{{ t("about.vision") }}»</p>
        </BaseReveal>
      </div>

      <BaseReveal :delay="150">
        <BaseCard class="p-6">
          <LandingStreams />
        </BaseCard>
      </BaseReveal>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { computed } from "vue"
import { useI18n } from "vue-i18n"
import LucideGauge from "~icons/lucide/gauge"
import LucideHandshake from "~icons/lucide/handshake"
import LucideLightbulb from "~icons/lucide/lightbulb"

import BaseCard from "@/components/base/BaseCard.vue"
import BasePill from "@/components/base/BasePill.vue"
import BaseReveal from "@/components/base/BaseReveal.vue"
import BaseSectionHeading from "@/components/base/BaseSectionHeading.vue"
import { useMessageList } from "@/composables/useMessageList"
import LandingStreams from "./LandingStreams.vue"

/** One icon per goal in about.goals, same order. */
const ICONS = [LucideGauge, LucideHandshake, LucideLightbulb]

const { t } = useI18n()
const { list } = useMessageList()
const goals = computed(() => {
	const bodies = list("about.goals", "body")
	return list("about.goals", "title").map((title, i) => ({
		title,
		body: bodies[i],
	}))
})
</script>
