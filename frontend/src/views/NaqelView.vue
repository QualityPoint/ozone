<template>
  <!-- The Naqel system, as its own site's home page presents it (docs/naqel_page/README.md), between
       Ozone's header and footer. `.naqel` gives everything inside Naqel's identity
       (assets/styles/naqel.css). -->
  <div class="naqel">
    <NaqelHero />
    <NaqelPlatform />
    <NaqelContracting />
    <NaqelFinance />
    <NaqelCalculator />
    <NaqelOperations />
    <NaqelGovernance />
    <NaqelContact />
  </div>
</template>

<script lang="ts" setup>
import NaqelCalculator from "@/components/naqel/NaqelCalculator.vue"
import NaqelContact from "@/components/naqel/NaqelContact.vue"
import NaqelContracting from "@/components/naqel/NaqelContracting.vue"
import NaqelFinance from "@/components/naqel/NaqelFinance.vue"
import NaqelGovernance from "@/components/naqel/NaqelGovernance.vue"
import NaqelHero from "@/components/naqel/NaqelHero.vue"
import NaqelOperations from "@/components/naqel/NaqelOperations.vue"
import NaqelPlatform from "@/components/naqel/NaqelPlatform.vue"
</script>
