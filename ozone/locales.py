"""Texts the server shares with the SPA, read from its JSON files (frontend/src/i18n/locales/),
so the two never differ: meta.json (page paths, titles, descriptions)."""

import json
from functools import lru_cache
from pathlib import Path

import frappe

LOCALES = Path(frappe.get_app_path("ozone")).parent / "frontend" / "src" / "i18n" / "locales"

# The site's languages; the first is the default, served without a path prefix. The same
# list as SUPPORTED_LOCALES in frontend/src/types/index.ts.
SUPPORTED_LOCALES = ("ar", "en")
DEFAULT_LOCALE = SUPPORTED_LOCALES[0]


@lru_cache
def shared_json(name: str) -> dict:
	"""One of the SPA's JSON files ("meta.json"…), read once per process."""
	return json.loads((LOCALES / name).read_text(encoding="utf-8"))
