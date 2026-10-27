<template>
  <!-- The establishment: the producer's own Lead or Customer (ozone/portal/establishment.py). The
       transporter keeps its name, type, group and territory; the producer keeps its industry,
       market segment and website up to date. -->
  <section>
    <DashboardHeading :eyebrow="t('dashboard.nav.groups.account')" :title="t('dashboard.nav.establishment')" :intro="t('dashboard.establishment.intro')" />
    <BaseNotice v-if="failed" class="mt-8">{{ t("dashboard.loadFailed") }}</BaseNotice>

    <div v-if="establishment" class="mt-8 grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
      <BaseCard class="p-6">
        <h2 class="text-title font-extrabold text-site-heading">{{ t("dashboard.establishment.details") }}</h2>
        <dl class="mt-4 grid gap-4 text-caption sm:grid-cols-2">
          <div v-for="row in readOnly" :key="row.label">
            <dt class="text-site-muted">{{ row.label }}</dt>
            <dd class="mt-1 font-bold text-site-heading">{{ row.value }}</dd>
          </div>
        </dl>
        <p class="mt-5 text-caption text-site-muted">{{ t("dashboard.establishment.readOnlyNote") }}</p>
      </BaseCard>

      <BaseCard as="form" class="p-6" novalidate @submit.prevent="form.submit">
        <BaseNotice v-if="form.notice.value" :kind="form.notice.value.kind" class="mb-4">{{ form.notice.value.text }}</BaseNotice>
        <div class="grid gap-4">
          <BaseSelect v-model="draft.industry" :label="t('dashboard.establishment.industry')" :options="withBlank(establishment.options.industry)" />
          <BaseSelect v-model="draft.market_segment" :label="t('dashboard.establishment.marketSegment')" :options="withBlank(establishment.options.market_segment)" />
          <BaseInput v-model="draft.website" :label="t('dashboard.establishment.website')" type="url" inputmode="url" autocomplete="url" dir="ltr" />
        </div>
        <BaseButton type="submit" :loading="form.busy.value" class="mt-6">{{ t("dashboard.save") }}</BaseButton>
      </BaseCard>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref } from "vue"
import { useI18n } from "vue-i18n"

import BaseButton from "@/components/base/BaseButton.vue"
import BaseCard from "@/components/base/BaseCard.vue"
import BaseInput from "@/components/base/BaseInput.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import BaseSelect from "@/components/base/BaseSelect.vue"
import DashboardHeading from "@/components/dashboard/DashboardHeading.vue"
import { useFormSubmit } from "@/composables/useFormSubmit"
import {
	type Establishment,
	type Option,
	getEstablishment,
	updateEstablishment,
} from "@/services/portal"

const { t } = useI18n()

const establishment = ref<Establishment | null>(null)
const failed = ref(false)
const draft = reactive({ industry: "", market_segment: "", website: "" })

function fill(value: Establishment) {
	establishment.value = value
	Object.assign(draft, {
		industry: value.industry ?? "",
		market_segment: value.market_segment ?? "",
		website: value.website ?? "",
	})
}

onMounted(async () => {
	try {
		fill(await getEstablishment())
	} catch {
		failed.value = true
	}
})

/** The details the transporter keeps, in the order a Customer or a Lead has them. */
const readOnly = computed(() => {
	const value = establishment.value
	if (!value) return []
	const rows: { label: string; value: string | null | undefined }[] = [
		{ label: t("dashboard.establishment.name"), value: value.title },
		{
			label: t("dashboard.profile.party"),
			value: t(`dashboard.stage.${value.doctype}`),
		},
	]
	if (value.doctype === "Customer") {
		rows.push(
			{
				label: t("dashboard.establishment.customerType"),
				value: value.customer_type,
			},
			{
				label: t("dashboard.establishment.customerGroup"),
				value: value.customer_group,
			},
		)
	}
	rows.push({
		label: t("dashboard.establishment.territory"),
		value: value.territory,
	})
	return rows.filter((row) => row.value)
})

/** A select that can be left empty: the first choice clears it. */
function withBlank(options: Option[]): Option[] {
	return [{ value: "", label: t("dashboard.establishment.pick") }, ...options]
}

const form = useFormSubmit<never>({
	validate: () => ({}),
	send: async () => {
		fill(
			await updateEstablishment({
				industry: draft.industry || null,
				market_segment: draft.market_segment || null,
				website: draft.website.trim() || null,
			}),
		)
	},
	sent: "dashboard.saved",
})
</script>
