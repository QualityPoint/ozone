/**
 * The equipment photos by slug (src/assets/images/equipment/<slug>.webp, made by
 * scripts/build-brand-assets.py from the operation file). config/site.ts lists the slugs.
 */
const files = import.meta.glob<string>("@/assets/images/equipment/*.webp", {
	eager: true,
	import: "default",
})

export const equipmentPhotos: Record<string, string> = Object.fromEntries(
	Object.entries(files).map(([path, url]) => [
		path.split("/").pop()?.replace(".webp", ""),
		url,
	]),
)
