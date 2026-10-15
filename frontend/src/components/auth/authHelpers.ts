import { ref } from "vue"
import type { LocationQuery } from "vue-router"

import { authPaths, basePath, dashboardPath, localePath } from "@/config/site"
import {
	AuthRequestError,
	DESK_PATH,
	type LoginOptions,
	type LoginResult,
	getLoginOptions,
	isStaff,
} from "@/services/auth"
import type { LocaleCode, Notice } from "@/types"
import { isEmail } from "@/utils/validation"

/** A result message shown above an auth form. */
export type AuthNotice = Notice

type Translate = (key: string) => string

/**
 * Text for a failed auth request, following Frappe's login page: the server's own messages when
 * it sent any (account locked, IP not allowed…), otherwise a translated default for the status.
 */
export function authErrorMessage(error: unknown, t: Translate): string {
	const status = error instanceof AuthRequestError ? error.status : 0
	if (status === 429) return t("auth.errors.tooManyAttempts")
	const server =
		error instanceof AuthRequestError ? error.serverMessages.join(" ") : ""
	if (server) return server
	return status === 401
		? t("auth.errors.invalidCredentials")
		: t("auth.errors.generic")
}

/** The error for an email field (required, then format), or undefined when it's fine. */
export function emailError(value: string, t: Translate): string | undefined {
	if (!value.trim()) return t("auth.errors.required")
	return isEmail(value) ? undefined : t("auth.errors.invalidEmail")
}

/** The auth pages' base paths: in any language, never a post-login destination (they'd loop). */
const AUTH_PATHS: string[] = Object.values(authPaths)

/**
 * A same-site path (path + query + hash) from an untrusted redirect value, or null. Mirrors
 * Frappe's sanitize_redirect: other origins, protocol-relative URLs (//evil.com) and non-http
 * schemes are rejected.
 */
export function safeRedirect(raw: unknown): string | null {
	if (typeof raw !== "string" || !raw.trim()) return null
	try {
		const url = new URL(raw, window.location.origin)
		const base = basePath(url.pathname.replace(/(.)\/+$/, "$1"))
		if (url.origin !== window.location.origin || AUTH_PATHS.includes(base))
			return null
		return url.pathname + url.search + url.hash
	} catch {
		return null
	}
}

/** The `redirect-to` query parameter Frappe pages use when sending visitors to /login. */
export function redirectToFromQuery(query: LocationQuery): string | null {
	const value = query["redirect-to"]
	return safeRedirect(Array.isArray(value) ? value[0] : value)
}

/** The producer's dashboard in a language: /dashboard, /en/dashboard. */
export function dashboardHome(locale: LocaleCode): string {
	return localePath(dashboardPath, locale)
}

/** The Desk's addresses: staff only (frappe/www/desk.py refuses Website Users). */
export function isDeskPath(path: string): boolean {
	return ["/desk", "/app"].some(
		(prefix) =>
			path === prefix ||
			path.startsWith(`${prefix}/`) ||
			path.startsWith(`${prefix}?`),
	)
}

/**
 * Where a logged-in user goes (docs/producer_dashboard/routing.md), from the redirects on offer,
 * first wins:
 * - Staff: the first redirect, else the Desk.
 * - Producers: the first redirect outside the Desk, else their dashboard in the page's language.
 *   A Frappe page that sent them to /login often asks to come back to a Desk page
 *   (/login?redirect-to=/desk/…), which would only refuse them.
 */
export function landingUrl(
	staff: boolean,
	redirects: (string | null)[],
	locale: LocaleCode,
): string {
	const offered = redirects.filter((path): path is string => !!path)
	if (staff) return offered[0] ?? DESK_PATH
	return offered.find((path) => !isDeskPath(path)) ?? dashboardHome(locale)
}

/**
 * Where a successful login goes: `landingUrl`, with producers' page saved at sign-up first. Never
 * Frappe's `home_page`: for a Website User it is the default app's path. A URL for a full page
 * load: the Desk is outside this app, and the load picks up the new session's CSRF token.
 */
export function postLoginUrl(
	result: LoginResult,
	redirectTo: string | null,
	locale: LocaleCode,
): string {
	return isStaff(result)
		? landingUrl(true, [redirectTo], locale)
		: landingUrl(false, [safeRedirect(result.redirect_to), redirectTo], locale)
}

/**
 * Frappe's old login page used hashes for its other forms (/login#signup, /login#forgot); some
 * links still do. The page each one stands for, or null.
 */
export function loginHashPage(
	hash: string,
): "Signup" | "ForgotPassword" | null {
	if (hash === "#signup") return "Signup"
	if (hash === "#forgot") return "ForgotPassword"
	return null
}

const options = ref<LoginOptions | null>(null)
let pending: Promise<void> | null = null

/** Sign-in methods enabled on the site, fetched once and shared by the auth pages. */
export function useLoginOptions() {
	if (!options.value && !pending) {
		pending = getLoginOptions()
			.then((value) => {
				options.value = value
			})
			.catch(() => {
				// Fall back to password login only; the server still enforces everything.
				options.value = {
					password_login: true,
					login_with_username: false,
					login_with_mobile: false,
					email_link: false,
					signup: false,
					providers: [],
				}
			})
	}
	return options
}

/** The look of the links under the auth forms and beside their fields. */
export const AUTH_LINK =
	"inline-flex items-center gap-1.5 font-bold text-brand-green underline-offset-4 hover:underline dark:text-brand-leaf"
