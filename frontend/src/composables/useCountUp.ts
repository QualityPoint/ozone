import { useTransition } from "@vueuse/core"
import { type Ref, computed } from "vue"

/**
 * A number that counts up from 0 to `value` once `active` turns true (a key figure coming
 * into view). With reduced motion it shows the value at once.
 */
export function useCountUp(
	value: number,
	active: Ref<boolean>,
	duration = 1400,
) {
	const reduced =
		typeof window !== "undefined" &&
		window.matchMedia?.("(prefers-reduced-motion: reduce)").matches
	const source = computed(() => (active.value || reduced ? value : 0))
	const shown = useTransition(source, { duration: reduced ? 0 : duration })
	return computed(() => Math.round(shown.value))
}
