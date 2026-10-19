/**
 * The Naqel page's AI-calibration chart (NaqelCalibrationChart; Naqel's presentation, pp. 54-57),
 * as numbers: over a year of operation, the AI pulls a facility's generation estimate from the
 * calculator's theoretical value toward what the trucks actually weigh. Illustrative values, not
 * a facility's data (the chart says so).
 */

/** The calculator's theoretical estimate, m³ a day. */
export const THEORETICAL = 0.3

/** What the trucks weighed each month, January to December, m³ a day. */
export const WEIGHED = [
	0.44, 0.41, 0.45, 0.43, 0.4, 0.46, 0.42, 0.44, 0.41, 0.43, 0.45, 0.42,
] as const

/** How fast the calibration closes in on reality: the gap shrinks by e each this many months. */
const LEARNING_MONTHS = 3.5

/** The actual rate the weighings point to: their mean. */
export function actualRate(weighed: readonly number[] = WEIGHED): number {
	return weighed.reduce((sum, value) => sum + value, 0) / weighed.length
}

/**
 * The AI-calibrated estimate month by month: starting from the theoretical value, closing in on
 * the actual rate as the weighings come in.
 */
export function calibrated(
	weighed: readonly number[] = WEIGHED,
	theoretical = THEORETICAL,
): number[] {
	const actual = actualRate(weighed)
	return weighed.map(
		(_, month) =>
			actual - (actual - theoretical) * Math.exp(-month / LEARNING_MONTHS),
	)
}

/** How far an estimate is from the actual rate, as a whole percentage of it. */
export function gapPercent(estimate: number, actual: number): number {
	return Math.round((Math.abs(actual - estimate) / actual) * 100)
}
