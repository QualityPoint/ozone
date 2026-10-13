import { describe, expect, it } from "vitest"
import { createMemoryHistory, createRouter } from "vue-router"

import { routes } from "../routes"

const router = createRouter({ history: createMemoryHistory(), routes })

describe("routes", () => {
	it("serves the landing page at /", () => {
		const route = router.resolve("/")
		expect(route.name).toBe("Landing")
		expect(route.meta).toMatchObject({ layout: "public" })
	})

	it("sends unknown paths to the landing page", () => {
		const [record] = router.resolve("/no-such-page").matched
		expect(record.redirect).toBe("/")
	})

	it("gives every page a layout", () => {
		for (const route of router.getRoutes().filter((r) => !r.redirect)) {
			expect(route.meta.layout).toBeTruthy()
		}
	})
})
