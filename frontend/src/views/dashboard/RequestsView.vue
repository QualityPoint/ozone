<template>
  <!-- Service requests (ozone/portal/requests.py): the producer's requests, and the form to ask for
       a service at one of its facilities. A request is a Draft the producer can change until it sends
       it; then Ozone's sales team reviews it, and may ask for clarification in its comments
       (CommentThread) before the quotation; a request that has turned into one moves to the Quotations page. The form asks only what the producer knows: the size in the Service Setup's unit, the
       wastes of each waste type (its defaults start it, and stay unless the service allows removing them;
       others may be added), the annexes a composite
       facility's request covers, when it starts and for how long, and the license it holds when
       the service grants one. -->
  <section>
    <DashboardHeading :title="t('dashboard.nav.requests')" :intro="t('dashboard.requests.intro')">
      <BaseButton v-if="!editing && options?.facilities.length" @click="open()">
        <LucidePlus class="size-4" aria-hidden="true" />
        {{ t("dashboard.requests.add") }}
      </BaseButton>
    </DashboardHeading>
    <BaseNotice v-if="failed" class="mt-8">{{ t("dashboard.loadFailed") }}</BaseNotice>
    <BaseNotice v-if="sent" kind="success" class="mt-8">{{ t(sent) }}</BaseNotice>
    <p v-if="options && !options.facilities.length" class="mt-8 text-site-muted">
      {{ t("dashboard.requests.noFacilities") }}
      <RouterLink :to="facilitiesLink" class="font-bold text-brand-green underline dark:text-brand-leaf">{{ t("dashboard.nav.facilities") }}</RouterLink>
    </p>

    <BaseCard v-if="editing && options" as="form" class="mt-8 p-6" novalidate @submit.prevent="send(false)">
      <h2 class="text-title font-extrabold text-site-heading">
        {{ editingName ? t("dashboard.requests.editTitle") : t("dashboard.requests.addTitle") }}
        <span v-if="editingName" class="text-caption font-bold text-site-muted" dir="ltr">{{ editingName }}</span>
      </h2>
      <BaseNotice v-if="form.notice.value" :kind="form.notice.value.kind" class="mt-4">{{ form.notice.value.text }}</BaseNotice>
      <BaseNotice v-if="formFailed" class="mt-4">{{ formFailed }}</BaseNotice>
      <div class="mt-5 grid gap-5 md:grid-cols-2">
        <BaseSelect v-model="draft.facility" :label="t('dashboard.requests.facility')" :options="options.facilities" :placeholder="t('dashboard.requests.facilityPick')" :error="form.errors.value.facility" />
        <BaseSelect v-model="draft.service_type" :label="t('dashboard.requests.service')" :options="options.service_types" :placeholder="t('dashboard.requests.servicePick')" :error="form.errors.value.service_type" />

        <template v-if="spec">
          <BaseSelect v-model="draft.facility_uom" :label="t('dashboard.requests.measure')" :options="spec.uoms" />
          <template v-if="unit && !unit.composite">
            <BaseInput v-model="draft.facility_measurement" :label="t('dashboard.requests.measurement')" type="number" inputmode="decimal" min="0" :step="unit.whole_number ? 1 : 'any'" dir="ltr" :error="form.errors.value.facility_measurement" />
          </template>
          <template v-else-if="unit">
            <BaseInput
              v-for="part in unit.parts"
              :key="part.value"
              v-model="parts[part.value]"
              :label="part.label"
              type="number"
              inputmode="decimal"
              min="0"
              :step="part.whole_number ? 1 : 'any'"
              dir="ltr"
              :error="form.errors.value[`part:${part.value}`]"
            />
          </template>
          <!-- The dates: the start, and the end when the service has one (from its minimum period at the
               earliest); the duration and its unit follow from them (utils/duration, as naqel sets them) -->
          <BaseInput v-model="draft.start_date" :label="t('dashboard.requests.startDate')" type="date" :error="form.errors.value.start_date" />
          <template v-if="spec.has_end_date">
            <BaseInput v-model="draft.end_date" :label="t('dashboard.requests.endDate')" type="date" :min="minimumEnd || draft.start_date || undefined" :error="form.errors.value.end_date" />
            <div class="grid grid-cols-[minmax(0,1fr)_minmax(0,1fr)] gap-3 md:col-start-2">
              <BaseInput :model-value="duration ? String(duration.count) : ''" :label="t('dashboard.requests.duration')" dir="ltr" readonly />
              <BaseInput :model-value="durationUnit" :label="t('dashboard.requests.durationUom')" readonly />
            </div>
          </template>
          <template v-if="spec.grants_license">
            <BaseSelect v-model="draft.license_status" :label="t('dashboard.requests.licenseStatus')" :options="spec.license_statuses" :placeholder="t('dashboard.establishment.pick')" :error="form.errors.value.license_status" />
            <template v-if="draft.license_status === 'Renewal'">
              <BaseInput v-model="draft.license_no" :label="t('dashboard.requests.licenseNo')" dir="ltr" :error="form.errors.value.license_no" />
              <FileField v-model="draft.license_document" :label="t('dashboard.requests.licenseDocument')" />
            </template>
          </template>
        </template>
      </div>

      <!-- The document the service requires (one of its Registration Documents): kept with the facility, so a
           facility that already holds one shows it, and isn't asked again -->
      <fieldset v-if="spec?.documents.required.length" class="mt-8">
        <legend class="text-caption font-bold text-site-heading">{{ t("dashboard.requests.document") }}</legend>
        <p class="mt-1 text-caption text-site-muted">{{ t("dashboard.requests.documentHint") }}</p>
        <div
          v-if="spec.documents.on_file"
          class="mt-3 flex flex-wrap items-center gap-3 rounded-2xl border-2 border-brand-leaf/60 bg-brand-leaf/10 px-4 py-3"
        >
          <LucideFileCheck class="size-5 text-brand-green dark:text-brand-leaf" aria-hidden="true" />
          <span class="font-bold text-site-heading">{{ spec.documents.on_file.label }}</span>
          <span class="text-site-text" dir="ltr">{{ spec.documents.on_file.document_number }}</span>
          <span class="ms-auto text-caption font-bold text-brand-green dark:text-brand-leaf">{{ t("dashboard.requests.documentOnFile") }}</span>
        </div>
        <div v-else class="mt-4 grid gap-5 md:grid-cols-2">
          <BaseSelect v-model="doc.key" :label="t('dashboard.facilities.documentType')" :options="documentOptions" :placeholder="t('dashboard.facilities.documentPick')" :error="form.errors.value['document:type']" />
          <BaseInput v-model="doc.document_number" :label="t('dashboard.facilities.documentNumber')" dir="ltr" :error="form.errors.value['document:number']" />
          <BaseInput v-model="doc.issue_date" :label="t('dashboard.facilities.issueDate')" type="date" />
          <BaseInput v-if="documentType?.has_expiry_date" v-model="doc.expiry_date" :label="t('dashboard.facilities.expiryDate')" type="date" />
          <FileField v-model="doc.credential" :label="t('dashboard.facilities.file')" :error="form.errors.value['document:file']" class="md:col-span-2" />
        </div>
      </fieldset>

      <!-- The wastes of each waste type: its defaults to start with (locked when the service keeps them), and
           the others the producer adds -->
      <fieldset v-if="spec?.waste_types.length" class="mt-8">
        <legend class="text-caption font-bold text-site-heading">{{ t("dashboard.requests.wastes") }}</legend>
        <p class="mt-1 text-caption text-site-muted">
          {{ spec.defaults_locked ? t("dashboard.requests.wastesHint") : t("dashboard.requests.wastesHintOpen") }}
        </p>
        <div class="mt-4 grid gap-4 lg:grid-cols-3">
          <div v-for="type in spec.waste_types" :key="type.waste_type" class="rounded-2xl border-2 border-site-line p-4">
            <p class="flex items-baseline justify-between gap-3 font-extrabold text-site-heading">
              {{ type.label }}
              <span class="text-caption font-bold text-site-muted" dir="ltr">{{ type.percentage }}%</span>
            </p>
            <ul class="mt-3 flex flex-wrap gap-2">
              <template v-for="name in chosen[type.waste_type]" :key="name">
              <li
                v-if="isLocked(type, name)"
                class="inline-flex items-center gap-1.5 rounded-full bg-brand-green px-3 py-1 text-label font-bold text-white"
                :title="t('dashboard.requests.defaultWaste')"
              >
                <LucideLock class="size-3" aria-hidden="true" />
                {{ wasteLabel(type, name) }}
              </li>
              <li
                v-else
                class="inline-flex items-center gap-1 rounded-full border-2 border-brand-green px-3 py-0.5 text-label font-bold text-site-heading dark:border-brand-leaf"
              >
                {{ wasteLabel(type, name) }}
                <button
                  type="button"
                  class="grid size-5 place-items-center rounded-full hover:bg-site-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
                  :aria-label="`${t('dashboard.cancel')} ${wasteLabel(type, name)}`"
                  @click="removeWaste(type.waste_type, name)"
                >
                  <LucideX class="size-3.5" aria-hidden="true" />
                </button>
              </li>
              </template>
            </ul>
            <p v-if="form.errors.value[`wastes:${type.waste_type}`]" class="mt-2 text-caption font-bold text-brand-red dark:text-brand-red-300">
              {{ form.errors.value[`wastes:${type.waste_type}`] }}
            </p>
            <BaseSelect
              v-if="addable(type).length"
              :model-value="''"
              :label="t('dashboard.requests.addWaste')"
              :options="addable(type)"
              :placeholder="t('dashboard.requests.wastePick')"
              class="mt-4"
              @update:model-value="addWaste(type.waste_type, $event)"
            />
          </div>
        </div>
      </fieldset>

      <!-- A composite facility: the annexes the request covers -->
      <fieldset v-if="spec?.annexes.length" class="mt-8">
        <legend class="text-caption font-bold text-site-heading">{{ t("dashboard.requests.annexes") }}</legend>
        <p class="mt-1 text-caption text-site-muted">{{ t("dashboard.requests.annexesHint") }}</p>
        <div class="mt-3 flex flex-wrap gap-3">
          <label
            v-for="annex in spec.annexes"
            :key="annex.value"
            class="flex cursor-pointer items-center gap-3 rounded-2xl border-2 border-site-line px-4 py-3 font-bold text-site-heading has-[:checked]:border-brand-green dark:has-[:checked]:border-brand-leaf"
          >
            <input v-model="annexes" type="checkbox" :value="annex.value" class="size-5 rounded accent-brand-green" />
            {{ annex.label }}
          </label>
        </div>
      </fieldset>

      <!-- Saved as a Draft, it can still change; sent, it is Ozone's team's -->
      <p class="mt-8 text-caption text-site-muted">{{ t("dashboard.requests.submitHint") }}</p>
      <div class="mt-3 flex flex-wrap gap-3">
        <BaseButton :loading="form.busy.value && submitting" :disabled="!spec || form.busy.value" @click="send(true)">{{ t("dashboard.requests.submit") }}</BaseButton>
        <BaseButton type="submit" variant="outline" :loading="form.busy.value && !submitting" :disabled="!spec || form.busy.value">{{ t("dashboard.requests.saveDraft") }}</BaseButton>
        <BaseButton variant="outline" @click="editing = false">{{ t("dashboard.cancel") }}</BaseButton>
      </div>
    </BaseCard>

    <div v-if="requests && options && (requests.length || filtered)" class="mt-8 flex flex-wrap items-end gap-3">
      <BaseSelect v-model="filters.facility" :label="t('dashboard.requests.facility')" :options="withAll(options.facilities)" class="min-w-44 flex-1" />
      <BaseSelect v-model="filters.service_type" :label="t('dashboard.requests.service')" :options="withAll(options.service_types)" class="min-w-44 flex-1" />
      <BaseSelect v-model="filters.status" :label="t('dashboard.requests.status')" :options="withAll(options.statuses)" class="min-w-44 flex-1" />
    </div>
    <p v-if="requests && !requests.length && !editing" class="mt-8 text-site-muted">{{ t("dashboard.requests.none") }}</p>
    <ul class="mt-6 space-y-3">
      <li v-for="request in requests" :key="request.name">
        <BaseCard :class="['p-5', request.status === 'Require Clarification' ? 'ring-2 ring-brand-red/60' : '']">
          <div class="flex flex-wrap items-start justify-between gap-4">
            <div class="flex min-w-0 gap-4">
              <span class="grid size-11 shrink-0 place-items-center rounded-xl bg-site-hover text-brand-green dark:text-brand-leaf">
                <LucideClipboardList class="size-5" aria-hidden="true" />
              </span>
              <div class="min-w-0">
                <p class="font-extrabold text-site-heading">{{ request.service_title }}</p>
                <p class="mt-0.5 text-caption text-site-muted">{{ request.facility_title }} · <span dir="ltr">{{ request.name }}</span></p>
                <p class="mt-1 text-caption text-site-muted">{{ t("dashboard.requests.created") }}: {{ formatDate(request.creation) }}</p>
              </div>
            </div>
            <span :class="['rounded-full px-3 py-1 text-caption font-bold', statusBadge(request.status_color)]">{{ request.status_label }}</span>
          </div>

          <p v-if="request.status === 'Require Clarification'" class="mt-3 text-caption font-bold text-brand-red dark:text-brand-red-300">
            {{ t("dashboard.requests.clarify") }}
          </p>

          <BaseNotice v-if="rowError[request.name]" class="mt-3">{{ rowError[request.name] }}</BaseNotice>

          <!-- A Draft is the producer's: change it, or send it (after a confirmation: it can't change then) -->
          <div v-if="request.status === 'Draft'" class="mt-4 flex flex-wrap items-center gap-2">
            <template v-if="confirming === request.name">
              <span class="text-caption text-site-text">{{ t("dashboard.requests.submitConfirm") }}</span>
              <button type="button" :class="[rowButton, 'bg-brand-green text-white hover:bg-brand-green-700']" :disabled="busyRow === request.name" @click="submitDraft(request.name)">
                {{ t("dashboard.requests.submit") }}
              </button>
              <button type="button" :class="[rowButton, 'border-2 border-site-line text-site-heading hover:bg-site-hover']" @click="confirming = null">{{ t("dashboard.cancel") }}</button>
            </template>
            <template v-else>
              <button type="button" :class="[rowButton, 'border-2 border-site-line text-site-heading hover:bg-site-hover']" :disabled="busyRow === request.name || editing" @click="edit(request.name)">
                <LucidePencil class="size-3.5" aria-hidden="true" />
                {{ t("dashboard.edit") }}
              </button>
              <button type="button" :class="[rowButton, 'bg-brand-green text-white hover:bg-brand-green-700']" @click="confirming = request.name">
                <LucideSend class="size-3.5 rtl:-scale-x-100" aria-hidden="true" />
                {{ t("dashboard.requests.submit") }}
              </button>
            </template>
          </div>
          <!-- Sent: its comments with Ozone's team, open while the team waits for an answer -->
          <template v-else>
            <button
              type="button"
              :class="[rowButton, 'mt-4 border-2 border-site-line text-site-heading hover:bg-site-hover']"
              :aria-expanded="threadOpen(request)"
              @click="threads[request.name] = !threadOpen(request)"
            >
              <LucideMessageSquare class="size-3.5" aria-hidden="true" />
              {{ t("dashboard.requests.comments") }}
            </button>
            <CommentThread
              v-if="threadOpen(request)"
              :load="() => getServiceRequest(request.name)"
              :send="(text, files) => clarify(request, text, files)"
              :send-label="t('dashboard.requests.sendClarification')"
            />
          </template>
        </BaseCard>
      </li>
    </ul>
  </section>
