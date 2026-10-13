<template>
  <!-- The site has two languages, so the switch is one link to this page's twin in the other
       one (/#about ↔ /en#about), named in that language. -->
  <RouterLink
    :to="twin(other)"
    :hreflang="other"
    :lang="other"
    :aria-label="`${t('language.switchTo')} ${languages[other].native}`"
    :class="[
      'inline-flex h-10 shrink-0 items-center gap-2 rounded-full px-3 text-caption font-bold text-site-heading transition hover:bg-site-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-leaf',
      other === 'ar' ? 'font-arabic' : 'font-sans',
    ]"
  >
    <LucideLanguages class="size-5" aria-hidden="true" />
    <span class="sm:hidden">{{ languages[other].short }}</span>
    <span class="hidden sm:inline">{{ languages[other].native }}</span>
  </RouterLink>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideLanguages from "~icons/lucide/languages"

import { useLocale } from "@/composables/useLocale"
import { languages } from "@/config/site"

const { t } = useI18n()
const { other, twin } = useLocale()
</script>
