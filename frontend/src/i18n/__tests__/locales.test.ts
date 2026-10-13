import { describe, expect, it } from "vitest"

import ar from "../locales/ar"
import en from "../locales/en"

/** Every leaf message as [path, text], with array indices: "brand.tagline.2". */
function leaves(value: unknown, prefix = ""): [string, string][] {
	if (Array.isArray(value)) {
		return value.flatMap((item, i) => leaves(item, `${prefix}.${i}`))
	}
	if (value && typeof value === "object") {
		return Object.entries(value).flatMap(([key, item]) =>
			leaves(item, prefix ? `${prefix}.${key}` : key),
		)
	}
	return [[prefix, String(value)]]
}

const paths = (value: unknown) => leaves(value).map(([path]) => path)

describe("locales", () => {
	it("en has exactly the same keys and list lengths as ar", () => {
		expect(paths(en).sort()).toEqual(paths(ar).sort())
	})

	it("has no empty messages", () => {
		for (const [path, text] of [...leaves(ar), ...leaves(en)]) {
			expect(text.trim(), path).not.toBe("")
		}
	})

	it("avoids characters vue-i18n treats as syntax", () => {
		for (const [path, text] of [...leaves(ar), ...leaves(en)]) {
			expect(text, path).not.toMatch(/[@{}|]/)
		}
	})
})
