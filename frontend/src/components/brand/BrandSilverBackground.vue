<template>
  <!-- The documents' backdrop: white pages with soft diagonal silver shards and faint dots.
       Built from the `site-silver` token, so it follows the theme; purely decorative. -->
  <div class="pointer-events-none fixed inset-0 -z-10 overflow-hidden bg-site-bg" aria-hidden="true">
    <div class="shard shard-a" />
    <div class="shard shard-b" />
    <div class="shard shard-c" />
    <div class="dots" />
  </div>
</template>

<style scoped>
.shard {
	position: absolute;
	inset: 0;
}
.shard-a {
	background: linear-gradient(135deg, rgb(var(--site-silver) / 0.9), transparent 55%);
	clip-path: polygon(0 0, 46% 0, 0 62%);
}
.shard-b {
	background: linear-gradient(315deg, rgb(var(--site-silver) / 0.8), transparent 60%);
	clip-path: polygon(100% 38%, 100% 100%, 58% 100%);
}
.shard-c {
	background: linear-gradient(160deg, transparent 30%, rgb(var(--site-silver) / 0.45) 50%, transparent 70%);
}
.dots {
	position: absolute;
	inset: 0;
	background-image: radial-gradient(rgb(var(--site-silver)) 1px, transparent 1.5px);
	background-size: 22px 22px;
	mask-image: linear-gradient(200deg, #000 0%, transparent 45%);
	opacity: 0.7;
}
</style>
