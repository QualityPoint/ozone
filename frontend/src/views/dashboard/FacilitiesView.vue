<template>
  <!-- Facilities and annexes: the producer's Facility tree (ozone/portal/facilities.py). A composite
       facility can have annexes; each has its activity, its address and a pin (its rating is the desk's own, never shown here). Its
       documents come with the services it requests (the request form); a composite facility gives
       here the one its annexes share, which they carry too. -->
  <section>
    <DashboardHeading :title="t('dashboard.nav.facilities')" :intro="t('dashboard.facilities.intro')">
      <BaseButton v-if="!editing && settings" @click="edit(null)">
        <LucidePlus class="size-4" aria-hidden="true" />
        {{ t("dashboard.facilities.add") }}
      </BaseButton>
    </DashboardHeading>
    <BaseNotice v-if="failed" class="mt-8">{{ t("dashboard.loadFailed") }}</BaseNotice>
    <!-- The first step: a new producer starts here, with the form open -->
    <BaseNotice v-if="first && editing" kind="success" class="mt-8">{{ t("dashboard.facilities.firstStep") }}</BaseNotice>
    <!-- Then the next one: a service for the facility just registered -->
    <BaseNotice v-if="created && !editing" kind="success" class="mt-8">
      {{ t("dashboard.facilities.firstSaved") }}
      <RouterLink :to="requestLink(created)" class="ms-1 font-bold text-brand-green underline dark:text-brand-leaf">
        {{ t("dashboard.facilities.requestService") }}
      </RouterLink>
    </BaseNotice>

    <BaseCard v-if="editing && settings" as="form" class="mt-8 p-6" novalidate @submit.prevent="saveForm">
      <h2 class="text-title font-extrabold text-site-heading">
        {{ draft.name ? t("dashboard.facilities.editTitle") : t("dashboard.facilities.addTitle") }}
      </h2>
      <BaseNotice v-if="form.notice.value" :kind="form.notice.value.kind" class="mt-4">{{ form.notice.value.text }}</BaseNotice>
      <div class="mt-5 grid gap-5 md:grid-cols-2">
        <BaseInput v-model="draft.facility_name" :label="t('dashboard.facilities.name')" :error="form.errors.value.facility_name" required />
        <IsicPicker
          :key="formKey"
          v-model="draft.isic_classification"
          :initial="draftIsic"
          :label="t('dashboard.facilities.isic')"
          :error="form.errors.value.isic_classification"
        />
        <BaseSelect v-model="kind" :label="t('dashboard.facilities.kind')" :options="kinds" />
        <BaseSelect
          v-if="kind === 'branch'"
          v-model="parent"
          :label="t('dashboard.facilities.parent')"
          :options="parents"
          :placeholder="t('dashboard.facilities.parentPick')"
          :error="form.errors.value.parent_facility"
        />
      </div>

      <h3 class="mt-8 text-body-lg font-extrabold text-site-heading">{{ t("dashboard.facilities.address") }}</h3>
      <div class="mt-4 grid gap-5 md:grid-cols-2">
        <!-- The region (Naqel Settings): it fills the city and the district -->
        <RegionPicker
          v-if="settings.requires_region"
          :key="formKey"
          v-model="draft.region"
          :label="regionLabel"
          :chosen="draftRegion"
          :error="form.errors.value.region"
          class="md:col-span-2"
          @pick="applyRegion"
        />
        <BaseInput v-model="draft.street" :label="t('dashboard.facilities.street')" :error="form.errors.value.street" autocomplete="address-line1" required />
        <BaseInput v-model="draft.building_no" :label="t('dashboard.facilities.buildingNo')" dir="ltr" />
        <BaseInput v-model="draft.secondary_no" :label="t('dashboard.facilities.secondaryNo')" dir="ltr" />
        <!-- At the District level the region is the district (the server fills it from the region) -->
        <BaseInput v-if="settings.region_level !== 'District'" v-model="draft.district" :label="t('dashboard.facilities.district')" :readonly="regionFills.district" />
        <BaseInput v-model="draft.city" :label="t('dashboard.facilities.city')" :error="form.errors.value.city" autocomplete="address-level2" :readonly="regionFills.city" required />
        <BaseInput v-model="draft.pincode" :label="t('dashboard.facilities.pincode')" autocomplete="postal-code" dir="ltr" />
        <BaseInput v-model="draft.country" :label="t('dashboard.facilities.country')" :error="form.errors.value.country" autocomplete="country-name" required />
      </div>

      <h3 class="mt-8 text-body-lg font-extrabold text-site-heading">{{ t("dashboard.facilities.map") }}</h3>
      <div class="mt-4 grid gap-5">
        <BaseInput v-model="draft.google_maps_location" :label="t('dashboard.facilities.location')" dir="ltr" autocomplete="off" />
        <p class="-mt-3 text-caption text-site-muted">{{ t("dashboard.facilities.locationHint") }}</p>
        <FacilityMap
          v-model:latitude="draft.latitude"
          v-model:longitude="draft.longitude"
          :label="t('dashboard.facilities.map')"
          :hint="t('dashboard.facilities.mapHint')"
          :center="settings.map"
          :error="form.errors.value.pin"
        />
      </div>

      <!-- Documents come with the services requested; a composite facility gives here the one its annexes share -->
      <template v-if="kind === 'main'">
      <h3 class="mt-8 text-body-lg font-extrabold text-site-heading">{{ t("dashboard.facilities.credentials") }}</h3>
      <p class="mt-1 text-caption text-site-muted">{{ t("dashboard.facilities.credentialsHint") }}</p>
      <p v-if="form.errors.value.credentials" class="mt-2 text-caption font-bold text-red-600 dark:text-red-400">{{ form.errors.value.credentials }}</p>
      <ul class="mt-4 space-y-4">
        <li v-for="(row, index) in draft.credentials" :key="index" class="rounded-xl border-2 border-site-line p-4">
          <div class="grid gap-4 md:grid-cols-2">
            <BaseSelect
              :model-value="documentKey(row)"
              :label="t('dashboard.facilities.documentType')"
              :options="documentOptions"
              :placeholder="t('dashboard.facilities.documentPick')"
              :error="form.errors.value[`credential:${index}:type`]"
              @update:model-value="(value: string) => setDocument(row, value)"
            />
            <BaseInput v-model="row.document_number" :label="t('dashboard.facilities.documentNumber')" dir="ltr" :error="form.errors.value[`credential:${index}:number`]" />
            <BaseInput :model-value="row.issue_date ?? ''" :label="t('dashboard.facilities.issueDate')" type="date" @update:model-value="(value: string) => (row.issue_date = value || null)" />
            <BaseInput
              v-if="documentOf(row)?.has_expiry_date"
              :model-value="row.expiry_date ?? ''"
              :label="t('dashboard.facilities.expiryDate')"
              type="date"
              @update:model-value="(value: string) => (row.expiry_date = value || null)"
            />
            <FileField v-model="row.credential" :label="t('dashboard.facilities.file')" :error="form.errors.value[`credential:${index}:file`]" class="md:col-span-2" />
          </div>
          <div class="mt-3 flex items-center justify-between gap-3">
            <span v-if="documentOf(row)?.eligible_for_multiple_facility_branches" class="rounded-full bg-site-hover px-3 py-1 text-caption font-bold text-brand-green dark:text-brand-leaf">
              {{ t("dashboard.facilities.shared") }}
            </span>
            <BaseButton variant="outline" class="ms-auto" @click="draft.credentials.splice(index, 1)">{{ t("dashboard.facilities.removeCredential") }}</BaseButton>
          </div>
        </li>
      </ul>
      <BaseButton variant="outline" class="mt-4" @click="draft.credentials.push(blankCredential())">
        <LucidePlus class="size-4" aria-hidden="true" />
        {{ t("dashboard.facilities.addCredential") }}
      </BaseButton>
      </template>

      <div class="mt-8 flex gap-3">
        <BaseButton type="submit" :loading="form.busy.value">{{ t("dashboard.save") }}</BaseButton>
        <BaseButton variant="outline" @click="editing = false">{{ t("dashboard.cancel") }}</BaseButton>
      </div>
    </BaseCard>

    <p v-if="facilities && !facilities.length && !editing" class="mt-8 text-site-muted">{{ t("dashboard.facilities.none") }}</p>
    <ul class="mt-8 space-y-3">
      <li v-for="facility in facilities" :key="facility.name" :class="{ 'ms-6 border-s-2 border-site-line ps-4 sm:ms-10': facility.parent_facility }">
        <BaseCard class="p-5">
          <div class="flex flex-wrap items-start justify-between gap-4">
            <div class="flex min-w-0 gap-4">
              <span class="grid size-11 shrink-0 place-items-center rounded-xl bg-site-hover text-brand-green dark:text-brand-leaf">
                <component :is="facility.is_group ? LucideBuilding2 : LucideStore" class="size-5" aria-hidden="true" />
              </span>
              <div class="min-w-0">
                <p class="font-extrabold text-site-heading">{{ facility.facility_name }}</p>
                <p class="mt-0.5 text-caption text-site-muted">
                  {{ t(`dashboard.facilities.kinds.${kindOf(facility)}`) }}<template v-if="facility.isic_title"> · {{ facility.isic_title }}</template>
                </p>
                <p class="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 text-caption text-site-muted">
                  <span v-if="facility.latitude" class="inline-flex items-center gap-1">
                    <LucideMapPin class="size-4" aria-hidden="true" />
                    {{ facility.region_title ?? t("dashboard.facilities.pinned") }}
                  </span>
                  <span v-if="facility.city">{{ [facility.district, facility.city].filter(Boolean).join(t("dashboard.separator")) }}</span>
                </p>
              </div>
            </div>
            <div class="flex flex-wrap gap-1">
              <RouterLink :to="requestLink(facility.name)" class="inline-flex items-center gap-1 rounded-full px-3 py-2 text-caption font-bold text-brand-green transition hover:bg-site-hover dark:text-brand-leaf">
                <LucideClipboardPlus class="size-4" aria-hidden="true" />
                {{ t("dashboard.facilities.requestService") }}
              </RouterLink>
              <BaseButton v-if="facility.is_group" variant="outline" :disabled="editing" @click="edit(null, facility.name)">
                <LucidePlus class="size-4" aria-hidden="true" />
                {{ t("dashboard.facilities.addBranch") }}
              </BaseButton>
              <button
                type="button"
                class="grid size-10 place-items-center rounded-full text-site-muted transition hover:bg-site-hover hover:text-site-heading"
                :aria-label="t('dashboard.facilities.activity')"
                :title="t('dashboard.facilities.activity')"
                :aria-expanded="shown === facility.name"
                @click="toggleActivity(facility.name)"
              >
                <LucideHistory class="size-4" aria-hidden="true" />
              </button>
              <button
                type="button"
                class="grid size-10 place-items-center rounded-full text-site-muted transition hover:bg-site-hover hover:text-site-heading"
                :aria-label="t('dashboard.edit')"
                :title="t('dashboard.edit')"
                :disabled="editing"
                @click="edit(facility)"
              >
                <LucidePencil class="size-4" aria-hidden="true" />
              </button>
            </div>
          </div>
          <div v-if="shown === facility.name" class="mt-4 border-t-2 border-site-line pt-4">
            <p v-if="activityFailed" class="text-caption font-bold text-red-600 dark:text-red-400">{{ t("dashboard.loadFailed") }}</p>
            <p v-else-if="!activity" class="text-caption text-site-muted">…</p>
            <p v-else-if="!activityRows.length" class="text-caption text-site-muted">{{ t("dashboard.facilities.activityNone") }}</p>
            <dl v-else class="grid gap-3 text-caption sm:grid-cols-2">
              <div v-for="group in activityRows" :key="group.kind">
                <dt class="font-bold text-site-heading">{{ t(`dashboard.facilities.activityKinds.${group.kind}`) }}</dt>
                <dd v-for="row in group.rows" :key="row.name" class="mt-1 flex justify-between gap-3 text-site-muted">
                  <span dir="ltr">{{ row.name }}</span>
                  <span class="font-bold">{{ row.status_label }}</span>
                </dd>
              </div>
            </dl>
          </div>
        </BaseCard>
      </li>
    </ul>
  </section>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref, watch } from "vue"
