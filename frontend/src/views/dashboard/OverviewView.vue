<template>
  <!-- The dashboard's first page (ozone/portal/overview.py): who the account belongs to and its next step
       (a contract to pay, a quotation to answer…), the journey from facility to contract with the latest of
       each, what else waits, its latest contracts, and what Ozone's team did lately (the notifications). -->
  <section class="space-y-6">
    <DashboardHeading
      :eyebrow="t(`dashboard.stage.${producer?.doctype ?? 'Lead'}`)"
      :title="producer?.title ?? ''"
      :intro="t(`dashboard.overview.intro.${producer?.doctype ?? 'Lead'}`)"
    >
      <template #actions>
        <BaseButton :to="pageLink('requests')">
          <LucidePlus class="size-4" aria-hidden="true" />
          {{ t("dashboard.overview.newRequest") }}
        </BaseButton>
        <BaseButton :to="pageLink('facilities')" variant="outline">{{ t("dashboard.overview.addFacility") }}</BaseButton>
      </template>

      <!-- The next step -->
      <div
        v-if="overview"
        :class="[
          'w-full rounded-3xl border-2 bg-site-bg p-5 shadow-card lg:w-[26rem]',
          next ? 'border-amber-300 dark:border-amber-700' : 'border-site-line',
        ]"
      >
        <template v-if="next">
          <div class="flex items-center justify-between gap-3">
            <span class="rounded-full bg-brand-red px-3 py-0.5 text-label font-bold text-white">{{ t("dashboard.overview.next.label") }}</span>
            <span v-if="next.name" class="truncate text-label font-bold text-site-muted" dir="ltr">{{ next.name }}</span>
          </div>
          <p class="mt-3 font-extrabold text-site-heading">{{ t(`dashboard.overview.next.${next.kind}`) }}</p>
          <p class="mt-0.5 text-caption text-site-muted">
            <template v-if="next.title">
              {{ next.title }}<template v-if="next.facility"> · {{ next.facility }}</template>
              <template v-if="next.payment"> · {{ next.payment.requirement_label }}</template>
            </template>
            <template v-else>{{ t(`dashboard.overview.next.${next.kind}Hint`) }}</template>
          </p>

          <template v-if="next.payment">
            <div class="mt-4 flex flex-wrap items-center justify-between gap-3">
              <p class="text-title font-extrabold text-site-heading" dir="ltr">{{ money(next.payment.to_pay, next.payment.currency) }}</p>
              <BaseButton
                v-if="next.payment.can_pay_online"
                :loading="paying === next.name"
                @click="pay(next.name ?? '')"
              >
                <LucideCreditCard class="size-4" aria-hidden="true" />
                {{ paying === next.name ? t("dashboard.contracts.payment.paying") : t("dashboard.contracts.payment.pay") }}
              </BaseButton>
            </div>
            <div
              class="mt-4 h-2 overflow-hidden rounded-full bg-site-hover"
              role="progressbar"
              :aria-valuenow="next.payment.received"
              aria-valuemin="0"
              :aria-valuemax="next.payment.required"
              :aria-label="t('dashboard.contracts.payment.received')"
            >
              <div class="h-full rounded-full bg-brand-leaf transition-[width] duration-700" :style="{ width: `${paid(next.payment)}%` }" />
            </div>
            <div class="mt-2 flex justify-between gap-3 text-label text-site-muted">
              <span>{{ t("dashboard.contracts.payment.received") }} <b class="text-site-heading" dir="ltr">{{ money(next.payment.received, next.payment.currency) }}</b></span>
              <span>{{ t("dashboard.contracts.payment.required") }} <b class="text-site-heading" dir="ltr">{{ money(next.payment.required, next.payment.currency) }}</b></span>
            </div>
            <p v-if="!next.payment.can_pay_online" class="mt-3 text-caption text-site-muted">{{ t("dashboard.contracts.payment.offline") }}</p>
            <BaseNotice v-if="payFailed === next.name" class="mt-3">{{ t("dashboard.contracts.payment.failed") }}</BaseNotice>
          </template>

          <div v-else class="mt-4 flex flex-wrap items-center justify-between gap-3">
            <p v-if="next.amount && next.currency" class="text-title font-extrabold text-site-heading" dir="ltr">{{ money(next.amount, next.currency) }}</p>
            <BaseButton :to="next.kind === 'sign' ? { path: pageLink(next.section), query: { sign: next.name } } : pageLink(next.section)" class="ms-auto">
              {{ t("dashboard.overview.next.open") }}
              <LucideArrowRight class="size-4 rtl:-scale-x-100" aria-hidden="true" />
            </BaseButton>
          </div>
        </template>

        <div v-else class="flex items-start gap-4">
          <span class="grid size-11 shrink-0 place-items-center rounded-2xl bg-site-hover text-brand-green dark:text-brand-leaf">
            <LucideCircleCheck class="size-5" aria-hidden="true" />
          </span>
          <div>
            <p class="font-extrabold text-site-heading">{{ t("dashboard.overview.next.upToDate") }}</p>
            <p class="mt-1 text-caption text-site-muted">{{ t("dashboard.overview.next.upToDateHint") }}</p>
          </div>
        </div>
      </div>
    </DashboardHeading>

    <BaseNotice v-if="failed && !overview">{{ t("dashboard.loadFailed") }}</BaseNotice>

    <!-- The journey -->
    <ol v-if="overview" class="grid grid-cols-2 gap-3 sm:gap-4 xl:grid-cols-4">
      <li v-for="(stage, index) in STAGES" :key="stage.id" class="dash-rise" :style="{ '--rise-delay': `${80 * (index + 1)}ms` }">
        <JourneyStage
          :to="pageLink(stage.id)"
          :icon="stage.icon"
          :step="index + 1"
          :count="overview.counts[stage.count]"
          :label="t(`dashboard.overview.counts.${stage.id}`)"
          :latest="overview.stages[stage.id]"
          :empty="t(`dashboard.overview.empty.${stage.id}`)"
          :status="stage.id === 'contracts' ? t('dashboard.contracts.preparing') : undefined"
        />
      </li>
    </ol>

    <div v-if="overview" class="grid gap-6 lg:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)]">
      <div class="min-w-0 space-y-6">
        <!-- What else waits -->
        <BaseCard v-if="others.length" class="dash-rise p-5 sm:p-6">
          <h2 class="text-title font-extrabold text-site-heading">{{ t("dashboard.overview.next.more") }}</h2>
          <ul class="mt-4 space-y-2">
            <li v-for="step in others" :key="`${step.kind}-${step.name}`">
              <RouterLink
                :to="pageLink(step.section)"
                class="flex items-center gap-3 rounded-2xl bg-site-tint p-3 transition hover:bg-site-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
              >
                <span class="size-2 shrink-0 rounded-full bg-brand-red" aria-hidden="true" />
                <span class="min-w-0 flex-1">
                  <span class="block font-bold text-site-heading">{{ t(`dashboard.overview.next.${step.kind}`) }}</span>
                  <span v-if="step.title" class="block truncate text-caption text-site-muted">
                    {{ step.title }}<template v-if="step.facility"> · {{ step.facility }}</template>
                  </span>
                </span>
                <LucideChevronRight class="size-4 shrink-0 text-site-muted rtl:-scale-x-100" aria-hidden="true" />
              </RouterLink>
            </li>
          </ul>
        </BaseCard>

        <!-- The latest contracts -->
        <BaseCard class="dash-rise p-5 sm:p-6">
          <div class="flex items-center justify-between gap-3">
            <h2 class="text-title font-extrabold text-site-heading">{{ t("dashboard.overview.contracts") }}</h2>
            <RouterLink
              v-if="overview.contracts.length"
              :to="pageLink('contracts')"
              class="inline-flex items-center gap-1 text-caption font-bold text-brand-green hover:underline dark:text-brand-leaf"
            >
              {{ t("dashboard.overview.allContracts") }}
              <LucideChevronRight class="size-4 rtl:-scale-x-100" aria-hidden="true" />
            </RouterLink>
          </div>
          <p v-if="!overview.contracts.length" class="mt-4 text-caption text-site-muted">{{ t("dashboard.overview.empty.contracts") }}</p>
          <ul v-else class="mt-4 space-y-2">
            <li v-for="entry in overview.contracts" :key="entry.quotation ?? entry.contract?.name">
              <RouterLink
                :to="pageLink('contracts')"
                class="flex flex-wrap items-center gap-3 rounded-2xl bg-site-tint p-3 transition hover:bg-site-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
              >
                <span class="grid size-10 shrink-0 place-items-center rounded-xl bg-site-bg text-brand-green dark:text-brand-leaf">
                  <LucideHandshake class="size-5" aria-hidden="true" />
                </span>
                <span class="min-w-0 flex-1">
                  <span class="block truncate font-bold text-site-heading">{{ entry.service_title || entry.contract?.name }}</span>
                  <span v-if="entry.facility_title" class="block truncate text-caption text-site-muted">{{ entry.facility_title }}</span>
                  <span v-if="entry.start_date" class="block text-label text-site-muted">
                    {{ formatDate(entry.start_date, current) }}<template v-if="entry.end_date"> – {{ formatDate(entry.end_date, current) }}</template>
                  </span>
                </span>
                <span class="text-end">
                  <span
                    :class="[
                      'inline-flex rounded-full px-3 py-0.5 text-label font-bold',
                      entry.contract ? statusBadge(entry.contract.status_color) : 'bg-site-hover text-site-heading',
                    ]"
                  >
                    {{ entry.contract?.status_label ?? t("dashboard.contracts.preparing") }}
                  </span>
                  <span v-if="entry.amount" class="mt-1 block text-caption font-extrabold text-site-heading" dir="ltr">{{ money(entry.amount, entry.currency) }}</span>
                </span>
              </RouterLink>
            </li>
          </ul>
        </BaseCard>
      </div>

      <!-- Recent activity: the latest notifications -->
      <BaseCard class="dash-rise min-w-0 p-5 sm:p-6">
        <h2 class="text-title font-extrabold text-site-heading">{{ t("dashboard.overview.activity") }}</h2>
        <p v-if="!activity.length" class="mt-4 text-caption text-site-muted">{{ t("dashboard.overview.noActivity") }}</p>
        <ol v-else class="mt-4">
          <li v-for="(item, index) in activity" :key="item.name" class="relative flex gap-3 pb-4 last:pb-0">
            <span
              v-if="index < activity.length - 1"
              class="absolute start-[0.4375rem] top-5 h-[calc(100%-1rem)] w-0.5 bg-site-line"
              aria-hidden="true"
            />
            <span
              :class="[
                'relative mt-1 size-4 shrink-0 rounded-full border-[3px] border-site-bg ring-[1.5px]',
                item.read ? 'bg-brand-green ring-site-line dark:bg-brand-leaf' : 'bg-brand-red ring-brand-red',
              ]"
              aria-hidden="true"
            />
            <button
              type="button"
              class="min-w-0 rounded-lg text-start focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
              @click="openActivity(item)"
            >
              <span :class="['block text-caption hover:underline', item.read ? 'text-site-text' : 'font-bold text-site-heading']">{{ item.subject }}</span>
              <span class="mt-0.5 block text-label text-site-muted" dir="ltr">{{ formatDateTime(item.creation, current) }}</span>
            </button>
          </li>
        </ol>
      </BaseCard>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia"
