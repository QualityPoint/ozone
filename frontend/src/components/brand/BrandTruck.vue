<template>
  <!-- The green compactor truck, cut out of the operation file (scripts/build-brand-assets.py),
       over a soft contact shadow. Placed right above a band, its wheels stand on it. Still. -->
  <div class="relative">
    <span class="absolute inset-x-[4%] -bottom-1.5 h-5 rounded-[50%] bg-black/25 blur-md" aria-hidden="true" />
    <img
      :src="truck"
      :alt="alt"
      width="1200"
      height="529"
      :fetchpriority="eager ? 'high' : undefined"
      :loading="eager ? undefined : 'lazy'"
      decoding="async"
      class="brand-art relative w-full"
    />
  </div>
</template>

<script lang="ts" setup>
import truck from "@/assets/images/hero-truck.webp"

withDefaults(
	defineProps<{
		/** Empty where it's decoration. */
		alt?: string
		/** Load at once and first: on screen from the start (the hero). */
		eager?: boolean
	}>(),
	{ alt: "" },
)
</script>
