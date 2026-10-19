import about from "./about"
import auth from "./auth"
import capabilities from "./capabilities"
import common from "./common"
import contact from "./contact"
import dashboard from "./dashboard"
import equipment from "./equipment"
import hero from "./hero"
import industries from "./industries"
import naqel from "./naqel"
import services from "./services"
import why from "./why"

const ar = {
	...common,
	hero,
	about,
	services,
	equipment,
	industries,
	why,
	contact,
	auth,
	capabilities,
	naqel,
	dashboard,
}

/** Arabic, the default language, is the source of truth: every locale must match this shape. */
export type MessageSchema = typeof ar

export default ar
