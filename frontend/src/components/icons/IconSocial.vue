<template>
  <!-- A social platform's brand mark, in the current text colour. -->
  <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path :d="socialIconPaths[platform]" />
  </svg>
</template>

<script lang="ts" setup>
import type { SocialPlatform } from "@/types"
import { socialIconPaths } from "./socialIconPaths"

defineProps<{ platform: SocialPlatform }>()
</script>
