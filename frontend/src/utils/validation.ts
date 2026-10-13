/** Loose checks for form fields; the server does the real validation. */

export function isEmail(value: string): boolean {
	return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim())
}
