import { useIntersectionObserver } from "@vueuse/core"
import { type MaybeRefOrGetter, ref } from "vue"

/**
 * Becomes true once `target` scrolls into view, then stays true: the cue for an entrance
 * (fade-up, count-up). One place for it, so every section reveals the same way.
 */
export function useReveal(
	target: MaybeRefOrGetter<HTMLElement | null | undefined>,
	threshold = 0.15,
) {
	const revealed = ref(false)
	const { stop } = useIntersectionObserver(
		target,
		([entry]) => {
			if (entry?.isIntersecting) {
				revealed.value = true
				stop()
			}
		},
		{ threshold },
	)
	return revealed
}
