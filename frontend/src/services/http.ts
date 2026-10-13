/**
 * Plain `fetch` calls to Frappe methods (`/api/method/<method>`), for public pages, which
 * don't use frappe-ui resources.
 */

/** A failed call: the HTTP status and Frappe's exception class (`exc_type`), when it sent one. */
export class MethodError extends Error {
	constructor(
		readonly status: number,
		readonly excType: string | null,
	) {
		super(`${excType ?? "Request failed"} (${status})`)
	}
}

async function result<T>(response: Response): Promise<T> {
	const body = (await response.json().catch(() => ({}))) as {
		message?: T
		exc_type?: string
	}
	if (!response.ok) {
		throw new MethodError(response.status, body.exc_type ?? null)
	}
	return body.message as T
}

/** GET a method; resolves to its `message`. */
export async function getMethod<T>(
	method: string,
	params: Record<string, string> = {},
): Promise<T> {
	const query = new URLSearchParams(params).toString()
	const response = await fetch(
		`/api/method/${method}${query ? `?${query}` : ""}`,
		{ headers: { Accept: "application/json" } },
	)
	return result<T>(response)
}
