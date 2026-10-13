import { fileURLToPath } from "node:url"
import { defineConfig } from "vitest/config"

// Standalone on purpose: vite.config.ts loads frappe-ui's dev-server plugins
// (proxy, icons, boot data), which unit tests don't need.
export default defineConfig({
	resolve: {
		alias: {
			"@": fileURLToPath(new URL("./src", import.meta.url)),
		},
	},
	test: {
		include: ["src/**/__tests__/**/*.test.ts"],
		environment: "node",
	},
})
