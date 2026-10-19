/**
 * naqel's Desk icons (naqel/public/icons/module-icons.svg, the sprite its dock and sidebars use;
 * naqel is a required app, so every Ozone site serves it), put into the page once, as Frappe does
 * for its own pages (frappe/utils/jinja_globals.py: include_icons): fetch the file, insert it into a
 * hidden element, and point every <use> at `#icon-naqel-…` in the page. Referencing the file itself
 * (`file.svg#id`) draws the icons, but browsers don't all apply the sprite's own stylesheet to it,
 * which holds the icons' animations.
 */
const SPRITE_URL = "/assets/naqel/icons/module-icons.svg"
const HOLDER_ID = "naqel-desk-symbols"

let requested = false

/** Fetch and insert the sprite, once per page load. Icons draw as soon as it arrives. */
export function ensureNaqelSprite(): void {
	if (requested || typeof document === "undefined") return
	requested = true
	const holder = document.createElement("div")
	holder.id = HOLDER_ID
	holder.hidden = true
	document.body.prepend(holder)
	// The build version busts the browser's cache when the sprite changes (Frappe does the same
	// with ?v=window._version_number). Boot data; absent on the dev server.
	const version = window.build_version ? `?v=${window.build_version}` : ""
	fetch(`${SPRITE_URL}${version}`, { credentials: "same-origin" })
		.then((response) => (response.ok ? response.text() : ""))
		.then((svg) => holder.insertAdjacentHTML("beforeend", svg))
		.catch(() => {
			// No icons: they're decorative.
		})
}

/** A Desk icon's reference in the page: "truck" → "#icon-naqel-truck-duotone". */
export function naqelIcon(name: string): string {
	return `#icon-naqel-${name}-duotone`
}
