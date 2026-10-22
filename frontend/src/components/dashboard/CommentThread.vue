<template>
  <!-- A record's comments with Ozone's team (ozone/portal/comments.py): a request's while it requires
       clarification, a quotation's while the producer answers it. `load` reads them (and whether the
       producer may write now), `send` posts the producer's, with the files it attaches (uploaded as it
       picks them, private; a comment links them and they are attached to the record), and answers the
       thread as it is then (a request's answer closes the box until the team asks again). The team's comments sit at the start, the
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
          <p v-if="comment.text" class="mt-1 whitespace-pre-line text-body text-site-text">{{ comment.text }}</p>
          <ul v-if="comment.attachments?.length" class="mt-2 flex flex-wrap gap-2">
            <li v-for="file in comment.attachments" :key="file.url">
              <a
                :href="file.url"
                target="_blank"
                rel="noopener"
                class="inline-flex max-w-full items-center gap-1.5 rounded-full bg-site-hover px-3 py-1 text-caption font-bold text-brand-green underline dark:text-brand-leaf"
              >
                <LucidePaperclip class="size-3.5 shrink-0" aria-hidden="true" />
                <span class="truncate">{{ file.name }}</span>
              </a>
            </li>
          </ul>
        </li>
      </ol>

      <form v-if="canReply && send" class="mt-4" novalidate @submit.prevent="reply">
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
        <ul v-if="files.length" class="mt-2 flex flex-wrap gap-2">
          <li
            v-for="(file, index) in files"
            :key="file.url"
            class="inline-flex max-w-full items-center gap-1.5 rounded-full border-2 border-site-line py-1 pe-1.5 ps-3 text-caption font-bold text-site-heading"
          >
            <LucidePaperclip class="size-3.5 shrink-0" aria-hidden="true" />
            <span class="truncate">{{ file.name }}</span>
            <button
              type="button"
              class="rounded-full p-0.5 text-site-muted transition hover:bg-site-hover hover:text-site-heading"
              :aria-label="`${t('dashboard.requests.removeFile')} ${file.name}`"
              @click="files.splice(index, 1)"
            >
              <LucideX class="size-3.5" aria-hidden="true" />
            </button>
          </li>
        </ul>
        <p v-if="error" class="mt-1.5 text-caption font-bold text-brand-red dark:text-brand-red-300">{{ error }}</p>
        <div class="mt-3 flex flex-wrap items-center gap-3">
          <BaseButton type="submit" :loading="busy" :disabled="uploading">{{ sendLabel || t("dashboard.requests.send") }}</BaseButton>
          <label
            v-if="room > 0"
            :class="[
              'inline-flex cursor-pointer items-center gap-2 rounded-xl border-2 border-site-line px-4 py-2.5 text-caption font-bold text-site-heading transition',
              'hover:border-brand-green focus-within:ring-4 focus-within:ring-brand-leaf/20',
              uploading || busy ? 'pointer-events-none opacity-60' : '',
            ]"
          >
            <LucidePaperclip class="size-4" aria-hidden="true" />
            {{ uploading ? t("dashboard.requests.uploading") : t("dashboard.requests.attach") }}
            <input type="file" class="sr-only" multiple :accept="ACCEPT" @change="attach" />
          </label>
        </div>
      </form>
    </template>
  </div>
</template>

<script lang="ts" setup>
import { computed, onBeforeUnmount, onMounted, ref, useId } from "vue"
import { useI18n } from "vue-i18n"
import LucidePaperclip from "~icons/lucide/paperclip"
import LucideX from "~icons/lucide/x"

import BaseButton from "@/components/base/BaseButton.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import { refusal } from "@/composables/useFormSubmit"
import { uploadFile } from "@/services/http"
import type { RequestComment } from "@/services/portal"

/** What website users may upload (frappe/handler.py: ALLOWED_MIMETYPES): documents, sheets and pictures. */
const ACCEPT = [
	"application/pdf",
	"image/jpeg",
	"image/png",
	".doc",
	".docx",
	".xls",
	".xlsx",
	".csv",
	".txt",
].join(",")

interface Thread {
	comments: RequestComment[]
	can_reply: boolean
	/** How many more files the record takes; none or null: no limit. */
	attachments_left?: number | null
}

const props = defineProps<{
	load: () => Promise<Thread>
	/** Posts the producer's text and the URLs of the files it uploaded for it; the thread as it is then.
	 *  Without it the thread is read only. */
	send?: (text: string, files: string[]) => Promise<Thread>
	/** The answer box's label (default: "Your answer"). */
	label?: string
	/** The send button's label (default: "Send"). */
	sendLabel?: string
}>()

const { t, locale } = useI18n()
const fieldId = useId()
const comments = ref<RequestComment[] | null>(null)
const canReply = ref(false)
const failed = ref("")
const text = ref("")
const error = ref("")
const busy = ref(false)
/** The files uploaded for the answer being written (private: only the producer and the team open them). */
const files = ref<{ name: string; url: string }[]>([])
const uploading = ref(false)
/** How many more files the record takes (its DocType's Max Attachments); null: no limit. */
const left = ref<number | null>(null)
/** How many more files this answer may carry. */
const room = computed(() =>
	left.value === null
		? Number.POSITIVE_INFINITY
		: left.value - files.value.length,
)

/** How often the conversation is read again while it is on screen. */
const REFRESH_MS = 15_000
let timer: number | undefined

function show(detail: Thread) {
	comments.value = detail.comments
	canReply.value = detail.can_reply
	left.value = detail.attachments_left ?? null
}

onMounted(async () => {
	try {
		show(await props.load())
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
		show(await props.load())
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

/** Uploads the chosen files, as many as the record still takes. */
async function attach(event: Event) {
	const input = event.target as HTMLInputElement
	const chosen = Array.from(input.files ?? []).slice(0, room.value)
	input.value = ""
	if (!chosen.length) return
	uploading.value = true
	error.value = ""
	try {
		for (const file of chosen) {
			files.value.push({ name: file.name, url: await uploadFile(file) })
		}
	} catch (err) {
		error.value = refusal(err, t)
	} finally {
		uploading.value = false
	}
}

async function reply() {
	error.value =
		text.value.trim() || files.value.length ? "" : t("auth.errors.required")
	if (error.value) return
	busy.value = true
	try {
		if (!props.send) return
		show(
			await props.send(
				text.value.trim(),
				files.value.map((file) => file.url),
			),
		)
		text.value = ""
		files.value = []
	} catch (err) {
		error.value = refusal(err, t)
	} finally {
		busy.value = false
	}
}
</script>
