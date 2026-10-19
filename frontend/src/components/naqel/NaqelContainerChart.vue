<template>
  <!-- The presentation's chart of inferred containers (p. 35): each container at its capacity on
       the generation-rate scale, here as a bar per container, largest first. The bars grow from
       the start side, light green to the logo green at their tip; the scale's lines and numbers sit
       under them. Moves (styles below): once in view the bars grow in turn and their values follow,
       then a light runs along them now and then; a row's container lifts its lid while it grows
       and on hover. Still with reduced motion. -->
  <figure ref="root" :class="{ revealed }">
    <ol class="space-y-3">
      <li v-for="(row, i) in rows" :key="row.id" :style="{ '--i': i }" :class="{ lifting: lifting.has(row.id) }" class="chart-row grid grid-cols-[7.5rem_minmax(0,1fr)] items-center gap-3 sm:grid-cols-[9.5rem_minmax(0,1fr)]">
        <span class="flex items-center gap-2.5">
          <NaqelIcon :name="row.id" class="size-8 shrink-0" />
          <span class="text-caption font-extrabold text-site-heading">{{ t(`naqel.calculator.containers.names.${row.id}`) }}</span>
        </span>
        <span class="relative h-9">
          <span v-for="tick in ticks" :key="tick" class="absolute inset-y-0 w-px bg-site-line" :style="{ insetInlineStart: at(tick) }" aria-hidden="true" />
          <span class="bar absolute inset-y-1.5 start-0 overflow-hidden rounded-e-lg from-naqel-green-300 to-naqel-green ltr:bg-gradient-to-r rtl:bg-gradient-to-l" :style="{ width: at(row.capacity) }" aria-hidden="true">
            <span class="glint absolute inset-y-0 w-1/3" />
          </span>
          <span
            :class="['value absolute top-1/2 -translate-y-1/2 whitespace-nowrap text-caption font-extrabold', row.inside ? 'text-white' : 'text-site-heading']"
            :style="row.inside ? { insetInlineEnd: `calc(100% - ${at(row.capacity)} + 0.6rem)` } : { insetInlineStart: `calc(${at(row.capacity)} + 0.5rem)` }"
          >
            <bdi>{{ formatNumber(row.capacity, 2) }}</bdi> {{ t("naqel.calculator.containers.unit") }}
          </span>
        </span>
      </li>
    </ol>
    <!-- The scale under the bars: 0 to 16 m³. -->
    <div class="mt-2 grid grid-cols-[7.5rem_minmax(0,1fr)] gap-3 sm:grid-cols-[9.5rem_minmax(0,1fr)]" aria-hidden="true">
      <span />
      <span class="relative h-5 border-t border-site-line">
        <span
          v-for="tick in ticks"
          :key="tick"
          class="absolute top-1 text-label font-bold text-site-muted ltr:-translate-x-1/2 rtl:translate-x-1/2"
          :style="{ insetInlineStart: at(tick) }"
          >{{ tick }}</span
        >
      </span>
    </div>
    <figcaption class="mt-3 text-end text-caption font-bold text-site-muted">{{ t("naqel.calculator.containers.axis") }}</figcaption>
  </figure>
</template>

<script lang="ts" setup>
import { computed, reactive, ref, watch } from "vue"
import { useI18n } from "vue-i18n"

import NaqelIcon from "@/components/naqel/brand/NaqelIcon.vue"
import { useReveal } from "@/composables/useReveal"
import {
	generationScale,
	inferredContainers,
	naqelRevealThreshold,
} from "@/config/naqel"
import { formatNumber } from "@/utils/format"

const { t } = useI18n()

const root = ref<HTMLElement | null>(null)
const revealed = useReveal(root, naqelRevealThreshold)

/**
 * The rows whose container is lifting its lid: each from the moment its bar starts growing, for
 * LIFT_MS. That ends inside the lid's closed phase (60-100% of the sprite's 1.8 s cycle), so it
 * comes to rest shut. Not with reduced motion.
 */
const LIFT_MS = 1500
const STAGGER_MS = 120
const lifting = reactive(new Set<string>())
watch(revealed, (shown) => {
	if (!shown || matchMedia("(prefers-reduced-motion: reduce)").matches) return
	rows.value.forEach((row, i) => {
		setTimeout(() => lifting.add(row.id), i * STAGGER_MS)
		setTimeout(() => lifting.delete(row.id), i * STAGGER_MS + LIFT_MS)
	})
})

/** The scale's lines: 0, 4, 8, 12, 16. */
const ticks = Array.from(
	{ length: generationScale.max / generationScale.step + 1 },
	(_, i) => i * generationScale.step,
)

/** A value's place along the bar's track, from the start side. */
const at = (value: number) => `${(value / generationScale.max) * 100}%`

/** Largest first, as the presentation stacks them. A long bar carries its value inside. */
const rows = computed(() =>
	[...inferredContainers].reverse().map((container) => ({
		...container,
		inside: container.capacity / generationScale.max > 0.7,
	})),
)
</script>

<style scoped>
/*
 * Motion only for visitors who don't ask for reduced motion; without it everything shows at rest.
 * Rows go top to bottom (`--i`), largest container first.
 */
@media (prefers-reduced-motion: no-preference) {
	/* The bars grow from the start side in turn once the chart is in view. */
	.bar {
		transform: scaleX(0);
		transform-origin: left;
		transition: transform 0.9s cubic-bezier(0.22, 1, 0.36, 1);
		transition-delay: calc(var(--i) * 0.12s);
	}
	:dir(rtl) .bar {
		transform-origin: right;
	}
	.revealed .bar {
		transform: scaleX(1);
	}

	/* Each value fades in as its bar arrives. */
	.value {
		opacity: 0;
		transition: opacity 0.4s ease-out;
		transition-delay: calc(var(--i) * 0.12s + 0.6s);
	}
	.revealed .value {
		opacity: 1;
	}

	/* Then, now and then, a light runs along each bar toward its tip, one row after another. */
	.glint {
		inset-inline-start: -40%;
		background: linear-gradient(90deg, transparent, rgb(255 255 255 / 0.45), transparent);
		opacity: 0;
	}
	.revealed .glint {
		animation: chart-glint 5s ease-in-out infinite;
		animation-delay: calc(1.6s + var(--i) * 0.15s);
	}
	:dir(rtl) .glint {
		background: linear-gradient(270deg, transparent, rgb(255 255 255 / 0.45), transparent);
	}
	@keyframes chart-glint {
		0% { inset-inline-start: -40%; opacity: 1; }
		30% { inset-inline-start: 110%; opacity: 1; }
		31%, 100% { inset-inline-start: 110%; opacity: 0; }
	}

	/* The container lifts its lid (the Desk sprite's own motion, through --icon-motion, as the dock
	   does) while its bar grows (`lifting`, set from the script), and whenever its row is hovered. */
	.lifting :deep(.brand-icon),
	.chart-row:hover :deep(.brand-icon) {
		--icon-motion: running;
	}
}
</style>
