/**
 * A whole number with thousands separators and Latin digits, in both languages (as blinktech
 * shows figures): 50000 → "50,000".
 */
export function formatNumber(value: number): string {
	return new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(
		value,
	)
}

/** An amount in its currency, with Latin digits in both languages: "3,900.00 SAR" / "3,900.00 ر.س.". */
export function formatMoney(
	value: number,
	currency: string,
	locale: string,
): string {
	return new Intl.NumberFormat(locale === "ar" ? "ar-SA-u-nu-latn" : "en-US", {
		style: "currency",
		currency,
		maximumFractionDigits: 2,
	}).format(value)
}

export type PluralForms = Record<
	"one" | "two" | "few" | "many" | "other",
	string
>

/**
 * A counted phrase from its plural forms (Intl.PluralRules): "one" and "two" are whole phrases
 * ("شهران", "twice"); the others follow the number, after `lead` when given ("كل 3 أيام", "every
 * 3 days").
 */
export function counted(
	count: number,
	forms: PluralForms,
	locale: string,
	lead = "",
): string {
	const form = new Intl.PluralRules(locale).select(count)
	if (form === "one" || form === "two") return forms[form]
	const phrase = `${formatNumber(count)} ${forms[form === "zero" ? "other" : form]}`
	return lead ? `${lead} ${phrase}` : phrase
}
