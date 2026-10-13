<template>
  <!-- A login form as one of the documents' white panels: the red section tag, the title, the
       result notice, the form (slot) and a footer link under a silver rule. -->
  <BaseCard class="p-6 sm:p-8">
    <BaseSectionTag>{{ t("auth.tag") }}</BaseSectionTag>
    <h1 class="mt-5 text-heading font-extrabold text-site-heading">{{ title }}</h1>
    <p v-if="subtitle" class="mt-2 text-site-muted">{{ subtitle }}</p>

    <BaseNotice v-if="notice" :kind="notice.kind" class="mt-6">{{ notice.text }}</BaseNotice>

    <div class="mt-6">
      <slot />
    </div>

    <p v-if="$slots.footer" class="mt-8 border-t border-site-line pt-6 text-center text-caption">
      <slot name="footer" />
    </p>
  </BaseCard>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"

import BaseCard from "@/components/base/BaseCard.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import BaseSectionTag from "@/components/base/BaseSectionTag.vue"
import type { AuthNotice } from "./authHelpers"

defineProps<{
	title: string
	subtitle?: string
	/** Result message above the form; errors are announced at once (role=alert). */
	notice?: AuthNotice | null
}>()

const { t } = useI18n()
</script>
