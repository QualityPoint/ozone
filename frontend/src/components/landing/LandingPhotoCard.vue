<template>
  <!-- A product photo on its white card, with its name and a line under it. Texts come translated. -->
  <BaseCard class="group h-full overflow-hidden p-3">
    <LandingPhoto :slug="slug" :alt="name" class="transition duration-500 motion-safe:group-hover:scale-[1.03]" />
    <div class="px-3 pb-3 pt-4">
      <h3 class="font-extrabold text-site-heading">{{ name }}</h3>
      <p class="mt-1.5 text-caption text-site-muted">{{ body }}</p>
    </div>
  </BaseCard>
</template>

<script lang="ts" setup>
import BaseCard from "@/components/base/BaseCard.vue"
import LandingPhoto from "./LandingPhoto.vue"

defineProps<{ slug: string; name: string; body: string }>()
</script>
