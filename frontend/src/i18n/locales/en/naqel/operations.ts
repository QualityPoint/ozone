export default {
	title: "Smart operations",
	intro:
		"A connected fleet, smart scales, an operations dashboard, and AI that brings estimates closer to reality.",
	iot: {
		gps: {
			title: "Live compactor tracking",
			body: "Advanced tracking of collection vehicles and compactor trucks, to check routes and speeds and ensure geographic coverage.",
		},
		weighing: {
			title: "On-board weighing",
			body: "Scales and weight sensors on the trucks measure the actual weight of every container emptied, automatically and instantly.",
		},
		attribution: {
			title: "Weights linked to facilities",
			body: "The measured weights are linked automatically to the facilities and activities the truck serves on its route.",
		},
	},
	devicesTitle: "On every compactor",
	devices: {
		"gps-unit": {
			name: "GPS transmitter",
			body: "Sends the compactor's position, live.",
		},
		"card-reader": {
			name: "Reader",
			body: "Identifies every container emptied.",
		},
		"cab-tablet": {
			name: "Control screen",
			body: "In the driver's cab: the route and the tasks.",
		},
		"weighing-scale": {
			name: "Electronic scale",
			body: "Weighs each container after it's emptied into the compactor.",
		},
	},
	dashboardTitle: "The operations dashboard",
	dashboard: [
		"Active vehicles tracked on the map.",
		"Operational routes: their paths, occupancy and waste generation rates.",
		"Container sites and their coverage of nearby facilities.",
		"Drivers rotated and assigned to routes, and shifts scheduled.",
		"Container fill reports from the contracted producer or the operations team.",
	],
	ai: {
		title: "AI calibration",
		body: "AI compares each facility's operational generation rate with the theoretical estimate, and updates the calculation automatically from the actual operating history.",
		theoretical: "Theoretical estimate",
		weighed: "Weighed in operation",
		calibrated: "AI-calibrated estimate",
		gap: "Gap",
		illustration: "Illustrative values",
		steps: ["Weighed data", "AI learns", "Rate updated"],
	},
}