</template>

<script lang="ts" setup>
import { computed, nextTick, onMounted, reactive, ref, watch } from "vue"
import { useI18n } from "vue-i18n"
import { useRoute } from "vue-router"
import LucideClipboardList from "~icons/lucide/clipboard-list"
import LucideFileCheck from "~icons/lucide/file-check"
import LucideLock from "~icons/lucide/lock"
import LucideMessageSquare from "~icons/lucide/message-square"
import LucidePencil from "~icons/lucide/pencil"
import LucidePlus from "~icons/lucide/plus"
import LucideSend from "~icons/lucide/send"
import LucideX from "~icons/lucide/x"

import BaseButton from "@/components/base/BaseButton.vue"
import BaseCard from "@/components/base/BaseCard.vue"
import BaseInput from "@/components/base/BaseInput.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import BaseSelect from "@/components/base/BaseSelect.vue"
import CommentThread from "@/components/dashboard/CommentThread.vue"
import DashboardHeading from "@/components/dashboard/DashboardHeading.vue"
import FileField from "@/components/dashboard/FileField.vue"
import { refusal, useFormSubmit } from "@/composables/useFormSubmit"
import { dashboardPath, localePath } from "@/config/site"
import {
	type Option,
	type RequestDetail,
	type RequestForm,
	type RequestOptions,
	type RequestWasteType,
	type ServiceRequest,
	clarifyRequest,
	getRequestForm,
	getRequestOptions,
	getServiceRequest,
	getServiceRequests,
	saveServiceRequest,
	submitServiceRequest,
} from "@/services/portal"
import type { LocaleCode } from "@/types"
import { durationBetween, minimumEndDate } from "@/utils/duration"
import { statusBadge } from "@/utils/status"

