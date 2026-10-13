import { describe, expect, it } from "vitest"

import { formatPhone, sanitizeContact, whatsappHref } from "../useSiteContact"

describe("useSiteContact helpers", () => {
	it("formats Saudi mobiles and leaves other numbers alone", () => {
		expect(formatPhone("+966546906900")).toBe("+966 54 690 6900")
		expect(formatPhone("+966 54 690 6900")).toBe("+966 54 690 6900")
		expect(formatPhone("+20 100 123 4567")).toBe("+20 100 123 4567")
	})

	it("builds a digits-only wa.me link", () => {
		expect(whatsappHref("+966 54 690 6900")).toBe("https://wa.me/966546906900")
	})

	it("keeps only known platforms and https links, and nulls empty details", () => {
		const contact = sanitizeContact({
			email: " info@ozone.sa ",
			phone: "",
			address: { ar: " المدينة المنورة ", en: "", fr: 3 },
			map: "http://maps.example.com",
			socials: [
				{ platform: "X", url: "https://x.com/ozone" },
				{ platform: "Facebook", url: "facebook.com/ozone" },
				{ platform: "Myspace", url: "https://myspace.com/x" },
				{ platform: "YouTube", url: "javascript:alert(1)" },
			],
		})
		expect(contact.email).toBe("info@ozone.sa")
		expect(contact.phone).toBeNull()
		expect(contact.address).toEqual({ ar: "المدينة المنورة" })
		expect(contact.map).toBeNull()
		expect(contact.socials).toEqual([
			{ platform: "X", url: "https://x.com/ozone" },
		])
	})

	it("survives missing or malformed boot data", () => {
		expect(sanitizeContact(undefined)).toEqual({
			email: null,
			phone: null,
			whatsapp: null,
			address: {},
			map: null,
			socials: [],
		})
		expect(sanitizeContact("{{ site_contact }}").socials).toEqual([])
	})
})
