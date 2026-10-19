import { describe, expect, it } from "vitest"

import {
	THEORETICAL,
	WEIGHED,
	actualRate,
	calibrated,
	gapPercent,
} from "../calibration"

describe("calibration", () => {
	it("starts at the theoretical estimate and closes in on the weighed rate", () => {
		const estimate = calibrated()
		const actual = actualRate()
		expect(estimate).toHaveLength(WEIGHED.length)
		expect(estimate[0]).toBe(THEORETICAL)
		for (let month = 1; month < estimate.length; month++) {
			expect(estimate[month]).toBeGreaterThan(estimate[month - 1])
			expect(estimate[month]).toBeLessThan(actual)
		}
		expect(gapPercent(estimate[0], actual)).toBe(30)
		expect(gapPercent(estimate[estimate.length - 1], actual)).toBe(1)
	})
})
