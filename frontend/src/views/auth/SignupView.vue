<template>
  <AuthCard :title="t('auth.signup.title')" :subtitle="t('auth.signup.subtitle')" :notice="notice">
    <form v-if="options?.signup && !done" class="space-y-4" novalidate @submit.prevent="submit">
      <BaseInput
        v-model="fullName"
        :label="t('auth.signup.fullName')"
        :error="errors.fullName"
        autocomplete="name"
        required
      />
      <BaseInput
        v-model="email"
        type="email"
        :label="t('auth.email')"
        :error="errors.email"
        autocomplete="email"
        inputmode="email"
        dir="ltr"
        required
      />
      <BaseButton type="submit" :loading="busy" class="w-full">
        {{ t("auth.signup.submit") }}
      </BaseButton>
    </form>

    <template #footer>
      {{ t("auth.signup.haveAccount") }}
      <RouterLink :to="{ name: localizedName('Login', current), query: route.query }" :class="AUTH_LINK">
        {{ t("auth.signup.loginLink") }}
      </RouterLink>
    </template>
  </AuthCard>
</template>

<script lang="ts" setup>
import { computed, reactive, ref } from "vue"
import { useI18n } from "vue-i18n"
import { useRoute } from "vue-router"

import AuthCard from "@/components/auth/AuthCard.vue"
import {
	AUTH_LINK,
	type AuthNotice,
	authErrorMessage,
	emailError,
	redirectToFromQuery,
	useLoginOptions,
} from "@/components/auth/authHelpers"
import BaseButton from "@/components/base/BaseButton.vue"
import BaseInput from "@/components/base/BaseInput.vue"
import { useLocale } from "@/composables/useLocale"
import { localizedName } from "@/router/routes"
import { SignupStatus, signUp } from "@/services/auth"

const { t } = useI18n()
const route = useRoute()
const { current } = useLocale()
const options = useLoginOptions()

const fullName = ref("")
const email = ref("")
const errors = reactive<{ fullName?: string; email?: string }>({})
const result = ref<AuthNotice | null>(null)
const done = ref(false)
const busy = ref(false)

const notice = computed<AuthNotice | null>(() =>
	options.value && !options.value.signup
		? { kind: "error", text: t("auth.signup.unavailable") }
		: result.value,
)

const statusMessage: Record<SignupStatus, string> = {
	[SignupStatus.AlreadyRegistered]: "auth.signup.alreadyRegistered",
	[SignupStatus.CheckEmail]: "auth.signup.checkEmail",
	[SignupStatus.PendingApproval]: "auth.signup.pending",
}

async function submit() {
	result.value = null
	errors.fullName = fullName.value.trim()
		? undefined
		: t("auth.errors.required")
	errors.email = emailError(email.value, t)
	if (errors.fullName || errors.email) return

	busy.value = true
	try {
		// Like Frappe: after the first login, return to where the visitor came from.
		const status = await signUp(
			email.value.trim(),
			fullName.value.trim(),
			redirectToFromQuery(route.query),
		)
		const created = status !== SignupStatus.AlreadyRegistered
		result.value = {
			kind: created ? "success" : "error",
			text: t(statusMessage[status]),
		}
		done.value = created
	} catch (error) {
		result.value = { kind: "error", text: authErrorMessage(error, t) }
	} finally {
		busy.value = false
	}
}
</script>
