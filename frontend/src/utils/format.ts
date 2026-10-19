import type { LocaleCode } from "@/types"

/**
 * A number with thousands separators and Latin digits, in both languages (as blinktech shows
 * figures), with at most `digits` decimals: 50000 → "50,000", 15.291 → "15.29" with 2.
 */
export function formatNumber(value: number, digits = 0): string {
	return new Intl.NumberFormat("en-US", {
		maximumFractionDigits: digits,
	}).format(value)
}

/**
 * Dates in the visitor's language: the Gregorian calendar in Arabic too (ar-SA would default to the
 * Hijri one), with Latin digits.
 */
const DATE_LOCALE: Record<LocaleCode, string> = {
	ar: "ar-SA-u-nu-latn-ca-gregory",
	en: "en-GB",
}

/** A month's short name, January being 0: "Jan", "يناير". */
export function formatMonth(month: number, code: LocaleCode): string {
	return new Intl.DateTimeFormat(DATE_LOCALE[code], { month: "short" }).format(
		new Date(2026, month, 1),
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
