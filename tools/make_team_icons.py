#!/usr/bin/env python3
"""Make a team's app icons and splash background from its settings file.

    python3 tools/make_team_icons.py wmu      # writes wmu/icons/*

Original artwork in the style of the Spartans Tracker icon: two-letter monogram in a
ring with a heartbeat line, in the team's colors. No school logos are used.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def logo(size, bg, fg, letters):
    S = 1024  # draw large, then scale down for clean edges
    im = Image.new("RGB", (S, S), bg)
    d = ImageDraw.Draw(im)
    ring = 34
    d.ellipse([110, 110, S - 110, S - 110], outline=fg, width=ring)
    # slanted monogram
    font = ImageFont.truetype(FONT, 350)
    layer = Image.new("L", (S, S), 0)
    ld = ImageDraw.Draw(layer)
    w = ld.textlength(letters, font=font)
    ld.text(((S - w) / 2 - 25, 290), letters, font=font, fill=255)
    layer = layer.transform((S, S), Image.AFFINE, (1, 0.2, -95, 0, 1, 0), resample=Image.BICUBIC)
    im.paste(Image.new("RGB", (S, S), fg), (0, 0), layer)
    # heartbeat line
    y = 760
    pts = [(300, y), (430, y), (465, y - 60), (510, y + 50), (545, y - 25), (575, y), (725, y)]
    d.line(pts, fill=fg, width=26, joint="curve")
    return im.resize((size, size), Image.LANCZOS)


def splash(bg_dark, bg, accent, out):
    W, H = 1080, 1500
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    top, mid = hex_rgb(bg_dark), hex_rgb(bg)
    for y in range(H):  # night sky fading into team color
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] * 0.45 + (mid[i] - top[i] * 0.45) * t) for i in range(3)))
    fy = int(H * 0.80)  # field
    for y in range(fy, H):
        t = (y - fy) / (H - fy)
        d.line([(0, y), (W, y)], fill=(int(30 + 12 * t), int(70 + 25 * t), int(36 + 10 * t)))
    for i in range(-6, 7):
        d.line([(W / 2 + i * 60, fy), (W / 2 + i * 260, H)], fill=(70, 120, 76), width=3)
    d.line([(0, fy), (W, fy)], fill=hex_rgb(accent), width=4)
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    for cx in (130, W - 130):  # stadium lights
        gd.ellipse([cx - 150, -10, cx + 150, 290], fill=110)
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    im = Image.composite(Image.new("RGB", (W, H), (255, 236, 180)), im, glow)
    im.save(out, quality=85, optimize=True)


def main(slug):
    with open(os.path.join(ROOT, "teams", f"{slug}.json"), encoding="utf-8") as f:
        team = json.load(f)
    c = team["colors"]
    bg, fg = hex_rgb(c["primary"]), hex_rgb(c["accent"])
    letters = team.get("monogram", team["nick"][0] + "T")
    out = os.path.join(ROOT, slug, "icons")
    os.makedirs(out, exist_ok=True)
    for size, name in [(192, "icon-192.png"), (512, "icon-512.png"), (180, "apple-touch-icon.png")]:
        logo(size, bg, fg, letters).save(os.path.join(out, name), optimize=True)
    # maskable: logo inset on a solid background so phones can crop it to any shape
    m = Image.new("RGB", (512, 512), bg)
    m.paste(logo(400, bg, fg, letters), (56, 56))
    m.save(os.path.join(out, "icon-maskable-512.png"), optimize=True)
    splash(c["primaryDark"], c["primary"], c["accent"], os.path.join(out, "splash.jpg"))
    print(f"Wrote {slug}/icons")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "wmu")
