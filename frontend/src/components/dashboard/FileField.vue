<template>
  <!-- A document to attach: uploads the chosen file with Frappe's upload_file (private unless
       `public`), then holds its URL. The server accepts only files this user uploaded. Website users may
       upload only some types (frappe/handler.py: ALLOWED_MIMETYPES), so only PDF, JPG and PNG are offered. -->
  <div :class="$attrs.class">
    <span :id="labelId" class="mb-1.5 block text-caption font-bold text-site-heading">{{ label }}</span>
    <div class="flex flex-wrap items-center gap-3">
      <label
        :class="[
          'inline-flex cursor-pointer items-center gap-2 rounded-xl border-2 px-4 py-2.5 text-caption font-bold transition',
          'border-site-line text-site-heading hover:border-brand-green focus-within:ring-4 focus-within:ring-brand-leaf/20',
          busy ? 'pointer-events-none opacity-60' : '',
          error ? 'border-red-500' : '',
        ]"
      >
        <LucideUpload class="size-4" aria-hidden="true" />
        {{ t("dashboard.facilities.fileUpload") }}
        <input type="file" class="sr-only" :accept="accept" :aria-labelledby="labelId" @change="pick" />
      </label>
      <a
        v-if="model"
        :href="model"
        target="_blank"
        rel="noopener"
        class="inline-flex items-center gap-1 text-caption font-bold text-brand-green underline dark:text-brand-leaf"
      >
        <LucideFileCheck class="size-4" aria-hidden="true" />
        {{ t("dashboard.facilities.fileUploaded") }}
      </a>
    </div>
    <p v-if="error || failed" class="mt-1.5 text-caption font-bold text-red-600 dark:text-red-400">{{ error || failed }}</p>
  </div>
</template>

<script lang="ts" setup>
import { ref, useId } from "vue"
import { useI18n } from "vue-i18n"
import LucideFileCheck from "~icons/lucide/file-check"
import LucideUpload from "~icons/lucide/upload"

import { refusal } from "@/composables/useFormSubmit"
import { uploadFile } from "@/services/http"

defineOptions({ inheritAttrs: false })

const props = withDefaults(
	defineProps<{
		label: string
		error?: string
		accept?: string
		public?: boolean
	}>(),
	{ accept: "application/pdf,image/jpeg,image/png", public: false },
)

const model = defineModel<string | null>({ default: null })
const { t } = useI18n()
const labelId = useId()
const busy = ref(false)
const failed = ref("")

async function pick(event: Event) {
	const input = event.target as HTMLInputElement
	const file = input.files?.[0]
	input.value = ""
	if (!file) return
	busy.value = true
	failed.value = ""
	try {
		model.value = await uploadFile(file, !props.public)
	} catch (error) {
		failed.value = refusal(error, t)
	} finally {
		busy.value = false
	}
}
</script>
