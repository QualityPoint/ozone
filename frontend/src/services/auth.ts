/**
 * Frappe authentication endpoints used by the login pages.
 * Server side: Frappe core, plus ozone/api/auth.py for the login options, the session user
 * and the social login redirect.
 */
import { csrfHeaders, getMethod } from "@/services/http"

/** A failed auth request. `serverMessages` are only the texts Frappe's own login page shows. */
export class AuthRequestError extends Error {
	constructor(
		readonly status: number,
		readonly serverMessages: string[],
	) {
		super(serverMessages[0] ?? `Request failed (${status})`)
	}
}

/**
 * POST to a Frappe method. On failure it keeps only `_server_messages` (shown by Frappe's login
 * page) and drops the bare `message` ("Incorrect password" vs "User disabled or missing"),
 * which Frappe hides because it reveals whether an account exists.
 */
async function request<T>(
	method: string,
	args: Record<string, unknown> = {},
	wholeResponse = false,
): Promise<T> {
	const response = await fetch(`/api/method/${method}`, {
		method: "POST",
		headers: {
			Accept: "application/json",
			"Content-Type": "application/json; charset=utf-8",
			...csrfHeaders(),
		},
		body: JSON.stringify(args),
	})
	const data = await response.json().catch(() => ({}))
	if (!response.ok) {
		throw new AuthRequestError(
			response.status,
			parseServerMessages(data._server_messages),
		)
	}
	return (wholeResponse ? data : data.message) as T
}

function parseServerMessages(raw: unknown): string[] {
	if (typeof raw !== "string") return []
	try {
		return (JSON.parse(raw) as string[])
			.map((entry) => {
				try {
					return (JSON.parse(entry) as { message?: string }).message ?? entry
				} catch {
					return entry
				}
			})
			.map(toPlainText)
			.filter(Boolean)
	} catch {
		return []
	}
}

/** Server messages may contain HTML; render them as text only. */
function toPlainText(html: string): string {
	return (
		new DOMParser()
			.parseFromString(html, "text/html")
			.body.textContent?.trim() ?? ""
	)
}

export interface LoginOptions {
	password_login: boolean
	/** Usernames are accepted as well as emails (System Settings). */
	login_with_username: boolean
	/** Mobile numbers are accepted as well as emails (System Settings). */
	login_with_mobile: boolean
	email_link: boolean
	providers: { name: string; label: string }[]
}

/** Second step of two-factor login (System Settings → Enable Two Factor Auth). */
export interface TwoFactorChallenge {
	method: "OTP App" | "SMS" | "Email"
	/** False when the code could not be delivered or the OTP app isn't set up. */
	setup: boolean
	/** Server text, e.g. where an SMS code was sent. */
	prompt?: string
}

export interface LoginResult {
	/**
	 * "Logged In" (staff), "No App" (website users), "Password Reset" (password expired; a
	 * reset link was emailed) or absent while two-factor is pending.
	 */
	message?: "Logged In" | "No App" | "Password Reset" | string
	verification?: TwoFactorChallenge
	/** Identifies the pending two-factor login; send it back with the code. */
	tmp_id?: string
}

/** The logged-in user as the server sees it (the cookies outlive an expired session). */
export interface SessionUser {
	name: string
	/** "System User" for staff, "Website User" otherwise, null for guests. */
	user_type: "System User" | "Website User" | null
}

export function getLoginOptions(): Promise<LoginOptions> {
	return getMethod("ozone.api.auth.get_login_options")
}

export function getSessionUser(): Promise<SessionUser> {
	return getMethod("ozone.api.auth.get_session_user")
}

export function login(user: string, password: string): Promise<LoginResult> {
	return request("login", { usr: user, pwd: password }, true)
}

/** Completes a two-factor login (the server cached the user and password). */
export function verifyLogin(otp: string, tmpId: string): Promise<LoginResult> {
	return request("login", { otp, tmp_id: tmpId }, true)
}

/** Emails a one-time login link. Responds the same whether or not the account exists. */
export function sendLoginLink(email: string): Promise<void> {
	return request("frappe.www.login.send_login_link", { email })
}

/** Emails a password reset link. Responds the same whether or not the account exists. */
export function resetPassword(email: string): Promise<void> {
	return request("frappe.core.doctype.user.user.reset_password", {
		user: email,
	})
}

/** Full-page URL that starts an OAuth login (browser navigation, not fetch). */
export function socialLoginUrl(
	provider: string,
	redirectTo?: string | null,
): string {
	const params = new URLSearchParams({ provider })
	if (redirectTo) params.set("redirect_to", redirectTo)
	return `/api/method/ozone.api.auth.social_login?${params}`
}

/** Frappe Desk, where staff work (outside this app; use a full-page navigation). */
export const DESK_PATH = "/desk"

/** True for staff, who belong in the Frappe Desk. */
export function isStaff(result: LoginResult): boolean {
	return result.message === "Logged In"
}
