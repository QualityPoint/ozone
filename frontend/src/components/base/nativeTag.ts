import { type Component, defineComponent, h } from "vue"

/**
 * A component that renders exactly the native `tag`, for `<component :is>`.
 *
 * `<component :is="'button'">` doesn't: Vue resolves a string against registered components
 * first, and frappe-ui registers Button, Input, Dialog… globally (main.ts), so "button" renders
 * frappe-ui's Button, with its own size and layout. Attributes, classes, listeners and slots pass
 * through; a template ref gets the component, whose `$el` is the element.
 */
const tags = new Map<string, Component>()

export function nativeTag(tag: string): Component {
	let component = tags.get(tag)
	if (!component) {
		component = defineComponent({
			name: `Native${tag}`,
			setup(_, { slots }) {
				return () => h(tag, slots.default?.())
			},
		})
		tags.set(tag, component)
	}
	return component
}
