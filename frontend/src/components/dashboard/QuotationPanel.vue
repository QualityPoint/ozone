<template>
  <!-- A quotation Ozone's team has sent for a request (ozone/portal/quotations.py): the amount to pay,
       how and how often the waste is collected (the container type only when the collection deploys
       one), the service period, and the waste calculation report. An Open quotation is accepted or
       rejected here (a rejection says why, in its comments); the producer reads its comments with the team
       but doesn't write there. -->
  <div class="mt-4 border-t-2 border-site-line pt-4">
    <BaseNotice v-if="failed">{{ failed }}</BaseNotice>
    <p v-else-if="!quotation" class="text-caption text-site-muted">{{ t("dashboard.requests.loading") }}</p>
    <template v-else>
      <div class="grid gap-4 md:grid-cols-2">
        <!-- What to pay -->
        <div class="rounded-2xl bg-brand-green p-5 text-white">
          <p class="text-caption font-bold text-white/80">{{ t("dashboard.quotations.amount") }}</p>
          <p class="mt-1 text-[2rem] font-extrabold leading-tight">{{ money(amounts.rounded_total) }}</p>
          <p class="mt-1 text-caption text-white/80">{{ periodText }}</p>
          <dl class="mt-4 space-y-1 border-t border-white/25 pt-3 text-caption">
            <div class="flex justify-between gap-4">
              <dt>{{ t("dashboard.quotations.net") }}</dt>
              <dd class="font-bold">{{ money(amounts.net_total) }}</dd>
            </div>
            <div v-if="amounts.discount" class="flex justify-between gap-4">
              <dt>{{ t("dashboard.quotations.discount") }}</dt>
              <dd class="font-bold">− {{ money(amounts.discount) }}</dd>
            </div>
            <div v-for="tax in amounts.taxes" :key="tax.description" class="flex justify-between gap-4">
              <dt>{{ tax.description }}</dt>
              <dd class="font-bold">{{ money(tax.amount) }}</dd>
            </div>
          </dl>
          <p v-if="quotation.valid_till" class="mt-3 text-label text-white/75">
            {{ t("dashboard.quotations.validTill") }} {{ formatDate(quotation.valid_till) }}
          </p>
        </div>

        <!-- How the waste is collected: each container line's collection (its waste type when there are several) -->
        <div class="rounded-2xl border-2 border-site-line p-5">
          <p class="text-caption font-bold text-site-muted">{{ t("dashboard.quotations.collection") }}</p>
          <div
            v-for="(collection, index) in quotation.collections"
            :key="index"
            :class="index ? 'mt-4 border-t-2 border-site-line pt-4' : 'mt-1'"
          >
            <p v-if="quotation.collections.length > 1" class="text-label font-bold text-site-muted">{{ collection.waste_type }}</p>
            <p class="flex items-center gap-2 text-title font-extrabold text-site-heading">
              <LucideTruck class="size-5 shrink-0 text-brand-green dark:text-brand-leaf" aria-hidden="true" />
              {{ collection.mechanism }}
            </p>
            <p v-if="collection.description" class="mt-1 text-caption text-site-muted">{{ collection.description }}</p>
            <div class="mt-3 flex flex-wrap gap-2">
              <p class="inline-flex items-center gap-2 rounded-full bg-site-hover px-3 py-1 text-caption font-bold text-site-heading">
                <LucideRepeat class="size-3.5" aria-hidden="true" />
                {{ frequency(collection) }}
              </p>
              <p
                v-if="collection.container"
                :title="t('dashboard.quotations.containers')"
                class="inline-flex items-center gap-2 rounded-full border-2 border-brand-green px-3 py-1 text-caption font-bold text-site-heading dark:border-brand-leaf"
              >
                <LucideContainer class="size-4" aria-hidden="true" />
                {{ collection.container.container_type }}<span v-if="collection.container.count > 1" dir="ltr"> × {{ collection.container.count }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- The waste calculation report: naqel's own page, on white in both themes -->
      <details v-if="quotation.report" class="group mt-4 rounded-2xl border-2 border-site-line">
        <summary class="flex cursor-pointer list-none items-center justify-between gap-3 px-5 py-3 font-bold text-site-heading">
          <span class="flex items-center gap-2">
            <LucideFileBarChart class="size-4 text-brand-green dark:text-brand-leaf" aria-hidden="true" />
            {{ t("dashboard.quotations.report") }}
          </span>
          <LucideChevronDown class="size-4 transition group-open:rotate-180" aria-hidden="true" />
        </summary>
        <div class="overflow-x-auto rounded-b-2xl bg-white p-4" v-html="quotation.report" />
      </details>

      <!-- The producer's answer -->
      <div v-if="quotation.can_decide" class="mt-4 rounded-2xl border-2 border-brand-green/40 p-5 dark:border-brand-leaf/40">
        <p class="font-extrabold text-site-heading">{{ t("dashboard.quotations.decide") }}</p>
        <p class="mt-1 text-caption text-site-muted">{{ t("dashboard.quotations.decideHint") }}</p>
        <label :for="commentId" class="mb-1.5 mt-4 block text-caption font-bold text-site-heading">{{ t("dashboard.quotations.comment") }}</label>
        <textarea
          :id="commentId"
          v-model="comment"
          rows="2"
          maxlength="4000"
          :aria-invalid="decisionError ? 'true' : undefined"
          :class="[
            'block w-full rounded-2xl border-2 bg-site-bg px-4 py-3 text-body text-site-text transition',
            'focus:border-brand-green focus:outline-none focus:ring-4 focus:ring-brand-leaf/25 dark:focus:border-brand-leaf',
            decisionError ? 'border-brand-red' : 'border-site-line',
          ]"
        />
        <p v-if="decisionError" class="mt-1.5 text-caption font-bold text-brand-red dark:text-brand-red-300">{{ decisionError }}</p>
        <div v-if="confirming" class="mt-4 flex flex-wrap items-center gap-3">
          <span class="text-caption text-site-text">
            {{ confirming === "Accepted" ? `${t("dashboard.quotations.acceptConfirm")} ${money(amounts.rounded_total)}${t("dashboard.quotations.questionMark")}` : t("dashboard.quotations.rejectConfirm") }}
          </span>
          <BaseButton :variant="confirming === 'Accepted' ? 'primary' : 'accent'" :loading="busy" @click="decide(confirming)">
            {{ confirming === "Accepted" ? t("dashboard.quotations.accept") : t("dashboard.quotations.reject") }}
          </BaseButton>
          <BaseButton variant="outline" :disabled="busy" @click="confirming = null">{{ t("dashboard.cancel") }}</BaseButton>
        </div>
        <div v-else class="mt-4 flex flex-wrap gap-3">
          <BaseButton @click="ask('Accepted')">
            <LucideCheck class="size-4" aria-hidden="true" />
            {{ t("dashboard.quotations.accept") }}
          </BaseButton>
          <BaseButton variant="outline" @click="ask('Rejected')">
            <LucideX class="size-4" aria-hidden="true" />
            {{ t("dashboard.quotations.reject") }}
          </BaseButton>
        </div>
      </div>
      <BaseNotice v-else-if="quotation.status === 'Accepted'" kind="success" class="mt-4">{{ t("dashboard.quotations.accepted") }}</BaseNotice>
      <BaseNotice v-else-if="quotation.status === 'Rejected'" class="mt-4">{{ t("dashboard.quotations.rejected") }}</BaseNotice>

      <!-- The conversation with the team, read only: the producer's one comment is a rejection's reason -->
      <h3 class="mt-6 flex items-center gap-2 text-caption font-bold text-site-heading">
        <LucideMessageSquare class="size-4" aria-hidden="true" />
        {{ t("dashboard.quotations.conversation") }}
      </h3>
      <CommentThread :key="threadKey" :load="loadThread" />
    </template>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref, useId } from "vue"