const { t, locale } = useI18n()
const route = useRoute()

const requests = ref<ServiceRequest[] | null>(null)
const options = ref<RequestOptions | null>(null)
const failed = ref(false)
/** The success message's key: a request sent, or a draft saved. */
const sent = ref("")
const filters = reactive({ facility: "", service_type: "", status: "" })
const filtered = computed(() => Object.values(filters).some(Boolean))
const facilitiesLink = computed(() =>
	localePath(`${dashboardPath}/facilities`, locale.value as LocaleCode),
)

onMounted(async () => {
	try {
		;[requests.value, options.value] = await Promise.all([
			getServiceRequests(),
			getRequestOptions(),
		])
	} catch {
		failed.value = true
		return
	}
	// Opened from a facility's "Request a service": the form starts on that facility.
	const facility =
		typeof route.query.facility === "string" ? route.query.facility : ""
	if (facility && options.value.facilities.some((f) => f.value === facility))
		open(facility)
})

// Each filter change fetches anew; only the latest call's answer is shown. A reset after sending
// already has the fresh list, so it doesn't fetch again.
let fetches = 0
let skipFetch = false
watch(filters, async () => {
	if (skipFetch) {
		skipFetch = false
		return
	}
	const call = ++fetches
	try {
		const result = await getServiceRequests(
			Object.fromEntries(Object.entries(filters).filter(([, value]) => value)),
		)
		if (call === fetches) requests.value = result
	} catch {
		if (call === fetches) failed.value = true
	}
})

