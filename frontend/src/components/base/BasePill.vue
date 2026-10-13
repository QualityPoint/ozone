<template>
  <!-- The documents' rounded titles: a green outline, a filled green pill, or a small red label. -->
  <span
    :class="[
      'inline-flex items-center gap-2 rounded-full font-bold',
      size === 'sm' ? 'px-3 py-0.5 text-label' : 'px-5 py-2 text-body',
      variants[variant],
    ]"
  >
    <slot />
  </span>
</template>

<script lang="ts" setup>
withDefaults(
	defineProps<{
		variant?: "outline" | "solid" | "accent"
		size?: "sm" | "md"
	}>(),
	{
		variant: "outline",
		size: "md",
	},
)

const variants = {
	outline: "border-2 border-site-heading text-site-heading",
	solid: "bg-brand-green text-white",
	accent: "bg-brand-red text-white",
} as const
</script>
