<template>
  <component :is="layout" v-if="layout">
    <RouterView />
  </component>
</template>

<script lang="ts" setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

import PublicLayout from "@/layouts/PublicLayout.vue"
import type { LayoutName } from "@/router/routes"

const layouts = {
	public: PublicLayout,
} satisfies Record<LayoutName, unknown>

const route = useRoute()
// Render nothing until the first navigation resolves, so no layout flashes.
const layout = computed(() =>
	route.matched.length ? layouts[route.meta.layout] : null,
)
</script>
