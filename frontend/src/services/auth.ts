/**
 * Frappe authentication endpoints used by the login pages (services/auth.ts).
 * Server side: Frappe core, plus ozone/api/auth.py for the session user, the login options,
 * sign-up (Frappe's, with the producer's Lead) and the social login redirect.
 */
import { csrfHeaders, parseServerMessages } from "@/services/http"

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
 * POST to a Frappe method. Like frappe-ui's call(), but on failure it keeps
 * only `_server_messages` (shown by Frappe's login page) and drops the bare
 * `message` (e.g. "Incorrect password" vs "User disabled or missing"), which
 * Frappe hides because it reveals whether an account exists.
 */
async function request<T>(
	method: string,
	args: Record<string, unknown> = {},
	wholeResponse = false,
): Promise<T> {
	const headers = {
		Accept: "application/json",
		"Content-Type": "application/json; charset=utf-8",
		...csrfHeaders(),
	}
	const response = await fetch(`/api/method/${method}`, {
		method: "POST",
		headers,
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

export interface LoginOptions {
	password_login: boolean
	/** Usernames are accepted as well as emails (System Settings). */
	login_with_username: boolean
	/** Mobile numbers are accepted as well as emails (System Settings). */
	login_with_mobile: boolean
	email_link: boolean
	signup: boolean
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
	 * "Logged In" (staff), "No App" (producers), "Password Reset" (password
	 * expired; a reset link was emailed) or absent while two-factor is pending.
	 */
	message?: "Logged In" | "No App" | "Password Reset" | string
	/** Producers: Frappe's default path, which can be an app's Desk page: never followed. Staff: the
	 * site home page, not the Desk. */
	home_page?: string
	/** Producers: the page saved at sign up to return to after the first login. */
	redirect_to?: string
	full_name?: string
	verification?: TwoFactorChallenge
	/** Identifies the pending two-factor login; send it back with the code. */
	tmp_id?: string
}

/** Outcome codes of Frappe's sign_up (ozone.api.auth.sign_up returns them as they are). */
export enum SignupStatus {
	AlreadyRegistered = 0,
	CheckEmail = 1,
	PendingApproval = 2,
}

export function getLoginOptions(): Promise<LoginOptions> {
	return request("ozone.api.auth.get_login_options")
}

/** The logged-in user, as the server sees it (the cookies outlive an expired session). */
export function getSessionUser(): Promise<SessionUser> {
	return request("ozone.api.auth.get_session_user")
}

/** Makes an unlinked website account a producer of its own (its Lead), then answers as getSessionUser. */
export function startProducer(): Promise<SessionUser> {
	return request("ozone.api.auth.start_producer")
}

export function login(email: string, password: string): Promise<LoginResult> {
	return request("login", { usr: email, pwd: password }, true)
}

/** Completes a two-factor login (the server cached the email and password). */
export function verifyLogin(otp: string, tmpId: string): Promise<LoginResult> {
	return request("login", { otp, tmp_id: tmpId }, true)
}

export function logout(): Promise<void> {
	return request("logout")
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

export async function signUp(
	email: string,
	fullName: string,
	redirectTo?: string | null,
): Promise<SignupStatus> {
	const [status] = await request<[SignupStatus, string]>(
		"ozone.api.auth.sign_up",
		{
			email,
			full_name: fullName,
			redirect_to: redirectTo ?? "",
		},
	)
	return status
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

/** True for staff, who belong in the Frappe Desk rather than the SPA. */
export function isStaff(result: LoginResult): boolean {
	return result.message === "Logged In"
}

/** The party a producer's account belongs to (ozone/producer.py). */
export interface Producer {
	doctype: "Customer" | "Lead"
	name: string
	title: string
	/** How many facilities it has registered: none, and the dashboard starts with adding one. */
	facilities: number
}

/** The logged-in user as the server reports it (ozone.api.auth.get_session_user). */
export interface SessionUser {
	name: string
	full_name: string | null
	/** "System User" for staff, "Website User" for producers, null for guests. */
	user_type: "System User" | "Website User" | null
	/** The producer's party; null for staff, guests and accounts nobody has linked yet. */
	producer: Producer | null
}
