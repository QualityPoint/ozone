<template>
  <!-- Staff (by Frappe's login cookies): the Desk, outside this app, so a plain link. -->
  <a v-if="staff" :href="DESK_PATH" v-bind="labelAttrs(t('auth.account.desk'))" :class="classes">
    <LucideLayoutDashboard class="size-5" aria-hidden="true" />
    <span v-if="labelled">{{ t("auth.account.desk") }}</span>
  </a>
  <!-- A producer (logged in, not staff): their dashboard; a guest: the login page, in the current
       language. -->
  <RouterLink v-else :to="target" v-bind="labelAttrs(label)" :class="classes">
    <LucideUserRound class="size-5" aria-hidden="true" />
    <span v-if="labelled">{{ label }}</span>
  </RouterLink>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"
import LucideLayoutDashboard from "~icons/lucide/layout-dashboard"
import LucideUserRound from "~icons/lucide/user-round"

import { dashboardHome } from "@/components/auth/authHelpers"
import { useLocale } from "@/composables/useLocale"
import { cookieLoggedIn, cookieStaff } from "@/composables/useSession"
import { localizedName } from "@/router/routes"
import { DESK_PATH } from "@/services/auth"

const props = defineProps<{
	/** With its text, as a row of the phone menu; otherwise an icon button. */
	labelled?: boolean
}>()

const { t } = useI18n()
const { current } = useLocale()

const classes = props.labelled
	? "flex items-center gap-3 rounded-2xl px-4 py-3 font-bold text-site-heading hover:bg-site-hover"
	: "grid size-10 shrink-0 place-items-center rounded-full text-site-heading transition hover:bg-site-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"

/** An icon button is named by its label; a labelled row by its text. */
function labelAttrs(label: string) {
	return props.labelled ? {} : { "aria-label": label, title: label }
}

// Read once mounted; an expired session's cookies only send staff to the Desk, which then
// asks them to log in again.
const staff = ref(false)
const loggedIn = ref(false)
const label = computed(() =>
	loggedIn.value ? t("auth.account.dashboard") : t("auth.account.login"),
)
const target = computed(() =>
	loggedIn.value
		? dashboardHome(current.value)
		: { name: localizedName("Login", current.value) },
)
onMounted(() => {
	staff.value = cookieStaff()
	loggedIn.value = cookieLoggedIn()
})
</script>
