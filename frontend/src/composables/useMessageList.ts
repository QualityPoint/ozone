import { useI18n } from "vue-i18n"

/**
 * Reads an array from the locale messages as translated strings, e.g.
 * `list("sectors.software.items")`. Plain `t()` only resolves single keys.
 * Pass `field` for arrays of objects: `list("why.items", "title")`.
 */
export function useMessageList() {
	const { t, tm } = useI18n()

	function list(key: string, field?: string): string[] {
		const raw = tm(key)
		if (!Array.isArray(raw)) {
			return []
		}
		return raw.map((_, i) => t(field ? `${key}.${i}.${field}` : `${key}.${i}`))
	}

	return { list }
}
