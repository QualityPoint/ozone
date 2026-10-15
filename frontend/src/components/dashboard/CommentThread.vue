<template>
  <!-- A record's comments with Ozone's team (ozone/portal/comments.py): a request's while it requires
       clarification, a quotation's while the producer answers it. `load` reads them (and whether the
       producer may write now), `send` posts the producer's. The team's comments sit at the start, the
       producer's at the end. It reads them again every 15 seconds while the tab is visible, and as soon
       as the producer comes back to it, so the team's answers show without reloading the page. -->
  <div class="mt-4 border-t-2 border-site-line pt-4">
    <BaseNotice v-if="failed">{{ failed }}</BaseNotice>
    <p v-else-if="!comments" class="text-caption text-site-muted">{{ t("dashboard.requests.loading") }}</p>
    <template v-else>
      <p v-if="!comments.length" class="text-caption text-site-muted">{{ t("dashboard.requests.noComments") }}</p>
      <ol v-else class="space-y-3">
        <li
          v-for="comment in comments"
          :key="comment.name"
          :class="[
            'max-w-[85%] rounded-2xl px-4 py-3',
            comment.from_team ? 'me-auto bg-brand-green/10 dark:bg-brand-leaf/10' : 'ms-auto border-2 border-site-line',
          ]"
        >
          <p class="flex flex-wrap items-baseline justify-between gap-x-4 text-label font-bold text-site-muted">
            <span :class="comment.from_team ? 'text-brand-green dark:text-brand-leaf' : 'text-site-heading'">
              {{ comment.from_team ? t("dashboard.requests.team") : t("dashboard.requests.you") }}
            </span>
            <time :datetime="comment.creation">{{ formatTime(comment.creation) }}</time>
          </p>
          <p class="mt-1 whitespace-pre-line text-body text-site-text">{{ comment.text }}</p>
        </li>
      </ol>

      <form v-if="canReply" class="mt-4" novalidate @submit.prevent="reply">
        <label :for="fieldId" class="mb-1.5 block text-caption font-bold text-site-heading">{{ label || t("dashboard.requests.answer") }}</label>
        <textarea
          :id="fieldId"
          v-model="text"
          rows="3"
          maxlength="4000"
          :aria-invalid="error ? 'true' : undefined"
          :class="[
            'block w-full rounded-2xl border-2 bg-site-bg px-4 py-3 text-body text-site-text transition',
            'focus:border-brand-green focus:outline-none focus:ring-4 focus:ring-brand-leaf/25 dark:focus:border-brand-leaf',
            error ? 'border-brand-red' : 'border-site-line',
          ]"
        />
        <p v-if="error" class="mt-1.5 text-caption font-bold text-brand-red dark:text-brand-red-300">{{ error }}</p>
        <BaseButton type="submit" class="mt-3" :loading="busy">{{ t("dashboard.requests.send") }}</BaseButton>
      </form>
    </template>
  </div>
</template>

<script lang="ts" setup>
import { onBeforeUnmount, onMounted, ref, useId } from "vue"
import { useI18n } from "vue-i18n"

import BaseButton from "@/components/base/BaseButton.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import { refusal } from "@/composables/useFormSubmit"
import type { RequestComment } from "@/services/portal"

const props = defineProps<{
	load: () => Promise<{ comments: RequestComment[]; can_reply: boolean }>
	send: (text: string) => Promise<RequestComment[]>
	/** The answer box's label (default: "Your answer"). */
	label?: string
}>()

const { t, locale } = useI18n()
const fieldId = useId()
const comments = ref<RequestComment[] | null>(null)
const canReply = ref(false)
const failed = ref("")
const text = ref("")
const error = ref("")
const busy = ref(false)

/** How often the conversation is read again while it is on screen. */
const REFRESH_MS = 15_000
let timer: number | undefined

onMounted(async () => {
	try {
		const detail = await props.load()
		comments.value = detail.comments
		canReply.value = detail.can_reply
	} catch (err) {
		failed.value = refusal(err, t)
		return
	}
	timer = window.setInterval(refresh, REFRESH_MS)
	document.addEventListener("visibilitychange", refresh)
})

onBeforeUnmount(() => {
	window.clearInterval(timer)
	document.removeEventListener("visibilitychange", refresh)
})

/** The comments as they are now; a failed read keeps those on screen (the next one may succeed). */
async function refresh() {
	if (document.hidden || busy.value) return
	try {
		const detail = await props.load()
		comments.value = detail.comments
		canReply.value = detail.can_reply
	} catch {
		// Offline for a moment: keep what is shown
	}
}

function formatTime(value: string): string {
	return new Intl.DateTimeFormat(locale.value, {
		dateStyle: "medium",
		timeStyle: "short",
	}).format(new Date(value.replace(" ", "T")))
}

async function reply() {
	error.value = text.value.trim() ? "" : t("auth.errors.required")
	if (error.value) return
	busy.value = true
	try {
		comments.value = await props.send(text.value.trim())
		text.value = ""
	} catch (err) {
		error.value = refusal(err, t)
	} finally {
		busy.value = false
	}
}
</script>
