<template>
  <!-- A logged-in account nobody has linked to a producer yet (docs/producer_dashboard/identity.md):
       not an error, a step. The transporter links it; the page says how to reach them. -->
  <section class="mx-auto max-w-xl py-8 text-center">
    <span class="mx-auto grid size-16 place-items-center rounded-2xl bg-site-hover text-brand-green dark:text-brand-leaf">
      <LucideLink2Off class="size-8" aria-hidden="true" />
    </span>
    <h1 class="mt-6 text-heading font-extrabold text-site-heading">{{ t("dashboard.notLinked.title") }}</h1>
    <p class="mt-3 text-site-muted">{{ t("dashboard.notLinked.body") }}</p>
    <div v-if="actions.length" class="mt-8 flex flex-wrap justify-center gap-3">
      <BaseButton v-for="(action, i) in actions" :key="action.href" :href="action.href" :variant="i ? 'outline' : 'primary'">
        <component :is="action.icon" class="size-4" aria-hidden="true" />
        {{ action.label }}
      </BaseButton>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideLink2Off from "~icons/lucide/link-2-off"

import BaseButton from "@/components/base/BaseButton.vue"
import { useContactActions } from "@/composables/useContactActions"

const { t } = useI18n()
const actions = useContactActions()
</script>