import { useI18n } from "vue-i18n"
import LucideBuilding2 from "~icons/lucide/building-2"
import LucideClipboardPlus from "~icons/lucide/clipboard-plus"
import LucideHistory from "~icons/lucide/history"
import LucideMapPin from "~icons/lucide/map-pin"
import LucidePencil from "~icons/lucide/pencil"
import LucidePlus from "~icons/lucide/plus"
import LucideStore from "~icons/lucide/store"

import BaseButton from "@/components/base/BaseButton.vue"
import BaseCard from "@/components/base/BaseCard.vue"
import BaseInput from "@/components/base/BaseInput.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import BaseSelect from "@/components/base/BaseSelect.vue"
import DashboardHeading from "@/components/dashboard/DashboardHeading.vue"
import FacilityMap from "@/components/dashboard/FacilityMap.vue"
import FileField from "@/components/dashboard/FileField.vue"
import IsicPicker from "@/components/dashboard/IsicPicker.vue"
import RegionPicker from "@/components/dashboard/RegionPicker.vue"
import { useFormSubmit } from "@/composables/useFormSubmit"
import { dashboardPath, localePath } from "@/config/site"
import {
	type Credential,
	type DocumentType,
	type Facility,
	type FacilityActivity,
	type FacilityInput,
	type FacilitySettings,
	type RegionOption,
	getFacilities,
	getFacilityActivity,
	getFacilitySettings,
	regionAt,
	saveFacility,
} from "@/services/portal"
import { useUserStore } from "@/stores/user"
import type { LocaleCode } from "@/types"

