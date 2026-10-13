<template>
  <!-- One navbar entry, in the current language: a section of the landing page (/#about,
       /en#about) or a page (/capabilities). Styling comes from the parent. -->
  <RouterLink :to="navTarget(item)" :aria-current="current ? 'page' : undefined">{{ t(`nav.${item.id}`) }}</RouterLink>
</template>

<script lang="ts" setup>
import { computed } from "vue"
import { useI18n } from "vue-i18n"
import { useRoute } from "vue-router"

import { useLocale } from "@/composables/useLocale"
import type { NavItem } from "@/types"

const props = defineProps<{ item: NavItem }>()

const { t } = useI18n()
const route = useRoute()
const { navTarget } = useLocale()
/** A page entry on its own page (section entries never are: they're parts of one page). */
const current = computed(
	() => "page" in props.item && route.meta.page === props.item.page,
)
</script>
