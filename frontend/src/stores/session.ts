import { defineStore } from "pinia"
import { computed, ref } from "vue"

import * as auth from "@/services/auth"
import { useUserStore } from "./user"

/** Reads the logged-in user from Frappe's `user_id` cookie; Guest counts as logged out. */
export function sessionUser(): string | null {
	const cookies = new URLSearchParams(document.cookie.split("; ").join("&"))
	const user = cookies.get("user_id")
	return user && user !== "Guest" ? user : null
}

/**
 * Session state only. Navigation after login/logout belongs to the caller
 * (views and router guards), so this store never imports the router.
 */
export const useSessionStore = defineStore("session", () => {
	const userStore = useUserStore()

	const user = ref<string | null>(sessionUser())
	const isLoggedIn = computed(() => !!user.value)

	async function login(
		email: string,
		password: string,
	): Promise<auth.LoginResult> {
		const result = await auth.login(email, password)
		user.value = sessionUser()
		userStore.reload()
		return result
	}

	async function verifyLogin(
		otp: string,
		tmpId: string,
	): Promise<auth.LoginResult> {
		const result = await auth.verifyLogin(otp, tmpId)
		user.value = sessionUser()
		userStore.reload()
		return result
	}

	async function logout(): Promise<void> {
		await auth.logout()
		user.value = sessionUser()
		userStore.reset()
	}

	return { user, isLoggedIn, login, verifyLogin, logout }
})
