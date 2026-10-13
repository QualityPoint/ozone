import { describe, expect, it } from "vitest"
import { createMemoryHistory, createRouter } from "vue-router"

import { routes } from "../routes"

const router = createRouter({ history: createMemoryHistory(), routes })

describe("routes", () => {
	it("serves the Arabic landing page at /", () => {
		const route = router.resolve("/")
		expect(route.name).toBe("Landing")
		expect(route.meta).toMatchObject({
			layout: "public",
			locale: "ar",
			page: "landing",
		})
	})

	it("serves the English landing page at /en", () => {
		const route = router.resolve("/en")
		expect(route.name).toBe("LandingEn")
		expect(route.meta).toMatchObject({
			layout: "public",
			locale: "en",
			page: "landing",
		})
	})

	it("serves the capabilities page in each language", () => {
		for (const [path, name, locale] of [
			["/capabilities", "Capabilities", "ar"],
			["/en/capabilities", "CapabilitiesEn", "en"],
		]) {
			const route = router.resolve(path)
			expect(route.name, path).toBe(name)
			expect(route.meta, path).toMatchObject({
				layout: "public",
				locale,
				page: "capabilities",
			})
		}
	})

	it("serves the login pages in each language, on the auth layout, for guests", () => {
		for (const [path, name, locale] of [
			["/login", "Login", "ar"],
			["/en/login", "LoginEn", "en"],
			["/forgot-password", "ForgotPassword", "ar"],
			["/en/forgot-password", "ForgotPasswordEn", "en"],
		]) {
			const route = router.resolve(path)
			expect(route.name, path).toBe(name)
			expect(route.meta, path).toMatchObject({
				layout: "auth",
				locale,
				guestOnly: true,
			})
			expect(route.meta.page, path).toBeUndefined() // not a public page: not indexed
		}
	})

	it("sends unknown paths to their language's landing page", () => {
		expect(router.resolve("/no-such-page").matched[0].redirect).toBe("/")
		expect(router.resolve("/en/no-such-page").matched[0].redirect).toBe("/en")
	})

	it("gives every page a layout", () => {
		for (const route of router.getRoutes().filter((r) => !r.redirect)) {
			expect(route.meta.layout).toBeTruthy()
		}
	})
})
