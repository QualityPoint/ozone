<template>
  <button
    type="button"
    :aria-label="isDark ? t('theme.toLight') : t('theme.toDark')"
    :title="isDark ? t('theme.toLight') : t('theme.toDark')"
    class="grid size-10 place-items-center rounded-full text-site-heading transition hover:bg-site-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf"
    @click="toggle()"
  >
    <LucideSun v-if="isDark" class="size-5" aria-hidden="true" />
    <LucideMoon v-else class="size-5" aria-hidden="true" />
  </button>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideMoon from "~icons/lucide/moon"
import LucideSun from "~icons/lucide/sun"

import { useTheme } from "@/composables/useTheme"

const { t } = useI18n()
const { isDark, toggle } = useTheme()
</script>
