import { computed } from "vue"
import { useI18n } from "vue-i18n"
import { type RouteLocationRaw, useRoute } from "vue-router"

import { basePath, localeHome, localePath, pagePaths } from "@/config/site"
import { isRtl } from "@/i18n"
import { type LocaleCode, type NavItem, SUPPORTED_LOCALES } from "@/types"

/** Current language and direction, and links that keep or switch the language. */
export function useLocale() {
	const { locale } = useI18n()
	const route = useRoute()

	const current = computed(() => locale.value as LocaleCode)
	/** The other language: the site has two. */
	const other = computed(
		() =>
			SUPPORTED_LOCALES.find((code) => code !== current.value) as LocaleCode,
	)
	const rtl = computed(() => isRtl(current.value))
	const home = computed(() => localeHome[current.value])

	/** This page in another language, keeping its query and #section: /#about → /en#about. */
	function twin(code: LocaleCode): RouteLocationRaw {
		return {
			path: localePath(basePath(route.path), code),
			query: route.query,
			hash: route.hash,
		}
	}

	/** A section of the landing page in the current language: /#about, /en#about. */
	function sectionLink(section: string): RouteLocationRaw {
		return { path: home.value, hash: `#${section}` }
	}

	/** Where a navbar item leads: its page, or its section of the landing page. */
	function navTarget(item: NavItem): RouteLocationRaw {
		return "page" in item
			? { path: localePath(pagePaths[item.page], current.value) }
			: sectionLink(item.section)
	}

	return { current, other, rtl, home, twin, sectionLink, navTarget }
}
