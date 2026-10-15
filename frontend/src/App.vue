<template>
  <component :is="layout" v-if="layout">
    <!-- Keyed by language: switching it mounts the page anew, so labels the server sends follow. -->
    <RouterView :key="route.meta.locale" />
  </component>
</template>

<script lang="ts" setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

import AuthLayout from "@/layouts/AuthLayout.vue"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PublicLayout from "@/layouts/PublicLayout.vue"
import type { LayoutName } from "@/router/routes"

const layouts = {
	public: PublicLayout,
	auth: AuthLayout,
	dashboard: DashboardLayout,
} satisfies Record<LayoutName, unknown>

const route = useRoute()
// Render nothing until the first navigation resolves, so no layout flashes.
const layout = computed(() =>
	route.matched.length ? layouts[route.meta.layout] : null,
)
</script>
