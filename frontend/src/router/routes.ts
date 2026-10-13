import type { RouteComponent, RouteMeta, RouteRecordRaw } from "vue-router"

import { forgotHash } from "@/components/auth/authHelpers"
import { authPaths, defaultLocale, localePath, pagePaths } from "@/config/site"
import { type LocaleCode, type PageKey, SUPPORTED_LOCALES } from "@/types"

export type LayoutName = "public" | "auth"

declare module "vue-router" {
	interface RouteMeta {
		/** Layout from src/layouts/ that wraps the view (see App.vue). */
		layout: LayoutName
		/** Language the route is served in. */
		locale?: LocaleCode
		/** The public page it is (its title, description and twin addresses in meta.json). */
		page?: PageKey
		/** The tab title's message, for pages outside meta.json (the login pages). */
		title?: string
		/** Logged-in visitors are sent on (the login pages): see guards.ts. */
		guestOnly?: boolean
	}
}

/** A route's name in a language: `Landing` in the default one, `LandingEn` in English. */
export function localizedName(name: string, locale: LocaleCode): string {
	return locale === defaultLocale
		? name
		: `${name}${locale[0].toUpperCase()}${locale.slice(1)}`
}

/** A page in every language, at its base path's address in each (config/site.ts: localePath). */
function inEveryLocale(
	path: string,
	name: string,
	component: () => Promise<RouteComponent>,
	meta: Omit<RouteMeta, "locale">,
	extra: Partial<RouteRecordRaw> = {},
): RouteRecordRaw[] {
	return SUPPORTED_LOCALES.map(
		(locale) =>
			({
				...extra,
				path: localePath(path, locale),
				name: localizedName(name, locale),
				component,
				meta: { ...meta, locale },
			}) as RouteRecordRaw,
	)
}

/** A public page (meta.json `paths`) on the public layout. */
function localizedRoutes(
	page: PageKey,
	name: string,
	component: () => Promise<RouteComponent>,
): RouteRecordRaw[] {
	return inEveryLocale(pagePaths[page], name, component, {
		layout: "public",
		page,
	})
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
	...localizedRoutes(
		"capabilities",
		"Capabilities",
		() => import("@/views/CapabilitiesView.vue"),
	),
	// Replaces Frappe's /login (website_route_rules in ozone/hooks.py).
	...inEveryLocale(
		authPaths.login,
		"Login",
		() => import("@/views/auth/LoginView.vue"),
		{ layout: "auth", title: "auth.login.pageTitle", guestOnly: true },
		{
			beforeEnter: (to) =>
				forgotHash(to.hash)
					? {
							name: localizedName(
								"ForgotPassword",
								to.meta.locale ?? defaultLocale,
							),
							query: to.query,
						}
					: undefined,
		},
	),
	...inEveryLocale(
		authPaths.forgotPassword,
		"ForgotPassword",
		() => import("@/views/auth/ForgotPasswordView.vue"),
		{ layout: "auth", title: "auth.forgot.pageTitle", guestOnly: true },
	),
	...fallbacks,
]
