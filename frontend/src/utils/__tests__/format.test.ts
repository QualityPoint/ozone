import { describe, expect, it } from "vitest"

import { formatNumber } from "../format"

describe("formatNumber", () => {
	it("groups thousands with Latin digits", () => {
		expect(formatNumber(50000)).toBe("50,000")
		expect(formatNumber(200)).toBe("200")
		expect(formatNumber(1234567.8)).toBe("1,234,568")
	})
})
