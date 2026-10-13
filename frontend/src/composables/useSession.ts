import { getSessionUser } from "@/services/auth"

/** Frappe's login cookies; they stay behind when a session expires, until logout clears them. */
function cookie(name: string): string | null {
	return new URLSearchParams(document.cookie.split("; ").join("&")).get(name)
}

/** Whether the cookies say someone is logged in (instant; the server has the last word). */
export function cookieLoggedIn(): boolean {
	const user = cookie("user_id")
	return !!user && user !== "Guest"
}

/** Whether the cookies say the logged-in user is staff (Frappe sets `system_user` at login). */
export function cookieStaff(): boolean {
	return cookieLoggedIn() && cookie("system_user") === "yes"
}

/**
 * Whether the server confirms a logged-in user, and whether it's staff. Guests are answered
 * by the cookies alone; anyone else is asked once (an expired session leaves its cookies).
 */
export async function confirmedSession(): Promise<{
	loggedIn: boolean
	staff: boolean
}> {
	if (!cookieLoggedIn()) return { loggedIn: false, staff: false }
	try {
		const user = await getSessionUser()
		return {
			loggedIn: user.name !== "Guest",
			staff: user.user_type === "System User",
		}
	} catch {
		return { loggedIn: false, staff: false }
	}
}
