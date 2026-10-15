<template>
  <!-- A dashboard page's title in the documents' look: the red section tag (an optional line
       above), the title, an intro, and the page's main action at the end. -->
  <div class="flex flex-wrap items-end justify-between gap-4">
    <div class="min-w-0">
      <BaseSectionTag v-if="eyebrow" class="mb-4">{{ eyebrow }}</BaseSectionTag>
      <h1 class="text-heading font-extrabold text-site-heading">{{ title }}</h1>
      <p v-if="intro" class="mt-3 max-w-2xl text-site-muted">{{ intro }}</p>
    </div>
    <slot />
  </div>
</template>

<script lang="ts" setup>
import BaseSectionTag from "@/components/base/BaseSectionTag.vue"

defineProps<{ title: string; intro?: string; eyebrow?: string }>()
</script>
