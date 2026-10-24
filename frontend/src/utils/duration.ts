/**
 * A service's duration from its dates, as naqel works it out (naqel/utils/party.py: duration_between): inclusive,
 * in the largest whole unit. The form shows it; the server sets it.
 */
export type DurationUom = "Day" | "Month" | "Year"

/** "2026-12-01" as a UTC date. */
function parse(value: string): Date {
	const [year, month, day] = value.split("-").map(Number)
	return new Date(Date.UTC(year, month - 1, day))
}

/** The last day of `count` whole units from `start`, inclusive (a month past its end keeps the month's last day). */
export function addDuration(
	start: Date,
	count: number,
	uom: DurationUom,
): Date {
	const year = start.getUTCFullYear()
	const month = start.getUTCMonth()
	const day = start.getUTCDate()
	if (uom === "Day") return new Date(Date.UTC(year, month, day + count - 1))
	const target = month + (uom === "Year" ? count * 12 : count)
	const lastDay = new Date(Date.UTC(year, target + 1, 0)).getUTCDate()
	return new Date(Date.UTC(year, target, Math.min(day, lastDay) - 1))
}

/** The earliest end date of a service started on `startDate` that lasts at least `period`, as "2026-10-31"
 *  (naqel/utils/service_term.py: minimum_end_date); "" without either. */
export function minimumEndDate(
	startDate: string,
	period: { count: number; uom: DurationUom } | null,
): string {
	if (!startDate || !period) return ""
	return addDuration(parse(startDate), period.count, period.uom)
		.toISOString()
		.slice(0, 10)
}

/** Jan 1 – Dec 31 → 1 Year; Dec 1 – Feb 28 → 3 Months; Mar 1 – Mar 10 → 10 Days. Null for a missing or reversed range. */
export function durationBetween(
	startDate: string,
	endDate: string,
): { count: number; uom: DurationUom } | null {
	if (!startDate || !endDate) return null
	const start = parse(startDate)
	const end = parse(endDate)
	if (end < start) return null
	for (const [uom, most] of [
		["Year", 100],
		["Month", 1200],
	] as const) {
		for (let count = 1; count <= most; count++) {
			const last = addDuration(start, count, uom).getTime()
			if (last === end.getTime()) return { count, uom }
			if (last > end.getTime()) break
		}
	}
	return {
		count: Math.round((end.getTime() - start.getTime()) / 86_400_000) + 1,
		uom: "Day",
	}
}
