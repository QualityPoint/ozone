<template>
  <!-- A key figure: a large number over the documents' green underline bar, counting up once
       in view. Takes its label translated. -->
  <div ref="root">
    <p class="text-display font-extrabold leading-none" dir="ltr">
      {{ prefix }}{{ formatNumber(shown) }}{{ suffix }}
    </p>
    <span class="mt-4 block h-1 w-16 rounded-full bg-brand-leaf" aria-hidden="true" />
    <p class="mt-4 text-body">{{ label }}</p>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"

import { useCountUp } from "@/composables/useCountUp"
import { useReveal } from "@/composables/useReveal"
import { formatNumber } from "@/utils/format"

const props = defineProps<{
	value: number
	label: string
	prefix?: string
	suffix?: string
}>()

const root = ref<HTMLElement | null>(null)
const shown = useCountUp(props.value, useReveal(root, 0.4))
</script>
