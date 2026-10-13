# Styling

Tailwind 3.4 with frappe-ui's preset (`tailwind.config.ts`), as in blinktech.

## What the preset changes

- **Dark mode** is `[data-theme="dark"]` on `<html>` (`darkMode: ['selector', …]`), which is
  what `useTheme` sets. `dark:` classes work, but public pages use the `site-*` tokens
  instead ([branding.md](branding.md#light-and-dark)).
- **`text-xs…3xl`** carry letter-spacing and weights tuned for app UI. Public pages use the
  site scale (`text-label`, `text-caption`, `text-body`, `text-body-lg`, `text-title`,
  `text-heading`, `text-display`…) instead.
- **Images are dimmed in dark mode** (`[data-theme='dark'] img`). Logos opt out with
  `brand-art`.

## Shared classes (`src/assets/styles/components.css`)

| Class | Use |
| --- | --- |
| `.section` | A page section's container: centred, `max-w-6xl`, side padding |
| `.float-layer` | With `motion-safe:animate-float`: puts the element on its own GPU layer |

Add a class here only when a second component needs the same utility list. Otherwise keep
utilities in the template.

## Right to left

Arabic is the default, so every layout must work in both directions:

- Use logical utilities: `ps-`/`pe-`, `ms-`/`me-`, `start-`/`end-`, `text-start`. Never
  `pl-`, `left-`, `text-left`.
- Shapes that point one way (the stripe's slanted segment, the section tag) flip with
  `:dir(rtl)` in their scoped styles.
- Icons that mean a direction (arrows, chevrons) need `rtl:-scale-x-100`.

## Motion

`animate-fade-up` and `animate-float` are in the theme. Use them as `motion-safe:animate-…`, so
they stay off under `prefers-reduced-motion`. Smooth scrolling is also motion-safe
(`main.css`).

## Responsive

Mobile first. The header shows the nav from `lg`, and a menu button below it. Check every
change at 320–414 px and on desktop, with no sideways scrolling.
