// frappe-ui ships these entry points as plain JS without type declarations.

declare module "frappe-ui/vite" {
	import type { PluginOption } from "vite"

	export default function frappeui(
		options?: Record<string, unknown>,
	): PluginOption[]
}

declare module "frappe-ui/tailwind" {
	import type { Config } from "tailwindcss"

	const preset: Partial<Config>
	export default preset
}
