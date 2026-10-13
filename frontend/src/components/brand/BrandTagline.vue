<template>
  <!-- The logo's slogan ("صيانة - نظافة - مقاولات عامة"): its items with red dots between. -->
  <p class="flex flex-wrap items-center gap-x-3 gap-y-1 font-bold">
    <template v-for="(item, i) in tagline" :key="item">
      <span v-if="i" class="size-1.5 rounded-full bg-brand-red" aria-hidden="true" />
      <span>{{ item }}</span>
    </template>
  </p>
</template>

<script lang="ts" setup>
import { computed } from "vue"
import { useI18n } from "vue-i18n"

const { tm, rt } = useI18n()
const tagline = computed(() =>
	(tm("brand.tagline") as unknown[]).map((item) => rt(item as string)),
)
</script>
