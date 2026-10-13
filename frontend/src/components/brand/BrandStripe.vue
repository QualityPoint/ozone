<template>
  <!-- The bands framing every page of Ozone's documents: green with a slanted red segment at
       the start (top), or green over a lighter green line (bottom). Purely decorative. -->
  <div :class="['relative h-2 w-full bg-brand-green', edge === 'bottom' && 'border-t-2 border-brand-leaf']" aria-hidden="true">
    <span
      v-if="edge === 'top'"
      class="stripe-segment absolute start-0 top-0 h-full w-1/3 bg-brand-red"
    />
  </div>
</template>

<script lang="ts" setup>
withDefaults(defineProps<{ edge?: "top" | "bottom" }>(), { edge: "top" })
</script>

<style scoped>
/* The segment's far end is cut on a slant, as in the documents; mirrored in RTL. */
.stripe-segment {
	clip-path: polygon(0 0, 100% 0, calc(100% - 12px) 100%, 0 100%);
}
:dir(rtl) .stripe-segment {
	clip-path: polygon(0 0, 100% 0, 100% 100%, 12px 100%);
}
</style>
