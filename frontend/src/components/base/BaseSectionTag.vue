<template>
  <!-- The documents' section label: white text on a slanted red tag with a darker edge
       (mirrored in RTL). Takes its text through the slot. -->
  <span class="relative isolate inline-flex px-5 py-1.5 text-caption font-bold text-white">
    <span class="tag-edge absolute inset-0 -z-10 translate-y-1 bg-brand-red-800" aria-hidden="true" />
    <span class="tag-face absolute inset-0 -z-10 bg-brand-red" aria-hidden="true" />
    <slot />
  </span>
</template>

<style scoped>
.tag-face,
.tag-edge {
	clip-path: polygon(10px 0, 100% 0, calc(100% - 10px) 100%, 0 100%);
}
:dir(rtl) .tag-face,
:dir(rtl) .tag-edge {
	clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 10px 100%);
}
</style>
