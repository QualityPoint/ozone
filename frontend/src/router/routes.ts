import type { RouteComponent, RouteRecordRaw } from "vue-router"

import { defaultLocale, localePath, pagePaths } from "@/config/site"
import { type LocaleCode, type PageKey, SUPPORTED_LOCALES } from "@/types"

export type LayoutName = "public"

declare module "vue-router" {
	interface RouteMeta {
		/** Layout from src/layouts/ that wraps the view (see App.vue). */
		layout: LayoutName
		/** Language the route is served in. */
		locale?: LocaleCode
		/** The public page it is (its title, description and twin addresses in meta.json). */
		page?: PageKey
	}
}

/** A route's name in a language: `Landing` in the default one, `LandingEn` in English. */
export function localizedName(name: string, locale: LocaleCode): string {
	return locale === defaultLocale
		? name
		: `${name}${locale[0].toUpperCase()}${locale.slice(1)}`
}

/** A public page in every language (meta.json `paths`, config/site.ts: localePath), on the public layout. */
function localizedRoutes(
	page: PageKey,
	name: string,
	component: () => Promise<RouteComponent>,
): RouteRecordRaw[] {
	return SUPPORTED_LOCALES.map((locale) => ({
		path: localePath(pagePaths[page], locale),
		name: localizedName(name, locale),
		component,
		meta: { layout: "public", locale, page },
	}))
}

/** Unknown addresses go to the landing page of their language. */
const fallbacks: RouteRecordRaw[] = SUPPORTED_LOCALES.filter(
	(locale) => locale !== defaultLocale,
)
	.map(
		(locale): RouteRecordRaw => ({
			path: `/${locale}/:pathMatch(.*)*`,
			redirect: localePath("/", locale),
		}),
	)
	.concat({ path: "/:pathMatch(.*)*", redirect: "/" })

// Every top-level path here needs a matching website_route_rules entry in
// ozone/hooks.py, otherwise a full page load returns Frappe's 404. `/` is served by
// `home_page = "frontend"`.
export const routes: RouteRecordRaw[] = [
	...localizedRoutes(
		"landing",
		"Landing",
		() => import("@/views/LandingView.vue"),
	),
	...fallbacks,
]
