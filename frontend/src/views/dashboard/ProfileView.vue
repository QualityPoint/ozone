<template>
  <!-- My details: the user's own contact details, the party they belong to (kept by the
       transporter), and the party's addresses (ozone/portal/profile.py). -->
  <section>
    <DashboardHeading :eyebrow="t('dashboard.nav.groups.account')" :title="t('dashboard.nav.profile')" :intro="t('dashboard.profile.intro')" />
    <BaseNotice v-if="failed" class="mt-8">{{ t("dashboard.loadFailed") }}</BaseNotice>

    <div v-if="profile" class="mt-8 grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
      <BaseCard as="form" class="p-6" novalidate @submit.prevent="account.submit">
        <h2 class="text-title font-extrabold text-site-heading">{{ t("dashboard.profile.account") }}</h2>
        <BaseNotice v-if="account.notice.value" :kind="account.notice.value.kind" class="mt-4">{{ account.notice.value.text }}</BaseNotice>
        <div class="mt-4 flex items-center gap-4">
          <img v-if="profile.user_image" :src="profile.user_image" :alt="t('dashboard.profile.picture')" class="size-16 shrink-0 rounded-full object-cover" />
          <span v-else class="grid size-16 shrink-0 place-items-center rounded-full bg-site-hover text-title font-extrabold text-brand-green dark:text-brand-leaf" aria-hidden="true">
            {{ (profile.first_name || profile.email).charAt(0).toUpperCase() }}
          </span>
          <div class="min-w-0">
            <div class="flex flex-wrap gap-2">
              <label class="inline-flex cursor-pointer items-center gap-2 rounded-xl border-2 border-site-line px-3 py-2 text-caption font-bold text-site-heading transition hover:border-brand-green focus-within:ring-4 focus-within:ring-brand-leaf/20" :class="{ 'pointer-events-none opacity-60': pictureBusy }">
                {{ t("dashboard.profile.pictureChange") }}
                <input type="file" class="sr-only" accept="image/jpeg,image/png" @change="pickPicture" />
              </label>
              <BaseButton v-if="profile.user_image" variant="outline" :loading="pictureBusy" @click="setPicture(null)">{{ t("dashboard.profile.pictureRemove") }}</BaseButton>
            </div>
            <p class="mt-1 text-caption text-site-muted">{{ t("dashboard.profile.pictureHint") }}</p>
            <p v-if="pictureFailed" class="mt-1 text-caption font-bold text-red-600 dark:text-red-400">{{ pictureFailed }}</p>
          </div>
        </div>
        <dl class="mt-4 text-caption">
          <dt class="text-site-muted">{{ t("auth.email") }}</dt>
          <dd class="mt-1 font-bold text-site-heading" dir="ltr">{{ profile.email }}</dd>
        </dl>
        <div class="mt-5 grid gap-4 sm:grid-cols-2">
          <BaseInput v-model="contact.first_name" :label="t('dashboard.profile.firstName')" :error="account.errors.value.first_name" autocomplete="given-name" required />
          <BaseInput v-model="contact.last_name" :label="t('dashboard.profile.lastName')" autocomplete="family-name" />
        </div>
        <BaseInput v-model="contact.mobile_no" :label="t('dashboard.profile.mobile')" class="mt-4" type="text" inputmode="tel" autocomplete="tel" dir="ltr" />
        <BaseButton type="submit" :loading="account.busy.value" class="mt-6">{{ t("dashboard.save") }}</BaseButton>
      </BaseCard>

      <BaseCard class="p-6">
        <h2 class="text-title font-extrabold text-site-heading">{{ t("dashboard.profile.party") }}</h2>
        <p class="mt-4 text-body-lg font-bold text-site-heading">{{ profile.party.title }}</p>
        <p class="mt-1 text-caption text-brand-green dark:text-brand-leaf">{{ t(`dashboard.stage.${profile.party.doctype}`) }}</p>
        <p class="mt-4 text-caption text-site-muted">{{ t("dashboard.profile.partyNote") }}</p>
      </BaseCard>
    </div>

    <div v-if="profile" class="mt-10">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <h2 class="text-title-lg font-extrabold text-site-heading">{{ t("dashboard.profile.addresses") }}</h2>
        <BaseButton v-if="!editing" variant="outline" @click="edit(null)">
          <LucidePlus class="size-4" aria-hidden="true" />
          {{ t("dashboard.profile.addAddress") }}
        </BaseButton>
      </div>

      <BaseCard v-if="editing" as="form" class="mt-4 p-6" novalidate @submit.prevent="saveAddressForm">
        <BaseNotice v-if="address.notice.value" :kind="address.notice.value.kind" class="mb-4">{{ address.notice.value.text }}</BaseNotice>
        <div class="grid gap-4 sm:grid-cols-2">
          <BaseSelect v-model="draft.address_type" :label="t('dashboard.profile.addressType')" :options="addressTypes" />
          <BaseInput v-model="draft.city" :label="t('dashboard.profile.city')" :error="address.errors.value.city" autocomplete="address-level2" required />
          <BaseInput v-model="draft.address_line1" :label="t('dashboard.profile.line1')" :error="address.errors.value.address_line1" class="sm:col-span-2" autocomplete="address-line1" required />
          <BaseInput v-model="draft.address_line2" :label="t('dashboard.profile.line2')" class="sm:col-span-2" autocomplete="address-line2" />
          <BaseInput v-model="draft.state" :label="t('dashboard.profile.state')" autocomplete="address-level1" />
          <BaseInput v-model="draft.pincode" :label="t('dashboard.profile.pincode')" autocomplete="postal-code" dir="ltr" />
        </div>
        <div class="mt-6 flex gap-3">
          <BaseButton type="submit" :loading="address.busy.value">{{ t("dashboard.save") }}</BaseButton>
          <BaseButton variant="outline" @click="editing = false">{{ t("dashboard.cancel") }}</BaseButton>
        </div>
      </BaseCard>

      <p v-if="!profile.addresses.length && !editing" class="mt-4 text-site-muted">{{ t("dashboard.profile.noAddresses") }}</p>
      <ul class="mt-4 grid gap-4 sm:grid-cols-2">
        <li v-for="item in profile.addresses" :key="item.name">
          <BaseCard class="flex h-full items-start justify-between gap-4 p-5">
            <div class="min-w-0 text-caption">
              <p class="font-bold text-brand-green dark:text-brand-leaf">{{ t(`dashboard.profile.types.${item.address_type}`) }}</p>
              <p class="mt-2 text-site-heading">{{ item.address_line1 }}</p>
              <p v-if="item.address_line2" class="text-site-text">{{ item.address_line2 }}</p>
              <p class="text-site-muted">{{ [item.city, item.state, item.pincode].filter(Boolean).join(t("dashboard.separator")) }}</p>
            </div>
            <button
              type="button"
              class="grid size-9 shrink-0 place-items-center rounded-full text-site-muted transition hover:bg-site-hover hover:text-site-heading"
              :aria-label="t('dashboard.edit')"
              :title="t('dashboard.edit')"
              @click="edit(item)"
            >
              <LucidePencil class="size-4" aria-hidden="true" />
            </button>
          </BaseCard>
        </li>
      </ul>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref } from "vue"
