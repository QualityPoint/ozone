<template>
  <!-- The presentation's pill sub-heading: a rounded bar, green or black (it alternates them). -->
  <component
    :is="nativeTag(as)"
    :class="[
      'inline-flex w-full items-center rounded-full px-5 py-2.5 text-body font-extrabold text-white',
      tone === 'ink' ? 'bg-naqel-ink dark:bg-white/10' : 'bg-naqel-green',
    ]"
  >
    <slot />
  </component>
</template>

<script lang="ts" setup>
import { nativeTag } from "@/components/base/nativeTag"

withDefaults(defineProps<{ tone?: "green" | "ink"; as?: string }>(), {
	tone: "green",
	as: "h3",
})
</script>
