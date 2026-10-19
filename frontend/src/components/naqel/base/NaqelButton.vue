<template>
  <!-- Naqel's button (hawya's BaseButton). Explicit branches instead of <component :is="'button'">:
       a string `is` would resolve to frappe-ui's global Button (base/nativeTag.ts explains). -->
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
		/** In-app route (a section of the page: { hash: "#calculator" }); renders a RouterLink. */
		to?: RouteLocationRaw
		/** A link outside the SPA, mailto: or tel:. */
		href?: string
		type?: "button" | "submit"
		/** `primary` green; `outline` a green border; `ghost` light on the dark hero and bands. */
		variant?: "primary" | "outline" | "ghost"
		/** A button waiting for its request: a spinner, and disabled. */
		loading?: boolean
		disabled?: boolean
	}>(),
	{ variant: "primary", type: "button" },
)

const VARIANTS = {
	primary:
		"bg-naqel-green text-white shadow-naqel-card hover:bg-naqel-green-600",
	outline: "border-2 border-naqel-green text-site-heading hover:bg-site-hover",
	ghost: "border border-white/25 text-white hover:bg-white/10",
}

const classes = computed(() => [
	"inline-flex items-center justify-center gap-2 rounded-xl px-5 py-3 text-caption font-bold transition",
	"focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-naqel-green/40",
	"disabled:pointer-events-none disabled:opacity-60",
	VARIANTS[props.variant],
])
</script>
