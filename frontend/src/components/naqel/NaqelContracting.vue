<template>
  <section id="contracting" class="overflow-x-clip py-16 sm:py-20">
    <NaqelSectionHeading :title="t('naqel.contracting.title')" :intro="t('naqel.contracting.intro')" />

    <div ref="root" :class="['section mt-10 grid items-center gap-12 lg:grid-cols-[1fr_1fr]', { revealed }]">
      <!-- The presentation's ring of six steps around "the contracting cycle" (from md up). Moves
           (styles below): once in view the ring draws itself and the steps appear in order; then a
           marker travels the cycle, and each step pulses as it arrives, with its row in the list.
           Still with reduced motion. -->
      <figure class="relative mx-auto hidden aspect-square w-full max-w-[26rem] md:block" aria-hidden="true">
        <!-- The ring and its marker, through the steps (r = RING_RADIUS% of the figure). Drawn
             clockwise for Arabic, as in the presentation; English mirrors it, as it mirrors the
             steps. ("cycle-ring", not "ring": that's a Tailwind utility, a blue box-shadow.) -->
        <svg viewBox="0 0 100 100" class="cycle-ring absolute inset-0 size-full overflow-visible">
          <circle cx="50" cy="50" :r="RING_RADIUS" fill="none" class="stroke-site-hover" stroke-width="3" />
          <circle cx="50" cy="50" :r="RING_RADIUS" fill="none" class="ring-draw stroke-naqel-green" stroke-width="1.2" pathLength="1" />
          <g class="orbit">
            <circle :cx="50 + RING_RADIUS" cy="50" r="5" class="fill-naqel-green" opacity="0.25" />
            <circle :cx="50 + RING_RADIUS" cy="50" r="2.6" class="fill-naqel-green" />
          </g>
        </svg>
        <div class="absolute inset-[31%] grid place-items-center rounded-full bg-naqel-night p-3 dark:border dark:border-white/15 text-center text-body font-extrabold text-white">
          {{ t("naqel.contracting.cycleTitle") }}
        </div>
        <!-- The steps on the ring, their names just outside it, clear of the line. -->
        <template v-for="(step, i) in steps" :key="step.title">
          <span
            class="node node-badge absolute grid size-11 -translate-x-1/2 -translate-y-1/2 place-items-center rounded-full border-4 border-site-bg bg-naqel-green text-body font-extrabold text-white shadow-naqel-card"
            :style="{ ...place(i, RING_RADIUS), '--i': i }"
            dir="ltr"
            >{{ i + 1 }}</span
          >
          <span
            class="node absolute w-24 -translate-x-1/2 -translate-y-1/2 text-center text-caption font-extrabold leading-snug text-site-heading"
            :style="{ ...place(i, LABEL_RADIUS), '--i': i }"
            >{{ step.title }}</span
          >
        </template>
      </figure>

      <ol class="space-y-4">
        <li v-for="(step, i) in steps" :key="step.title" class="step flex gap-4" :style="{ '--i': i }">
          <span class="step-number grid size-10 shrink-0 place-items-center rounded-xl border-2 border-naqel-green text-body font-extrabold" dir="ltr">{{ i + 1 }}</span>
          <div>
            <h3 class="font-extrabold text-site-heading">{{ step.title }}</h3>
            <p class="text-caption text-site-muted">{{ step.body }}</p>
          </div>
        </li>
      </ol>
    </div>

    <ul class="section mt-14 grid gap-6 md:grid-cols-3">
      <li v-for="(id, i) in FEATURES" :key="id">
        <NaqelPillHeading :tone="i % 2 ? 'ink' : 'green'">{{ t(`naqel.contracting.features.${id}.title`) }}</NaqelPillHeading>
        <p class="mt-3 px-2 text-site-text">{{ t(`naqel.contracting.features.${id}.body`) }}</p>
      </li>
    </ul>
  </section>
</template>

<script lang="ts" setup>
import { computed, ref } from "vue"
import { useI18n } from "vue-i18n"

import NaqelPillHeading from "@/components/naqel/base/NaqelPillHeading.vue"
import NaqelSectionHeading from "@/components/naqel/base/NaqelSectionHeading.vue"
import { useLocale } from "@/composables/useLocale"
import { useMessageList } from "@/composables/useMessageList"
import { useReveal } from "@/composables/useReveal"
import { naqelRevealThreshold } from "@/config/naqel"

const FEATURES = ["crm", "producer", "governance"] as const

const { t } = useI18n()
const { list } = useMessageList()
const { rtl } = useLocale()

const root = ref<HTMLElement | null>(null)
const revealed = useReveal(root, naqelRevealThreshold)

const steps = computed(() => {
	const bodies = list("naqel.contracting.steps", "body")
	return list("naqel.contracting.steps", "title").map((title, i) => ({
		title,
		body: bodies[i],
	}))
})

/** The ring's radius, and the circle the step names sit on, outside it (% of the figure). */
const RING_RADIUS = 31
const LABEL_RADIUS = 46

/**
 * Step `i` at `radius` from the centre, as in the presentation (p. 16): clockwise, step 1 on the
 * start side just above the middle and step 6 at the top. English mirrors it, so it also begins on
 * the start side.
 */
function place(i: number, radius: number) {
	const angle = ((-30 + i * 60) * Math.PI) / 180
	const x = 50 + radius * Math.cos(angle) * (rtl.value ? 1 : -1)
	const y = 50 + radius * Math.sin(angle)
	return { left: `${x}%`, top: `${y}%` }
}
</script>

<style scoped>
/* A step's number in the list: its colour is a variable, so the highlight below returns to it. */
.step-number {
	--step-color: theme("colors.naqel.green.700");
	color: var(--step-color);
}
[data-theme="dark"] .step-number {
	--step-color: theme("colors.naqel.green.300");
}

/* The marker only shows while it travels (below): with reduced motion there's nothing to mark. */
.orbit {
	display: none;
}

/* English mirrors the ring with its steps. */
:dir(ltr) .cycle-ring {
	transform: scaleX(-1);
}

/*
 * Motion only for visitors who don't ask for reduced motion; without it the ring shows complete.
 * The cycle: 6 steps, 1.2 s each (7.2 s round), starting when the entry is done (1.6 s).
 */
@media (prefers-reduced-motion: no-preference) {
	/* Entry: the ring draws itself clockwise from step 1, and the steps pop in, in order. */
	.ring-draw {
		stroke-dasharray: 1;
		stroke-dashoffset: 1;
		transform-box: view-box;
		transform-origin: 50px 50px;
		transform: rotate(-30deg);
		transition: stroke-dashoffset 1.4s ease-in-out;
	}
	.revealed .ring-draw {
		stroke-dashoffset: 0;
	}
	.node {
		opacity: 0;
		scale: 0.6;
		transition:
			opacity 0.4s ease-out,
			scale 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
		transition-delay: calc(var(--i) * 0.2s);
	}
	.revealed .node {
		opacity: 1;
		scale: 1;
	}

	/* Then the marker goes round, from step 1, reaching each step every 1.2 s. */
	.orbit {
		display: inline;
		opacity: 0;
		transform-box: view-box;
		transform-origin: 50px 50px;
		transform: rotate(-30deg);
	}
	.revealed .orbit {
		animation: contract-orbit 7.2s linear 1.6s infinite;
	}
	@keyframes contract-orbit {
		from { opacity: 1; transform: rotate(-30deg); }
		to { opacity: 1; transform: rotate(330deg); }
	}

	/* As it arrives, the step pulses, and its row in the list lights up. */
	.revealed .node-badge {
		animation: contract-pulse 7.2s ease-out infinite;
		animation-delay: calc(1.6s + var(--i) * 1.2s);
	}
	@keyframes contract-pulse {
		0% { box-shadow: 0 0 0 0 rgb(61 186 107 / 0.55); scale: 1.15; }
		12% { box-shadow: 0 0 0 14px rgb(61 186 107 / 0); scale: 1; }
		100% { box-shadow: 0 0 0 0 rgb(61 186 107 / 0); scale: 1; }
	}
	.revealed .step-number {
		animation: contract-step 7.2s ease-out infinite;
		animation-delay: calc(1.6s + var(--i) * 1.2s);
	}
	@keyframes contract-step {
		0%, 14% { background-color: theme("colors.naqel.green.DEFAULT"); color: white; }
		22%, 100% { background-color: transparent; color: var(--step-color); }
	}
}
</style>
