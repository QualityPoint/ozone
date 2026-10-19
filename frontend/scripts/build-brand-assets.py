"""Generate the website's brand assets from Ozone's official logo files in ~/Projects/Ozone.

Sources (outside the repo):
  logo.svg   the official logo, vector, 500x235: red (#af2625) and green (#11532a) inks
  logo.png   the same logo, 2084x980 on transparent
  References/ملف تشغيل أوزون نهائي copy.pdf
             the operation file: its pages are images of the fleet and containers in Ozone's
             livery, rendered with poppler's pdftoppm and cropped (PHOTOS below)

The script writes:

  src/assets/brand/logo-color.svg     header logo on light backgrounds (the official inks)
  src/assets/brand/logo-white.svg     the same with the green ink white, for dark backgrounds
  public/favicon.ico                  16/32/48 px: the logo's red "O" and its location pin
  public/favicon-32.png               browser tab
  public/apple-touch-icon.png         180 px, on white
  public/icon-192.png, icon-512.png   web app manifest icons, on white
  public/og-image.png                 1200x630 social preview: the logo between the brand stripes
  src/assets/images/equipment/<slug>.webp   fleet and container photos (listed in src/config/site.ts)
  src/assets/images/hero-truck.webp   the hero's compactor truck, cut out on transparency
  src/assets/images/<folder>/<slug>.webp  photos embedded in the operation file (EMBEDDED_PHOTOS)
  src/assets/naqel/quality-point.webp      Naqel's developer's logo, for the Naqel page (QP_LOGO)

The Naqel page's developer logo comes from Quality Point's own media (QP_LOGO, outside the repo).

Usage (from frontend/):  ~/frappe-bench/env/bin/python scripts/build-brand-assets.py [SOURCE_DIR]
Requires Pillow, OpenCV and NumPy (all in the bench's env), and poppler-utils (pdftoppm and
pdfimages) for the photos.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw

FRONTEND = Path(__file__).resolve().parent.parent
SOURCE = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / "Projects/Ozone")
BRAND_OUT = FRONTEND / "src/assets/brand"
IMAGES_OUT = FRONTEND / "src/assets/images"
PHOTOS_OUT = IMAGES_OUT / "equipment"
PUBLIC_OUT = FRONTEND / "public"

GREEN = "#11532a"
RED = "#af2625"
WHITE = (255, 255, 255, 255)

# The operation file, and each photo's page and crop box at PHOTO_DPI (left, top, right, bottom),
# around the product only: below the page's header and its red section tag.
OPERATION_FILE = "References/ملف تشغيل أوزون نهائي copy.pdf"
PHOTO_DPI = 150
PHOTO_WIDTH = 1100
PHOTOS = {
	"compactor-trucks": (17, (122, 301, 1671, 1013)),
	"hook-lift-truck": (18, (281, 307, 1557, 1001)),
	"tipper-truck": (19, (146, 229, 1710, 965)),
	"skip-loader": (20, (101, 290, 1719, 920)),
	"indoor-bins": (28, (215, 290, 1632, 1013)),
	"outdoor-containers": (29, (137, 343, 1485, 1094)),
	"compactors": (30, (221, 427, 1590, 887)),
	"debris-containers": (31, (74, 445, 1707, 881)),
	# The capabilities page: support vehicles and the crews' safety gear.
	"supervision-cars": (22, (100, 490, 1530, 1000)),
	"support-pickups": (23, (110, 380, 1670, 870)),
	"mobile-workshop": (25, (180, 450, 1460, 1010)),
	"staff-bus": (26, (310, 405, 1435, 1055)),
	"safety-gear": (37, (220, 280, 1545, 1110)),
}

# The hero's truck: the green compactor truck, embedded image 6 on page 17 (`pdfimages -list`),
# and its box body (left, top, right, bottom) in that image, kept whole: the white top edge of
# the body is too faint against the white page to find.
HERO_TRUCK = (17, 6)
HERO_TRUCK_BODY = (500, 178, 1060, 500)
HERO_WIDTH = 1200

# Photos embedded in the operation file, at their full resolution: published path under
# src/assets/images/ → (page, image number from `pdfimages -list`, trim the white page around it).
EMBEDDED_PHOTOS = {
	# The capabilities page's opening and methodology: the head office (pages 13 and 14).
	"office/towers": (13, 10, False),
	"office/entrance": (13, 8, False),
	"office/reception": (14, 5, False),
	# Its daily routes: the compactor truck of each sorting stream (pages 54 to 56).
	"equipment/route-residuals": (54, 0, True),
	"equipment/route-organics": (55, 0, True),
	"equipment/route-recyclables": (56, 0, True),
}
EMBEDDED_WIDTH = 1100

# Quality Point's logo (blue on white), trimmed to its ink, for the Naqel page's closing panel.
QP_LOGO = Path.home() / "Documents/Companies-Media/QP/QP_Software/assests/QualityPoint_Logo_Software.png"
QP_LOGO_WIDTH = 360

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


def write_photos() -> None:
	"""Each PHOTOS entry: its page rendered at PHOTO_DPI, cropped, scaled to PHOTO_WIDTH, as WebP.
	The photos keep the documents' off-white background; the site shows them on white cards."""
	PHOTOS_OUT.mkdir(parents=True, exist_ok=True)
	with tempfile.TemporaryDirectory() as tmp:
		for slug, (page, box) in PHOTOS.items():
			stem = Path(tmp) / slug
			subprocess.run(
				[
					"pdftoppm",
					"-r",
					str(PHOTO_DPI),
					"-png",
					"-singlefile",
					"-f",
					str(page),
					"-l",
					str(page),
					str(SOURCE / OPERATION_FILE),
					str(stem),
				],
				check=True,
			)
			photo = Image.open(f"{stem}.png").convert("RGB").crop(box)
			photo = photo.resize(
				(PHOTO_WIDTH, round(photo.height * PHOTO_WIDTH / photo.width)), Image.LANCZOS
			)
			photo.save(PHOTOS_OUT / f"{slug}.webp", quality=82, method=6)


