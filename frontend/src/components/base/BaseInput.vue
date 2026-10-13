<template>
  <!-- A labelled text field in the documents' look: a rounded white field with a green focus
       ring, red with its error under it. Passwords get a reveal button. Labels come translated. -->
  <div>
    <label :for="id" class="mb-1.5 block text-caption font-bold text-site-heading">{{ label }}</label>
    <!-- A forced direction (dir="ltr" for emails and passwords in Arabic) applies to the wrapper
         too, so the reveal button sits at the same end as the input's padding. -->
    <div class="relative" :dir="$attrs.dir as string | undefined">
      <input
        :id="id"
        v-model="model"
        v-bind="$attrs"
        :type="type === 'password' && revealed ? 'text' : type"
        :aria-invalid="error ? 'true' : undefined"
        :aria-describedby="error ? `${id}-error` : undefined"
        :class="[
          'block w-full rounded-2xl border-2 bg-site-bg px-4 py-3 text-body text-site-text transition placeholder:text-site-muted/70',
          'focus:border-brand-green focus:outline-none focus:ring-4 focus:ring-brand-leaf/25 dark:focus:border-brand-leaf',
          error ? 'border-brand-red' : 'border-site-line',
          type === 'password' ? 'pe-12' : '',
        ]"
      />
      <button
        v-if="type === 'password'"
        type="button"
        :aria-label="revealed ? hidePasswordLabel : showPasswordLabel"
        :aria-pressed="revealed"
        class="absolute inset-y-0 end-0 grid w-12 place-items-center rounded-e-2xl text-site-muted transition hover:text-site-heading focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
        @click="revealed = !revealed"
      >
        <LucideEyeOff v-if="revealed" class="size-5" aria-hidden="true" />
        <LucideEye v-else class="size-5" aria-hidden="true" />
      </button>
    </div>
    <p v-if="error" :id="`${id}-error`" class="mt-1.5 text-caption font-bold text-brand-red dark:text-brand-red-300">{{ error }}</p>
  </div>
</template>

<script lang="ts" setup>
import { ref, useId } from "vue"
import LucideEye from "~icons/lucide/eye"
import LucideEyeOff from "~icons/lucide/eye-off"

defineOptions({ inheritAttrs: false })

defineProps<{
	label: string
	type?: "text" | "email" | "password"
	error?: string
	/** Accessible names of the password reveal button. */
	showPasswordLabel?: string
	hidePasswordLabel?: string
}>()

const model = defineModel<string>({ default: "" })
const id = useId()
const revealed = ref(false)
</script>
