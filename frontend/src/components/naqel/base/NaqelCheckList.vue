<template>
  <!-- A list with green check marks. Takes its items translated. -->
  <ul class="space-y-3">
    <li v-for="item in items" :key="item" class="flex items-start gap-3">
      <span class="mt-0.5 grid size-6 shrink-0 place-items-center rounded-md bg-naqel-green text-white" aria-hidden="true">
        <LucideCheck class="size-4" />
      </span>
      <span>{{ item }}</span>
    </li>
  </ul>
</template>

<script lang="ts" setup>
import LucideCheck from "~icons/lucide/check"

defineProps<{ items: string[] }>()
</script>
