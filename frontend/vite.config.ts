import path from "node:path"
import vue from "@vitejs/plugin-vue"
import frappeui from "frappe-ui/vite"
import { defineConfig } from "vite"

import { seoHead } from "./vite-plugins/seo-head"

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		frappeui({
			frappeProxy: true,
			jinjaBootData: true,
			lucideIcons: true,
			buildConfig: {
				outDir: "../ozone/public/frontend",
				indexHtmlPath: "../ozone/www/frontend.html",
				emptyOutDir: true,
				sourcemap: true,
			},
		}),
		vue(),
		seoHead(),
	],
	define: {
		// vue-i18n feature flags: Composition API only, no devtools in production.
		__VUE_I18N_FULL_INSTALL__: true,
		__VUE_I18N_LEGACY_API__: false,
		__INTLIFY_PROD_DEVTOOLS__: false,
	},
	build: {
		chunkSizeWarningLimit: 1500,
		outDir: "../ozone/public/frontend",
		emptyOutDir: true,
		target: "es2015",
		sourcemap: true,
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "src"),
			"tailwind.config.js": path.resolve(__dirname, "tailwind.config.ts"),
		},
	},
	optimizeDeps: {
		// frappe-ui ships source that imports `~icons/lucide/*` virtual modules, which
		// only its vite plugin can resolve. esbuild pre-bundling does not run vite
		// plugins, so frappe-ui must be served unbundled through the plugin pipeline.
		exclude: ["frappe-ui"],
		// Pre-bundle frappe-ui's largest many-file dependencies so dev page loads stay fast.
		include: [
			"feather-icons",
			"highlight.js/lib/core",
			"interactjs",
			"frappe-ui > reka-ui",
			"frappe-ui > echarts",
			"frappe-ui > lowlight",
			"frappe-ui > @popperjs/core",
		],
	},
	server: {
		allowedHosts: true,
	},
})
