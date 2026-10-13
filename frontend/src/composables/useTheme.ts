import { createSharedComposable, useDark, useToggle } from "@vueuse/core"
import { watchEffect } from "vue"

/** localStorage key; values "light" | "dark" | "auto". Also read by index.html. */
export const THEME_STORAGE_KEY = "ozone-theme"

/** Browser UI colour (mobile address bar) per theme: the brand green, and the dark page. */
export const THEME_COLOR = { light: "#11532a", dark: "#08190f" }

/**
 * Light/dark theme, shared by every component.
 *
 * Follows the system setting until the visitor picks one, then remembers it.
 * Sets `data-theme` on <html>, which drives both our `site-*` tokens and
 * frappe-ui's own dark styles (its Tailwind preset uses the same selector).
 */
export const useTheme = createSharedComposable(() => {
	const isDark = useDark({
		selector: "html",
		attribute: "data-theme",
		valueDark: "dark",
		valueLight: "light",
		storageKey: THEME_STORAGE_KEY,
	})
	const toggle = useToggle(isDark)

	watchEffect(() => {
		document
			.querySelector('meta[name="theme-color"]')
			?.setAttribute(
				"content",
				isDark.value ? THEME_COLOR.dark : THEME_COLOR.light,
			)
	})

	return { isDark, toggle }
})
