<template>
  <!-- The hero's picture of the platform, abstract: a route map with its pins, a donut of waste
       types, rising bars, and naqel's own container icons, on glass panels in the brand greens.
       Each panel moves in its own way (styles below): the route draws itself and its pins pulse,
       the donut's segments sweep in, the bars rise and settle, and the containers lift their lids
       with the Desk's own animation. Still for visitors who prefer reduced motion. No text;
       decorative: the hero's text says what the platform does. -->
  <svg viewBox="0 0 560 420" class="h-auto w-full" aria-hidden="true">
    <defs>
      <linearGradient id="art-route" x1="0" x2="1" y1="0" y2="0">
        <stop offset="0" class="stop-mint" />
        <stop offset="1" class="stop-green" />
      </linearGradient>
      <pattern id="art-grid" width="22" height="22" patternUnits="userSpaceOnUse">
        <path d="M22 0H0V22" fill="none" stroke="white" stroke-opacity="0.06" stroke-width="1" />
      </pattern>
    </defs>

    <!-- Map: streets on a grid, the route between collection points. -->
    <rect x="8" y="8" width="330" height="236" rx="22" class="panel" />
    <rect x="8" y="8" width="330" height="236" rx="22" fill="url(#art-grid)" />
    <path d="M40 210 C 90 200, 70 150, 120 140 S 190 170, 210 120 S 260 60, 306 52" fill="none" stroke="white" stroke-opacity="0.12" stroke-width="16" stroke-linecap="round" />
    <path d="M40 210 C 90 200, 70 150, 120 140 S 190 170, 210 120 S 260 60, 306 52" fill="none" stroke="url(#art-route)" stroke-width="5" stroke-linecap="round" pathLength="1" class="route" />
    <g v-for="(pin, i) in PINS" :key="pin.join()" :transform="`translate(${pin[0]} ${pin[1]})`" :style="{ '--i': i }">
      <circle r="13" class="green pulse" fill-opacity="0.2" />
      <circle r="7" class="green" />
      <circle r="2.6" class="night" />
    </g>

    <!-- Donut: the three waste streams of a facility. -->
    <rect x="352" y="8" width="200" height="236" rx="22" class="panel" />
    <g transform="translate(452 126) rotate(-90)">
      <circle r="58" fill="none" stroke="white" stroke-opacity="0.08" stroke-width="20" />
      <circle
        v-for="(segment, i) in SEGMENTS"
        :key="i"
        r="58"
        fill="none"
        stroke-width="20"
        :class="['segment', segment.tone]"
        :stroke-dasharray="dash(segment.share)"
        :stroke-dashoffset="-length(segment.from)"
        :style="{ '--length': length(segment.share), '--circle': CIRCUMFERENCE, '--i': i }"
      />
    </g>
    <circle cx="452" cy="126" r="26" fill="white" fill-opacity="0.06" />

    <!-- Bars: generation, rising. -->
    <rect x="8" y="258" width="330" height="154" rx="22" class="panel" />
    <rect v-for="(h, i) in BARS" :key="i" :x="34 + i * 40" :y="390 - h" width="24" :height="h" rx="6" class="green bar" :fill-opacity="0.35 + i * 0.09" :style="{ '--i': i }" />
    <line x1="30" y1="390" x2="316" y2="390" stroke="white" stroke-opacity="0.15" stroke-width="2" />

    <!-- naqel's containers, smallest to largest (its Desk sprite: NaqelIcon). -->
    <rect x="352" y="258" width="200" height="154" rx="22" class="panel" />
    <line x1="372" y1="368" x2="532" y2="368" stroke="white" stroke-opacity="0.15" stroke-width="2" stroke-linecap="round" />
    <svg v-for="(c, i) in CONTAINERS" :key="c.name" :x="c.x" :y="c.y" :width="c.size" :height="c.size" viewBox="0 0 24 24" class="art-icon" :style="{ '--i': i }">
      <use :href="naqelIcon(c.name)" />
    </svg>
  </svg>
</template>

<script lang="ts" setup>
import { ensureNaqelSprite, naqelIcon } from "./naqelSprite"

ensureNaqelSprite()

/** Collection points along the route. */
const PINS = [
	[40, 210],
	[120, 140],
	[210, 120],
	[306, 52],
]
/** The bars' heights, rising. */
const BARS = [34, 52, 46, 70, 84, 100, 118]
/**
 * Three containers growing, standing on one ground line, inside the panel's padding: the panel is
 * x 352–552, y 258–412; inside 20 units of padding the icons (36 + 48 + 62, 7 apart) fill
 * x 372–532, and the group (y 305–368) is centred on the panel's height.
 */
