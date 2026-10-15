<template>
  <!-- The facility's activity: type a code or a name, pick from the matching ISIC activities
       (ozone.api.portal.search_isic). The chosen one shows with its code. -->
  <div class="relative">
    <BaseInput
      v-model="query"
      :label="label"
      :error="error"
      :placeholder="t('dashboard.facilities.isicSearch')"
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
      <li v-for="activity in results" :key="activity.name" role="option" :aria-selected="activity.name === model">
        <button type="button" class="flex w-full gap-3 rounded-lg px-3 py-2 text-start text-caption hover:bg-site-hover" @click="choose(activity)">
          <span class="shrink-0 font-bold text-site-heading" dir="ltr">{{ activity.code }}</span>
          <span class="text-site-text">{{ activity.title }}</span>
        </button>
      </li>
    </ul>
    <p v-else-if="open && searched && !results.length" class="mt-1.5 text-caption text-site-muted">{{ t("dashboard.facilities.isicNone") }}</p>
  </div>
</template>

<script lang="ts" setup>
import { ref, useId } from "vue"
import { useI18n } from "vue-i18n"

import BaseInput from "@/components/base/BaseInput.vue"
import { type Activity, searchIsic } from "@/services/portal"

const props = defineProps<{
	label: string
	error?: string
	/** The chosen activity's text, when editing a facility. */
	initial?: string | null
}>()

/** The chosen activity's name (ISIC Classification). */
const model = defineModel<string>({ default: "" })
const { t } = useI18n()
const listId = useId()

const query = ref(props.initial ?? "")
const results = ref<Activity[]>([])
const open = ref(false)
const searched = ref(false)
let timer: ReturnType<typeof setTimeout> | undefined

function search() {
	model.value = ""
	clearTimeout(timer)
	timer = setTimeout(async () => {
		results.value = await searchIsic(query.value).catch(() => [])
		searched.value = true
		open.value = true
	}, 250)
}

function choose(activity: Activity) {
	model.value = activity.name
	query.value = `${activity.code} — ${activity.title}`
	open.value = false
}
</script>