import { computed, onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"
import { useRouter } from "vue-router"
import LucideArrowRight from "~icons/lucide/arrow-right"
import LucideBuilding2 from "~icons/lucide/building-2"
import LucideChevronRight from "~icons/lucide/chevron-right"
import LucideCircleCheck from "~icons/lucide/circle-check"
import LucideClipboardList from "~icons/lucide/clipboard-list"
import LucideCreditCard from "~icons/lucide/credit-card"
import LucideFileText from "~icons/lucide/file-text"
import LucideHandshake from "~icons/lucide/handshake"
import LucidePlus from "~icons/lucide/plus"

import BaseButton from "@/components/base/BaseButton.vue"
import BaseCard from "@/components/base/BaseCard.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import DashboardHeading from "@/components/dashboard/DashboardHeading.vue"
import JourneyStage from "@/components/dashboard/JourneyStage.vue"
import { useLocale } from "@/composables/useLocale"
import { usePayContract } from "@/composables/usePayContract"
import { dashboardPath, localePath } from "@/config/site"
import {
	type ContractPayment,
	type Notification,
	getNotifications,
	markNotificationsRead,
} from "@/services/portal"
import { useDashboardStore } from "@/stores/dashboard"
import { useUserStore } from "@/stores/user"
import { formatDate, formatDateTime, formatMoney } from "@/utils/format"
import { statusBadge } from "@/utils/status"

const { t, locale } = useI18n()
const { current } = useLocale()
const router = useRouter()
const { producer } = storeToRefs(useUserStore())
// Loaded by the layout on every page
const { overview, failed } = storeToRefs(useDashboardStore())
const { paying, failed: payFailed, pay } = usePayContract()

/** The journey's stages, in its order, with the overview's count of each. */
const STAGES = [
	{ id: "facilities", count: "facilities", icon: LucideBuilding2 },
	{ id: "requests", count: "service_requests", icon: LucideClipboardList },
	{ id: "quotations", count: "quotations", icon: LucideFileText },
	{ id: "contracts", count: "contracts", icon: LucideHandshake },
] as const

// The most pressing step leads; the others are listed under the journey
const next = computed(() => overview.value?.next_steps[0] ?? null)
const others = computed(() => overview.value?.next_steps.slice(1) ?? [])

/** The latest notifications, as the bell lists them. */
const ACTIVITY = 5
const activity = ref<Notification[]>([])

onMounted(async () => {
	try {
		activity.value = (await getNotifications()).items.slice(0, ACTIVITY)
	} catch {
		// The rest of the page stands without it
	}
})

async function openActivity(item: Notification) {
	if (!item.read) markNotificationsRead([item.name]).catch(() => {})
	router.push(pageLink(item.section))
}

function pageLink(page: string): string {
	return localePath(`${dashboardPath}/${page}`, current.value)
}

/** How much of the required payment is received, in percent. */
function paid(payment: ContractPayment): number {
	return payment.required
		? Math.min(100, (payment.received / payment.required) * 100)
		: 0
}

function money(amount: number, currency: string): string {
	return formatMoney(amount, currency, locale.value)
}
</script>