const rowButton =
	"inline-flex items-center gap-1.5 rounded-full px-4 py-1.5 text-label font-bold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf disabled:opacity-60"

// A sent request's comments: shown while Ozone's team waits for an answer, else when opened.
const threads = reactive<Record<string, boolean>>({})
function threadOpen(request: ServiceRequest): boolean {
	return threads[request.name] ?? request.status === "Require Clarification"
}

/** The producer's answer to the team's clarification: the request is Clarified at once (the team asks
 *  again or quotes it), and its thread stays open on the answer. */
async function clarify(request: ServiceRequest, text: string, files: string[]) {
	const detail = await clarifyRequest(request.name, text, files)
	request.status = detail.status
	request.status_label = detail.status_label
	request.status_color = detail.status_color
	threads[request.name] = true
	return detail
}

// Sending a Draft from the list.
const confirming = ref<string | null>(null)
const busyRow = ref<string | null>(null)
const rowError = reactive<Record<string, string>>({})

async function submitDraft(name: string) {
	busyRow.value = name
	delete rowError[name]
	try {
		const result = await submitServiceRequest(name)
		showList(result.requests)
		sent.value = "dashboard.requests.sent"
	} catch (error) {
		rowError[name] = refusal(error, t)
	} finally {
		busyRow.value = null
		confirming.value = null
	}
}

