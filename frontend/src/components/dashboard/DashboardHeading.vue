<template>
  <!-- A dashboard page's title in the website's hero look: a white panel with the documents' diagonal
       silver shards and faint dots (as BrandSilverBackground draws the site's pages), the red section tag
       (an optional line above), the title, an intro and its `actions`, and at the end the default slot:
       the page's main action, or the overview's next step. -->
  <header class="dash-rise relative overflow-hidden rounded-4xl border border-site-line/70 bg-site-bg p-6 shadow-card sm:p-8">
    <div class="shard shard-a" aria-hidden="true" />
    <div class="shard shard-b" aria-hidden="true" />
    <div class="dots" aria-hidden="true" />
    <div class="relative flex flex-wrap items-center justify-between gap-6">
      <div class="min-w-0 max-w-2xl">
        <BaseSectionTag v-if="eyebrow" class="mb-4">{{ eyebrow }}</BaseSectionTag>
        <h1 class="text-heading font-extrabold text-site-heading">{{ title }}</h1>
        <p v-if="intro" class="mt-3 text-site-muted">{{ intro }}</p>
        <div v-if="$slots.actions" class="mt-5 flex flex-wrap gap-3">
          <slot name="actions" />
        </div>
      </div>
      <slot />
    </div>
  </header>
</template>

<script lang="ts" setup>
import BaseSectionTag from "@/components/base/BaseSectionTag.vue"

defineProps<{ title: string; intro?: string; eyebrow?: string }>()
</script>

<style scoped>
.shard {
	position: absolute;
	inset: 0;
	pointer-events: none;
}
/* A broad silver band across the middle, and a fainter one after it, slanted as the site's */
.shard-a {
	background: linear-gradient(115deg, transparent 0 44%, rgb(var(--site-silver) / 0.55) 44% 62%, transparent 62%);
}
.shard-b {
	background: linear-gradient(115deg, transparent 0 68%, rgb(var(--site-silver) / 0.3) 68% 80%, transparent 80%);
}
:dir(rtl) .shard {
	transform: scaleX(-1);
}
/* The dots fade in from the panel's far end */
.dots {
	position: absolute;
	inset-block: 0;
	inset-inline-end: 0;
	width: 50%;
	pointer-events: none;
	background-image: radial-gradient(rgb(var(--site-silver)) 1.2px, transparent 1.5px);
	background-size: 18px 18px;
	mask-image: linear-gradient(to right, transparent, #000 70%);
	opacity: 0.8;
}
:dir(rtl) .dots {
	mask-image: linear-gradient(to left, transparent, #000 70%);
}
</style>
