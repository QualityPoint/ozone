import { defineStore } from "pinia"
import { computed, ref } from "vue"

import {
	type SessionUser,
	getSessionUser,
	startProducer,
} from "@/services/auth"

/** The logged-in user as reported by the server (ozone.api.auth.get_session_user). */
export const useUserStore = defineStore("user", () => {
	const user = ref<SessionUser | null>(null)
	let pending: Promise<void> | null = null

	/** Staff work in the Frappe Desk; producers use this app's dashboard. */
	const isStaff = computed(() => user.value?.user_type === "System User")
	/** The producer's party, once someone has linked the account (docs/producer_dashboard/identity.md). */
	const producer = computed(() => user.value?.producer ?? null)

	/** Loads the user once; later calls reuse the result until reload(). */
	function ensureLoaded(): Promise<void> {
		if (user.value) return Promise.resolve()
		pending ??= getSessionUser()
			.then(async (data) => {
				// A website account nobody has linked yet starts as a producer of its own (its Lead), so it
				// can register its facility at once; only an email on a Customer's contact stays unlinked.
				user.value =
					data.user_type === "Website User" && !data.producer
						? await startProducer().catch(() => data)
						: data
			})
			.finally(() => {
				pending = null
			})
		return pending
	}

	/** Asks the server again (after logging in or out). */
	function reload(): Promise<void> {
		user.value = null
		return ensureLoaded()
	}

	/** Forgets the user (after logging out). */
	function reset(): void {
		user.value = null
	}

	return { user, isStaff, producer, ensureLoaded, reload, reset }
})
