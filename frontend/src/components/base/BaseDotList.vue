<template>
  <!-- A list with the documents' small red dots. Takes its items translated. -->
  <ul class="space-y-2.5">
    <li v-for="item in items" :key="item" class="flex gap-2.5">
      <span class="mt-2.5 size-1.5 shrink-0 rounded-full bg-brand-red" aria-hidden="true" />
      <span>{{ item }}</span>
    </li>
  </ul>
</template>

<script lang="ts" setup>
defineProps<{ items: string[] }>()
</script>
