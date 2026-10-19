<template>
  <!-- AI calibration (the presentation, pp. 54-57), as a story over a year of operation: the
       calculator's theoretical estimate (dashed), what the trucks weighed each month (dots), and
       the AI-calibrated estimate (the line) closing in on them, the gap between estimate and
       reality (shaded) shrinking. Time runs right to left in Arabic, as in the presentation.
       Moves once in view (styles below); still with reduced motion. Illustrative values
       (utils/calibration.ts). -->
  <figure ref="root" :class="{ revealed }">
    <div class="flex flex-wrap items-center justify-between gap-2">
      <span class="inline-flex items-center gap-2 rounded-full bg-site-hover px-3 py-1 text-caption font-extrabold text-site-heading">
        {{ t("naqel.operations.ai.gap") }}
        <span class="inline-flex items-center gap-1.5">
          <span class="text-site-muted line-through decoration-2">{{ gapBefore }}%</span>
          <LucideArrowRight class="size-3.5 text-naqel-green rtl:-scale-x-100" aria-hidden="true" />
          <span class="text-naqel-green-700 dark:text-naqel-green-300">{{ gapAfter }}%</span>
        </span>
      </span>
      <span class="text-label text-site-muted">{{ t("naqel.operations.ai.illustration") }}</span>
    </div>

    <svg viewBox="0 0 340 170" class="mt-3 w-full overflow-visible" aria-hidden="true">
      <line v-for="v in GRID" :key="v" :x1="LEFT" :x2="RIGHT" :y1="y(v)" :y2="y(v)" class="stroke-site-line" stroke-width="1" />
      <!-- The gap between the calibrated estimate and the actual rate. -->
      <polygon :points="gapArea" class="gap fill-naqel-green" fill-opacity="0.14" />
      <!-- The theoretical estimate: flat, from the calculator. -->
      <line :x1="LEFT" :x2="RIGHT" :y1="y(THEORETICAL)" :y2="y(THEORETICAL)" class="stroke-site-muted" stroke-width="2" stroke-dasharray="5 5" />
      <!-- The AI-calibrated estimate. -->
      <polyline :points="calibratedLine" fill="none" class="calibrated stroke-naqel-green" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" pathLength="1" />
      <!-- What the trucks weighed, month by month. -->
      <circle
        v-for="(value, month) in WEIGHED"
        :key="month"
        :cx="x(month)"
        :cy="y(value)"
        r="4"
        class="dot fill-site-bg stroke-naqel-night dark:stroke-white"
        stroke-width="2"
        :style="{ '--i': month }"
      />
      <text v-for="month in LABELLED" :key="month" :x="x(month)" y="168" text-anchor="middle" class="fill-site-muted text-[12px] font-bold">
        {{ formatMonth(month, current) }}
      </text>
    </svg>

    <ul class="mt-3 flex flex-wrap gap-x-5 gap-y-1.5 text-caption">
      <li class="flex items-center gap-2 text-site-muted"><span class="w-5 border-t-2 border-dashed border-site-muted" />{{ t("naqel.operations.ai.theoretical") }}</li>
      <li class="flex items-center gap-2 text-site-text"><span class="size-2.5 rounded-full border-2 border-naqel-night dark:border-white" />{{ t("naqel.operations.ai.weighed") }}</li>
      <li class="flex items-center gap-2 font-bold text-site-heading"><span class="w-5 border-t-[3px] border-naqel-green" />{{ t("naqel.operations.ai.calibrated") }}</li>
    </ul>

    <!-- How: the weighings feed the AI, which updates the generation rate. -->
    <ol class="mt-5 grid grid-cols-[1fr_auto_1fr_auto_1fr] items-center gap-2 border-t border-site-line pt-5">
      <template v-for="(icon, i) in STEP_ICONS" :key="i">
        <li class="flex flex-col items-center gap-1.5 text-center">
          <span class="grid size-10 place-items-center rounded-xl bg-site-hover text-naqel-green-700 dark:text-naqel-green-300">
            <component :is="icon" class="size-5" aria-hidden="true" />
          </span>
          <span class="text-label font-extrabold text-site-heading sm:text-caption">{{ steps[i] }}</span>
        </li>
        <LucideChevronRight v-if="i < STEP_ICONS.length - 1" class="size-4 text-site-muted rtl:-scale-x-100" aria-hidden="true" />
      </template>
    </ol>
  </figure>
