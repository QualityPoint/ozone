// Runs vue-tsc and reports only errors in this project.
//
// frappe-ui is published as raw .ts/.vue source rather than compiled .d.ts files,
// so vue-tsc type-checks it along with our code (skipLibCheck does not apply) and
// reports a large number of strict-mode errors inside node_modules/frappe-ui.
// Those are not ours to fix, so they are filtered out here.
import { spawnSync } from "node:child_process"
import { createRequire } from "node:module"

const vueTsc = createRequire(import.meta.url).resolve("vue-tsc/bin/vue-tsc.js")
const result = spawnSync(
	process.execPath,
	[vueTsc, "-b", "--pretty", "false"],
	{
		encoding: "utf8",
	},
)

if (result.error) {
	console.error(result.error.message)
	process.exit(1)
}

// Each diagnostic starts with "<file>(line,col): error TSxxxx" and may continue
// on indented lines.
const diagnostics = []
for (const line of `${result.stdout}${result.stderr}`.split("\n")) {
	if (!line.trim()) continue
	if (/^\s/.test(line) && diagnostics.length) {
		diagnostics[diagnostics.length - 1] += `\n${line}`
	} else {
		diagnostics.push(line)
	}
}

const ignored = diagnostics.filter((d) => d.startsWith("node_modules/"))
const own = diagnostics.filter((d) => !d.startsWith("node_modules/"))

if (own.length) {
	console.error(own.join("\n"))
	console.error(`\n${own.length} type error(s) in project files.`)
}
if (ignored.length) {
	console.log(`(ignored ${ignored.length} type error(s) inside node_modules)`)
}

process.exit(own.length ? 1 : 0)
