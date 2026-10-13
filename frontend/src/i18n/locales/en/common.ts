// Note: vue-i18n reserves `@ { } | $` in messages. Keep emails, URLs and phone
// numbers out of messages (they come from Ozone Settings).
import meta from "../meta.json"

export default {
	// The page title and description: one file for the SPA and the server (ozone/www/frontend.py).
	meta: meta.en,
	brand: {
		// One name for the SPA and the server (og:site_name), from meta.json.
		name: meta.site.en,
		/** The logo's slogan, shown as separate items. */
		tagline: ["Maintenance", "Cleaning", "General Contracting"],
		about:
			"A Madinah company specialising in collecting and transporting waste and construction debris, and in cleaning. We sort waste at source by type.",
	},
	a11y: {
		skipToContent: "Skip to content",
		openMenu: "Open menu",
		closeMenu: "Close menu",
		home: "Ozone home",
	},
	nav: {
		about: "About",
		services: "Services",
		industries: "Industries",
		contact: "Contact",
	},
	language: {
		/** The switch's accessible name, followed by the other language's name. */
		switchTo: "View the site in",
	},
	theme: {
		toDark: "Switch to dark mode",
		toLight: "Switch to light mode",
	},
	footer: {
		contact: "Contact",
		follow: "Follow us",
		/** Accessible name of a social icon link, followed by the platform name. */
		socialLabel: "Ozone on",
		whatsapp: "WhatsApp",
		map: "Find us on the map",
		explore: "Explore",
		rights: "All rights reserved.",
	},
}