/** A list fresh from the server (all requests): the filters are cleared without fetching again. */
function showList(list: ServiceRequest[]) {
	fetches++ // an older filter fetch still running mustn't replace this list
	if (Object.values(filters).some(Boolean)) {
		skipFetch = true
		Object.assign(filters, { facility: "", service_type: "", status: "" })
	}
	requests.value = list
}

function withAll(list: Option[]): Option[] {
	return [{ value: "", label: t("dashboard.requests.all") }, ...list]
}

function formatDate(value: string): string {
	return new Intl.DateTimeFormat(locale.value, { dateStyle: "medium" }).format(
		new Date(value.replace(" ", "T")),
	)
}

// The form: a new request, or a Draft being changed (editingName).
const editing = ref(false)
const editingName = ref<string | null>(null)
/** Whether the form is being sent to Ozone's team (else saved as a Draft). */
const submitting = ref(false)
/** A Draft's values, applied once its facility and service have loaded the form. */
let prefill: RequestDetail["values"] | null = null
const spec = ref<RequestForm | null>(null)
const formFailed = ref("")
const draft = reactive(blank())
const parts = reactive<Record<string, string>>({})
/** Each waste type's wastes, as chosen: its defaults to start with, then those the producer adds. */
const chosen = reactive<Record<string, string[]>>({})
/** The annexes a composite facility's request covers: all of them, unless unticked. */
const annexes = ref<string[]>([])
/** The required document, when the facility has none on file: one of the service's, numbered and uploaded. */
const doc = reactive(blankDocument())

