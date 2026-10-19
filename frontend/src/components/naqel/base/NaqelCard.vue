<template>
  <!-- A white panel with a soft shadow. nativeTag: `as` is always the native element. -->
  <component :is="nativeTag(as)" class="rounded-2xl border border-site-line bg-site-bg shadow-naqel-card">
    <slot />
  </component>
</template>

<script lang="ts" setup>
import { nativeTag } from "@/components/base/nativeTag"

withDefaults(defineProps<{ as?: string }>(), { as: "div" })
</script>