const GROUND = 367
const CONTAINERS = [
	{ name: "bin-240l", x: 372, size: 36 },
	{ name: "container-6yd", x: 415, size: 48 },
	{ name: "container-20yd", x: 470, size: 62 },
].map((c) => ({ ...c, y: GROUND - c.size }))

/** The donut's segments: a facility's three waste streams, each from where the last one ends. */
const SEGMENTS = [
	{ share: 0.45, from: 0, tone: "stroke-green" },
	{ share: 0.3, from: 0.45, tone: "stroke-mint mint-soft" },
	{ share: 0.25, from: 0.75, tone: "stroke-white" },
]

/** The donut's circle (r = 58): a share's arc length, and its stroke-dasharray. */
const CIRCUMFERENCE = 2 * Math.PI * 58
const length = (share: number) => share * CIRCUMFERENCE
const dash = (share: number) => `${length(share)} ${CIRCUMFERENCE}`
</script>

<style scoped>
/* The palette's own values (tailwind.config.ts: naqel), not copies. */
.green {
	fill: theme("colors.naqel.green.DEFAULT");
}
.night {
	fill: theme("colors.naqel.night.DEFAULT");
}
.stroke-green {
	stroke: theme("colors.naqel.green.DEFAULT");
}
.stroke-mint {
	stroke: theme("colors.naqel.mint.DEFAULT");
}
.stop-green {
	stop-color: theme("colors.naqel.green.DEFAULT");
}
.stop-mint {
	stop-color: theme("colors.naqel.mint.DEFAULT");
}
.stroke-white {
	stroke: white;
	stroke-opacity: 0.85;
}
.mint-soft {
	stroke-opacity: 0.65;
}
.panel {
	fill: white;
	fill-opacity: 0.05;
	stroke: white;
	stroke-opacity: 0.12;
}
/* naqel's icons, light on the dark hero: the green body and a white detail. */
.art-icon {
	--duotone-light: theme("colors.naqel.green.DEFAULT");
	--duotone-dark: white;
	overflow: visible;
}

/*
 * The motion, one style per panel, only for visitors who don't ask for reduced motion. Every loop
 * lasts 6 s, so the panels keep time with one another.
 */
@media (prefers-reduced-motion: no-preference) {
	/* Map: the route draws itself from the first pin to the last, holds, then fades to draw again. */
	.route {
		stroke-dasharray: 1;
		animation: art-route 6s ease-in-out infinite;
	}
	@keyframes art-route {
		0% { stroke-dashoffset: 1; opacity: 1; }
		45%, 85% { stroke-dashoffset: 0; opacity: 1; }
		100% { stroke-dashoffset: 0; opacity: 0; }
	}
	/* Each pin pulses as the route reaches it. */
	.pulse {
		transform-box: fill-box;
		transform-origin: center;
		animation: art-pulse 6s ease-out infinite;
		animation-delay: calc(var(--i) * 0.75s);
	}
	@keyframes art-pulse {
		0%, 100% { transform: scale(1); opacity: 0.2; }
		12% { transform: scale(1.9); opacity: 0; }
		13% { transform: scale(1); opacity: 0; }
		30% { opacity: 0.2; }
	}

	/* Donut: the three streams sweep in one after another, hold, then clear. */
	.segment {
		animation: art-sweep 6s ease-in-out infinite;
		animation-delay: calc(var(--i) * 0.35s);
	}
	@keyframes art-sweep {
		0% { stroke-dasharray: 0 calc(var(--circle) * 1px); }
		30%, 85% { stroke-dasharray: calc(var(--length) * 1px) calc(var(--circle) * 1px); }
		100% { stroke-dasharray: 0 calc(var(--circle) * 1px); }
	}

	/* Bars: they rise from the baseline in turn and settle, like readings coming in. */
	.bar {
		transform-box: fill-box;
		transform-origin: bottom;
		animation: art-rise 6s cubic-bezier(0.34, 1.3, 0.64, 1) infinite;
		animation-delay: calc(var(--i) * 0.12s);
	}
	@keyframes art-rise {
		0% { transform: scaleY(0.15); }
		25%, 80% { transform: scaleY(1); }
		90% { transform: scaleY(0.82); }
		100% { transform: scaleY(0.15); }
	}

	/* Containers: the Desk sprite's own motion (its lids lift on their hinges), switched on as the
	   dock does, through --icon-motion. */
	.art-icon {
		--icon-motion: running;
	}
}
</style>
