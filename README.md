# floating.

brand identity for floating point. engineering solutions company.

## live

- brand guidelines: `/index.html`
- email signature options: `/email-signatures.html`

## assets

- `assets/floating.svg` — static logo, paths outlined, no font dependency
- `assets/floating.mp4` — pixar-style bounce, 1600 × 600, h.264, 60fps
- `assets/floating.gif` — same animation, gif format
- `assets/wordmark/` — wordmark in ink soft, ink and paper, svg + png at 800, 1600, 3200 wide
- `assets/point/` — the point on its own, plus round avatar and sticker marks, svg + png at 256, 512, 1024
- `assets/icon/` — app icons (paper, ink) and favicons (svg, ico, png 16 to 180)
- `assets/banner/` — linkedin banners on paper and on ink, profile 1584 × 396 and company page 1128 × 191, png at 1x and 2x + svg
- `assets/floating-brand-assets.zip` — all of the above in one file

every file is linked from the downloads section of `/index.html`. to rebuild them after
changing `assets/floating.svg`, run `python3 scripts/build-assets.py` (needs `rsvg-convert` and pillow).
the banners are built by `python3 scripts/build-banners.py`, which also needs inter installed as a system font.

## type

inter (regular / medium / semibold) for the wordmark and copy.
jetbrains mono (regular) for utility, captions, technical metadata.
both fonts are embedded as base64 woff2, no external requests at runtime.

## colors

paper `#f5f3ee` · mist `#e8e5dd` · fog `#9a9a9e` · ink soft `#2a2730` · ink `#15141a`

## contact

daniel ferreira · co-founder · daniel@floatingpoint.pt
