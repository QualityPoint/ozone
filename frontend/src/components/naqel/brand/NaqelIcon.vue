<template>
  <!-- One of naqel's Desk icons (naqel/public/icons/module-icons.svg, the sprite the dock uses),
       from the same file, put into the page (naqelSprite.ts), so the website and the Desk never
       differ. Its two tones come from the duotone custom properties, set here to the brand green
       and the heading colour. -->
  <svg viewBox="0 0 24 24" class="brand-icon" aria-hidden="true">
    <use :href="naqelIcon(name)" />
  </svg>
</template>

<script lang="ts" setup>
import { ensureNaqelSprite, naqelIcon } from "./naqelSprite"

defineProps<{ name: string }>()

ensureNaqelSprite()
</script>

<style scoped>
.brand-icon {
	--duotone-light: theme("colors.naqel.green.DEFAULT");
	--duotone-dark: rgb(var(--site-heading));
	overflow: visible;
}
</style>
