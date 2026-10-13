<template>
  <!--
    Explicit branches instead of <component :is="'button'">: a string `is` is resolved against
    global components first (components/base/nativeTag.ts explains).
  -->
  <RouterLink v-if="to" :to="to" :class="classes"><slot /></RouterLink>
  <a v-else-if="href" :href="href" :class="classes"><slot /></a>
  <button v-else :type="type" :disabled="disabled || loading" :aria-busy="loading || undefined" :class="classes">
    <LucideLoaderCircle v-if="loading" class="size-4 motion-safe:animate-spin" aria-hidden="true" />
    <slot />
  </button>
</template>

<script lang="ts" setup>
import { computed } from "vue"
import type { RouteLocationRaw } from "vue-router"
import LucideLoaderCircle from "~icons/lucide/loader-circle"

const props = withDefaults(
	defineProps<{
		/** In-app route (a section: sectionLink("contact")); renders a RouterLink. */
		to?: RouteLocationRaw
		/** External link, mailto: or tel:. */
		href?: string
		/** `primary` green, `accent` red, `outline` green border; `light` on the green bands. */
		variant?: "primary" | "accent" | "outline" | "light"
		/** A button's type: `submit` in forms. */
		type?: "button" | "submit"
		/** A button waiting for its request: a spinner, and disabled. */
		loading?: boolean
		disabled?: boolean
	}>(),
	{ variant: "primary", type: "button" },
)

const variants = {
	primary: "bg-brand-green text-white shadow-card hover:bg-brand-green-700",
	accent: "bg-brand-red text-white shadow-card hover:bg-brand-red-700",
	outline: "border-2 border-site-heading text-site-heading hover:bg-site-hover",
	light: "bg-white text-brand-green hover:bg-brand-silver-100",
}

const classes = computed(() => [
	"inline-flex items-center justify-center gap-2 rounded-full px-6 py-3 text-caption font-bold transition",
	"focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-brand-leaf/60",
	"motion-safe:hover:-translate-y-0.5 disabled:pointer-events-none disabled:opacity-60",
	variants[props.variant],
])
</script>
