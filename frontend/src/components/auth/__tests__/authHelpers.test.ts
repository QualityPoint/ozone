// @vitest-environment jsdom
import { describe, expect, it } from "vitest"

import { AuthRequestError, DESK_PATH } from "@/services/auth"
import {
	authErrorMessage,
	emailError,
	forgotHash,
	postLoginUrl,
	redirectToFromQuery,
	safeRedirect,
} from "../authHelpers"

const t = (key: string) => `t:${key}`

describe("safeRedirect", () => {
	it("keeps same-site paths with query and hash", () => {
		expect(safeRedirect("/desk/todo?x=1#top")).toBe("/desk/todo?x=1#top")
		expect(safeRedirect(`${window.location.origin}/en`)).toBe("/en")
	})

	it("rejects other sites, protocol-relative URLs and other schemes", () => {
		for (const bad of [
			"https://evil.com/x",
			"//evil.com/x",
			"javascript:alert(1)",
			"",
			"   ",
			null,
			42,
		]) {
			expect(safeRedirect(bad), String(bad)).toBeNull()
		}
	})

	it("rejects the auth pages themselves, in every language (redirect loops)", () => {
		for (const page of [
			"/login?redirect-to=/desk",
			"/login/",
			"/en/login",
			"/forgot-password",
			"/en/forgot-password",
		]) {
			expect(safeRedirect(page), page).toBeNull()
		}
		expect(safeRedirect("/desk/login-log")).toBe("/desk/login-log")
	})

	it("reads Frappe's redirect-to query parameter", () => {
		expect(redirectToFromQuery({ "redirect-to": "/desk/user" })).toBe(
			"/desk/user",
		)
		expect(
			redirectToFromQuery({ "redirect-to": "https://evil.com" }),
		).toBeNull()
		expect(redirectToFromQuery({})).toBeNull()
	})
})

describe("postLoginUrl", () => {
	it("goes to redirect-to, else the Desk for staff and the website for anyone else", () => {
		expect(postLoginUrl({ message: "Logged In" }, "/desk/todo")).toBe(
			"/desk/todo",
		)
		expect(postLoginUrl({ message: "Logged In" }, null)).toBe(DESK_PATH)
		expect(postLoginUrl({ message: "No App" }, null)).toBe("/")
	})
})

describe("forgotHash", () => {
	it("recognises the reset form's hash of Frappe's old login page", () => {
		expect(forgotHash("#forgot")).toBe(true)
		expect(forgotHash("#login")).toBe(false)
		expect(forgotHash("")).toBe(false)
	})
})

describe("authErrorMessage", () => {
	it("follows Frappe: server messages first, then a default per status", () => {
		expect(authErrorMessage(new AuthRequestError(401, []), t)).toBe(
			"t:auth.errors.invalidCredentials",
		)
		expect(
			authErrorMessage(new AuthRequestError(401, ["Account locked"]), t),
		).toBe("Account locked")
		expect(authErrorMessage(new AuthRequestError(429, ["Too many"]), t)).toBe(
			"t:auth.errors.tooManyAttempts",
		)
		expect(authErrorMessage(new AuthRequestError(500, []), t)).toBe(
			"t:auth.errors.generic",
		)
		expect(authErrorMessage(new Error("network"), t)).toBe(
			"t:auth.errors.generic",
		)
	})
})

describe("emailError", () => {
	it("asks for a value first, then a plausible address", () => {
		expect(emailError("  ", t)).toBe("t:auth.errors.required")
		expect(emailError("not-an-email", t)).toBe("t:auth.errors.invalidEmail")
		expect(emailError(" someone@ozone-services.net ", t)).toBeUndefined()
	})
})
