import { computed, ref } from "vue"
import { useI18n } from "vue-i18n"

import { MethodError } from "@/services/http"
import type { Notice } from "@/types"

/**
 * How the dashboard's forms send themselves (blinktech's useFormSubmit, for forms whose refusals
 * come from frappe.throw). Each form gives its rules (`validate`: a translated message per field
 * in error) and how it sends (`send`).
 * - Errors show from the first attempt to send, then follow each change.
 * - A refusal shows the server's own message (frappe.throw), else a translated default.
 */
export function useFormSubmit<Field extends string>(options: {
	validate: () => Partial<Record<Field, string>>
	send: () => Promise<void>
	/** The success message's key, if the form shows one. */
	sent?: string
}) {
	const { t } = useI18n()
	const tried = ref(false)
	const busy = ref(false)
	const notice = ref<Notice | null>(null)
	const errors = computed<Partial<Record<Field, string>>>(() =>
		tried.value ? options.validate() : {},
	)

	async function submit(): Promise<boolean> {
		tried.value = true
		notice.value = null
		if (Object.keys(errors.value).length) return false
		busy.value = true
		try {
			await options.send()
			tried.value = false
			if (options.sent)
				notice.value = { kind: "success", text: t(options.sent) }
			return true
		} catch (error) {
			notice.value = { kind: "error", text: refusal(error, t) }
			return false
		} finally {
			busy.value = false
		}
	}

	function reset(): void {
		tried.value = false
		notice.value = null
	}

	return { errors, busy, notice, submit, reset }
}

/** The text for a refused call: what frappe.throw said, else a default for its kind. */
export function refusal(error: unknown, t: (key: string) => string): string {
	if (error instanceof MethodError) {
		if (error.serverMessages.length) return error.serverMessages.join(" ")
		if (error.excType === "PermissionError")
			return t("dashboard.errors.notPermitted")
	}
	return t("dashboard.errors.generic")
}
