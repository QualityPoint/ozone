export default {
	title: "Naqel's calculator",
	intro:
		"A smart, standard calculator that estimates each facility's waste precisely, for every waste type: commercial, residential, construction and demolition, and any type you add.",
	isic: {
		title: "Activities classified by ISIC",
		body: "The calculator works from the economic activity, by the latest edition of the International Standard Industrial Classification, and can be set at any of its levels.",
		levels: ["Section", "Division", "Group", "Class", "Activity"],
	},
	rate: {
		title: "A flexible generation rate",
		body: "Production tiers for each activity, several units of measure, and safety margins for each classification, adjusted to operational reality.",
	},
	rating: {
		title: "Fair evaluation",
		body: "Each facility's waste is estimated by its own rating, one to five stars: by how busy it really is, not its size alone.",
		factor: "Factor",
	},
	containers: {
		title: "The inferred container",
		body: "The generation rate is turned into the right container for the facility, automatically.",
		/** The chart's scale (config/naqel.ts: generationScale) and each capacity's unit. */
		axis: "Generation rate (m³)",
		unit: "m³",
		/** Each container's name (config/naqel.ts: inferredContainers). */
		names: {
			"bin-240l": "240 litres",
			"container-2yd": "2 yards",
			"container-4yd": "4 yards",
			"container-6yd": "6 yards",
			"container-12yd": "12 yards",
			"container-20yd": "20 yards",
		},
	},
	geo: {
		title: "Geographic precision",
		body: "Estimates reflect population density and commercial activity, so they differ from one district to the next for the same activity.",
		levels: ["Region", "Amanah", "Municipality", "District"],
	},
	tree: {
		title: "Waste tree and weights",
		body: "A multi-level tree of every waste type, with a specific gravity for each that turns volume into actual weight in tonnes.",
	},
}