def ellipse(size: int) -> np.ndarray:
	return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))


def largest(mask: np.ndarray) -> np.ndarray:
	"""Only the largest connected part of `mask`."""
	_, labels, stats, _ = cv2.connectedComponentsWithStats((mask > 127).astype(np.uint8))
	return np.where(labels == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA]), mask, 0).astype(np.uint8)


def truck_alpha(bgr: np.ndarray) -> np.ndarray:
	"""The truck's mask on the page's white background, without the ground shadow."""
	height, width = bgr.shape[:2]
	gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
	low = bgr.min(axis=2).astype(int)
	spread = bgr.max(axis=2).astype(int) - low

	# The background is what the page's corners reach without crossing an edge or a coloured
	# or grey pixel. Around the wheels only dark or coloured pixels stop it, so the grey ground
	# shadow is background.
	barrier = cv2.dilate(cv2.Canny(cv2.GaussianBlur(gray, (3, 3), 0), 10, 30), ellipse(3))
	barrier |= (((low < 215) | (spread > 25)) * 255).astype(np.uint8)
	rows = np.where(((low < 215) | (spread > 25)).any(axis=1))[0]
	wheel_band = int(rows[0] + (rows[-1] - rows[0]) * 0.72)
	dark = (((low < 60) | (spread > 40)) * 255).astype(np.uint8)
	barrier[wheel_band:] = cv2.dilate(dark, ellipse(3))[wheel_band:]
	reach = 255 - barrier
	for seed in ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)):
		if reach[seed[1], seed[0]] == 255:
			cv2.floodFill(reach, None, seed, 128)
	alpha = np.where(reach == 128, 0, 255).astype(np.uint8)
	x0, y0, x1, y1 = HERO_TRUCK_BODY
	alpha[y0:y1, x0:x1] = 255
	alpha = largest(cv2.morphologyEx(alpha, cv2.MORPH_OPEN, ellipse(5)))
	alpha = cv2.erode(alpha, ellipse(3))  # the dilated edges leave a halo outside the contour

	# Below the axles, the tyres' dark contact shadow passes the rule above. Keep only the
	# tyres (found as circles), the textured tread beside them, and nothing under the ground.
	circles = cv2.HoughCircles(
		cv2.medianBlur(gray, 5),
		cv2.HOUGH_GRADIENT,
		dp=1.5,
		minDist=300,
		param1=120,
		param2=40,
		minRadius=90,
		maxRadius=160,
	)[0]
	wheels = [(round(x), round(y), round(r)) for x, y, r in circles if y > height * 0.6][:2]
	if len(wheels) != 2:
		raise SystemExit(f"found {len(wheels)} wheels on the hero truck, expected 2")
	blur = cv2.blur(gray.astype(np.float32), (9, 9))
	deviation = np.sqrt(np.maximum(cv2.blur(gray.astype(np.float32) ** 2, (9, 9)) - blur**2, 0))
	keep = cv2.morphologyEx(((deviation > 8) * 255).astype(np.uint8), cv2.MORPH_OPEN, ellipse(5))
	axle = min(y for _, y, _ in wheels)
	keep[axle + min(r for _, _, r in wheels) // 2 :] = 0
	for x, y, r in wheels:
		cv2.circle(keep, (x, y), r, 255, -1)
	alpha[axle:] &= keep[axle:]
	alpha[max(y + r for _, y, r in wheels) - 6 :] = 0
	return cv2.GaussianBlur(largest(alpha), (3, 3), 0)


def embedded_image(page: int, number: int) -> Image.Image:
	"""An image embedded in the operation file, at its own resolution (`pdfimages -list`)."""
	with tempfile.TemporaryDirectory() as tmp:
		subprocess.run(
			["pdfimages", "-f", str(page), "-l", str(page), "-j", str(SOURCE / OPERATION_FILE), f"{tmp}/img"],
			check=True,
		)
		image = Image.open(f"{tmp}/img-{number:03d}.jpg")
		# Adobe CMYK JPEGs: Pillow reads their inks inverted.
		return (ImageChops.invert(image) if image.mode == "CMYK" else image).convert("RGB")


def scaled(image: Image.Image, width: int) -> Image.Image:
	"""`image` at most `width` wide."""
	if image.width <= width:
		return image
	return image.resize((width, round(image.height * width / image.width)), Image.LANCZOS)


def trimmed(image: Image.Image, margin: float) -> Image.Image:
	"""`image` cropped to its subject on a white ground, keeping `margin` of its width around it."""
	ink = ImageChops.difference(image, Image.new("RGB", image.size, WHITE[:3])).convert("L")
	box = ink.point(lambda v: 255 if v > 24 else 0).getbbox()
	pad = round(image.width * margin)
	return image.crop(
		(
			max(box[0] - pad, 0),
			max(box[1] - pad, 0),
			min(box[2] + pad, image.width),
			min(box[3] + pad, image.height),
		)
	)


def write_embedded_photos() -> None:
	"""Each EMBEDDED_PHOTOS entry as WebP, trimmed to its subject on the white page when asked."""
	for path, (page, number, trim) in EMBEDDED_PHOTOS.items():
		photo = embedded_image(page, number)
		if trim:
			photo = trimmed(photo, 0.02)
		out = IMAGES_OUT / f"{path}.webp"
		out.parent.mkdir(parents=True, exist_ok=True)
		scaled(photo, EMBEDDED_WIDTH).save(out, quality=82, method=6)


def write_hero_truck() -> None:
	"""The compactor truck from the operation file, cut out, cropped and scaled to HERO_WIDTH."""
	photo = embedded_image(*HERO_TRUCK)
	rgba = photo.convert("RGBA")
	rgba.putalpha(Image.fromarray(truck_alpha(cv2.cvtColor(np.asarray(photo), cv2.COLOR_RGB2BGR))))
	truck = rgba.crop(rgba.getchannel("A").point(lambda a: 255 if a > 10 else 0).getbbox())
	truck = scaled(truck, HERO_WIDTH)
	truck.save(IMAGES_OUT / "hero-truck.webp", quality=85, alpha_quality=90, method=6)


def write_qp_logo() -> None:
	"""Quality Point's logo on its white ground (the page shows it on a white plate), trimmed."""
	logo = trimmed(Image.open(QP_LOGO).convert("RGB"), 0)
	out = FRONTEND / "src/assets/naqel/quality-point.webp"
	scaled(logo, QP_LOGO_WIDTH).save(out, lossless=True, method=6)


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
	write_photos()
	write_hero_truck()
	write_embedded_photos()
	write_qp_logo()
	print(f"wrote brand assets from {SOURCE}")


if __name__ == "__main__":
	main()