function blankDocument() {
	return {
		key: "",
		document_number: "",
		credential: null as string | null,
		issue_date: "",
		expiry_date: "",
	}
}
const documentOptions = computed(() =>
	(spec.value?.documents.required ?? []).map((d) => ({
		value: `${d.credential_type}::${d.document_type}`,
		label: d.label,
	})),
)
const documentType = computed(() =>
	spec.value?.documents.required.find(
		(d) => `${d.credential_type}::${d.document_type}` === doc.key,
	),
)
const documentNeeded = computed(
	() =>
		Boolean(spec.value?.documents.required.length) &&
		!spec.value?.documents.on_file,
)

function blank() {
	return {
		facility: "",
		service_type: "",
		facility_uom: "",
		facility_measurement: "",
		start_date: "",
		end_date: "",
		license_status: "",
		license_no: "",
		license_document: "" as string | null,
	}
}

function open(facility = "") {
	Object.assign(draft, blank(), { facility })
	editingName.value = null
	prefill = null
	spec.value = null
	formFailed.value = ""
	sent.value = ""
	form.reset()
	editing.value = true
}

/** Change a Draft: the form opens on its values. */
async function edit(name: string) {
	busyRow.value = name
	delete rowError[name]
	let detail: RequestDetail
	try {
		detail = await getServiceRequest(name)
	} catch (error) {
		rowError[name] = refusal(error, t)
		return
	} finally {
		busyRow.value = null
	}
	const values = detail.values
	open()
	editingName.value = name
	prefill = values
	Object.assign(draft, {
		facility: values.facility,
		service_type: values.service_type,
		start_date: values.start_date ?? "",
		end_date: values.end_date ?? "",
		license_status: values.license_status ?? "",
		license_no: values.license_no ?? "",
		license_document: values.license_document,
	})
	window.scrollTo({ top: 0, behavior: "smooth" })
}

