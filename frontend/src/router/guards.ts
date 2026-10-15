import type { Router } from "vue-router"

import {
	dashboardHome,
	landingUrl,
	redirectToFromQuery,
} from "@/components/auth/authHelpers"
import { dashboardPath, defaultLocale, localePath } from "@/config/site"
import { setLocale, setPageTitle } from "@/i18n"
import { DESK_PATH } from "@/services/auth"
import { useSessionStore } from "@/stores/session"
import { useUserStore } from "@/stores/user"
import { localizedName } from "./routes"

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
 * Enforces `meta.guestOnly`, `meta.requiresAuth` and `meta.producerOnly`
 * (docs/producer_dashboard/routing.md). Access to data is the server's: this only picks the page.
 * - Logged-in visitors on the login pages go on, like Frappe's /login: to `redirect-to`, else
 *   staff to the Desk and producers to their dashboard.
 * - Guests on a dashboard page go to the login page, and come back after it.
 * - Producer pages: staff go to the Desk, an account nobody has linked to the not-linked page.
 */
export function installAuthGuard(router: Router): void {
	router.beforeEach(async (to) => {
		if (!to.meta.requiresAuth && !to.meta.guestOnly) {
			return true
		}

		const session = useSessionStore()
		const user = useUserStore()
		const locale = to.meta.locale ?? defaultLocale

		// The cookie answers instantly for guests; the server confirms the rest (an expired session
		// still leaves the cookie behind).
		let isLoggedIn = session.isLoggedIn
		if (isLoggedIn) {
			try {
				await user.ensureLoaded()
				isLoggedIn = user.user?.name !== "Guest"
			} catch {
				isLoggedIn = false
			}
		}

		if (to.meta.guestOnly && isLoggedIn) {
			const target = landingUrl(
				user.isStaff,
				[redirectToFromQuery(to.query)],
				locale,
			)
			if (target === dashboardHome(locale)) return { path: target }
			// The Desk, or another page outside this app.
			window.location.assign(target)
			return false
		}
		if (to.meta.requiresAuth && !isLoggedIn) {
			return {
				name: localizedName("Login", locale),
				query: { "redirect-to": to.fullPath },
			}
		}
		if (to.meta.requiresAuth && user.isStaff) {
			// Staff work in the Desk; the dashboard is the producers'.
			window.location.assign(DESK_PATH)
			return false
		}
		if (to.meta.producerOnly && !user.producer) {
			return { name: localizedName("DashboardNotLinked", locale) }
		}
		if (
			to.name === localizedName("Dashboard", locale) &&
			user.producer?.facilities === 0
		) {
			// A producer starts with its facility: everything else (requests, quotations) is for one.
			return { path: localePath(`${dashboardPath}/facilities`, locale) }
		}
		if (!to.meta.producerOnly && to.meta.requiresAuth && user.producer) {
			// Linked since: the not-linked page has nothing more to say.
			return { path: dashboardHome(locale) }
		}
		return true
	})
}
