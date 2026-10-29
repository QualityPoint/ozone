/**
 * Plain `fetch` calls to Frappe methods (`/api/method/<method>`), for public pages, which don't
 * use frappe-ui resources (services/http.ts, the parts the site uses).
 */

/**
 * A failed call: the HTTP status, Frappe's exception class (`exc_type`) when it sent one, and the
 * texts of its `_server_messages` (what frappe.throw said), as plain text.
 */
export class MethodError extends Error {
	constructor(
		readonly status: number,
		readonly excType: string | null,
		readonly serverMessages: string[] = [],
	) {
		super(serverMessages[0] ?? `${excType ?? "Request failed"} (${status})`)
	}
}

/** The texts in Frappe's `_server_messages` (a JSON list of JSON objects), as plain text. */
export function parseServerMessages(raw: unknown): string[] {
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

/**
 * The CSRF header for POSTs. Frappe checks it once the visitor has a session; the token is in the
 * page (boot data), except on the dev server, where the check is turned off.
 */
export function csrfHeaders(): Record<string, string> {
	const token = window.csrf_token
	return token && token !== "{{ csrf_token }}"
		? { "X-Frappe-CSRF-Token": token }
		: {}
}

/**
 * The page's language (`<html lang>`, set by setLocale) as `_lang`, which Frappe reads before the
 * user's own language (frappe/translate.py: get_language): server labels and refusals then follow
 * the page, /en or Arabic, whatever the account's language. A caller's own `_lang` wins.
 */
function withLang<T extends Record<string, unknown>>(
	args: T,
): T & { _lang?: string } {
	const lang =
		typeof document === "undefined" ? "" : document.documentElement.lang
	return lang && !("_lang" in args) ? { ...args, _lang: lang } : args
}

async function result<T>(response: Response): Promise<T> {
	const body = (await response.json().catch(() => ({}))) as {
		message?: T
		exc_type?: string
		_server_messages?: string
	}
	if (!response.ok) {
		throw new MethodError(
			response.status,
			body.exc_type ?? null,
			parseServerMessages(body._server_messages),
		)
	}
	return body.message as T
}

/** GET a method; resolves to its `message`. */
export async function getMethod<T>(
	method: string,
	params: Record<string, string> = {},
): Promise<T> {
	const query = new URLSearchParams(withLang(params)).toString()
	const response = await fetch(
		`/api/method/${method}${query ? `?${query}` : ""}`,
		{ headers: { Accept: "application/json" } },
	)
	return result<T>(response)
}

/**
 * Raised on `window` after every POST that succeeded: something changed on the server (a facility saved, a request
 * sent, a quotation answered, a contract signed…), so whatever shows a summary of it reloads (the dashboard's menu
 * counts: DashboardLayout).
 */
export const CHANGED = "ozone:changed"

/** POST JSON to a method (with the CSRF header); resolves to its `message`. */
export async function postMethod<T>(
	method: string,
	args: Record<string, unknown> = {},
): Promise<T> {
	const response = await fetch(`/api/method/${method}`, {
		method: "POST",
		headers: {
			Accept: "application/json",
			"Content-Type": "application/json; charset=utf-8",
			...csrfHeaders(),
		},
		body: JSON.stringify(withLang(args)),
	})
	const message = await result<T>(response)
	if (typeof window !== "undefined") window.dispatchEvent(new Event(CHANGED))
	return message
}

/**
 * Upload a file with Frappe's `upload_file` (any logged-in user may); resolves to its URL. Private
 * files (the default) are readable only by their owner and staff: credential documents. An avatar
 * is public, so it shows wherever the user appears.
 */
export async function uploadFile(
	file: File,
	isPrivate = true,
): Promise<string> {
	const form = new FormData()
	form.append("file", file, file.name)
	form.append("is_private", isPrivate ? "1" : "0")
	const response = await fetch("/api/method/upload_file", {
		method: "POST",
		headers: { Accept: "application/json", ...csrfHeaders() },
		body: form,
	})
	return (await result<{ file_url: string }>(response)).file_url
}
