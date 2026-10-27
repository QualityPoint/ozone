import { defineStore } from "pinia"
import { computed, ref } from "vue"

import { type Overview, getOverview } from "@/services/portal"

/**
 * The producer's overview (ozone.api.portal.get_overview), for the overview page and the menu's
 * counts. The layout reloads it on every dashboard page, so both follow what the producer just did.
 */
export const useDashboardStore = defineStore("dashboard", () => {
	const overview = ref<Overview | null>(null)
	const failed = ref(false)

	async function load(): Promise<void> {
		try {
			overview.value = await getOverview()
			failed.value = false
		} catch {
			failed.value = true
		}
	}

	/** The pages where a record waits for the producer (a payment, an answer, a draft). */
	const waiting = computed(
		() =>
			new Set<string>(
				(overview.value?.next_steps ?? [])
					.filter((step) => step.name)
					.map((step) => step.section),
			),
	)

	return { overview, failed, waiting, load }
})