type Kind = "single" | "main" | "branch"

const { t, locale } = useI18n()

const user = useUserStore()
const facilities = ref<Facility[] | null>(null)
/** The producer has no facility yet: this page is its first step (guards.ts sends it here). */
const first = ref(false)
/** The first facility, once saved: the next step is a service for it. */
const created = ref<string | null>(null)
const settings = ref<FacilitySettings | null>(null)
const failed = ref(false)

onMounted(async () => {
	try {
		;[facilities.value, settings.value] = await Promise.all([
			getFacilities(),
			getFacilitySettings(),
		])
	} catch {
		failed.value = true
		return
	}
	if (!facilities.value.length) {
		first.value = true
		edit(null)
	}
})

/** A facility on its own, a main one with branches (a group in the Facility tree), or a branch. */
function kindOf(
	facility: Pick<Facility, "is_group" | "parent_facility">,
): Kind {
	if (facility.parent_facility) return "branch"
	return facility.is_group ? "main" : "single"
}

function requestLink(facility: string) {
	return {
		path: localePath(`${dashboardPath}/requests`, locale.value as LocaleCode),
		query: { facility },
	}
}

// What a facility has led to, shown under it on demand.
const shown = ref<string | null>(null)
const activity = ref<FacilityActivity | null>(null)
const activityFailed = ref(false)
const activityRows = computed(() =>
	activity.value
		? (["requests", "quotations", "contracts", "operation_orders"] as const)
				.map((kind) => ({ kind, rows: activity.value?.[kind] ?? [] }))
				.filter((group) => group.rows.length)
		: [],
)

