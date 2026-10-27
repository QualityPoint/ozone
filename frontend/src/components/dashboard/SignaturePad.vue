<template>
  <!-- A pad to sign on with a finger, a pen or the mouse: dark ink on white whatever the theme, as on paper. The
       signature comes out as a PNG data URL (null while the pad is empty), as naqel's signature check takes it. -->
  <div>
    <div class="relative overflow-hidden rounded-2xl border-2 border-dashed border-site-line bg-white">
      <canvas
        ref="canvas"
        class="block h-40 w-full touch-none cursor-crosshair"
        :aria-label="label"
        role="img"
        @pointerdown="start"
        @pointermove="draw"
        @pointerup="end"
        @pointerleave="end"
        @pointercancel="end"
      />
      <span
        v-if="empty"
        class="pointer-events-none absolute inset-x-0 bottom-3 text-center text-label text-gray-400"
        aria-hidden="true"
      >
        {{ hint }}
      </span>
    </div>
    <button
      type="button"
      class="mt-2 inline-flex items-center gap-1.5 text-caption font-bold text-site-heading hover:underline disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
      :disabled="empty"
      @click="clear"
    >
      <LucideEraser class="size-4" aria-hidden="true" />
      {{ clearLabel }}
    </button>
  </div>
</template>

<script lang="ts" setup>
import { useResizeObserver } from "@vueuse/core"
import { onMounted, ref } from "vue"
import LucideEraser from "~icons/lucide/eraser"

defineProps<{ label: string; hint: string; clearLabel: string }>()
const signature = defineModel<string | null>({ default: null })

const canvas = ref<HTMLCanvasElement | null>(null)
const empty = ref(true)
let drawing = false
let last: { x: number; y: number } | null = null

/** The canvas at the screen's pixel density, so the strokes stay sharp; a resize starts it over. */
function setUp() {
	const el = canvas.value
	if (!el) return
	const ratio = window.devicePixelRatio || 1
	const { width, height } = el.getBoundingClientRect()
	el.width = Math.round(width * ratio)
	el.height = Math.round(height * ratio)
	const context = el.getContext("2d")
	if (!context) return
	context.scale(ratio, ratio)
	context.lineCap = "round"
	context.lineJoin = "round"
	context.lineWidth = 2.4
	context.strokeStyle = "#111827"
	clear()
}

onMounted(setUp)
useResizeObserver(canvas, setUp)

function point(event: PointerEvent) {
	const rect = (event.target as HTMLCanvasElement).getBoundingClientRect()
	return { x: event.clientX - rect.left, y: event.clientY - rect.top }
}

function start(event: PointerEvent) {
	drawing = true
	last = point(event)
	;(event.target as HTMLCanvasElement).setPointerCapture(event.pointerId)
	// A tap leaves a dot
	draw(event)
}

function draw(event: PointerEvent) {
	if (!drawing || !last) return
	const context = canvas.value?.getContext("2d")
	if (!context) return
	const next = point(event)
	context.beginPath()
	context.moveTo(last.x, last.y)
	context.lineTo(next.x + 0.01, next.y + 0.01)
	context.stroke()
	last = next
	empty.value = false
}

function end() {
	if (!drawing) return
	drawing = false
	last = null
	if (!empty.value)
		signature.value = canvas.value?.toDataURL("image/png") ?? null
}

function clear() {
	const el = canvas.value
	el?.getContext("2d")?.clearRect(0, 0, el.width, el.height)
	empty.value = true
	signature.value = null
}
</script>