/** A Draft's own size, wastes and annexes, once the form for its facility and service is known. */
async function applyPrefill(result: RequestForm) {
	const values = prefill
	prefill = null
	if (!values) return
	if (result.uoms.some((u) => u.value === values.facility_uom))
		draft.facility_uom = values.facility_uom ?? ""
	draft.facility_measurement = values.facility_measurement
		? String(values.facility_measurement)
		: ""
	for (const row of values.waste_types) {
		if (row.waste_type in chosen) chosen[row.waste_type] = [...row.wastes]
	}
	const annexNames = new Set(result.annexes.map((annex) => annex.value))
	annexes.value = values.annexes.filter((name) => annexNames.has(name))
	await nextTick() // after the unit's own reset of its parts
	for (const part of values.facility_uoms)
		parts[part.uom] = String(part.uom_value)
}

/** A Duration-Based service's earliest end date: the end date starts there, or moves up to it. */
const minimumEnd = computed(() =>
	minimumEndDate(draft.start_date, spec.value?.minimum_period ?? null),
)
watch(minimumEnd, (minimum) => {
	if (minimum && (!draft.end_date || draft.end_date < minimum))
		draft.end_date = minimum
})

/** The service's duration, from its dates (naqel sets the same on save). */
const duration = computed(() =>
	durationBetween(draft.start_date, draft.end_date),
)
const durationUnit = computed(() => {
	const uom = duration.value?.uom
	return uom
		? (spec.value?.duration_uoms.find((u) => u.value === uom)?.label ?? uom)
		: ""
})

/** The chosen unit, and whether it is measured part by part. */
const unit = computed(
	() => spec.value?.uoms.find((u) => u.value === draft.facility_uom) ?? null,
)

// A facility and a service decide how the request is measured.
watch(
	() => [draft.facility, draft.service_type] as const,
	async ([facility, serviceType]) => {
		spec.value = null
		formFailed.value = ""
		if (!facility || !serviceType) return
		try {
			const result = await getRequestForm(
				facility,
				serviceType,
				editingName.value,
			)
			if (draft.facility !== facility || draft.service_type !== serviceType)
				return
			spec.value = result
			draft.facility_uom = result.uoms[0]?.value ?? ""
			for (const key of Object.keys(chosen)) delete chosen[key]
			for (const type of result.waste_types)
				chosen[type.waste_type] = type.defaults.map((waste) => waste.value)
			annexes.value = result.annexes.map((annex) => annex.value)
			Object.assign(doc, blankDocument())
			if (
				prefill?.facility === facility &&
				prefill.service_type === serviceType
			)
				await applyPrefill(result)
			else prefill = null
		} catch (error) {
			formFailed.value = refusal(error, t)
		}
	},
)
watch(unit, () => {
	for (const key of Object.keys(parts)) delete parts[key]
})

/** The wastes a type can still take: its own, less those already chosen. */
function addable(type: RequestWasteType): Option[] {
	const taken = new Set(chosen[type.waste_type] ?? [])
	return type.wastes.filter((waste) => !taken.has(waste.value))
}

/** A default waste the service keeps (it can't be removed). */
function isLocked(type: RequestWasteType, name: string): boolean {
	return (
		Boolean(spec.value?.defaults_locked) &&
		type.defaults.some((waste) => waste.value === name)
	)
}

function wasteLabel(type: RequestWasteType, name: string): string {
	const known = [...type.defaults, ...type.wastes]
	return known.find((waste) => waste.value === name)?.label ?? name
}

function addWaste(wasteType: string, name: string) {
	if (name && !chosen[wasteType]?.includes(name)) chosen[wasteType]?.push(name)
}

function removeWaste(wasteType: string, name: string) {
	chosen[wasteType] = (chosen[wasteType] ?? []).filter(
		(waste) => waste !== name,
	)
}