async function toggleActivity(name: string) {
	if (shown.value === name) {
		shown.value = null
		return
	}
	shown.value = name
	activity.value = null
	activityFailed.value = false
	try {
		const result = await getFacilityActivity(name)
		if (shown.value === name) activity.value = result
	} catch {
		if (shown.value === name) activityFailed.value = true
	}
}

// The form.
const editing = ref(false)
/** A new key per opened form, so the activity picker starts over each time. */
const formKey = ref(0)
const draft = reactive<FacilityInput>(blank())
const draftIsic = ref<string | null>(null)
/** The region field is named by the level Naqel Settings picks it at (District, City…). */
const regionLevels = ["Region", "City", "Municipality", "District"] as const
const regionLabel = computed(() => {
	const level = settings.value?.region_level
	return regionLevels.find((l) => l === level)
		? t(`dashboard.facilities.regionLevels.${level}`)
		: t("dashboard.facilities.region")
})
/** The chosen region as the picker shows it. */
const draftRegion = ref<string | null>(null)
/** The address parts the chosen region fills: read only then (the server sets them from the region too). */
const regionFills = reactive({ city: false, district: false })

function applyRegion(region: RegionOption) {
	draft.region = region.value
	draftRegion.value = [region.label, ...region.within].join(
		t("dashboard.separator"),
	)
	regionFills.city = Boolean(region.city)
	regionFills.district = Boolean(region.district)
	if (region.city) draft.city = region.city
	if (region.district) draft.district = region.district
}

