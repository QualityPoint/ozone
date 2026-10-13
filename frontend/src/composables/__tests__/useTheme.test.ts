// @vitest-environment jsdom
import { describe, expect, it } from "vitest"
import { nextTick } from "vue"

import { THEME_COLOR, THEME_STORAGE_KEY, useTheme } from "../useTheme"

describe("useTheme", () => {
	it("toggles data-theme on <html>, remembers the choice and is shared", async () => {
		document.head.innerHTML = `<meta name="theme-color" content="${THEME_COLOR.light}" />`
		const html = document.documentElement
		const { isDark, toggle } = useTheme()

		// No saved choice and no dark system preference in jsdom: light.
		expect(isDark.value).toBe(false)

		toggle()
		await nextTick()
		expect(html.getAttribute("data-theme")).toBe("dark")
		expect(localStorage.getItem(THEME_STORAGE_KEY)).toBe("dark")
		expect(
			document
				.querySelector('meta[name="theme-color"]')
				?.getAttribute("content"),
		).toBe(THEME_COLOR.dark)

		// A second caller sees the same state.
		expect(useTheme().isDark.value).toBe(true)

		toggle()
		await nextTick()
		expect(html.getAttribute("data-theme")).toBe("light")
	})
})
