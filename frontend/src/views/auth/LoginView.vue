<template>
  <!-- Step 2 of a two-factor login: the verification code. -->
  <AuthCard v-if="challenge" :title="t('auth.otp.title')" :subtitle="otpPrompt" :notice="notice">
    <form v-if="challenge.setup" class="space-y-5" novalidate @submit.prevent="verify">
      <BaseInput
        v-model="otp"
        :label="t('auth.otp.code')"
        :error="errors.otp"
        autocomplete="one-time-code"
        inputmode="numeric"
        dir="ltr"
        required
      />
      <BaseButton type="submit" :loading="busy === 'otp'" :disabled="!!busy" class="w-full">
        {{ t("auth.otp.verify") }}
      </BaseButton>
    </form>
    <template #footer>
      <button type="button" :class="AUTH_LINK" @click="restart">{{ t("auth.otp.back") }}</button>
    </template>
  </AuthCard>

  <!-- Step 1: the login name and password, and the other sign-in methods enabled on the site. -->
  <AuthCard v-else :title="t('auth.login.title')" :subtitle="t('auth.login.subtitle')" :notice="notice">
    <form class="space-y-5" novalidate @submit.prevent="logIn">
      <!-- Any login name Frappe accepts: an email, "Administrator", and a username or mobile
           number when enabled. -->
      <BaseInput
        v-model="user"
        :label="identifierLabel"
        :error="errors.user"
        autocomplete="username"
        autocapitalize="none"
        spellcheck="false"
        dir="ltr"
        required
      />
      <template v-if="options?.password_login !== false">
        <div>
          <BaseInput
            v-model="password"
            type="password"
            :label="t('auth.password')"
            :error="errors.password"
            :show-password-label="t('auth.showPassword')"
            :hide-password-label="t('auth.hidePassword')"
            autocomplete="current-password"
            dir="ltr"
            required
          />
          <RouterLink
            :to="{ name: localizedName('ForgotPassword', current), query: route.query }"
            :class="[AUTH_LINK, 'mt-2 text-caption']"
          >
            {{ t("auth.login.forgot") }}
          </RouterLink>
        </div>
        <BaseButton type="submit" :loading="busy === 'password'" :disabled="!!busy" class="w-full">
          {{ t("auth.login.submit") }}
        </BaseButton>
      </template>
    </form>

    <template v-if="options && (options.email_link || options.providers.length)">
      <div v-if="options.password_login" class="my-6 flex items-center gap-3 text-caption text-site-muted">
        <span class="h-px flex-1 bg-site-line" />{{ t("auth.or") }}<span class="h-px flex-1 bg-site-line" />
      </div>
      <div class="space-y-3">
        <BaseButton
          v-if="options.email_link"
          variant="outline"
          :loading="busy === 'link'"
          :disabled="!!busy"
          class="w-full"
          @click="emailLink"
        >
          <LucideMail v-if="busy !== 'link'" class="size-4" aria-hidden="true" />
          {{ t("auth.login.emailLink") }}
        </BaseButton>
        <BaseButton
          v-for="provider in options.providers"
          :key="provider.name"
          :href="socialLoginUrl(provider.name, redirectTo)"
          variant="outline"
          class="w-full"
        >
          {{ t("auth.login.continueWith") }} {{ provider.label }}
        </BaseButton>
      </div>
    </template>

    <!-- Producers without an account register here, when the site allows sign-up. -->
    <template v-if="options?.signup" #footer>
      {{ t("auth.login.noAccount") }}
      <RouterLink :to="{ name: localizedName('Signup', current), query: route.query }" :class="AUTH_LINK">
        {{ t("auth.login.signupLink") }}
      </RouterLink>
    </template>
  </AuthCard>
</template>

<script lang="ts" setup>
import { computed, reactive, ref } from "vue"
import { useI18n } from "vue-i18n"
import { useRoute } from "vue-router"
import LucideMail from "~icons/lucide/mail"

