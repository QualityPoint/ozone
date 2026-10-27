import { ref } from "vue"

import { payContract } from "@/services/portal"

/**
 * Pays a contract's required payment: opens its checkout (its Payment Request's: Moyasar), which
 * brings the producer back once paid. `paying` is the contract being opened, `failed` the one
 * whose checkout couldn't be.
 */
export function usePayContract() {
	const paying = ref<string | null>(null)
	const failed = ref<string | null>(null)

	async function pay(name: string): Promise<void> {
		paying.value = name
		failed.value = null
		try {
			const { url } = await payContract(name)
			window.location.assign(url)
		} catch {
			failed.value = name
			paying.value = null
		}
	}

	return { paying, failed, pay }
}
