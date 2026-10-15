<template>
  <!-- The facility's region: type a name, pick from the regions Naqel Settings allows (its assigned
       Region Division and below; ozone.api.portal.search_regions). Each shows where it lies, since
       districts share names across cities. Picking one fills the address's city and district (the
       parent form listens to `pick`); a pin dropped on the map picks one too (`chosen`). -->
  <div class="relative">
    <BaseInput
      v-model="query"
      :label="label"
      :error="error"
      :placeholder="t('dashboard.facilities.regionSearch')"
      role="combobox"
      :aria-expanded="open"
      :aria-controls="listId"
      autocomplete="off"
      @focus="open = true"
      @input="search"
    />
    <ul
      v-if="open && results.length"
      :id="listId"
      role="listbox"
      class="absolute inset-x-0 z-20 mt-1 max-h-64 overflow-y-auto rounded-xl border border-site-line bg-site-bg p-1 shadow-card"
    >
      <li v-for="region in results" :key="region.value" role="option" :aria-selected="region.value === model">
        <button type="button" class="flex w-full flex-wrap items-baseline gap-x-3 rounded-lg px-3 py-2 text-start text-caption hover:bg-site-hover" @click="choose(region)">
          <span class="font-bold text-site-heading">{{ region.label }}</span>
          <span class="text-site-muted">{{ region.within.join(t("dashboard.separator")) }}</span>
        </button>
      </li>
    </ul>
    <p v-else-if="open && searched && !results.length" class="mt-1.5 text-caption text-site-muted">{{ t("dashboard.facilities.regionNone") }}</p>
  </div>
</template>

<script lang="ts" setup>
import { ref, useId, watch } from "vue"
import { useI18n } from "vue-i18n"

import BaseInput from "@/components/base/BaseInput.vue"
import { type RegionOption, searchRegions } from "@/services/portal"

const props = defineProps<{
	label: string
	error?: string
	/** The chosen region as text: when editing a facility, or after the map's pin picked one. */
	chosen?: string | null
}>()
const emit = defineEmits<{ pick: [region: RegionOption] }>()

/** The chosen region's name (Region). */
const model = defineModel<string>({ default: "" })
const { t } = useI18n()
const listId = useId()

const query = ref(props.chosen ?? "")
const results = ref<RegionOption[]>([])
const open = ref(false)
const searched = ref(false)
let timer: ReturnType<typeof setTimeout> | undefined

watch(
	() => props.chosen,
	(text) => {
		query.value = text ?? ""
	},
)

function search() {
	model.value = ""
	clearTimeout(timer)
	timer = setTimeout(async () => {
		results.value = await searchRegions(query.value).catch(() => [])
		searched.value = true
		open.value = true
	}, 250)
}

function choose(region: RegionOption) {
	model.value = region.value
	query.value = describe(region)
	open.value = false
	emit("pick", region)
}

function describe(region: RegionOption): string {
	return [region.label, ...region.within].join(t("dashboard.separator"))
}
</script>
