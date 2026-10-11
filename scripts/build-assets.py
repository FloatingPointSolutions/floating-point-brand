#!/usr/bin/env python3
"""build the downloadable brand assets from the outlined wordmark.

reads assets/floating.svg (the source of truth for the wordmark paths) and writes:
  assets/wordmark/   wordmark in ink soft, ink and paper, svg + png
  assets/point/      the point on its own, plus the round avatar and sticker marks
  assets/icon/       app icons and favicons
  assets/banner/     linkedin banners (built by scripts/build-banners.py, packed here)
  assets/floating-brand-assets.zip   everything above plus the motion files

needs rsvg-convert (brew install librsvg) and pillow.
run from the repo root: python3 scripts/build-assets.py
"""
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

PAPER = "#f5f3ee"
MIST = "#e8e5dd"
INK_SOFT = "#2a2730"
INK = "#15141a"

SVG_HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}" role="img" aria-label="{label}">\n'


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def png(svg_path, out_path, width, height=None):
    args = ["rsvg-convert", "-w", str(width)]
    if height:
        args += ["-h", str(height)]
    subprocess.run(args + ["-o", str(out_path), str(svg_path)], check=True)


# ---------------------------------------------------------------- wordmark
src = (ASSETS / "floating.svg").read_text()
vb = re.search(r'viewBox="([^"]+)"', src).group(1)
_, _, VW, VH = (float(v) for v in vb.split())
inner = src[src.index("<g fill="):src.rindex("</svg>")]
inner = re.sub(r'<g fill="#[0-9a-f]{6}">', '<g fill="{fill}">', inner, count=1)

wm_dir = ASSETS / "wordmark"
for name, fill in [("ink-soft", INK_SOFT), ("ink", INK), ("paper", PAPER)]:
    svg = wm_dir / f"floating-wordmark-{name}.svg"
    write(svg, SVG_HEAD.format(vb=vb, w=VW, h=VH, label="floating.") + "  " + inner.replace("{fill}", fill) + "</svg>\n")
    for w in (800, 1600, 3200):
        png(svg, wm_dir / f"floating-wordmark-{name}-{w}.png", w)

# ---------------------------------------------------------------- the point
# the dot alone, sized to its own box, in each of the three marking colors
pt_dir = ASSETS / "point"
for name, fill in [("ink-soft", INK_SOFT), ("ink", INK), ("paper", PAPER)]:
    svg = pt_dir / f"floating-point-{name}.svg"
    write(svg, SVG_HEAD.format(vb="0 0 100 100", w=100, h=100, label="floating point")
          + f'  <circle cx="50" cy="50" r="50" fill="{fill}"/>\n</svg>\n')
    for w in (256, 512, 1024):
        png(svg, pt_dir / f"floating-point-{name}-{w}.png", w)

# round marks: a disc with the point centred. ratios match the guidelines page
# (avatar: dot 38% of the disc; sticker: dot 36% of the disc)
ROUND = [
    ("avatar", PAPER, INK_SOFT, 0.38),
    ("avatar-dark", INK, PAPER, 0.38),
    ("sticker", PAPER, INK, 0.36),
    ("sticker-dark", INK, PAPER, 0.36),
]
for name, ground, dot, ratio in ROUND:
    svg = pt_dir / f"floating-point-{name}.svg"
    write(svg, SVG_HEAD.format(vb="0 0 100 100", w=100, h=100, label="floating point")
          + f'  <circle cx="50" cy="50" r="50" fill="{ground}"/>\n'
          + f'  <circle cx="50" cy="50" r="{ratio * 50:g}" fill="{dot}"/>\n</svg>\n')
    for w in (256, 512, 1024):
        png(svg, pt_dir / f"floating-point-{name}-{w}.png", w)

# ---------------------------------------------------------------- icons
icon_dir = ASSETS / "icon"
# app icon: 22% corner radius, dot 44% of the tile
for name, ground, dot in [("app-icon", PAPER, INK), ("app-icon-dark", INK, PAPER)]:
    svg = icon_dir / f"floating-{name}.svg"
    write(svg, SVG_HEAD.format(vb="0 0 1024 1024", w=1024, h=1024, label="floating point")
          + f'  <rect width="1024" height="1024" rx="225.28" fill="{ground}"/>\n'
          + f'  <circle cx="512" cy="512" r="225.28" fill="{dot}"/>\n</svg>\n')
    for w in (180, 512, 1024):
        png(svg, icon_dir / f"floating-{name}-{w}.png", w)

# favicon: the same mark the site uses in its tab
fav = icon_dir / "favicon.svg"
write(fav, SVG_HEAD.format(vb="0 0 32 32", w=32, h=32, label="floating point")
      + f'  <rect width="32" height="32" rx="7" fill="{INK}"/>\n'
      + f'  <circle cx="16" cy="16" r="6" fill="{PAPER}"/>\n</svg>\n')
for w in (16, 32, 48, 180):
    png(fav, icon_dir / f"favicon-{w}.png", w)
Image.open(icon_dir / "favicon-48.png").save(icon_dir / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# ---------------------------------------------------------------- zip
zip_path = ASSETS / "floating-brand-assets.zip"
zip_path.unlink(missing_ok=True)
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for folder in ("wordmark", "point", "icon", "banner"):
        for f in sorted((ASSETS / folder).iterdir()):
            z.write(f, f"floating-brand-assets/{folder}/{f.name}")
    extras = {
        "floating.mp4": "motion", "floating.gif": "motion", "floating-wordmark.gif": "motion",
        "floating-wordmark@2x.png": "email", "floating-wordmark@3x.png": "email",
    }
    for f, folder in extras.items():
        z.write(ASSETS / f, f"floating-brand-assets/{folder}/{f}")

print("done:", sum(1 for _ in ASSETS.rglob("*") if _.is_file()), "files under assets/")
