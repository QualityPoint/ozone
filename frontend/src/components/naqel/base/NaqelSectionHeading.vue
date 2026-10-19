<template>
  <!-- The presentation's page title: a full-width band, the logo green at the start fading to the
       night green, with the title and its corner mark in white. The intro follows on the page. -->
  <div>
    <div class="bg-naqel-band">
      <h2 class="section flex items-center gap-3 py-4 text-title-lg font-extrabold text-white sm:py-5 sm:text-heading">
        <NaqelCorner class="size-5 shrink-0 text-naqel-green-200 sm:size-6" />
        {{ title }}
      </h2>
    </div>
    <div v-if="intro" class="section mt-6">
      <p class="max-w-3xl text-body-lg text-site-muted">{{ intro }}</p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import NaqelCorner from "@/components/naqel/brand/NaqelCorner.vue"

defineProps<{ title: string; intro?: string }>()
</script>