import AuthCard from "@/components/auth/AuthCard.vue"
import {
	AUTH_LINK,
	type AuthNotice,
	authErrorMessage,
	emailError,
	postLoginUrl,
	redirectToFromQuery,
	useLoginOptions,
} from "@/components/auth/authHelpers"
import BaseButton from "@/components/base/BaseButton.vue"
import BaseInput from "@/components/base/BaseInput.vue"
import { useLocale } from "@/composables/useLocale"
import { localizedName } from "@/router/routes"
import {
	AuthRequestError,
	type LoginResult,
	type TwoFactorChallenge,
	login,
	sendLoginLink,
	socialLoginUrl,
	verifyLogin,
} from "@/services/auth"

const { t } = useI18n()
const route = useRoute()
const { current } = useLocale()
const options = useLoginOptions()

/** Where Frappe asked to return after login (e.g. a Desk page after the session expired). */
const redirectTo = computed(() => redirectToFromQuery(route.query))

const user = ref("")
const password = ref("")
const otp = ref("")
const errors = reactive<{ user?: string; password?: string; otp?: string }>({})
const notice = ref<AuthNotice | null>(null)
const busy = ref<"password" | "link" | "otp" | null>(null)

/** A pending two-factor login, set when the server asks for a code. */
const challenge = ref<TwoFactorChallenge | null>(null)
const tmpId = ref("")

const otpPrompt = computed(() => {
	const c = challenge.value
	if (!c) return ""
	if (!c.setup) return t("auth.otp.notDelivered")
	// SMS prompts name the (masked) phone number, so keep the server's text.
	return c.method === "SMS" && c.prompt ? c.prompt : t("auth.otp.appPrompt")
})

/** The login name field's label: what Frappe accepts as a login name on this site. */
const identifierLabel = computed(() => {
	const username = options.value?.login_with_username
	const mobile = options.value?.login_with_mobile
	const key =
		username && mobile
			? "any"
			: username
				? "emailOrUsername"
				: mobile
					? "emailOrMobile"
					: "email"
	return t(`auth.login.identifier.${key}`)
})

/** Any login response: done, two-factor needed, or the password expired. */
function handleResult(result: LoginResult) {
	if (result.verification && result.tmp_id && !result.message) {
		challenge.value = result.verification
		tmpId.value = result.tmp_id
		notice.value = null
		return
	}
	if (result.message === "Password Reset") {
		notice.value = { kind: "success", text: t("auth.login.passwordExpired") }
		return
	}
	window.location.assign(postLoginUrl(result, redirectTo.value, current.value))
}

async function logIn() {
	notice.value = null
	// Like Frappe's page: any non-empty login name (it may be "Administrator").
	errors.user = user.value.trim() ? undefined : t("auth.errors.required")
	errors.password = password.value ? undefined : t("auth.errors.required")
	if (errors.user || errors.password) return

	busy.value = "password"
	try {
		handleResult(await login(user.value.trim(), password.value))
	} catch (error) {
		notice.value = { kind: "error", text: authErrorMessage(error, t) }
	} finally {
		busy.value = null
	}
}

async function verify() {
	notice.value = null
	errors.otp = otp.value.trim() ? undefined : t("auth.errors.required")
	if (errors.otp) return

	busy.value = "otp"
	try {
		handleResult(await verifyLogin(otp.value.trim(), tmpId.value))
	} catch (error) {
		// A wrong code is a 401 with no server message: say so, rather than "incorrect password".
		const wrongCode =
			error instanceof AuthRequestError &&
			error.status === 401 &&
			!error.serverMessages.length
		notice.value = {
			kind: "error",
			text: wrongCode ? t("auth.otp.invalid") : authErrorMessage(error, t),
		}
	} finally {
		busy.value = null
	}
}

function restart() {
	challenge.value = null
	tmpId.value = ""
	otp.value = ""
	password.value = ""
	notice.value = null
}

async function emailLink() {
	notice.value = null
	errors.password = undefined
	// A login link needs a real email address.
	errors.user = emailError(user.value, t)
	if (errors.user) return

	busy.value = "link"
	try {
		await sendLoginLink(user.value.trim())
		notice.value = { kind: "success", text: t("auth.login.linkSent") }
	} catch (error) {
		notice.value = { kind: "error", text: authErrorMessage(error, t) }
	} finally {
		busy.value = null
	}
}
</script>
