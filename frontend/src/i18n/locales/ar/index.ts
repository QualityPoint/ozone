import about from "./about"
import auth from "./auth"
import common from "./common"
import contact from "./contact"
import equipment from "./equipment"
import hero from "./hero"
import industries from "./industries"
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
}

/** Arabic, the default language, is the source of truth: every locale must match this shape. */
export type MessageSchema = typeof ar

export default ar
