<template>
  <!-- The operation file's three waste streams, each in the colour of its bins, bags and truck. -->
  <figure>
    <figcaption>
      <span class="block text-title font-extrabold text-site-heading">{{ t("about.streams.title") }}</span>
      <span class="mt-2 block text-caption text-site-muted">{{ t("about.streams.intro") }}</span>
    </figcaption>
    <ul class="mt-5 space-y-3">
      <li v-for="stream in wasteStreams" :key="stream.id" class="flex gap-4 rounded-2xl bg-site-tint p-4">
        <span
          class="grid size-11 shrink-0 place-items-center rounded-xl text-white ring-1 ring-white/20"
          :style="{ backgroundColor: stream.color }"
        >
          <component :is="ICONS[stream.id]" class="size-5" aria-hidden="true" />
        </span>
        <div>
          <p class="font-extrabold text-site-heading">{{ t(`about.streams.items.${stream.id}.name`) }}</p>
          <p class="mt-1 text-caption text-site-muted">{{ t(`about.streams.items.${stream.id}.examples`) }}</p>
        </div>
      </li>
    </ul>
  </figure>
</template>

<script lang="ts" setup>
import type { Component } from "vue"
import { useI18n } from "vue-i18n"
import LucideLeaf from "~icons/lucide/leaf"
import LucideRecycle from "~icons/lucide/recycle"
import LucideTrash2 from "~icons/lucide/trash-2"

import { wasteStreams } from "@/config/site"
import type { WasteStreamId } from "@/types"

/** The symbols on the operation file's bins. */
const ICONS: Record<WasteStreamId, Component> = {
	organics: LucideLeaf,
	recyclables: LucideRecycle,
	residuals: LucideTrash2,
}

const { t } = useI18n()
</script>
