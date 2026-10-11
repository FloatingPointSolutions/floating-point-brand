#!/usr/bin/env python3
"""build the linkedin banners from the outlined wordmark.

the word stands on the longitude line from the site, its period the last point on it, with the
contacts under it in inter medium. writes assets/banner/ as svg + png at both linkedin sizes,
on paper and on ink.

needs rsvg-convert (brew install librsvg), pillow, and inter installed as a system font
(the svg text is set in inter; the png is the file to hand out).
run from the repo root: python3 scripts/build-banners.py
"""
import re
import subprocess
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT = ASSETS / "banner"

PAPER = "#f5f3ee"
MIST = "#e8e5dd"
INK_SOFT = "#2a2730"
INK = "#15141a"
# ground, word, contacts; the line and ticks take the word's colour at the site's opacities
THEMES = {"paper": (PAPER, INK, INK_SOFT), "ink": (INK, PAPER, MIST)}
CONTACTS = ["info@flt.pt", "www.flt.pt", "aveiro, portugal"]
INTER_MEDIUM = next(p for p in [
    Path.home() / "Library/Fonts/Inter-Medium.ttf",
    Path("/Library/Fonts/Inter-Medium.ttf"),
    Path("/usr/share/fonts/truetype/inter/Inter-Medium.ttf"),
] if p.exists())

wm = (ASSETS / "wordmark" / "floating-wordmark-ink.svg").read_text()
GLYPHS = re.search(r'<g fill="#15141a">(.*)</g>\s*</svg>', wm, re.S).group(1)
VB_W, VB_H, BASELINE = 884.691, 290.391, 232.5   # the wordmark's box, and where its baseline sits in it


def banner(W, H, wm_h, gutter, line_y, gap, fs, min_gap, name, theme):
    ground, word, text = THEMES[theme]
    name = f"{name[:name.rindex('-')]}-{theme}-{name[name.rindex('-') + 1:]}"
    s = wm_h / VB_H
    wm_w = VB_W * s
    x = W - gutter - wm_w
    y = line_y - BASELINE * s          # the baseline, and so the period, rests on the line
    end = x - gap                      # the line stops short of the word
    ticks = []
    for i in range(16):                # a tick every 5 degrees over 75, a taller one every 15, as on the site
        tx = round(W * i / 15) + 0.5
        if tx > end:
            break
        major = i % 3 == 0
        ticks.append(f'<rect x="{tx - 0.5}" y="{line_y}" width="1" height="{16 if major else 8}" '
                     f'fill="{word}" fill-opacity="{0.45 if major else 0.28}"/>')
    # contacts under the word, measured in the real font, equal gaps, right edge on the word's right edge;
    # the left edge meets the word's left edge when the three fit in that width
    font = ImageFont.truetype(str(INTER_MEDIUM), fs)
    widths = [font.getlength(t) for t in CONTACTS]
    g = max(min_gap, (wm_w - sum(widths)) / (len(CONTACTS) - 1))
    cy = line_y + (VB_H - BASELINE) * s + fs * 1.6
    cx = W - gutter - (sum(widths) + g * (len(CONTACTS) - 1))
    spans = []
    for t, w in zip(CONTACTS, widths):
        spans.append(f'<text x="{cx:.1f}" y="{cy:.1f}" font-family="Inter" font-weight="500" '
                     f'font-size="{fs}" fill="{text}">{t}</text>')
        cx += w + g
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="floating. {", ".join(CONTACTS)}">\n'
           f'  <rect width="{W}" height="{H}" fill="{ground}"/>\n'
           f'  <rect x="0" y="{line_y}" width="{end:.1f}" height="1" fill="{word}" fill-opacity="0.32"/>\n'
           f'  {"".join(ticks)}\n'
           f'  <g transform="translate({x:.2f} {y:.2f}) scale({s:.5f})" fill="{word}">{GLYPHS}</g>\n'
           f'  {"".join(spans)}\n'
           f'</svg>\n')
    OUT.mkdir(parents=True, exist_ok=True)
    svg_path = OUT / f"{name}.svg"
    svg_path.write_text(svg)
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", str(OUT / f"{name}.png"), str(svg_path)], check=True)
    print(name)


for theme in THEMES:
    banner(1584, 396, 168, 96, 206, 40, 22, 36, "floating-linkedin-profile-1584x396", theme)
    banner(1128, 191, 82, 64, 98, 24, 14, 24, "floating-linkedin-company-1128x191", theme)
