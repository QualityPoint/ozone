import { describe, expect, it } from "vitest"

import {
	basePath,
	defaultLocale,
	localeHome,
	localePath,
	navItems,
	pagePaths,
} from "../site"

describe("page addresses", () => {
	it("serves the default language, Arabic, without a prefix", () => {
		expect(defaultLocale).toBe("ar")
		expect(localePath("/", "ar")).toBe("/")
		expect(localePath("/services", "ar")).toBe("/services")
	})

	it("puts English under /en and back", () => {
		expect(localePath("/", "en")).toBe("/en")
		expect(localePath("/services", "en")).toBe("/en/services")
		expect(basePath("/en")).toBe("/")
		expect(basePath("/en/services")).toBe("/services")
		expect(basePath("/services")).toBe("/services")
		expect(basePath("/english")).toBe("/english") // not the /en prefix
	})

	it("derives each language's landing page from the page paths", () => {
		expect(localeHome).toEqual({ ar: "/", en: "/en" })
		expect(pagePaths.landing).toBe("/")
	})
})

describe("navItems", () => {
	it("has unique ids", () => {
		const ids = navItems.map((item) => item.id)
		expect(new Set(ids).size).toBe(ids.length)
	})
})
