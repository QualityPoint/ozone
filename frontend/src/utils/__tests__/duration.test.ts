import { describe, expect, it } from "vitest"

import { durationBetween } from "../duration"

// The same cases as naqel's duration_between (naqel/utils/party.py)
describe("durationBetween", () => {
	it("takes the largest whole unit", () => {
		expect(durationBetween("2026-01-01", "2026-12-31")).toEqual({
			count: 1,
			uom: "Year",
		})
		expect(durationBetween("2026-01-01", "2027-12-31")).toEqual({
			count: 2,
			uom: "Year",
		})
		expect(durationBetween("2026-12-01", "2027-02-28")).toEqual({
			count: 3,
			uom: "Month",
		})
		expect(durationBetween("2026-01-15", "2026-04-14")).toEqual({
			count: 3,
			uom: "Month",
		})
		expect(durationBetween("2026-01-31", "2026-02-27")).toEqual({
			count: 1,
			uom: "Month",
		})
		expect(durationBetween("2026-03-01", "2026-03-10")).toEqual({
			count: 10,
			uom: "Day",
		})
	})

	it("has none for a missing or reversed range", () => {
		expect(durationBetween("2026-03-10", "")).toBeNull()
		expect(durationBetween("2026-03-10", "2026-03-01")).toBeNull()
	})
})
