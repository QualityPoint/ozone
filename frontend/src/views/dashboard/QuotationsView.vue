<template>
  <!-- Quotations (ozone/portal/quotations.py: get_quotations): the producer's requests that have turned
       into a quotation, each with the quotations Ozone's team has sent for it, or a note while the team
       prepares it. A quotation opens (QuotationPanel) on the amount, the collection, the waste report,
       the answer and the conversation; one waiting for the producer's answer is open from the start. -->
  <section>
    <DashboardHeading :title="t('dashboard.nav.quotations')" :intro="t('dashboard.quotations.intro')" />
    <BaseNotice v-if="failed" class="mt-8">{{ t("dashboard.loadFailed") }}</BaseNotice>
    <p v-else-if="!requests" class="mt-8 text-site-muted">{{ t("dashboard.requests.loading") }}</p>
    <p v-else-if="!requests.length" class="mt-8 text-site-muted">
      {{ t("dashboard.quotations.none") }}
      <RouterLink :to="requestsLink" class="font-bold text-brand-green underline dark:text-brand-leaf">{{ t("dashboard.nav.requests") }}</RouterLink>
    </p>

    <ul v-else class="mt-8 space-y-3">
      <li v-for="request in requests" :key="request.name">
        <BaseCard :class="['p-5', request.quotations.some((q) => q.status === 'Open') ? 'ring-2 ring-brand-red/60' : '']">
          <div class="flex min-w-0 gap-4">
            <span class="grid size-11 shrink-0 place-items-center rounded-xl bg-site-hover text-brand-green dark:text-brand-leaf">
              <LucideReceipt class="size-5" aria-hidden="true" />
            </span>
            <div class="min-w-0">
              <p class="font-extrabold text-site-heading">{{ request.service_title }}</p>
              <p class="mt-0.5 text-caption text-site-muted">{{ request.facility_title }} · <span dir="ltr">{{ request.name }}</span></p>
            </div>
          </div>

          <div v-for="quotation in request.quotations" :key="quotation.name" class="mt-4 rounded-2xl bg-site-hover/60 px-4 py-3">
            <button
              type="button"
              class="flex w-full flex-wrap items-center gap-3 rounded-xl text-start focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
              :aria-expanded="quotationOpen(quotation)"
              @click="panels[quotation.name] = !quotationOpen(quotation)"
            >
              <span class="font-extrabold text-site-heading">{{ t("dashboard.quotations.view") }}</span>
              <span class="text-caption text-site-muted" dir="ltr">{{ quotation.name }}</span>
              <span class="font-extrabold text-site-heading">{{ formatMoney(quotation.grand_total, quotation.currency, locale) }}</span>
              <span :class="['ms-auto rounded-full px-3 py-1 text-label font-bold', statusClass[quotation.status]]">
                {{ t(`dashboard.quotations.status.${quotation.status}`) }}
              </span>
              <LucideChevronDown :class="['size-4 text-site-muted transition', quotationOpen(quotation) ? 'rotate-180' : '']" aria-hidden="true" />
            </button>
            <QuotationPanel v-if="quotationOpen(quotation)" :name="quotation.name" @decided="(status) => answered(quotation, status)" />
          </div>
          <p v-if="!request.quotations.length" class="mt-4 flex items-center gap-2 text-caption text-site-muted">
            <LucideHourglass class="size-4" aria-hidden="true" />
            {{ t("dashboard.quotations.preparing") }}
          </p>
        </BaseCard>
      </li>
    </ul>
  </section>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref } from "vue"
import { useI18n } from "vue-i18n"
import LucideChevronDown from "~icons/lucide/chevron-down"
import LucideHourglass from "~icons/lucide/hourglass"
import LucideReceipt from "~icons/lucide/receipt"

import BaseCard from "@/components/base/BaseCard.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import DashboardHeading from "@/components/dashboard/DashboardHeading.vue"
import QuotationPanel from "@/components/dashboard/QuotationPanel.vue"
import { dashboardPath, localePath } from "@/config/site"
import {
	type QuotationStatus,
	type QuotationSummary,
	type ServiceRequest,
	getQuotations,
} from "@/services/portal"
import type { LocaleCode } from "@/types"
import { formatMoney } from "@/utils/format"

const { t, locale } = useI18n()
const requests = ref<ServiceRequest[] | null>(null)
const failed = ref(false)
const requestsLink = computed(() =>
	localePath(`${dashboardPath}/requests`, locale.value as LocaleCode),
)

onMounted(async () => {
	try {
		requests.value = await getQuotations()
	} catch {
		failed.value = true
	}
})

const statusClass: Record<QuotationStatus, string> = {
	Open: "bg-brand-red text-white",
	Accepted: "bg-brand-green text-white",
	Rejected: "bg-site-bg text-site-muted",
	"Sales Order": "bg-brand-green text-white",
}

// A quotation's details: open while it waits for the producer's answer, else when opened.
const panels = reactive<Record<string, boolean>>({})
function quotationOpen(quotation: QuotationSummary): boolean {
	return panels[quotation.name] ?? quotation.status === "Open"
}

/** An answer given (here or elsewhere): the quotation shows its new status, and stays open. */
function answered(quotation: QuotationSummary, status: QuotationStatus) {
	panels[quotation.name] = true
	quotation.status = status
}
</script>
