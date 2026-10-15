<template>
  <!-- The facility's pin on an OpenStreetMap map: click to drop it, drag to move it. It follows
       `latitude`/`longitude` (a pasted location is resolved by the server on save). Opens on the pin, or
       on Address Settings' default centre (FacilitySettings.map). -->
  <div :class="$attrs.class">
    <span class="mb-1.5 block text-caption font-bold text-site-heading">{{ label }}</span>
    <div ref="holder" dir="ltr" role="region" :aria-label="label" class="facility-map h-72 overflow-hidden rounded-xl border-2" :class="error ? 'border-red-500' : 'border-site-line'" />
    <p class="mt-1.5 text-caption text-site-muted">{{ hint }}</p>
    <p v-if="error" class="mt-1 text-caption font-bold text-red-600 dark:text-red-400">{{ error }}</p>
  </div>
</template>

<script lang="ts" setup>
import "leaflet/dist/leaflet.css"
import L from "leaflet"
import { onBeforeUnmount, onMounted, ref, watch } from "vue"

defineOptions({ inheritAttrs: false })

const props = defineProps<{
	label: string
	hint: string
	error?: string
	/** Where the map opens when there is no pin yet. */
	center: { latitude: number; longitude: number; zoom: number }
}>()

const latitude = defineModel<number | null>("latitude", { default: null })
const longitude = defineModel<number | null>("longitude", { default: null })

const holder = ref<HTMLElement | null>(null)
let map: L.Map | null = null
let marker: L.Marker | null = null

// A pin drawn in CSS (the brand green), so no marker images are needed from Leaflet's package.
const pinIcon = L.divIcon({
	className: "facility-pin",
	html: '<span class="facility-pin__dot"></span>',
	iconSize: [28, 28],
	iconAnchor: [14, 28],
})

function place(lat: number, lng: number, pan = false) {
	if (!map) return
	if (marker) marker.setLatLng([lat, lng])
	else {
		marker = L.marker([lat, lng], { draggable: true, icon: pinIcon }).addTo(map)
		marker.on("dragend", () => {
			const at = marker?.getLatLng()
			if (at) set(at.lat, at.lng)
		})
	}
	if (pan) map.setView([lat, lng], Math.max(map.getZoom(), 15))
}

/** The pin as this map last set it, so the watcher can tell its own changes from outside ones. */
let own: [number, number] | null = null

/** Six decimals: about 10 cm, as Frappe's Geolocation stores. */
function set(lat: number, lng: number) {
	own = [Number(lat.toFixed(6)), Number(lng.toFixed(6))]
	latitude.value = own[0]
	longitude.value = own[1]
}

onMounted(() => {
	if (!holder.value) return
	const hasPin = latitude.value != null && longitude.value != null
	map = L.map(holder.value, { attributionControl: true }).setView(
		hasPin
			? [latitude.value as number, longitude.value as number]
			: [props.center.latitude, props.center.longitude],
		hasPin ? 15 : props.center.zoom,
	)
	L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
		maxZoom: 19,
		attribution: "© OpenStreetMap",
	}).addTo(map)
	if (hasPin) place(latitude.value as number, longitude.value as number)
	map.on("click", (event: L.LeafletMouseEvent) => {
		set(event.latlng.lat, event.latlng.lng)
	})
})

watch([latitude, longitude], ([lat, lng]) => {
	if (lat == null || lng == null) {
		marker?.remove()
		marker = null
		return
	}
	// A click or drag here only moves the pin; a pin set from outside (another facility) brings
	// the map to it.
	const fromHere = own !== null && own[0] === lat && own[1] === lng
	place(lat, lng, !fromHere)
})

onBeforeUnmount(() => {
	map?.remove()
	map = null
	marker = null
})
</script>

<style>
.facility-pin__dot {
	display: block;
	width: 28px;
	height: 28px;
	border-radius: 50% 50% 50% 0;
	transform: rotate(-45deg);
	background: theme("colors.brand.red.DEFAULT"); /* the accent: stands out on the map */
	border: 3px solid #fff;
	box-shadow: 0 2px 6px rgb(0 0 0 / 0.35);
}
/* Leaflet's own stacking sits above the site's header; keep the map under it. */
.facility-map .leaflet-pane,
.facility-map .leaflet-control {
	z-index: 1;
}
</style>
