<template>
  <!-- One stage of the producer's journey on the overview (facility, request, quotation, contract): its
       place in the journey, how many records its page lists (counting up), and the latest one with its
       status. The whole card opens the page. -->
  <RouterLink
    :to="to"
    class="group flex h-full flex-col gap-3 rounded-3xl border border-site-line/70 bg-site-bg p-4 shadow-card sm:p-5 transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf motion-safe:hover:-translate-y-1"
  >
    <div class="flex items-center justify-between">
      <span class="grid size-10 place-items-center rounded-2xl sm:size-11 bg-site-hover text-brand-green transition group-hover:bg-brand-green group-hover:text-white dark:text-brand-leaf">
        <component :is="icon" class="size-5" aria-hidden="true" />
      </span>
      <span class="text-label font-extrabold text-site-muted" dir="ltr">{{ String(step).padStart(2, "0") }}</span>
    </div>
    <p class="text-heading font-extrabold leading-none text-site-heading sm:text-display">{{ formatNumber(shown) }}</p>
    <p class="font-extrabold text-site-heading">{{ label }}</p>
    <div class="mt-auto min-w-0 space-y-2 text-caption">
      <template v-if="latest">
        <p class="line-clamp-2 text-site-muted">
          {{ latest.title }}<template v-if="latest.detail"> · {{ latest.detail }}</template>
        </p>
        <span
          v-if="latest.status_label || status"
          :class="['inline-flex rounded-full px-3 py-0.5 text-label font-bold', latest.status_label ? statusBadge(latest.status_color) : 'bg-site-hover text-site-heading']"
        >
          {{ latest.status_label || status }}
        </span>
      </template>
      <p v-else class="text-site-muted">{{ empty }}</p>
    </div>
  </RouterLink>
</template>

<script lang="ts" setup>
import { type Component, ref } from "vue"
import type { RouteLocationRaw } from "vue-router"

import { useCountUp } from "@/composables/useCountUp"
import type { Stage } from "@/services/portal"
import { formatNumber } from "@/utils/format"
import { statusBadge } from "@/utils/status"

const props = defineProps<{
	to: RouteLocationRaw
	icon: Component
	/** Its place in the journey, from 1. */
	step: number
	count: number
	label: string
	latest: Stage | null
	/** What it says with nothing in it yet. */
	empty: string
	/** The latest one's status when it has none of its own (a contract being prepared). */
	status?: string
}>()

const shown = useCountUp(() => props.count, ref(true), 900)
</script>
