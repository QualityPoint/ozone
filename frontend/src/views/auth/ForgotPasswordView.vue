<template>
  <AuthCard :title="t('auth.forgot.title')" :subtitle="t('auth.forgot.subtitle')" :notice="notice">
    <form v-if="!sent" class="space-y-5" novalidate @submit.prevent="sendReset">
      <BaseInput
        v-model="email"
        type="email"
        :label="t('auth.email')"
        :error="error"
        autocomplete="email"
        inputmode="email"
        dir="ltr"
        required
      />
      <BaseButton type="submit" :loading="busy" class="w-full">{{ t("auth.forgot.submit") }}</BaseButton>
    </form>

    <template #footer>
      <RouterLink :to="{ name: localizedName('Login', current), query: route.query }" :class="AUTH_LINK">
        <LucideArrowLeft class="size-4 rtl:-scale-x-100" aria-hidden="true" />
        {{ t("auth.forgot.back") }}
      </RouterLink>
    </template>
  </AuthCard>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import { useI18n } from "vue-i18n"
import { useRoute } from "vue-router"
import LucideArrowLeft from "~icons/lucide/arrow-left"

import AuthCard from "@/components/auth/AuthCard.vue"
import {
	AUTH_LINK,
	type AuthNotice,
	authErrorMessage,
	emailError,
} from "@/components/auth/authHelpers"
import BaseButton from "@/components/base/BaseButton.vue"
import BaseInput from "@/components/base/BaseInput.vue"
import { useLocale } from "@/composables/useLocale"
import { localizedName } from "@/router/routes"
import { resetPassword } from "@/services/auth"

const { t } = useI18n()
const route = useRoute()
const { current } = useLocale()

const email = ref("")
const error = ref<string>()
const notice = ref<AuthNotice | null>(null)
const sent = ref(false)
const busy = ref(false)

async function sendReset() {
	notice.value = null
	error.value = emailError(email.value, t)
	if (error.value) return

	busy.value = true
	try {
		await resetPassword(email.value.trim())
		// The same message whether or not the account exists (no account probing).
		notice.value = { kind: "success", text: t("auth.forgot.sent") }
		sent.value = true
	} catch (err) {
		notice.value = { kind: "error", text: authErrorMessage(err, t) }
	} finally {
		busy.value = false
	}
}
</script>
