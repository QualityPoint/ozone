<template>
  <!-- The waste-sorting file's inverted triangle: the preferred options widest and darkest at the
       top, disposal last. Each tier is one step lighter and narrower. -->
  <figure>
    <figcaption class="mb-4 text-center font-bold text-site-heading">{{ t("about.hierarchy.title") }}</figcaption>
    <ol class="space-y-1.5">
      <li
        v-for="(tier, i) in tiers"
        :key="tier"
        class="mx-auto rounded-xl py-2.5 text-center text-caption font-bold text-white"
        :style="{ width: `${100 - i * 14}%`, backgroundColor: SHADES[i] }"
      >
        {{ tier }}
      </li>
    </ol>
  </figure>
</template>

<script lang="ts" setup>
import { computed } from "vue"
import { useI18n } from "vue-i18n"

import { useMessageList } from "@/composables/useMessageList"

/** From the brand green to the leaf green, one step per tier. */
const SHADES = ["#11532a", "#1e6435", "#2f8340", "#47a34a", "#61be51"]

const { t } = useI18n()
const { list } = useMessageList()
const tiers = computed(() => list("about.hierarchy.tiers"))
</script>
