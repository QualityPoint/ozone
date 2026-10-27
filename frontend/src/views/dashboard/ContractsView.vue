<template>
  <!-- Contracts (ozone/portal/contracts.py): each quotation the producer accepted that Ozone's team has
       submitted, with the Service Contract that follows it ("being prepared" until the team issues it),
       and any other contract of the producer's Customer. Read only; a quotation's details open below it. -->
  <section>
    <DashboardHeading :eyebrow="t('dashboard.nav.groups.operations')" :title="t('dashboard.nav.contracts')" :intro="t('dashboard.contracts.intro')" />
    <BaseNotice v-if="failed" class="mt-8">{{ t("dashboard.loadFailed") }}</BaseNotice>
    <p v-else-if="!entries" class="mt-8 text-site-muted">{{ t("dashboard.requests.loading") }}</p>
    <p v-else-if="!entries.length" class="mt-8 text-site-muted">
      {{ t("dashboard.contracts.none") }}
      <RouterLink :to="quotationsLink" class="font-bold text-brand-green underline dark:text-brand-leaf">{{ t("dashboard.nav.quotations") }}</RouterLink>
    </p>

    <ul v-else class="mt-8 space-y-3">
      <li v-for="entry in entries" :key="entry.quotation ?? entry.contract?.name" class="dash-rise">
        <BaseCard class="p-5">
          <div class="flex flex-wrap items-start justify-between gap-4">
            <div class="flex min-w-0 gap-4">
              <span class="grid size-11 shrink-0 place-items-center rounded-xl bg-site-hover text-brand-green dark:text-brand-leaf">
                <LucideHandshake class="size-5" aria-hidden="true" />
              </span>
              <div class="min-w-0">
                <p class="font-extrabold text-site-heading">{{ entry.service_title || entry.contract?.name }}</p>
                <p class="mt-0.5 text-caption text-site-muted">
                  <template v-if="entry.facility_title">{{ entry.facility_title }} · </template>
                  <span dir="ltr">{{ entry.contract?.name ?? entry.quotation }}</span>
                </p>
                <p v-if="entry.start_date" class="mt-1 text-caption text-site-muted">
                  {{ formatDate(entry.start_date, locale as LocaleCode) }}<template v-if="entry.end_date"> – {{ formatDate(entry.end_date, locale as LocaleCode) }}</template>
                </p>
              </div>
            </div>
            <div class="text-end">
              <span
                :class="[
                  'inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-caption font-bold',
                  entry.contract ? statusBadge(entry.contract.status_color) : 'bg-site-hover text-site-heading',
                ]"
              >
                <LucideHourglass v-if="!entry.contract" class="size-3.5" aria-hidden="true" />
                {{ entry.contract?.status_label ?? t("dashboard.contracts.preparing") }}
              </span>
              <p v-if="entry.amount" class="mt-2 font-extrabold text-site-heading">{{ formatMoney(entry.amount, entry.currency, locale) }}</p>
            </div>
          </div>

          <!-- What it requires paid before it is issued (a draft awaiting the producer's payment) -->
          <div
            v-if="entry.contract?.payment"
            class="mt-4 rounded-2xl border-2 border-amber-300 bg-amber-50 p-4 dark:border-amber-700 dark:bg-amber-950/30"
          >
            <p class="text-caption font-bold text-site-heading">
              {{ t("dashboard.contracts.payment.title") }} · {{ entry.contract.payment.requirement_label }}
            </p>
            <dl class="mt-2 grid grid-cols-3 gap-3 text-caption">
              <div>
                <dt class="text-site-muted">{{ t("dashboard.contracts.payment.required") }}</dt>
                <dd class="font-bold text-site-heading">{{ money(entry.contract.payment.required, entry.contract.payment.currency) }}</dd>
              </div>
              <div>
                <dt class="text-site-muted">{{ t("dashboard.contracts.payment.received") }}</dt>
                <dd class="font-bold text-site-heading">{{ money(entry.contract.payment.received, entry.contract.payment.currency) }}</dd>
              </div>
              <div>
                <dt class="text-site-muted">{{ t("dashboard.contracts.payment.toPay") }}</dt>
                <dd class="font-extrabold text-site-heading">{{ money(entry.contract.payment.to_pay, entry.contract.payment.currency) }}</dd>
              </div>
            </dl>
            <button
              v-if="entry.contract.payment.can_pay_online"
              type="button"
              class="mt-3 inline-flex items-center gap-1.5 rounded-full bg-brand-green px-5 py-2 text-label font-bold text-white transition hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf disabled:opacity-60"
              :disabled="paying === entry.contract.name"
              @click="pay(entry.contract.name)"
            >
              <LucideCreditCard class="size-4" aria-hidden="true" />
              {{ paying === entry.contract.name ? t("dashboard.contracts.payment.paying") : t("dashboard.contracts.payment.pay") }}
            </button>
            <p v-else-if="entry.contract.payment.to_pay > 0" class="mt-3 text-caption text-site-muted">
              {{ t("dashboard.contracts.payment.offline") }}
            </p>
            <p v-else class="mt-3 text-caption font-bold text-brand-green dark:text-brand-leaf">
              {{ t("dashboard.contracts.payment.issuing") }}
            </p>
            <BaseNotice v-if="payFailed === entry.contract.name" class="mt-3">{{ t("dashboard.contracts.payment.failed") }}</BaseNotice>
          </div>

          <!-- The accepted quotation it follows -->
          <template v-if="entry.quotation">
            <button
              type="button"
              class="mt-4 inline-flex items-center gap-1.5 rounded-full border-2 border-site-line px-4 py-1.5 text-label font-bold text-site-heading transition hover:bg-site-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
              :aria-expanded="Boolean(open[entry.quotation])"
              @click="open[entry.quotation] = !open[entry.quotation]"
            >
              <LucideReceipt class="size-3.5" aria-hidden="true" />
              {{ t("dashboard.contracts.details") }}
              <span dir="ltr">{{ entry.quotation }}</span>
            </button>
            <QuotationPanel v-if="open[entry.quotation]" :name="entry.quotation" />
          </template>
        </BaseCard>
      </li>
    </ul>
  </section>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref } from "vue"
import { useI18n } from "vue-i18n"
import LucideCreditCard from "~icons/lucide/credit-card"
import LucideHandshake from "~icons/lucide/handshake"
import LucideHourglass from "~icons/lucide/hourglass"
import LucideReceipt from "~icons/lucide/receipt"

import BaseCard from "@/components/base/BaseCard.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import DashboardHeading from "@/components/dashboard/DashboardHeading.vue"
import QuotationPanel from "@/components/dashboard/QuotationPanel.vue"
import { usePayContract } from "@/composables/usePayContract"
import { dashboardPath, localePath } from "@/config/site"
import { type ContractEntry, getContracts } from "@/services/portal"
import type { LocaleCode } from "@/types"
import { formatDate, formatMoney } from "@/utils/format"
import { statusBadge } from "@/utils/status"

const { t, locale } = useI18n()
const entries = ref<ContractEntry[] | null>(null)
const failed = ref(false)
const open = reactive<Record<string, boolean>>({})
// The contract whose payment is being opened, and the one whose payment couldn't be
const { paying, failed: payFailed, pay } = usePayContract()
const quotationsLink = computed(() =>
	localePath(`${dashboardPath}/quotations`, locale.value as LocaleCode),
)

onMounted(async () => {
	try {
		entries.value = await getContracts()
	} catch {
		failed.value = true
	}
})

function money(amount: number, currency: string): string {
	return formatMoney(amount, currency, locale.value)
}
</script>
