<template>
  <!-- A white card with the documents' soft ground shadow. nativeTag: `as` is always the native element. -->
  <component :is="nativeTag(as)" class="rounded-3xl border border-site-line/70 bg-site-bg shadow-card">
    <slot />
  </component>
</template>

<script lang="ts" setup>
import { nativeTag } from "./nativeTag"

withDefaults(defineProps<{ as?: string }>(), { as: "div" })
</script>
