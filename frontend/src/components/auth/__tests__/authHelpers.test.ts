// @vitest-environment jsdom
import { describe, expect, it } from "vitest"

import { AuthRequestError, DESK_PATH } from "@/services/auth"
import {
	authErrorMessage,
	dashboardHome,
	emailError,
	isDeskPath,
	loginHashPage,
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
			"/signup",
			"/en/signup",
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
	it("sends staff to redirect-to, else the Desk", () => {
		expect(postLoginUrl({ message: "Logged In" }, "/desk/todo", "ar")).toBe(
			"/desk/todo",
		)
		expect(postLoginUrl({ message: "Logged In" }, null, "en")).toBe(DESK_PATH)
	})

	it("sends producers to their sign-up page, else redirect-to, else their dashboard in the page's language", () => {
		const producer = { message: "No App", home_page: "/desk/spl-settings" }
		expect(postLoginUrl(producer, null, "ar")).toBe("/dashboard")
		expect(postLoginUrl(producer, null, "en")).toBe("/en/dashboard")
		expect(postLoginUrl(producer, "/en/dashboard", "ar")).toBe("/en/dashboard")
		expect(
			postLoginUrl({ ...producer, redirect_to: "/en" }, "/dashboard", "ar"),
		).toBe("/en")
		// Never Frappe's home_page, and never an unsafe redirect_to.
		expect(
			postLoginUrl(
				{ ...producer, redirect_to: "https://evil.com" },
				null,
				"ar",
			),
		).toBe("/dashboard")
	})

	it("never sends producers into the Desk, which refuses them", () => {
		const producer = { message: "No App" }
		expect(postLoginUrl(producer, "/desk/accounts/customer", "ar")).toBe(
			"/dashboard",
		)
		expect(postLoginUrl(producer, "/app/todo", "en")).toBe("/en/dashboard")
		// Staff still go where they asked.
		expect(
			postLoginUrl({ message: "Logged In" }, "/desk/accounts/customer", "ar"),
		).toBe("/desk/accounts/customer")
		// A page outside the Desk is fine.
		expect(postLoginUrl(producer, "/en", "ar")).toBe("/en")
	})

	it("recognises the Desk's addresses only", () => {
		for (const path of [
			"/desk",
			"/desk/hawya",
			"/app",
			"/app/todo",
			"/desk?x=1",
		]) {
			expect(isDeskPath(path), path).toBe(true)
		}
		for (const path of ["/dashboard", "/desktop", "/apps", "/en/desk"]) {
			expect(isDeskPath(path), path).toBe(false)
		}
	})

	it("builds the dashboard's address per language", () => {
		expect(dashboardHome("ar")).toBe("/dashboard")
		expect(dashboardHome("en")).toBe("/en/dashboard")
	})
})

describe("loginHashPage", () => {
	it("maps the hashes of Frappe's old login page to their pages", () => {
		expect(loginHashPage("#forgot")).toBe("ForgotPassword")
		expect(loginHashPage("#signup")).toBe("Signup")
		expect(loginHashPage("#login")).toBeNull()
		expect(loginHashPage("")).toBeNull()
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
		expect(emailError(" someone@naqel.sa ", t)).toBeUndefined()
	})
})
