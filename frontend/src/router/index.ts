import { createRouter, createWebHistory } from "vue-router"

import { installAuthGuard, installLocaleGuard } from "./guards"
import { routes } from "./routes"

const router = createRouter({
	history: createWebHistory("/"),
	routes,
	scrollBehavior(to, from, savedPosition) {
		if (savedPosition) {
			return savedPosition
		}
		// Same page and section, only the query changed: stay where you are.
		if (to.path === from.path && to.hash === from.hash) {
			return false
		}
		if (to.hash) {
			// Clear of the sticky header: the router scrolls with window.scrollTo, which ignores
			// CSS scroll-padding, so it reads main.css's scroll-padding-top and passes it on.
			const top = Number.parseFloat(
				getComputedStyle(document.documentElement).scrollPaddingTop,
			)
			return { el: to.hash, top: Number.isNaN(top) ? 0 : top }
		}
		return { top: 0 }
	},
})

installLocaleGuard(router)
installAuthGuard(router)

export default router
