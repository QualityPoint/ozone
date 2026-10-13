<template>
  <!-- One navbar entry: a section of the landing page (/#about, /en#about), in the current
       language. Styling comes from the parent. -->
  <RouterLink :to="navTarget(item)">{{ t(`nav.${item.id}`) }}</RouterLink>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"

import { useLocale } from "@/composables/useLocale"
import type { NavItem } from "@/types"

defineProps<{ item: NavItem }>()

const { t } = useI18n()
const { navTarget } = useLocale()
</script>
