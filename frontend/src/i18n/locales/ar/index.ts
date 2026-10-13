import common from "./common"
import hero from "./hero"

const ar = {
	...common,
	hero,
}

/** Arabic, the default language, is the source of truth: every locale must match this shape. */
export type MessageSchema = typeof ar

export default ar
