import type { Router } from "vue-router"

import { setLocale, setPageTitle } from "@/i18n"

/** Sets the language from `meta.locale` before each navigation, and the page title after it. */
export function installLocaleGuard(router: Router): void {
	router.beforeEach((to) => {
		if (to.meta.locale) {
			setLocale(to.meta.locale)
		}
	})
	router.afterEach((to) => setPageTitle(to.meta.page ?? "landing"))
}
