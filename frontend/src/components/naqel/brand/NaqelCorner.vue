<template>
  <!-- The presentation's corner mark: the green right angle beside every title. In Arabic it sits
       right of the title with its corner at the top-left (┏), as in the presentation; English
       mirrors it (┓). Decorative. -->
  <svg viewBox="0 0 24 24" class="corner inline-block shrink-0" aria-hidden="true">
    <path d="M3 3h18v7H10v11H3z" fill="currentColor" />
  </svg>
</template>

<style scoped>
:dir(ltr) .corner {
	transform: scaleX(-1);
}
</style>
