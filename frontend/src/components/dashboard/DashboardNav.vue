<template>
  <!-- The dashboard's pages (config/site.ts: dashboardPages): the overview, then the journey's pages
       (Operations) and the account's (Account). The journey's pages show how many records they list,
       and a red dot where one waits for the producer (stores/dashboard: the overview's next steps).
       On phones it is one scrolling row, without the groups' titles, scrolled to the open page. -->
  <nav ref="root" :aria-label="t('dashboard.nav.label')">
    <ul :class="horizontal ? 'flex gap-1' : 'space-y-1'">
      <template v-for="(page, index) in dashboardPages" :key="page.id">
        <li
          v-if="!horizontal && 'group' in page && page.group !== groupOf(index - 1)"
          class="px-3 pb-1 pt-5 text-label font-extrabold text-site-muted"
          aria-hidden="true"
        >
          {{ t(`dashboard.nav.groups.${page.group}`) }}
        </li>
        <li class="shrink-0">
          <RouterLink
            :to="localePath(`${dashboardPath}${page.path}`, current)"
            :class="[ITEM, 'group text-site-heading hover:bg-site-hover aria-[current=page]:bg-brand-green aria-[current=page]:text-white']"
          >
            <component :is="ICONS[page.id]" class="size-5 shrink-0" aria-hidden="true" />
            {{ t(`dashboard.nav.${page.id}`) }}
            <span
              v-if="waiting.has(page.id)"
              class="ms-auto size-2 shrink-0 rounded-full bg-brand-red group-aria-[current=page]:bg-white"
              :title="t('dashboard.overview.next.label')"
            />
            <span
              v-else-if="!horizontal && count(page.id) !== null"
              class="ms-auto min-w-6 rounded-full bg-site-hover px-2 text-center text-label font-extrabold text-site-heading group-aria-[current=page]:bg-white/20 group-aria-[current=page]:text-white"
            >
              {{ formatNumber(count(page.id) ?? 0) }}
            </span>
          </RouterLink>
        </li>
      </template>
    </ul>
  </nav>
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia"
import { type Component, nextTick, ref, watch } from "vue"
import { useI18n } from "vue-i18n"
import { useRoute } from "vue-router"
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
import { useDashboardStore } from "@/stores/dashboard"
import { formatNumber } from "@/utils/format"

const props = defineProps<{ horizontal?: boolean }>()

const { t } = useI18n()
const { current } = useLocale()
const { overview, waiting } = storeToRefs(useDashboardStore())
const route = useRoute()
const root = ref<HTMLElement | null>(null)

// The row on phones shows the open page, wherever it sits in it
watch(
	() => route.path,
	async () => {
		if (!props.horizontal) return
		await nextTick()
		root.value
			?.querySelector("[aria-current=page]")
			?.scrollIntoView({ block: "nearest", inline: "center" })
	},
	{ immediate: true },
)

const ICONS: Record<DashboardPageId, Component> = {
	overview: LucideLayoutDashboard,
	profile: LucideUserRound,
	establishment: LucideLandmark,
	facilities: LucideBuilding2,
	requests: LucideClipboardList,
	quotations: LucideFileText,
	contracts: LucideHandshake,
}

/** The overview's count for a page of the journey (none for the others, or before it loads). */
const COUNTS: Partial<
	Record<
		DashboardPageId,
		"facilities" | "service_requests" | "quotations" | "contracts"
	>
> = {
	facilities: "facilities",
	requests: "service_requests",
	quotations: "quotations",
	contracts: "contracts",
}

function count(page: DashboardPageId): number | null {
	const key = COUNTS[page]
	return key && overview.value ? overview.value.counts[key] : null
}

function groupOf(index: number): string | undefined {
	const page = dashboardPages[index]
	return page && "group" in page ? page.group : undefined
}

const ITEM =
	"flex items-center gap-3 whitespace-nowrap rounded-full px-4 py-2.5 text-caption font-bold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
</script>