</template>

<script lang="ts" setup>
import { computed, ref } from "vue"
import { useI18n } from "vue-i18n"
import LucideArrowRight from "~icons/lucide/arrow-right"
import LucideBrainCircuit from "~icons/lucide/brain-circuit"
import LucideChevronRight from "~icons/lucide/chevron-right"
import LucideRefreshCw from "~icons/lucide/refresh-cw"
import LucideWeight from "~icons/lucide/weight"

import { useLocale } from "@/composables/useLocale"
import { useMessageList } from "@/composables/useMessageList"
import { useReveal } from "@/composables/useReveal"
import { naqelRevealThreshold } from "@/config/naqel"
import {
	THEORETICAL,
	WEIGHED,
	actualRate,
	calibrated,
	gapPercent,
} from "@/utils/calibration"
import { formatMonth } from "@/utils/format"

/** The plot's edges in the viewBox, and its value range (m³ a day). */
const LEFT = 24
const RIGHT = 324
const TOP = 12
const BOTTOM = 150
const MIN = 0.27
const MAX = 0.5
/** Grid lines, and the months named under the axis. */
const GRID = [0.3, 0.4, 0.5]
const LABELLED = [0, 3, 6, 9]

/** One icon per step in operations.ai.steps. */
const STEP_ICONS = [LucideWeight, LucideBrainCircuit, LucideRefreshCw]

const { t } = useI18n()
const { list } = useMessageList()
const { current, rtl } = useLocale()

const root = ref<HTMLElement | null>(null)
const revealed = useReveal(root, naqelRevealThreshold)

const steps = computed(() => list("naqel.operations.ai.steps"))

/** A month's place on the time axis: January at the start side (the right in Arabic). */
function x(month: number): number {
	const step = (RIGHT - LEFT) / (WEIGHED.length - 1)
	return rtl.value ? RIGHT - month * step : LEFT + month * step
}
const y = (value: number) =>
	BOTTOM - ((value - MIN) / (MAX - MIN)) * (BOTTOM - TOP)

const estimate = calibrated()
const actual = actualRate()
const gapBefore = gapPercent(estimate[0], actual)
const gapAfter = gapPercent(estimate[estimate.length - 1], actual)

const calibratedLine = computed(() =>
	estimate.map((value, month) => `${x(month)},${y(value)}`).join(" "),
)
/** The band between the calibrated estimate and the actual rate. */
const gapArea = computed(() =>
	[
		...estimate.map((value, month) => `${x(month)},${y(value)}`),
		...estimate.map((_, month) => `${x(month)},${y(actual)}`).reverse(),
	].join(" "),
)
</script>

<style scoped>
@media (prefers-reduced-motion: no-preference) {
	/* The weighings come in month by month, the calibrated line follows them, and the gap fills in
	   behind it. */
	.dot {
		opacity: 0;
		transition: opacity 0.3s ease-out;
		transition-delay: calc(var(--i) * 0.16s);
	}
	.revealed .dot {
		opacity: 1;
	}
	.calibrated {
		stroke-dasharray: 1;
		stroke-dashoffset: 1;
		transition: stroke-dashoffset 2s ease-in-out 0.3s;
	}
	.revealed .calibrated {
		stroke-dashoffset: 0;
	}
	.gap {
		opacity: 0;
		transition: opacity 0.8s ease-out 1.8s;
	}
	.revealed .gap {
		opacity: 1;
	}
}
</style>
