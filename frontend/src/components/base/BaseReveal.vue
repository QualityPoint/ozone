<template>
  <!-- Fades up once it scrolls into view; `delay` (ms) staggers siblings. Off with reduced motion. -->
  <component
    :is="nativeTag(as)"
    ref="root"
    :style="{ transitionDelay: revealed ? `${delay}ms` : undefined }"
    :class="[
      'transition-[opacity,transform] duration-700 ease-out',
      revealed ? 'opacity-100' : 'motion-safe:translate-y-6 motion-safe:opacity-0',
    ]"
  >
    <slot />
  </component>
</template>

<script lang="ts" setup>
import { computed, ref } from "vue"

import { useReveal } from "@/composables/useReveal"
import { nativeTag } from "./nativeTag"

withDefaults(defineProps<{ as?: string; delay?: number }>(), {
	as: "div",
	delay: 0,
})

/** The component nativeTag renders exposes its element as `$el`. */
const root = ref<{ $el?: HTMLElement } | null>(null)
const revealed = useReveal(computed(() => root.value?.$el))
</script>
