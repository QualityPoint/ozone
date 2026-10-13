/// <reference types="vite/client" />

declare global {
	interface Window {
		/** Injected by Frappe into the page rendered from www/frontend.html */
		site_name: string
		/** CSRF token for POST requests (production page only; "{{ csrf_token }}" in dev). */
		csrf_token?: string
	}
}

export {}
