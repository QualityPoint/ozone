export default {
	title: "One system, two sides",
	intro:
		"A B2B system linking the transporter to waste producers: the transporter works inside it, each producer from its own account.",
	sides: {
		transporter: {
			title: "The transporter",
			term: "Transporter",
			who: "The transport company and its team, in the system.",
			points: [
				"Clients, facilities, requests, quotations and contracts.",
				"The fleet, drivers, container sites and routes.",
				"Daily operations, followed live.",
				"Invoicing, collection and statements.",
			],
		},
		producer: {
			title: "The waste producer",
			term: "Producer",
			who: "The client facility, from its dashboard.",
			points: [
				"Service requests and waste calculation.",
				"Quotations and contracts, tracked.",
				"Facilities and branches, one account.",
				"Reports, invoices and payments.",
			],
		},
	},
	exchange: {
		request: "Service request",
		quotation: "Quotation",
		contract: "Service contract",
		service: "Service and invoices",
	},
	modulesTitle: "The system's apps",
	/** The system's apps (config/naqel.ts: platformModules). */
	modules: {
		crm: "CRM",
		operations: "Operations",
		planning: "Planning",
		quality: "Quality",
		setup: "Setup",
		settings: "Settings",
	},
	foundationTitle: "Scalable foundations",
	foundation: {
		framework: {
			title: "Trusted framework",
			body: "Built on a robust framework for the highest security standards, stability and easy customisation.",
		},
		integration: {
			title: "Flexible integration",
			body: "APIs and an event-driven architecture make it easy to connect current and future municipal systems.",
		},
		ai: {
			title: "AI-ready",
			body: "A Python core that machine-learning models plug into, for predictive analytics and waste-volume forecasts.",
		},
		saas: {
			title: "Modules as a service",
			body: "Specialised modules for operational plans, costing and profitability, offered by subscription to transporters and companies.",
		},
		awareness: {
			title: "Outreach and awareness",
			body: "Connected to social media, with awareness campaigns on waste management and sorting at source.",
		},
	},
}