/** A size: above zero, and whole when the unit counts things. */
function sizeError(value: string, whole: 0 | 1): string | undefined {
	const number = Number(value)
	if (!value || !(number > 0)) return t("dashboard.requests.positive")
	if (whole && !Number.isInteger(number))
		return t("dashboard.requests.wholeNumber")
	return undefined
}

const form = useFormSubmit<string>({
	validate: () => {
		const errors: Record<string, string> = {}
		const required = t("auth.errors.required")
		if (!draft.facility) errors.facility = required
		if (!draft.service_type) errors.service_type = required
		if (!spec.value) return errors
		if (unit.value && !unit.value.composite) {
			const error = sizeError(
				draft.facility_measurement,
				unit.value.whole_number,
			)
			if (error) errors.facility_measurement = error
		}
		for (const part of unit.value?.composite ? unit.value.parts : []) {
			const error = sizeError(parts[part.value] ?? "", part.whole_number)
			if (error) errors[`part:${part.value}`] = error
		}
		if (!draft.start_date) errors.start_date = required
		for (const type of spec.value.waste_types) {
			if (!(chosen[type.waste_type] ?? []).length)
				errors[`wastes:${type.waste_type}`] = t(
					"dashboard.requests.wasteRequired",
				)
		}
		if (documentNeeded.value) {
			if (!doc.key) errors["document:type"] = required
			if (!doc.document_number.trim()) errors["document:number"] = required
			if (!doc.credential)
				errors["document:file"] = t("dashboard.facilities.fileRequired")
		}
		if (spec.value.has_end_date) {
			if (!draft.end_date) errors.end_date = required
			else if (draft.start_date && draft.end_date < draft.start_date)
				errors.end_date = t("dashboard.requests.endBeforeStart")
			else if (minimumEnd.value && draft.end_date < minimumEnd.value)
				errors.end_date = t("dashboard.requests.endBeforeMinimum")
		}
		if (spec.value.grants_license && !draft.license_status)
			errors.license_status = required
		if (draft.license_status === "Renewal" && !draft.license_no.trim())
			errors.license_no = required
		return errors
	},
	send: async () => {
		const composite = unit.value?.composite
		const renewal =
			Boolean(spec.value?.grants_license) && draft.license_status === "Renewal"
		const result = await saveServiceRequest({
			name: editingName.value ?? undefined,
			submit: submitting.value,
			facility: draft.facility,
			service_type: draft.service_type,
			facility_uom: draft.facility_uom,
			facility_measurement: composite
				? null
				: Number(draft.facility_measurement),
			facility_uoms: composite
				? (unit.value?.parts ?? []).map((part) => ({
						uom: part.value,
						uom_value: Number(parts[part.value]),
					}))
				: undefined,
			start_date: draft.start_date,
			end_date: spec.value?.has_end_date ? draft.end_date : null,
			license_status: draft.license_status || undefined,
			// A renewal's number and document only: switching back to a new issue drops them.
			license_no: renewal ? draft.license_no.trim() || undefined : undefined,
			license_document: renewal ? draft.license_document || null : null,
			waste_types: (spec.value?.waste_types ?? []).map((type) => ({
				waste_type: type.waste_type,
				wastes: chosen[type.waste_type] ?? [],
			})),
			annexes: spec.value?.annexes.length ? annexes.value : undefined,
			document:
				documentNeeded.value && documentType.value
					? {
							credential_type: documentType.value.credential_type,
							document_type: documentType.value.document_type,
							document_number: doc.document_number.trim(),
							credential: doc.credential,
							issue_date: doc.issue_date || null,
							expiry_date: doc.expiry_date || null,
						}
					: undefined,
		})
		showList(result.requests)
	},
})

async function send(submit: boolean) {
	submitting.value = submit
	if (await form.submit()) {
		editing.value = false
		editingName.value = null
		sent.value = submit
			? "dashboard.requests.sent"
			: "dashboard.requests.draftSaved"
	}
}
</script>
