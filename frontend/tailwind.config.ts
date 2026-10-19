import frappeUIPreset from "frappe-ui/tailwind"
import type { Config } from "tailwindcss"

/** A scale's steps: each mixes the official value with white (255) or black (0) by an amount. */
type Steps = Record<string, [target: number, amount: number]>

/** Ozone's steps. */
const OZONE_STEPS: Steps = {
	50: [255, 0.95],
	100: [255, 0.9],
	200: [255, 0.75],
	300: [255, 0.55],
	400: [255, 0.3],
	600: [0, 0.12],
	700: [0, 0.25],
	800: [0, 0.4],
	900: [0, 0.55],
	950: [0, 0.7],
}

/** Naqel's steps, as its own site makes them (hawya's tailwind.config.ts), so its shades match. */
const NAQEL_STEPS: Steps = {
	50: [255, 0.95],
	100: [255, 0.88],
	200: [255, 0.75],
	300: [255, 0.55],
	400: [255, 0.3],
	600: [0, 0.15],
	700: [0, 0.3],
	800: [0, 0.45],
	900: [0, 0.6],
	950: [0, 0.75],
}

/**
 * A colour's scale from its official value (500 and DEFAULT): lighter steps mix it with
 * white, darker steps with black. One function, so every brand colour steps the same way.
 */
function scale(
	hex: string,
	steps: Steps = OZONE_STEPS,
): Record<string, string> {
	const rgb = [1, 3, 5].map((i) => Number.parseInt(hex.slice(i, i + 2), 16))
	const mix = (target: number, amount: number) =>
		`#${rgb
			.map((c) =>
				Math.round(c + (target - c) * amount)
					.toString(16)
					.padStart(2, "0"),
			)
			.join("")}`
	return {
		DEFAULT: hex,
		500: hex,
		...Object.fromEntries(
			Object.entries(steps).map(([step, [target, amount]]) => [
				step,
				mix(target, amount),
			]),
		),
	}
}

// Ozone's palette (docs/frontend/branding.md): the logo's inks and the operation files' accents.
const brand = {
	green: scale("#11532a"),
	red: scale("#af2625"),
	leaf: scale("#61be51"),
	silver: scale("#d8deda"),
	ink: "#231f20",
}

// Naqel's palette, for the page that presents the Naqel system (docs/naqel_page/identity.md):
// the values of Naqel's own site (hawya's tailwind.config.ts).
const naqel = {
	/** The logo's green: marks, headings, buttons. */
	green: scale("#3dba6b", NAQEL_STEPS),
	/** The app icon's green: a cooler second green. */
	mint: scale("#22b573", NAQEL_STEPS),
	/** The deep green-black of the hero and the bands' dark end. */
	night: scale("#161b15", NAQEL_STEPS),
	/** The logo's black. */
	ink: scale("#100f0d", NAQEL_STEPS),
}

export default {
	presets: [frappeUIPreset],
	content: [
		"./index.html",
		"./src/**/*.{vue,js,ts,jsx,tsx}",
		"./node_modules/frappe-ui/src/components/**/*.{vue,js,ts,jsx,tsx}",
	],
	theme: {
		extend: {
			colors: {
				brand,
				naqel,
				// Theme-aware colours for the public site. Values are RGB channels in CSS
				// variables (src/assets/styles/main.css) that swap in dark mode, so components
				// never need `dark:` for these.
				site: Object.fromEntries(
					[
						"bg",
						"tint",
						"heading",
						"text",
						"muted",
						"hover",
						"line",
						"silver",
					].map((token) => [
						token,
						`rgb(var(--site-${token}) / <alpha-value>)`,
					]),
				),
			},
			fontFamily: {
				sans: [
					"Montserrat",
					"Almarai",
					"ui-sans-serif",
					"system-ui",
					"sans-serif",
				],
				arabic: [
					"Almarai",
					"Montserrat",
					"ui-sans-serif",
					"system-ui",
					"sans-serif",
				],
				// Naqel's (the Naqel page): Latin is Inter, frappe-ui's InterVar, already in its stylesheet.
				naqel: [
					"InterVar",
					"Inter",
					"Almarai",
					"ui-sans-serif",
					"system-ui",
					"sans-serif",
				],
				"naqel-arabic": [
					"Almarai",
					"InterVar",
					"ui-sans-serif",
					"system-ui",
					"sans-serif",
				],
			},
			// frappe-ui's text-xs…3xl also set font-weight and letter-spacing (tuned for app UI),
			// which space out Arabic letters. The public site uses this separate scale instead
			// (blinktech's); frappe-ui components never use these names.
			fontSize: {
				label: ["12px", { lineHeight: "1.4" }],
				caption: ["14px", { lineHeight: "1.6" }],
				body: ["16px", { lineHeight: "1.75" }],
				"body-lg": ["18px", { lineHeight: "1.7" }],
				title: ["20px", { lineHeight: "1.4" }],
				"title-lg": ["24px", { lineHeight: "1.35" }],
				heading: ["30px", { lineHeight: "1.25" }],
				"heading-lg": ["38px", { lineHeight: "1.2" }],
				display: ["48px", { lineHeight: "1.15" }],
				"display-lg": ["60px", { lineHeight: "1.1" }],
			},
			// The preset's radius scale stops at 2xl.
			borderRadius: {
				"3xl": "1.5rem",
				"4xl": "2rem",
			},
			boxShadow: {
				// Soft, layered: the documents' product photos sit on white with a gentle ground shadow.
				card: "0 1px 2px rgb(17 83 42 / 0.06), 0 12px 32px -12px rgb(17 83 42 / 0.18)",
				header: "0 8px 24px -16px rgb(17 83 42 / 0.35)",
				"naqel-card":
					"0 1px 2px rgb(22 27 21 / 0.06), 0 12px 32px -14px rgb(22 27 21 / 0.22)",
			},
			backgroundImage: {
				// Naqel's title bands and page-foot bar: deep green-black to the logo green, pointing to
				// the start side (--band-to, set on the Naqel page).
				"naqel-band": `linear-gradient(to var(--band-to, left), ${naqel.night.DEFAULT}, ${naqel.green[700]} 45%, ${naqel.green.DEFAULT})`,
			},
		},
	},
	plugins: [],
} satisfies Config
