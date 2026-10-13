import type { Plugin } from "vite"

const SEO_BLOCK = /<!-- seo:start[\s\S]*?<!-- seo:end -->/
const HTML_TAG = /<html[^>]*>/

/**
 * Production only: turns index.html's <html> tag and its `seo:start … seo:end` block into
 * Jinja, so Frappe renders language, direction and SEO tags on the server (values come from
 * `context.seo` in ozone/www/frontend.py). The dev server keeps the static Arabic defaults.
 * Same approach as frappe-ui's jinjaBootData plugin (and blinktech's seo-head).
 */
export function seoHead(): Plugin {
	return {
		name: "ozone-seo-head",
		apply: "build",
		transformIndexHtml(html) {
			if (!SEO_BLOCK.test(html) || !HTML_TAG.test(html)) {
				throw new Error(
					"seo-head: index.html is missing <html> or the seo:start/seo:end block",
				)
			}
			return html
				.replace(HTML_TAG, `<html lang="{{ seo.lang }}" dir="{{ seo.dir }}">`)
				.replace(
					SEO_BLOCK,
					`<title>{{ seo.title | e }}</title>
    <meta name="description" content="{{ seo.description | e }}" />
    <link rel="canonical" href="{{ seo.canonical | e }}" />
    {% if seo.robots %}<meta name="robots" content="{{ seo.robots }}" />{% endif %}
    {% for alt in seo.alternates %}<link rel="alternate" hreflang="{{ alt.hreflang }}" href="{{ alt.href | e }}" />
    {% endfor %}<meta property="og:type" content="website" />
    <meta property="og:site_name" content="{{ seo.site_name | e }}" />
    <meta property="og:locale" content="{{ seo.og_locale }}" />
    <meta property="og:title" content="{{ seo.title | e }}" />
    <meta property="og:description" content="{{ seo.description | e }}" />
    <meta property="og:url" content="{{ seo.canonical | e }}" />
    <meta property="og:image" content="{{ seo.og_image | e }}" />
    <meta name="twitter:card" content="summary_large_image" />`,
				)
		},
	}
}
