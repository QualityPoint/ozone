// Note: vue-i18n reserves `@ { } | $` in messages. Keep emails, URLs and phone
// numbers out of messages (they come from Ozone Settings).
import meta from "../meta.json"

export default {
	// The page title and description: one file for the SPA and the server (ozone/www/frontend.py).
	meta: meta.ar,
	brand: {
		// One name for the SPA and the server (og:site_name), from meta.json.
		name: meta.site.ar,
		/** The logo's slogan, shown as separate items. */
		tagline: ["صيانة", "نظافة", "مقاولات عامة"],
		about:
			"شركة من المدينة المنورة متخصصة في جمع ونقل النفايات ومخلفات البناء والنظافة، تطبّق فرز النفايات من المصدر حسب نوعها.",
	},
	a11y: {
		skipToContent: "انتقل إلى المحتوى",
		openMenu: "افتح القائمة",
		closeMenu: "أغلق القائمة",
		home: "الصفحة الرئيسية لأوزون",
	},
	nav: {
		about: "من نحن",
		capabilities: "قدراتنا",
		services: "خدماتنا",
		industries: "القطاعات",
		contact: "تواصل معنا",
	},
	language: {
		/** The switch's accessible name, followed by the other language's name. */
		switchTo: "اعرض الموقع باللغة",
	},
	theme: {
		toDark: "التبديل إلى الوضع الداكن",
		toLight: "التبديل إلى الوضع الفاتح",
	},
	footer: {
		contact: "تواصل معنا",
		follow: "تابعنا",
		/** Accessible name of a social icon link, followed by the platform name. */
		socialLabel: "أوزون على",
		whatsapp: "واتساب",
		map: "موقعنا على الخريطة",
		explore: "تصفح",
		rights: "جميع الحقوق محفوظة.",
	},
}
