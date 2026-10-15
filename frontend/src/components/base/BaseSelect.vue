<template>
  <!-- A labelled select in BaseInput's look. Options come translated: { value, label }. -->
  <div :class="$attrs.class" :style="$attrs.style as string | undefined">
    <label :for="id" class="mb-1.5 block text-caption font-bold text-site-heading">{{ label }}</label>
    <select
      :id="id"
      v-model="model"
      v-bind="controlAttrs"
      :aria-invalid="error ? 'true' : undefined"
      :aria-describedby="error ? `${id}-error` : undefined"
      :class="[
        'block w-full rounded-xl border-2 bg-site-bg py-3 pe-10 ps-4 text-body text-site-text transition',
        // The arrow (the forms plugin's background image) sits at the end, in either direction.
        '[background-position:right_0.75rem_center] rtl:[background-position:left_0.75rem_center]',
        'focus:border-brand-green focus:outline-none focus:ring-4 focus:ring-brand-leaf/20',
        error ? 'border-red-500' : 'border-site-line',
      ]"
    >
      <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
      <option v-for="option in options" :key="option.value" :value="option.value">{{ option.label }}</option>
    </select>
    <p v-if="error" :id="`${id}-error`" class="mt-1.5 text-caption font-bold text-red-600 dark:text-red-400">{{ error }}</p>
  </div>
</template>

<script lang="ts" setup>
import { computed, useAttrs, useId } from "vue"

defineOptions({ inheritAttrs: false })

defineProps<{
	label: string
	options: { value: string; label: string }[]
	placeholder?: string
	error?: string
}>()

const model = defineModel<string>({ default: "" })
const id = useId()

/** Layout classes and styles go on the field's wrapper; everything else on the select. */
const attrs = useAttrs()
const controlAttrs = computed(() => {
	const { class: _class, style: _style, ...rest } = attrs
	return rest
})
</script>
