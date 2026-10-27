<template>
  <!-- The producer's notifications (ozone/portal/notifications.py): what Ozone's team did on its records (a quotation
       sent, a clarification asked, a contract awaiting its payment, a payment received, a contract issued or
       renewed). The bell shows how many are unread; each one opens its page and is marked read. -->
  <div ref="root" class="relative">
    <button
      type="button"
      class="relative grid size-10 place-items-center rounded-full text-site-heading transition hover:bg-site-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
      :aria-label="unread ? t('dashboard.notifications.unread', { count: unread }) : t('dashboard.notifications.title')"
      :title="t('dashboard.notifications.title')"
      :aria-expanded="open"
      aria-haspopup="true"
      @click="toggle"
    >
      <LucideBell class="size-5" aria-hidden="true" />
      <span
        v-if="unread"
        class="absolute -end-0.5 -top-0.5 grid min-w-5 place-items-center rounded-full bg-brand-green px-1 text-[0.7rem] font-extrabold leading-5 text-white"
        aria-hidden="true"
      >
        {{ unread > 9 ? "9+" : unread }}
      </span>
    </button>

    <div
      v-if="open"
      class="absolute end-0 top-12 z-50 w-80 max-w-[calc(100vw-2rem)] overflow-hidden rounded-2xl border border-site-line bg-site-bg shadow-card"
      role="dialog"
      :aria-label="t('dashboard.notifications.title')"
    >
      <div class="flex items-center justify-between gap-2 border-b border-site-line px-4 py-3">
        <p class="font-extrabold text-site-heading">{{ t("dashboard.notifications.title") }}</p>
        <button
          v-if="unread"
          type="button"
          class="text-caption font-bold text-brand-green hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf dark:text-brand-leaf"
          @click="markAll"
        >
          {{ t("dashboard.notifications.markAll") }}
        </button>
      </div>
      <p v-if="!items.length" class="px-4 py-6 text-center text-caption text-site-muted">
        {{ t("dashboard.notifications.none") }}
      </p>
      <ul v-else class="max-h-96 overflow-y-auto">
        <li v-for="item in items" :key="item.name">
          <button
            type="button"
            class="flex w-full gap-3 px-4 py-3 text-start transition hover:bg-site-hover focus-visible:bg-site-hover focus-visible:outline-none"
            @click="openItem(item)"
          >
            <span
              :class="['mt-1.5 size-2 shrink-0 rounded-full', item.read ? 'bg-transparent' : 'bg-brand-green']"
              aria-hidden="true"
            />
            <span class="min-w-0">
              <span :class="['block text-caption', item.read ? 'text-site-muted' : 'font-bold text-site-heading']">
                {{ item.subject }}
              </span>
              <span class="mt-0.5 block text-label text-site-muted">{{ when(item.creation) }}</span>
            </span>
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onClickOutside, useIntervalFn } from "@vueuse/core"
import { onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"
import { useRouter } from "vue-router"
import LucideBell from "~icons/lucide/bell"

import { dashboardPath, localePath } from "@/config/site"
import {
	type Notification,
	type Notifications,
	getNotifications,
	markNotificationsRead,
} from "@/services/portal"
import type { LocaleCode } from "@/types"

const { t, locale } = useI18n()
const router = useRouter()
const root = ref<HTMLElement | null>(null)
const open = ref(false)
const unread = ref(0)
const items = ref<Notification[]>([])

function show(data: Notifications) {
	unread.value = data.unread
	items.value = data.items
}

async function load() {
	try {
		show(await getNotifications())
	} catch {
		// The bell stays as it was: a failed refresh isn't worth an error on every page
	}
}

onMounted(load)
// New ones arrive while the dashboard is open
useIntervalFn(load, 60_000)
onClickOutside(root, () => {
	open.value = false
})

function toggle() {
	open.value = !open.value
	if (open.value) load()
}

async function markAll() {
	show(await markNotificationsRead())
}

async function openItem(item: Notification) {
	open.value = false
	if (!item.read) show(await markNotificationsRead([item.name]))
	router.push(
		localePath(`${dashboardPath}/${item.section}`, locale.value as LocaleCode),
	)
}

function when(value: string): string {
	return new Intl.DateTimeFormat(locale.value, {
		dateStyle: "medium",
		timeStyle: "short",
	}).format(new Date(value.replace(" ", "T")))
}
</script>
