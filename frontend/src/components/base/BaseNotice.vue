<template>
  <!-- A form's result above it: an error (announced at once, role=alert) in the brand red, or a
       success (role=status) in green. The text comes translated, in the slot. -->
  <p
    :role="kind === 'error' ? 'alert' : 'status'"
    :class="[
      'flex items-start gap-3 rounded-2xl border-s-4 p-4 text-caption leading-relaxed text-site-text',
      kind === 'error' ? 'border-brand-red bg-brand-red/10' : 'border-brand-leaf bg-brand-leaf/15',
    ]"
  >
    <LucideCircleAlert v-if="kind === 'error'" class="mt-0.5 size-5 shrink-0 text-brand-red dark:text-brand-red-300" aria-hidden="true" />
    <LucideCircleCheck v-else class="mt-0.5 size-5 shrink-0 text-brand-green dark:text-brand-leaf" aria-hidden="true" />
    <span><slot /></span>
  </p>
</template>

<script lang="ts" setup>
import LucideCircleAlert from "~icons/lucide/circle-alert"
import LucideCircleCheck from "~icons/lucide/circle-check"

withDefaults(defineProps<{ kind?: "error" | "success" }>(), { kind: "error" })
</script>