// A pin dropped on the map picks the region it falls in (the producer can still choose another)
watch(
	() => [draft.latitude, draft.longitude] as const,
	async ([latitude, longitude], before) => {
		if (!editing.value || !settings.value?.requires_region) return
		if (latitude == null || longitude == null) return
		if (before && before[0] === latitude && before[1] === longitude) return
		const region = await regionAt(latitude, longitude).catch(() => null)
		if (region && draft.latitude === latitude && draft.longitude === longitude)
			applyRegion(region)
	},
)
const kind = ref<Kind>("single")
const parent = ref("")

function blank(): FacilityInput {
	return {
		facility_name: "",
		isic_classification: "",
		parent_facility: null,
		is_group: 0,
		region: "",
		google_maps_location: "",
		latitude: null,
		longitude: null,
		street: "",
		building_no: "",
		secondary_no: "",
		district: "",
		city: "",
		pincode: "",
		country: settings.value?.country ?? "",
		credentials: [],
	}
}

function blankCredential(): Credential {
	return {
		credential_type: "Government ID",
		document_type: "",
		document_number: "",
		credential: null,
		issue_date: null,
		expiry_date: null,
	}
}

/** Opens the form: a facility to edit, or a new one (a branch of `parentName` if given). */
function edit(facility: Facility | null, parentName?: string) {
	Object.assign(draft, blank(), { name: undefined })
	if (facility) {
		Object.assign(draft, {
			name: facility.name,
			facility_name: facility.facility_name,
			isic_classification: facility.isic_classification,
			region: facility.region ?? "",
			google_maps_location: facility.google_maps_location ?? "",
			latitude: facility.latitude,
			longitude: facility.longitude,
			street: facility.street ?? "",
			building_no: facility.building_no ?? "",
			secondary_no: facility.secondary_no ?? "",
			district: facility.district ?? "",
			city: facility.city ?? "",
			pincode: facility.pincode ?? "",
			country: facility.country ?? settings.value?.country ?? "",
			// Its shared documents only: those from requests aren't edited here
			credentials: facility.credentials
				.filter((row) => row.eligible_for_multiple_facility_branches)
				.map((row) => ({ ...row })),
		})
		draftIsic.value = facility.isic_title
		draftRegion.value = facility.region_title
		Object.assign(regionFills, {
			city: Boolean(facility.region),
			district: false,
		})
		kind.value = kindOf(facility)
		parent.value = facility.parent_facility ?? ""
	} else {
		draftIsic.value = null
		draftRegion.value = null
		Object.assign(regionFills, { city: false, district: false })
		kind.value = parentName ? "branch" : "single"
		parent.value = parentName ?? ""
	}
	form.reset()
	formKey.value++
	editing.value = true
}

