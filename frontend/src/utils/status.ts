/**
 * A status badge in its DocType state's colour (ozone/portal: status_color), as the Desk's indicator
 * pills show it: a light tint with darker text. The colours are those a DocType State offers.
 */
const BADGES = {
	blue: "bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-200",
	cyan: "bg-cyan-100 text-cyan-700 dark:bg-cyan-900/40 dark:text-cyan-200",
	gray: "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-200",
	green: "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-200",
	"light-blue":
		"bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-300",
	orange:
		"bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-200",
	pink: "bg-pink-100 text-pink-700 dark:bg-pink-900/40 dark:text-pink-200",
	purple:
		"bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-200",
	red: "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-200",
	yellow:
		"bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-200",
} as const

export type StateColor = keyof typeof BADGES

/** The badge's colour classes; gray for a colour it doesn't know. */
export function statusBadge(color: string | null | undefined): string {
	return BADGES[color as StateColor] ?? BADGES.gray
}
