import type { RouteRecordRaw } from "vue-router"

export type LayoutName = "public"

declare module "vue-router" {
	interface RouteMeta {
		/** Layout from src/layouts/ that wraps the view (see App.vue). */
		layout: LayoutName
	}
}

// Every top-level path here needs a matching website_route_rules entry in
// ozone/hooks.py, otherwise a full page load returns Frappe's 404. `/` is served
// by `home_page = "frontend"`.
export const routes: RouteRecordRaw[] = [
	{
		path: "/",
		name: "Landing",
		component: () => import("@/views/LandingView.vue"),
		meta: { layout: "public" },
	},
	{
		path: "/:pathMatch(.*)*",
		redirect: "/",
	},
]