const kinds = computed(() =>
	(["single", "main", "branch"] as const).map((value) => ({
		value,
		label: t(`dashboard.facilities.kinds.${value}`),
	})),
)
/** Branches go under a main facility (Frappe's tree: only a group has children). */
const parents = computed(() =>
	(facilities.value ?? [])
		.filter((f) => f.is_group && f.name !== draft.name)
		.map((f) => ({ value: f.name, label: f.facility_name })),
)

// Credentials: a document type is the pair (credential type, document), offered as one choice.
const documentOptions = computed(() =>
	(settings.value?.shared_document_types ?? []).map((d) => ({
		value: keyOf(d),
		label: d.label,
	})),
)
function keyOf(
	row: Pick<DocumentType, "credential_type" | "document_type">,
): string {
	return `${row.credential_type}::${row.document_type}`
}
function documentKey(row: Credential): string {
	return row.document_type ? keyOf(row) : ""
}
function documentOf(row: Credential): DocumentType | undefined {
	return settings.value?.shared_document_types.find(
		(d) => keyOf(d) === documentKey(row),
	)
}
function setDocument(row: Credential, value: string) {
	const [credentialType, documentType] = value.split("::")
	row.credential_type = credentialType as Credential["credential_type"]
	row.document_type = documentType
	if (!documentOf(row)?.has_expiry_date) row.expiry_date = null
}

const form = useFormSubmit<string>({
	validate: () => {
		const errors: Record<string, string> = {}
		const required = t("auth.errors.required")
		if (!draft.facility_name.trim()) errors.facility_name = required
		if (!draft.isic_classification)
			errors.isic_classification = t("dashboard.facilities.isicPick")
		if (kind.value === "branch" && !parent.value)
			errors.parent_facility = required
		if (!draft.street.trim()) errors.street = required
		if (!draft.city.trim()) errors.city = required
		if (settings.value?.requires_region && !draft.region)
			errors.region = t("dashboard.facilities.regionPick")
		if (!draft.country.trim()) errors.country = required
		const pinned =
			draft.google_maps_location.trim() ||
			(draft.latitude != null && draft.longitude != null)
		if (settings.value?.requires_pin && !pinned)
			errors.pin = t("dashboard.facilities.pinRequired")
		// A composite facility needs the document its annexes share: chosen, numbered and uploaded
		if (kind.value === "main") {
			if (!draft.credentials.length)
				errors.credentials = t("dashboard.facilities.credentialsRequired")
			draft.credentials.forEach((row, index) => {
				if (!row.document_type) errors[`credential:${index}:type`] = required
				if (!row.document_number.trim())
					errors[`credential:${index}:number`] = required
				if (!row.credential)
					errors[`credential:${index}:file`] = t(
						"dashboard.facilities.fileRequired",
					)
			})
		}
		return errors
	},
	send: async () => {
		const result = await saveFacility({
			...draft,
			google_maps_location: draft.google_maps_location.trim(),
			is_group: kind.value === "main" ? 1 : 0,
			parent_facility: kind.value === "branch" ? parent.value : null,
			credentials:
				kind.value === "main"
					? draft.credentials.map((row) => ({
							...row,
							document_number: row.document_number.trim(),
						}))
					: [],
		})
		facilities.value = result.facilities
		if (first.value) {
			first.value = false
			created.value = result.name
			// The session's count, so the overview opens again
			user.reload().catch(() => {})
		}
	},
})

async function saveForm() {
	if (await form.submit()) editing.value = false
}
</script>