import { useI18n } from "vue-i18n"
import LucidePencil from "~icons/lucide/pencil"
import LucidePlus from "~icons/lucide/plus"

import BaseButton from "@/components/base/BaseButton.vue"
import BaseCard from "@/components/base/BaseCard.vue"
import BaseInput from "@/components/base/BaseInput.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import BaseSelect from "@/components/base/BaseSelect.vue"
import DashboardHeading from "@/components/dashboard/DashboardHeading.vue"
import { refusal, useFormSubmit } from "@/composables/useFormSubmit"
import { uploadFile } from "@/services/http"
import {
	type Address,
	type AddressInput,
	type Profile,
	getProfile,
	saveAddress,
	updateAvatar,
	updateProfile,
} from "@/services/portal"

const { t } = useI18n()

const profile = ref<Profile | null>(null)
const failed = ref(false)
const contact = reactive({ first_name: "", last_name: "", mobile_no: "" })

function show(value: Profile) {
	profile.value = value
	contact.first_name = value.first_name ?? ""
	contact.last_name = value.last_name ?? ""
	contact.mobile_no = value.mobile_no ?? ""
}

onMounted(async () => {
	try {
		show(await getProfile())
	} catch {
		failed.value = true
	}
})

// The picture: uploaded as a public image (it shows wherever the user appears), then set.
const pictureBusy = ref(false)
const pictureFailed = ref("")

async function setPicture(fileUrl: string | null) {
	pictureBusy.value = true
	pictureFailed.value = ""
	try {
		show(await updateAvatar(fileUrl))
	} catch (error) {
		pictureFailed.value = refusal(error, t)
	} finally {
		pictureBusy.value = false
	}
}

async function pickPicture(event: Event) {
	const input = event.target as HTMLInputElement
	const file = input.files?.[0]
	input.value = ""
	if (!file) return
	pictureBusy.value = true
	pictureFailed.value = ""
	try {
		await setPicture(await uploadFile(file, false))
	} catch {
		pictureFailed.value = t("dashboard.profile.pictureFailed")
		pictureBusy.value = false
	}
}

const required = (value: string | null | undefined) =>
	value?.trim() ? undefined : t("auth.errors.required")

const account = useFormSubmit<"first_name">({
	validate: () => {
		const error = required(contact.first_name)
		return error ? { first_name: error } : {}
	},
	send: async () => show(await updateProfile({ ...contact })),
	sent: "dashboard.saved",
})

// The address being added (no name) or edited.
const editing = ref(false)
const draft = reactive<AddressInput>({})
const addressTypes = computed(() =>
	(profile.value?.address_types ?? []).map((value) => ({
		value,
		label: t(`dashboard.profile.types.${value}`),
	})),
)

function edit(item: Address | null) {
	for (const key of Object.keys(draft) as (keyof AddressInput)[])
		delete draft[key]
	Object.assign(
		draft,
		item ?? { address_type: profile.value?.address_types[0] },
	)
	address.reset()
	editing.value = true
}

const address = useFormSubmit<"address_line1" | "city">({
	validate: () => {
		const errors: Partial<Record<"address_line1" | "city", string>> = {}
		for (const field of ["address_line1", "city"] as const) {
			const error = required(draft[field])
			if (error) errors[field] = error
		}
		return errors
	},
	send: async () => {
		const result = await saveAddress({ ...draft })
		if (profile.value) profile.value.addresses = result.addresses
	},
})

async function saveAddressForm() {
	if (await address.submit()) editing.value = false
}
</script>
