<template>
  <!-- The presentation's diagram of a compactor's devices (p. 45), as icons: naqel's truck in the
       middle, its four devices around it, joined to it by dashed lines. On smaller screens, the truck
       above the devices. Moves once in view (styles below): each device in its own way, the dashes
       flow to the truck, and the truck runs its Desk animation. Still with reduced motion. -->
  <figure ref="root" :class="{ revealed }" class="grid items-center gap-4 md:grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] md:gap-6">
    <ul v-for="(side, s) in SIDES" :key="s" :class="['grid gap-4 sm:grid-cols-2 md:grid-cols-1 md:gap-8', s ? 'md:order-3' : 'md:order-1']">
      <li v-for="id in side" :key="id" class="relative">
        <div class="flex h-full items-start gap-3 rounded-2xl border border-site-line bg-site-bg p-4 shadow-naqel-card">
          <span :class="['badge relative grid size-11 shrink-0 place-items-center rounded-xl bg-naqel-green text-white', MOTION[id]]">
            <span class="ping absolute inset-0 rounded-xl" aria-hidden="true" />
            <component :is="ICONS[id]" class="icon size-5" aria-hidden="true" />
          </span>
          <span>
            <span class="block font-extrabold text-site-heading">{{ t(`naqel.operations.devices.${id}.name`) }}</span>
            <span class="mt-0.5 block text-caption text-site-muted">{{ t(`naqel.operations.devices.${id}.body`) }}</span>
          </span>
        </div>
        <!-- The dashed line to the truck's ring (from md up): across the grid's gap and the ring's
             margin, 1.5rem + 2rem. -->
        <span :class="['dashes absolute top-1/2 hidden h-0.5 w-14 -translate-y-1/2 md:block', s ? 'flow-start end-full' : 'flow-end start-full']" aria-hidden="true" />
      </li>
    </ul>
    <div class="order-first mx-auto grid size-40 place-items-center rounded-full border-2 border-dashed border-naqel-green/60 bg-site-hover md:order-2 md:mx-8 md:size-48">
      <span class="grid size-28 place-items-center rounded-full bg-site-bg shadow-naqel-card md:size-32">
        <NaqelIcon name="truck" class="truck size-16 md:size-20" />
      </span>
    </div>
  </figure>
</template>

<script lang="ts" setup>
import { type Component, ref } from "vue"
import { useI18n } from "vue-i18n"
import LucideMonitorSmartphone from "~icons/lucide/monitor-smartphone"
import LucideNfc from "~icons/lucide/nfc"
import LucideSatelliteDish from "~icons/lucide/satellite-dish"
import LucideWeight from "~icons/lucide/weight"

import NaqelIcon from "@/components/naqel/brand/NaqelIcon.vue"
import { useReveal } from "@/composables/useReveal"
import { devices, naqelRevealThreshold } from "@/config/naqel"

type DeviceId = (typeof devices)[number]

const ICONS: Record<DeviceId, Component> = {
	"gps-unit": LucideSatelliteDish,
	"card-reader": LucideNfc,
	"cab-tablet": LucideMonitorSmartphone,
	"weighing-scale": LucideWeight,
}

/** How each device moves (styles below), in keeping with what it does. */
const MOTION: Record<DeviceId, string> = {
	"gps-unit": "motion-signal",
	"card-reader": "motion-scan",
	"cab-tablet": "motion-screen",
	"weighing-scale": "motion-weigh",
}

/** Two devices on each side of the truck, in `devices` order. */
const SIDES = [devices.slice(0, 2), devices.slice(2)]

const { t } = useI18n()

const root = ref<HTMLElement | null>(null)
const revealed = useReveal(root, naqelRevealThreshold)
</script>

<style scoped>
/* The line to the truck: green dashes (they march toward the truck, below). */
.dashes {
	background: repeating-linear-gradient(90deg, theme("colors.naqel.green.DEFAULT") 0 6px, transparent 6px 12px);
}
/* Which way is "toward the truck": the start-side devices' lines run to the end, and the others'
   to the start; in Arabic both flip. */
.flow-end {
	--flow: 1;
}
.flow-start {
	--flow: -1;
}
:dir(rtl) .flow-end {
	--flow: -1;
}
:dir(rtl) .flow-start {
	--flow: 1;
}

/* Motion only for visitors who don't ask for reduced motion, once the diagram is in view. */
@media (prefers-reduced-motion: no-preference) {
	/* Data flows along the lines into the truck. */
	.revealed .dashes {
		animation: compactor-flow 0.9s linear infinite;
	}
	@keyframes compactor-flow {
		to { background-position-x: calc(var(--flow) * 12px); }
	}

	/* The truck: the Desk sprite's own motion (it rocks on its springs, speed lines stream past),
	   switched on as the dock does, through --icon-motion. */
	.revealed .truck {
		--icon-motion: running;
	}

	/* GPS transmitter: a signal radiates from it, again and again. */
	.revealed .motion-signal .ping {
		animation: compactor-ping 2.4s ease-out infinite;
	}
	@keyframes compactor-ping {
		0% { box-shadow: 0 0 0 0 rgb(61 186 107 / 0.6); }
		70%, 100% { box-shadow: 0 0 0 14px rgb(61 186 107 / 0); }
	}

	/* Reader: its waves pulse as it scans a container, in short bursts. */
	.revealed .motion-scan .icon {
		animation: compactor-scan 2.4s ease-in-out infinite;
		animation-delay: 0.6s;
	}
	@keyframes compactor-scan {
		0%, 40%, 100% { opacity: 1; scale: 1; }
		10%, 30% { opacity: 0.45; scale: 1.12; }
		20% { opacity: 1; scale: 1; }
	}

	/* Control screen: it refreshes, its badge blinking brighter now and then. */
	.revealed .motion-screen {
		animation: compactor-screen 3s ease-in-out infinite;
		animation-delay: 1.2s;
	}
	@keyframes compactor-screen {
		0%, 20%, 100% { background-color: theme("colors.naqel.green.DEFAULT"); }
		8% { background-color: theme("colors.naqel.green.300"); }
	}

	/* Scale: it dips under a load and settles, as it weighs a container. */
	.revealed .motion-weigh .icon {
		animation: compactor-weigh 2.4s cubic-bezier(0.34, 1.56, 0.64, 1) infinite;
		animation-delay: 1.8s;
	}
	@keyframes compactor-weigh {
		0%, 45%, 100% { translate: 0 0; }
		15% { translate: 0 3px; }
		30% { translate: 0 -1px; }
	}
}
</style>
