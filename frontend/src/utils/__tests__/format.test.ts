import { describe, expect, it } from "vitest"

import { formatMonth, formatNumber } from "../format"

describe("formatNumber", () => {
	it("groups thousands with Latin digits", () => {
		expect(formatNumber(50000)).toBe("50,000")
		expect(formatNumber(200)).toBe("200")
		expect(formatNumber(1234567.8)).toBe("1,234,568")
	})

	it("keeps at most the decimals asked for", () => {
		expect(formatNumber(15.29108, 2)).toBe("15.29")
		expect(formatNumber(16, 2)).toBe("16")
		expect(formatNumber(0.24, 2)).toBe("0.24")
	})
})

describe("formatMonth", () => {
	it("names Gregorian months in both languages", () => {
		expect(formatMonth(0, "en")).toBe("Jan")
		expect(formatMonth(0, "ar")).toBe("يناير")
		expect(formatMonth(11, "ar")).toBe("ديسمبر")
	})
})
