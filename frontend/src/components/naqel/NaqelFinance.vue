<template>
  <section id="finance" class="overflow-x-clip bg-site-tint py-16 sm:py-20">
    <NaqelSectionHeading :title="t('naqel.finance.title')" :intro="t('naqel.finance.intro')" />

    <div class="section mt-10">
      <ul class="grid gap-6 md:grid-cols-3">
        <li v-for="(icon, id) in PAYMENTS" :key="id">
          <NaqelCard as="article" class="h-full p-6">
            <span class="grid size-12 place-items-center rounded-xl bg-naqel-green text-white">
              <component :is="icon" class="size-6" aria-hidden="true" />
            </span>
            <h3 class="mt-4 text-title font-extrabold text-site-heading">{{ t(`naqel.finance.payments.${id}.title`) }}</h3>
            <p class="mt-2 text-site-muted">{{ t(`naqel.finance.payments.${id}.body`) }}</p>
          </NaqelCard>
        </li>
      </ul>

      <div class="mt-12 grid gap-10 md:grid-cols-2">
        <div>
          <NaqelPillHeading>{{ t("naqel.finance.pricingTitle") }}</NaqelPillHeading>
          <NaqelCheckList :items="list('naqel.finance.pricing')" class="mt-5 px-2 text-site-text" />
        </div>
        <div>
          <NaqelPillHeading tone="ink">{{ t("naqel.finance.billingTitle") }}</NaqelPillHeading>
          <NaqelCheckList :items="list('naqel.finance.billing')" class="mt-5 px-2 text-site-text" />
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useI18n } from "vue-i18n"
import LucideCreditCard from "~icons/lucide/credit-card"
import LucideReceiptText from "~icons/lucide/receipt-text"
import LucideWallet from "~icons/lucide/wallet"

import NaqelCard from "@/components/naqel/base/NaqelCard.vue"
import NaqelCheckList from "@/components/naqel/base/NaqelCheckList.vue"
import NaqelPillHeading from "@/components/naqel/base/NaqelPillHeading.vue"
import NaqelSectionHeading from "@/components/naqel/base/NaqelSectionHeading.vue"
import { useMessageList } from "@/composables/useMessageList"

const PAYMENTS = {
	gateways: LucideCreditCard,
	wallets: LucideWallet,
	invoicing: LucideReceiptText,
}

const { t } = useI18n()
const { list } = useMessageList()
</script>
