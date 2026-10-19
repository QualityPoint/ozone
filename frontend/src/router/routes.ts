import type { RouteComponent, RouteMeta, RouteRecordRaw } from "vue-router"

import { loginHashPage } from "@/components/auth/authHelpers"
import {
	authPaths,
	dashboardPath,
	defaultLocale,
	localePath,
	pagePaths,
} from "@/config/site"
import { type LocaleCode, type PageKey, SUPPORTED_LOCALES } from "@/types"

export type LayoutName = "public" | "auth" | "dashboard"

declare module "vue-router" {
	interface RouteMeta {
		/** Layout from src/layouts/ that wraps the view (see App.vue). */
		layout: LayoutName
		/** Language the route is served in. */
		locale?: LocaleCode
		/** The public page it is (its title, description and twin addresses in meta.json). */
		page?: PageKey
		/** The tab title's message, for pages outside meta.json (login, dashboard). */
		title?: string
		/** Logged-in visitors are sent on (the login pages): see guards.ts. */
		guestOnly?: boolean
		/** Guests are sent to the login page, then back. */
		requiresAuth?: boolean
		/** Producers only: staff go to the Desk, unlinked accounts to DashboardNotLinked. */
		producerOnly?: boolean
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

/** A login page (sign-in, sign-up, password reset) on the auth layout, for guests only. */
function authRoutes(
	path: string,
	name: string,
	component: () => Promise<RouteComponent>,
	title: string,
	extra: Partial<RouteRecordRaw> = {},
): RouteRecordRaw[] {
	return inEveryLocale(
		path,
		name,
		component,
		{ layout: "auth", title, guestOnly: true },
		extra,
	)
}

/** A page of the producer dashboard (docs/producer_dashboard/routing.md). */
function dashboardRoutes(
	path: string,
	name: string,
	component: () => Promise<RouteComponent>,
	title: string,
	producerOnly = true,
): RouteRecordRaw[] {
	return inEveryLocale(`${dashboardPath}${path}`, name, component, {
		layout: "dashboard",
		title,
		requiresAuth: true,
		producerOnly,
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
	...localizedRoutes("naqel", "Naqel", () => import("@/views/NaqelView.vue")),
	// Replaces Frappe's /login (website_route_rules in ozone/hooks.py): every Frappe link to the
	// login page lands here.
	...authRoutes(
		authPaths.login,
		"Login",
		() => import("@/views/auth/LoginView.vue"),
		"auth.login.pageTitle",
		{
			beforeEnter: (to) => {
				const page = loginHashPage(to.hash)
				return page
					? {
							name: localizedName(page, to.meta.locale ?? defaultLocale),
							query: to.query,
						}
					: undefined
			},
		},
	),
	...authRoutes(
		authPaths.signup,
		"Signup",
		() => import("@/views/auth/SignupView.vue"),
		"auth.signup.pageTitle",
	),
	...authRoutes(
		authPaths.forgotPassword,
		"ForgotPassword",
		() => import("@/views/auth/ForgotPasswordView.vue"),
		"auth.forgot.pageTitle",
	),
	...dashboardRoutes(
		"",
		"Dashboard",
		() => import("@/views/dashboard/OverviewView.vue"),
		"dashboard.titles.overview",
	),
	...dashboardRoutes(
		"/profile",
		"DashboardProfile",
		() => import("@/views/dashboard/ProfileView.vue"),
		"dashboard.titles.profile",
	),
	...dashboardRoutes(
		"/establishment",
		"DashboardEstablishment",
		() => import("@/views/dashboard/EstablishmentView.vue"),
		"dashboard.titles.establishment",
	),
	...dashboardRoutes(
		"/facilities",
		"DashboardFacilities",
		() => import("@/views/dashboard/FacilitiesView.vue"),
		"dashboard.titles.facilities",
	),
	...dashboardRoutes(
		"/requests",
		"DashboardRequests",
		() => import("@/views/dashboard/RequestsView.vue"),
		"dashboard.titles.requests",
	),
	...dashboardRoutes(
		"/quotations",
		"DashboardQuotations",
		() => import("@/views/dashboard/QuotationsView.vue"),
		"dashboard.titles.quotations",
	),
	...dashboardRoutes(
		"/contracts",
		"DashboardContracts",
		() => import("@/views/dashboard/ContractsView.vue"),
		"dashboard.titles.contracts",
	),
	// A logged-in account nobody has linked to a producer yet.
	...dashboardRoutes(
		"/not-linked",
		"DashboardNotLinked",
		() => import("@/views/dashboard/NotLinkedView.vue"),
		"dashboard.titles.notLinked",
		false,
	),
	...fallbacks,
]
