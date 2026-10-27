<template>
  <!-- A contract as it prints (ozone/portal/contracts.py: get_contract_print): its letter head, parties, terms and
       collection plan, marked DRAFT while Ozone's team prepares it. An issued one waiting for the producer's signature
       (can_sign) is signed below it: the producer agrees to its terms, writes its name and signs on the pad
       (sign_contract: naqel's utils/contract/signature). Print prints it from the browser, whose print dialog also
       saves it as a PDF. A native dialog: Escape and the close button close it. -->
  <dialog
    ref="dialog"
    class="m-auto flex h-[min(92vh,60rem)] w-[min(96vw,64rem)] flex-col overflow-hidden rounded-3xl border border-site-line bg-site-bg p-0 text-site-text shadow-card backdrop:bg-black/50"
    :aria-label="t('dashboard.contracts.document.title')"
    @close="emit('close')"
  >
    <header class="flex items-center justify-between gap-3 border-b border-site-line px-5 py-3">
      <div class="min-w-0">
        <p class="font-extrabold text-site-heading">{{ t("dashboard.contracts.document.title") }}</p>
        <p class="truncate text-caption text-site-muted" dir="ltr">{{ name }}</p>
      </div>
      <div class="flex shrink-0 items-center gap-1">
      <button
        v-if="html"
        type="button"
        class="inline-flex items-center gap-1.5 rounded-full border-2 border-site-heading px-4 py-1.5 text-label font-bold text-site-heading transition hover:bg-site-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
        :title="t('dashboard.contracts.document.printHint')"
        @click="print"
      >
        <LucidePrinter class="size-4" aria-hidden="true" />
        {{ t("dashboard.contracts.document.print") }}
      </button>
      <button
        type="button"
        class="grid size-10 shrink-0 place-items-center rounded-full text-site-heading transition hover:bg-site-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
        :aria-label="t('dashboard.contracts.document.close')"
        :title="t('dashboard.contracts.document.close')"
        @click="close"
      >
        <LucideX class="size-5" aria-hidden="true" />
      </button>
      </div>
    </header>

    <div class="flex min-h-0 flex-1 flex-col overflow-y-auto lg:flex-row lg:overflow-hidden">
      <!-- The contract: the print sits on white paper in both themes -->
      <div class="min-h-[60vh] flex-1 bg-site-tint p-3 lg:min-h-0 lg:overflow-hidden">
        <p v-if="failed" class="p-6 text-center text-site-muted">{{ t("dashboard.contracts.document.failed") }}</p>
        <p v-else-if="!html" class="p-6 text-center text-site-muted">{{ t("dashboard.contracts.document.loading") }}</p>
        <iframe
          v-else
          ref="frame"
          :srcdoc="html"
          :title="t('dashboard.contracts.document.title')"
          class="h-full min-h-[60vh] w-full rounded-2xl border border-site-line bg-white lg:min-h-0"
          @load="fit"
        />
      </div>

      <!-- Signing -->
      <aside
        v-if="canSign || isDraft"
        class="shrink-0 border-t border-site-line p-5 lg:w-80 lg:overflow-y-auto lg:border-s lg:border-t-0"
      >
        <p v-if="!canSign" class="text-caption text-site-muted">{{ t("dashboard.contracts.document.draftNote") }}</p>
        <form v-else class="space-y-4" @submit.prevent="sign">
          <div>
            <h2 class="font-extrabold text-site-heading">{{ t("dashboard.contracts.sign.title") }}</h2>
            <p class="mt-1 text-caption text-site-muted">{{ t("dashboard.contracts.sign.intro") }}</p>
          </div>
          <label class="flex items-start gap-2 text-caption text-site-heading">
            <input
              id="contract-consent"
              v-model="consent"
              type="checkbox"
              class="mt-0.5 size-4 shrink-0 rounded border-site-line text-brand-green focus:ring-brand-leaf"
            />
            <span>{{ t("dashboard.contracts.sign.consent") }}</span>
          </label>
          <BaseInput v-model="signee" :label="t('dashboard.contracts.sign.name')" autocomplete="name" required />
          <div>
            <p class="mb-1.5 text-caption font-bold text-site-heading">{{ t("dashboard.contracts.sign.pad") }}</p>
            <SignaturePad
              v-model="signature"
              :label="t('dashboard.contracts.sign.pad')"
              :hint="t('dashboard.contracts.sign.padHint')"
              :clear-label="t('dashboard.contracts.sign.clear')"
            />
          </div>
          <BaseNotice v-if="signFailed">{{ signFailed }}</BaseNotice>
          <BaseButton type="submit" class="w-full" :loading="signing" :disabled="!ready">
            <LucidePenLine class="size-4" aria-hidden="true" />
            {{ signing ? t("dashboard.contracts.sign.signing") : t("dashboard.contracts.sign.submit") }}
          </BaseButton>
        </form>
      </aside>
    </div>
  </dialog>
</template>

<script lang="ts" setup>
import { useResizeObserver } from "@vueuse/core"
import { computed, onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"
import LucidePenLine from "~icons/lucide/pen-line"
import LucidePrinter from "~icons/lucide/printer"
import LucideX from "~icons/lucide/x"

import BaseButton from "@/components/base/BaseButton.vue"
import BaseInput from "@/components/base/BaseInput.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import SignaturePad from "@/components/dashboard/SignaturePad.vue"
import { MethodError } from "@/services/http"
import {
	type ContractEntry,
	getContractPrint,
	signContract,
} from "@/services/portal"

const props = defineProps<{
	name: string
	/** Issued and waiting for the producer's signature. */
	canSign: boolean
	/** Still being prepared (awaiting its payment): read only. */
	isDraft: boolean
}>()
const emit = defineEmits<{
	close: []
	signed: [entries: ContractEntry[]]
}>()

const { t } = useI18n()
const dialog = ref<HTMLDialogElement | null>(null)
const frame = ref<HTMLIFrameElement | null>(null)
const html = ref("")
const failed = ref(false)

const consent = ref(false)
const signee = ref("")
const signature = ref<string | null>(null)
const signing = ref(false)
const signFailed = ref("")
const ready = computed(
	() =>
		consent.value && signee.value.trim() && signature.value && !signing.value,
)

onMounted(async () => {
	dialog.value?.showModal()
	try {
		html.value = (await getContractPrint(props.name)).html
	} catch {
		failed.value = true
	}
})

/**
 * The printed page in the window: without Frappe's print toolbar (its PDF button is the desk's: a producer
 * has no permission to print), and scaled down to the window's width when the A4 page is wider.
 */
function fit() {
	const page = frame.value?.contentDocument
	if (!page?.documentElement || !frame.value) return
	if (!page.getElementById("contract-document-style")) {
		const style = page.createElement("style")
		style.id = "contract-document-style"
		style.textContent = ".action-banner { display: none !important; }"
		page.head.append(style)
	}
	const root = page.documentElement
	root.style.zoom = "1"
	const available = frame.value.clientWidth
	const width = root.scrollWidth
	root.style.zoom = width > available ? String(available / width) : "1"
}

useResizeObserver(frame, fit)

/** Print the contract alone, at its own size (A4): the browser's dialog prints it or saves it as a PDF. */
function print() {
	const page = frame.value?.contentWindow
	if (!page) return
	page.document.documentElement.style.zoom = "1"
	page.addEventListener("afterprint", fit, { once: true })
	page.focus()
	page.print()
}

function close() {
	dialog.value?.close()
}

async function sign() {
	if (!ready.value || !signature.value) return
	signing.value = true
	signFailed.value = ""
	try {
		const entries = await signContract(
			props.name,
			signee.value.trim(),
			signature.value,
		)
		emit("signed", entries)
		close()
	} catch (error) {
		// The server's own reason when it gives one (a missing name, an unreadable signature)
		signFailed.value =
			error instanceof MethodError && error.serverMessages.length
				? error.serverMessages.join(" ")
				: t("dashboard.contracts.sign.failed")
	} finally {
		signing.value = false
	}
}
</script>
