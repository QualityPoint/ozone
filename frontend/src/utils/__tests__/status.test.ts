import { describe, expect, it } from "vitest"

import { statusBadge } from "../status"

describe("statusBadge", () => {
	it("colours a status as its DocType state", () => {
		expect(statusBadge("pink")).toContain("bg-pink-100")
		expect(statusBadge("purple")).toContain("bg-purple-100")
		expect(statusBadge("light-blue")).toContain("bg-blue-50")
	})

	it("falls back to gray", () => {
		expect(statusBadge("teal")).toBe(statusBadge("gray"))
		expect(statusBadge(null)).toBe(statusBadge("gray"))
	})
})
