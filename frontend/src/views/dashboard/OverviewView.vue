<template>
  <!-- The dashboard's first page: who the account belongs to, and what it holds so far. -->
  <section>
    <DashboardHeading
      :eyebrow="t(`dashboard.stage.${producer?.doctype ?? 'Lead'}`)"
      :title="producer?.title ?? ''"
      :intro="t(`dashboard.overview.intro.${producer?.doctype ?? 'Lead'}`)"
    />

    <BaseNotice v-if="failed" class="mt-8">{{ t("dashboard.loadFailed") }}</BaseNotice>
    <ul class="mt-8 grid gap-4 sm:grid-cols-2">
      <li v-for="item in COUNTS" :key="item.id">
        <BaseCard class="flex items-center gap-4 p-5">
          <span class="grid size-12 shrink-0 place-items-center rounded-xl bg-site-hover text-brand-green dark:text-brand-leaf">
            <component :is="item.icon" class="size-6" aria-hidden="true" />
          </span>
          <div>
            <p class="text-heading font-extrabold text-site-heading" dir="ltr">
              {{ overview ? formatNumber(overview.counts[item.count]) : "—" }}
            </p>
            <p class="text-caption text-site-muted">{{ t(`dashboard.overview.counts.${item.id}`) }}</p>
          </div>
        </BaseCard>
      </li>
    </ul>
  </section>
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia"
import { onMounted, ref } from "vue"
import { useI18n } from "vue-i18n"
import LucideBuilding2 from "~icons/lucide/building-2"
import LucideClipboardList from "~icons/lucide/clipboard-list"
import LucideHandshake from "~icons/lucide/handshake"
import LucideReceipt from "~icons/lucide/receipt"

import BaseCard from "@/components/base/BaseCard.vue"
import BaseNotice from "@/components/base/BaseNotice.vue"
import DashboardHeading from "@/components/dashboard/DashboardHeading.vue"
import { useLocale } from "@/composables/useLocale"
import { type Overview, getOverview } from "@/services/portal"
import { useUserStore } from "@/stores/user"
import { formatNumber } from "@/utils/format"

const { t } = useI18n()
const { current } = useLocale()
const { producer } = storeToRefs(useUserStore())

/** The records counted on the page (ozone.api.portal.get_overview: counts). */
const COUNTS = [
	{ id: "facilities", count: "facilities", icon: LucideBuilding2 },
	{ id: "requests", count: "service_requests", icon: LucideClipboardList },
	{ id: "quotations", count: "quotations", icon: LucideReceipt },
	{ id: "contracts", count: "contracts", icon: LucideHandshake },
] as const

const overview = ref<Overview | null>(null)
const failed = ref(false)

onMounted(async () => {
	try {
		overview.value = await getOverview()
	} catch {
		failed.value = true
	}
})
</script>
