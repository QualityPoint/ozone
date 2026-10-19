/**
 * The Naqel page's facts (docs/naqel_page/README.md): the Naqel system as its own site presents it
 * (hawya's config/site.ts). Translatable text lives in src/i18n/locales/<code>/naqel/, not here.
 */

/** Naqel's developer, whom the page's calls to action write to; its logo closes the page. */
export const naqelDeveloper = {
	name: "Quality Point",
	email: "erp@qp.sa",
} as const

/** A mailto: link to the developer. */
export const naqelContactHref = `mailto:${naqelDeveloper.email}`

/**
 * How much of a figure must show before it plays its entrance: Naqel's own (hawya's useReveal
 * default), so the page moves as Naqel's site does.
 */
export const naqelRevealThreshold = 0.25

/** The rating's factors, one star to five (the calculator section). */
export const ratingFactors = [1.1, 1.3, 1.5, 1.8, 2.0] as const

/** One cubic yard in cubic metres. */
const CUBIC_YARD = 0.764555

/**
 * The containers the calculator infers, smallest to largest, at their capacity in m³: the
 * presentation's chart (p. 35) places each at its capacity on the generation-rate scale. Each id is
 * a Desk icon in naqel's sprite (NaqelIcon) and a `naqel.calculator.containers.names.<id>` message.
 */
export const inferredContainers = [
	{ id: "bin-240l", capacity: 0.24 },
	{ id: "container-2yd", capacity: 2 * CUBIC_YARD },
	{ id: "container-4yd", capacity: 4 * CUBIC_YARD },
	{ id: "container-6yd", capacity: 6 * CUBIC_YARD },
	{ id: "container-12yd", capacity: 12 * CUBIC_YARD },
	{ id: "container-20yd", capacity: 20 * CUBIC_YARD },
] as const

/** The chart's generation-rate scale, in m³, as in the presentation: 0 to 16, a line every 4. */
export const generationScale = { max: 16, step: 4 } as const

/**
 * The platform's apps (its modules), as its apps screen lists them, each with one of naqel's Desk
 * icons (NaqelIcon). Names are `naqel.platform.modules.<id>`.
 */
export const platformModules = [
	{ id: "crm", icon: "contract" },
	{ id: "operations", icon: "truck" },
	{ id: "planning", icon: "route" },
	{ id: "quality", icon: "workshop" },
	{ id: "setup", icon: "sliders" },
	{ id: "settings", icon: "gear" },
] as const

/**
 * The devices on each compactor, as the presentation's diagram places them around the truck
 * (p. 45): two on the start side, two on the end side. Texts are `naqel.operations.devices.<id>`.
 */
export const devices = [
	"gps-unit",
	"card-reader",
	"cab-tablet",
	"weighing-scale",
] as const
