/**
 * A whole number with thousands separators and Latin digits, in both languages (as blinktech
 * shows figures): 50000 → "50,000".
 */
export function formatNumber(value: number): string {
	return new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(
		value,
	)
}
