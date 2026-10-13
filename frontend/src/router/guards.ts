import type { Router } from "vue-router"

import { redirectToFromQuery } from "@/components/auth/authHelpers"
import { confirmedSession } from "@/composables/useSession"
import { defaultLocale, localeHome } from "@/config/site"
import { setLocale, setPageTitle } from "@/i18n"
import { DESK_PATH } from "@/services/auth"

/** Sets the language from `meta.locale` before each navigation, and the page title after it. */
export function installLocaleGuard(router: Router): void {
	router.beforeEach((to) => {
		if (to.meta.locale) {
			setLocale(to.meta.locale)
		}
	})
	router.afterEach((to) =>
		setPageTitle(to.meta.title ?? `meta.${to.meta.page ?? "landing"}.title`),
	)
}

/**
 * Logged-in visitors on guest-only pages (the login pages) go on, like Frappe's /login:
 * to `redirect-to` if given, else staff to the Desk and anyone else to the website.
 */
export function installAuthGuard(router: Router): void {
	router.beforeEach(async (to) => {
		if (!to.meta.guestOnly) return true
		const session = await confirmedSession()
		if (!session.loggedIn) return true

		const target =
			redirectToFromQuery(to.query) ?? (session.staff ? DESK_PATH : null)
		if (!target) return { path: localeHome[to.meta.locale ?? defaultLocale] }
		window.location.assign(target)
		return false
	})
}