import { useI18n } from "vue-i18n"
import LucideCheck from "~icons/lucide/check"
import LucideChevronDown from "~icons/lucide/chevron-down"
import LucideContainer from "~icons/lucide/container"
import LucideFileBarChart from "~icons/lucide/file-bar-chart"
import LucideMessageSquare from "~icons/lucide/message-square"
import LucideRepeat from "~icons/lucide/repeat"
import LucideTruck from "~icons/lucide/truck"
import LucideX from "~icons/lucide/x"

import BaseButton from "@/components/base/BaseButton.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import CommentThread from "@/components/dashboard/CommentThread.vue"
import { refusal } from "@/composables/useFormSubmit"
import {
	type QuotationCollection,
	type QuotationDetail,
	decideQuotation,
	getQuotation,
	getQuotationThread,
} from "@/services/portal"
import { type PluralForms, counted, formatMoney } from "@/utils/format"

const props = defineProps<{ name: string }>()
const emit = defineEmits<{
	/** The producer answered: the list shows the quotation's new status, in its colour. */
	decided: [quotation: QuotationDetail]
}>()

const { t, locale } = useI18n()
const commentId = useId()
const quotation = ref<QuotationDetail | null>(null)
const failed = ref("")
const comment = ref("")
const confirming = ref<"Accepted" | "Rejected" | null>(null)
const decisionError = ref("")
const busy = ref(false)
/** Reloads the conversation after an answer (its comment joins it). */
const threadKey = ref(0)

