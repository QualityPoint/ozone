<template>
  <!-- An equipment photo as the documents show it: the product on white. The white card stays
       white in dark mode too, and multiply blends away the photo's off-white page. -->
  <div class="overflow-hidden rounded-3xl bg-white p-4">
    <img
      :src="equipmentPhotos[slug]"
      :alt="alt"
      loading="lazy"
      decoding="async"
      class="brand-art aspect-[16/9] w-full object-contain mix-blend-multiply"
    />
  </div>
</template>

<script lang="ts" setup>
import { equipmentPhotos } from "./equipmentPhotos"

defineProps<{ slug: string; alt: string }>()
</script>
