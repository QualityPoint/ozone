<template>
  <div :class="['max-w-3xl', align === 'center' ? 'mx-auto text-center' : 'text-start']">
    <BaseSectionTag>{{ tag }}</BaseSectionTag>
    <h2 class="mt-5 text-heading font-extrabold text-site-heading sm:text-heading-lg">{{ title }}</h2>
    <p v-if="intro" class="mt-4 text-body-lg text-site-muted">{{ intro }}</p>
  </div>
</template>

<script lang="ts" setup>
import BaseSectionTag from "@/components/base/BaseSectionTag.vue"

withDefaults(
	defineProps<{
		tag: string
		title: string
		intro?: string
		align?: "center" | "start"
	}>(),
	{ align: "center" },
)
</script>
