// The Naqel page's messages (docs/naqel_page/README.md): Naqel's own site's (hawya's), one file per
// section as there, under `naqel.` so they never clash with Ozone's.
import calculator from "./calculator"
import contact from "./contact"
import contracting from "./contracting"
import finance from "./finance"
import governance from "./governance"
import hero from "./hero"
import operations from "./operations"
import platform from "./platform"

export default {
	/** The logo's name, its alternative text. */
	name: "ناقل",
	/** The system's line, from the website mock in the presentation. */
	tagline: "نظام رقمي ذكي لإدارة النفايات الفردية والتجارية",
	hero,
	platform,
	contracting,
	finance,
	calculator,
	operations,
	governance,
	contact,
}
