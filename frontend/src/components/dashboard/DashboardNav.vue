<template>
  <!-- The dashboard's pages (config/site.ts: dashboardPages). Pages still to come show, dimmed,
       with a "soon" tag, so the producer sees what the dashboard will hold. -->
  <nav :aria-label="t('dashboard.nav.label')">
    <ul :class="horizontal ? 'flex gap-1' : 'space-y-1'">
      <li v-for="page in dashboardPages" :key="page.id" class="shrink-0">
        <span
          v-if="'soon' in page && page.soon"
          :class="[ITEM, 'cursor-default text-site-muted']"
          aria-disabled="true"
        >
          <component :is="ICONS[page.id]" class="size-5 shrink-0" aria-hidden="true" />
          {{ t(`dashboard.nav.${page.id}`) }}
          <span class="ms-auto rounded-full bg-site-hover px-2 py-0.5 text-[0.7rem] font-bold">{{ t("dashboard.soon") }}</span>
        </span>
        <RouterLink
          v-else
          :to="localePath(`${dashboardPath}${page.path}`, current)"
          :class="[ITEM, 'text-site-heading hover:bg-site-hover aria-[current=page]:bg-brand-green aria-[current=page]:text-white']"
        >
          <component :is="ICONS[page.id]" class="size-5 shrink-0" aria-hidden="true" />
          {{ t(`dashboard.nav.${page.id}`) }}
        </RouterLink>
      </li>
    </ul>
  </nav>
</template>

<script lang="ts" setup>
import type { Component } from "vue"
import { useI18n } from "vue-i18n"
import LucideBuilding2 from "~icons/lucide/building-2"
import LucideClipboardList from "~icons/lucide/clipboard-list"
import LucideFileText from "~icons/lucide/file-text"
import LucideHandshake from "~icons/lucide/handshake"
import LucideLandmark from "~icons/lucide/landmark"
import LucideLayoutDashboard from "~icons/lucide/layout-dashboard"
import LucideUserRound from "~icons/lucide/user-round"

import { useLocale } from "@/composables/useLocale"
import {
	type DashboardPageId,
	dashboardPages,
	dashboardPath,
	localePath,
} from "@/config/site"

defineProps<{ horizontal?: boolean }>()

const { t } = useI18n()
const { current } = useLocale()

const ICONS: Record<DashboardPageId, Component> = {
	overview: LucideLayoutDashboard,
	profile: LucideUserRound,
	establishment: LucideLandmark,
	facilities: LucideBuilding2,
	requests: LucideClipboardList,
	quotations: LucideFileText,
	contracts: LucideHandshake,
}

const ITEM =
	"flex items-center gap-3 whitespace-nowrap rounded-xl px-3 py-2.5 text-caption font-bold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
</script>
