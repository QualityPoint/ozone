/// <reference types="vite/client" />

import type { SiteContact } from "@/types"

declare global {
	interface Window {
		/** Injected by Frappe into the page rendered from www/frontend.html */
		site_name: string
		/** CSRF token for POST requests (production page only; "{{ csrf_token }}" in dev). */
		csrf_token?: string
		/** Frappe's build version (production page only): busts the cache of naqel's Desk sprite. */
		build_version?: string
		/** Ozone Settings contact details (production page only); read via useSiteContact. */
		site_contact?: SiteContact | string
	}
}
