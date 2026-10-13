"""Generate the website's brand assets from Ozone's official logo files in ~/Projects/Ozone.

Sources (outside the repo):
  logo.svg   the official logo, vector, 500x235: red (#af2625) and green (#11532a) inks
  logo.png   the same logo, 2084x980 on transparent

The script writes:

  src/assets/brand/logo-color.svg     header logo on light backgrounds (the official inks)
  src/assets/brand/logo-white.svg     the same with the green ink white, for dark backgrounds
  public/favicon.ico                  16/32/48 px: the logo's red "O" and its location pin
  public/favicon-32.png               browser tab
  public/apple-touch-icon.png         180 px, on white
  public/icon-192.png, icon-512.png   web app manifest icons, on white
  public/og-image.png                 1200x630 social preview: the logo between the brand stripes

Usage (from frontend/):  python3 scripts/build-brand-assets.py [SOURCE_DIR]
Requires Pillow.
"""

import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

FRONTEND = Path(__file__).resolve().parent.parent
SOURCE = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / "Projects/Ozone")
BRAND_OUT = FRONTEND / "src/assets/brand"
PUBLIC_OUT = FRONTEND / "public"

GREEN = "#11532a"
RED = "#af2625"
WHITE = (255, 255, 255, 255)

# Where the red "O" and its location pin sit in logo.png (measured from its pixels).
O_BOX = (56, 324, 528, 798)
PIN_BOX = (208, 92, 348, 282)


def clean_svg(svg: str) -> str:
	"""The logo without the XML prolog and Illustrator's generator comment."""
	svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
	return re.sub(r"\s*<!--.*?-->", "", svg, flags=re.S).strip() + "\n"


def write_logos() -> None:
	svg = clean_svg((SOURCE / "logo.svg").read_text(encoding="utf-8"))
	if GREEN not in svg.lower():
		raise SystemExit(f"logo.svg no longer uses the green ink {GREEN}")
	(BRAND_OUT / "logo-color.svg").write_text(svg, encoding="utf-8")
	white = re.sub(GREEN, "#ffffff", svg, flags=re.I)
	(BRAND_OUT / "logo-white.svg").write_text(white, encoding="utf-8")


def inside(box: tuple[int, int, int, int], x: int, y: int) -> bool:
	return box[0] <= x <= box[2] and box[1] <= y <= box[3]


def o_mark(logo: Image.Image) -> Image.Image:
	"""Only the red "O" and the pin above it, cut from the logo and trimmed."""
	mark = Image.new("RGBA", logo.size, (0, 0, 0, 0))
	src, out = logo.load(), mark.load()
	for y in range(min(O_BOX[1], PIN_BOX[1]), max(O_BOX[3], PIN_BOX[3]) + 1):
		for x in range(min(O_BOX[0], PIN_BOX[0]), max(O_BOX[2], PIN_BOX[2]) + 1):
			r, g, b, a = src[x, y]
			red = r > 120 and g < 100 and b < 100
			if a and ((red and inside(O_BOX, x, y)) or inside(PIN_BOX, x, y)):
				out[x, y] = (r, g, b, a)
	return mark.crop(mark.getbbox())


def square(img: Image.Image, size: int, background=None, fill: float = 0.86) -> Image.Image:
	"""`img` centred on a square canvas, scaled to `fill` of its side."""
	canvas = Image.new("RGBA", (size, size), background or (0, 0, 0, 0))
	scale = fill * size / max(img.size)
	art = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
	canvas.alpha_composite(art, ((size - art.width) // 2, (size - art.height) // 2))
	return canvas


def brand_stripe(draw: ImageDraw.ImageDraw, width: int, y: int, height: int, top: bool) -> None:
	"""The documents' stripe: green with a red segment at the start (top), or green over a
	lighter green line (bottom). Drawn for an Arabic page, so "start" is on the right."""
	draw.rectangle((0, y, width, y + height), fill=GREEN)
	if top:
		draw.rectangle((width - width // 3, y, width, y + height // 2), fill=RED)
	else:
		draw.rectangle((0, y, width, y + height // 4), fill="#61be51")


def og_image(logo: Image.Image) -> Image.Image:
	width, height, stripe = 1200, 630, 18
	image = Image.new("RGBA", (width, height), WHITE)
	draw = ImageDraw.Draw(image)
	brand_stripe(draw, width, 0, stripe, top=True)
	brand_stripe(draw, width, height - stripe, stripe, top=False)
	art = logo.crop(logo.getbbox())
	art = art.resize((720, round(art.height * 720 / art.width)), Image.LANCZOS)
	image.alpha_composite(art, ((width - art.width) // 2, (height - art.height) // 2))
	return image.convert("RGB")


def main() -> None:
	BRAND_OUT.mkdir(parents=True, exist_ok=True)
	PUBLIC_OUT.mkdir(parents=True, exist_ok=True)
	write_logos()

	logo = Image.open(SOURCE / "logo.png").convert("RGBA")
	mark = o_mark(logo)
	square(mark, 32, fill=0.98).save(PUBLIC_OUT / "favicon-32.png", optimize=True)
	icons = [square(mark, size, fill=0.98) for size in (16, 32, 48)]
	icons[-1].save(PUBLIC_OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=icons[:-1])
	square(mark, 180, WHITE, fill=0.76).save(PUBLIC_OUT / "apple-touch-icon.png", optimize=True)
	for size in (192, 512):
		square(mark, size, WHITE, fill=0.76).save(PUBLIC_OUT / f"icon-{size}.png", optimize=True)
	og_image(logo).save(PUBLIC_OUT / "og-image.png", optimize=True)
	print(f"wrote brand assets from {SOURCE}")


if __name__ == "__main__":
	main()