onMounted(async () => {
	try {
		quotation.value = await getQuotation(props.name)
	} catch (error) {
		failed.value = refusal(error, t)
	}
})

const EMPTY_AMOUNTS: QuotationDetail["amounts"] = {
	currency: "SAR",
	net_total: 0,
	taxes: [],
	discount: 0,
	grand_total: 0,
	rounded_total: 0,
	in_words: null,
}
const amounts = computed(() => quotation.value?.amounts ?? EMPTY_AMOUNTS)

function money(value: number): string {
	return formatMoney(value, amounts.value.currency, locale.value)
}

function formatDate(value: string): string {
	return new Intl.DateTimeFormat(locale.value, { dateStyle: "medium" }).format(
		new Date(`${value}T00:00:00`),
	)
}

/** A counted phrase from its plural forms in the messages (utils/format: counted). */
function count(value: number, key: string, lead = ""): string {
	const forms = Object.fromEntries(
		(["one", "two", "few", "many", "other"] as const).map((form) => [
			form,
			t(`${key}.${form}`),
		]),
	) as PluralForms
	return counted(value, forms, locale.value, lead)
}

/** "twice a day", "3 times every 2 weeks", "مرتان كل يوم"… */
function frequency({
	count: times,
	period_count,
	period_uom,
}: QuotationCollection): string {
	return `${count(times, "dashboard.quotations.times")} ${count(
		period_count,
		`dashboard.quotations.periods.${period_uom}`,
		t("dashboard.quotations.every"),
	)}`
}

/** The service period: its dates and duration, or from its start for a service without an end date. */
const periodText = computed(() => {
	const period = quotation.value?.period
	if (!period?.start_date) return ""
	const { start_date, end_date, duration, duration_uom } = period
	if (!end_date || !duration_uom)
		return `${t("dashboard.quotations.from")} ${formatDate(start_date)}`
	const length = count(
		Number(duration),
		`dashboard.quotations.durations.${duration_uom}`,
	)
	return `${formatDate(start_date)} – ${formatDate(end_date)} · ${length}`
})

/** The conversation, read afresh (CommentThread refreshes it); a status the team or the producer has
 *  changed elsewhere reloads the quotation too. */
async function loadThread() {
	const thread = await getQuotationThread(props.name)
	if (quotation.value && thread.status !== quotation.value.status) {
		quotation.value = await getQuotation(props.name)
		emit("decided", quotation.value)
	}
	return thread
}

function ask(decision: "Accepted" | "Rejected") {
	decisionError.value =
		decision === "Rejected" && !comment.value.trim()
			? t("dashboard.quotations.reasonRequired")
			: ""
	if (!decisionError.value) confirming.value = decision
}

async function decide(decision: "Accepted" | "Rejected") {
	busy.value = true
	try {
		// Only a rejection carries the producer's words (its reason)
		quotation.value = await decideQuotation(
			props.name,
			decision,
			decision === "Rejected" ? comment.value.trim() : "",
		)
		comment.value = ""
		threadKey.value++
		emit("decided", quotation.value)
	} catch (error) {
		decisionError.value = refusal(error, t)
	} finally {
		busy.value = false
		confirming.value = null
	}
}
</script>
