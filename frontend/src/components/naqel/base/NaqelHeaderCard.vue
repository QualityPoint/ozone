<template>
  <!-- The presentation's outlined card under a header strip (its dashboards page), green or ink
       (the presentation alternates them). The title comes as a prop, an optional icon in the `icon`
       slot, the body in the default slot. -->
  <component
    :is="nativeTag(as)"
    :class="['flex flex-col overflow-hidden rounded-2xl border-2 bg-site-bg', tone === 'ink' ? 'border-naqel-ink/70 dark:border-white/20' : 'border-naqel-green/70']"
  >
    <div :class="['px-5 py-4 text-center text-white', tone === 'ink' ? 'bg-naqel-ink dark:bg-white/10' : 'bg-naqel-green']">
      <div v-if="$slots.icon" class="mx-auto mb-2 grid size-12 place-items-center rounded-xl bg-white/15">
        <slot name="icon" />
      </div>
      <h3 class="text-title font-extrabold">{{ title }}</h3>
      <p v-if="term" class="mt-0.5 text-caption font-bold text-white/80" dir="ltr">{{ term }}</p>
    </div>
    <div class="flex-1 px-6 py-5 text-center font-bold text-site-heading">
      <slot />
    </div>
  </component>
</template>

<script lang="ts" setup>
import { nativeTag } from "@/components/base/nativeTag"

withDefaults(
	defineProps<{
		title: string
		/** The English term the presentation keeps beside the title ("Transporter"). */
		term?: string
		tone?: "green" | "ink"
		as?: string
	}>(),
	{ as: "div", tone: "green" },
)
</script>
