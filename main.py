#!/usr/bin/env python3
"""Draw the front page of Wednesday 25 November 2026 in one image.

Writes entry.png (1024x1024) next to this file, or to $MAKEFUN_OUTPUT_DIR
when set. Deterministic: fixed text, fixed colours, no network, no clock,
no randomness. Standard library + Pillow only.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
OUT_NAME = "entry.png"

INK = (18, 18, 22)
PAPER = (250, 247, 238)
RED = (178, 34, 34)
NAVY = (24, 52, 96)
TEAL = (14, 92, 84)
AMBER = (166, 106, 0)
GREY = (96, 96, 100)
LINE = (200, 196, 186)

STORIES = [
    {
        "tag": "UKRAINE WAR",
        "color": NAVY,
        "headline": "Ukraine hits Russian ships in two seas",
        "caption": (
            "Kyiv confirms drone strikes on a Russian cargo ship in the "
            "Gulf of Finland and a warship off Benghazi, Libya. Moscow "
            "calls the attacks terrorism and vows retaliation."
        ),
        "icon": "ship",
    },
    {
        "tag": "MIDDLE EAST",
        "color": RED,
        "headline": "Houthi strike hits Riyadh's tallest tower",
        "caption": (
            "A missile strikes a tower in the King Abdullah Financial "
            "District; 11 people are wounded, Saudi civil defence says. "
            "The Houthis have pushed to within 60 km of Aden."
        ),
        "icon": "tower",
    },
    {
        "tag": "EUROPE  |  SECURITY",
        "color": TEAL,
        "headline": "NATO jets to guard Poland's skies",
        "caption": (
            "NATO approves early-warning aircraft for Poland after "
            "Russian missiles landed there during strikes on Ukraine. "
            "Europe, allies say, sits between peace and war."
        ),
        "icon": "plane",
    },
    {
        "tag": "UNITED STATES  |  CHINA",
        "color": AMBER,
        "headline": "Huawei guilty on 10 counts in US trial",
        "caption": (
            "A Brooklyn jury convicts Huawei of bank fraud, sanctions "
            "violations and stealing US trade secrets after a 12-week "
            "trial. Sentencing is set for September 2027."
        ),
        "icon": "gavel",
    },
]


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 58)
F_DATE = font("DejaVuSans-Bold.ttf", 30)
F_KICKER = font("DejaVuSans-Bold.ttf", 22)
F_HEAD = font("DejaVuSerif-Bold.ttf", 31)
F_BODY = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans-Bold.ttf", 20)


def wrap(draw, text, fnt, width):
    """Greedy word wrap: every returned line fits within `width` pixels."""
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width or not line:
                line = trial
            else:
                out.append(line)
                line = word
        if line:
            out.append(line)
    return out


def draw_ship(d, x, y, s, color):
    d.polygon([(x, y + 22 * s), (x + 150 * s, y + 22 * s),
               (x + 130 * s, y + 48 * s), (x + 20 * s, y + 48 * s)],
              fill=color)
    d.rectangle([x + 55 * s, y, x + 95 * s, y + 22 * s], fill=color)
    d.rectangle([x + 70 * s, y - 18 * s, x + 76 * s, y], fill=color)
    for i, wy in enumerate((y + 62 * s, y + 76 * s)):
        for k in range(3):
            bx = x + 10 * s + k * 50 * s
            d.arc([bx, wy, bx + 34 * s, wy + 14 * s], 180, 360, fill=color, width=3)


def draw_tower(d, x, y, s, color):
    d.rectangle([x + 55 * s, y + 10 * s, x + 95 * s, y + 90 * s], fill=color)
    d.polygon([(x + 55 * s, y + 10 * s), (x + 95 * s, y + 10 * s),
               (x + 75 * s, y - 14 * s)], fill=color)
    for row in range(5):
        for col in range(3):
            d.rectangle([x + 62 * s + col * 11 * s, y + 22 * s + row * 13 * s,
                         x + 68 * s + col * 11 * s, y + 28 * s + row * 13 * s],
                        fill=PAPER)
    cx, cy = x + 118 * s, y + 6 * s
    for ang in range(0, 360, 45):
        import math
        r1, r2 = 8 * s, 22 * s
        a = math.radians(ang)
        d.line([(cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
                (cx + r2 * math.cos(a), cy + r2 * math.sin(a))],
               fill=(214, 120, 20), width=4)
    d.ellipse([cx - 6 * s, cy - 6 * s, cx + 6 * s, cy + 6 * s],
              fill=(214, 120, 20))


def draw_plane(d, x, y, s, color):
    d.polygon([(x, y + 30 * s), (x + 150 * s, y + 30 * s),
               (x + 128 * s, y + 44 * s), (x + 22 * s, y + 44 * s)],
              fill=color)
    d.polygon([(x + 60 * s, y + 30 * s), (x + 95 * s, y + 30 * s),
               (x + 78 * s, y + 6 * s)], fill=color)
    d.polygon([(x + 55 * s, y + 44 * s), (x + 80 * s, y + 44 * s),
               (x + 62 * s, y + 62 * s)], fill=color)
    for r in (34, 52, 70):
        d.arc([x + 150 * s - r * s, y - r * s + 30 * s,
               x + 150 * s + r * s, y + r * s + 30 * s],
              -60, 60, fill=GREY, width=3)


def draw_gavel(d, x, y, s, color):
    d.rectangle([x + 20 * s, y + 8 * s, x + 130 * s, y + 30 * s], fill=color)
    d.rectangle([x + 55 * s, y + 30 * s, x + 75 * s, y + 78 * s], fill=color)
    d.rectangle([x + 30 * s, y + 78 * s, x + 100 * s, y + 88 * s], fill=color)
    d.line([(x + 10 * s, y + 96 * s), (x + 120 * s, y + 96 * s)],
           fill=color, width=4)


ICONS = {"ship": draw_ship, "tower": draw_tower,
         "plane": draw_plane, "gavel": draw_gavel}


def draw_panel(d, box, story):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255),
                outline=LINE, width=2)
    d.rectangle([x0, y0, x1, y0 + 34], fill=story["color"])
    d.text((x0 + 14, y0 + 5), story["tag"], font=F_KICKER, fill=(255, 255, 255))
    # pictogram strip
    ICONS[story["icon"]](d, x0 + 150, y0 + 58, 1.0, story["color"])
    d.line([(x0 + 14, y0 + 172), (x1 - 14, y0 + 172)], fill=LINE, width=2)
    head_lines = wrap(d, story["headline"], F_HEAD, x1 - x0 - 28)
    yy = y0 + 186
    for line in head_lines:
        d.text((x0 + 14, yy), line, font=F_HEAD, fill=INK)
        yy += 37
    yy += 6
    for line in wrap(d, story["caption"], F_BODY, x1 - x0 - 28):
        d.text((x0 + 14, yy), line, font=F_BODY, fill=(52, 52, 56))
        yy += 26


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.text((24, 18), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK)
    d.rectangle([24, 96, 1000, 100], fill=RED)
    d.text((24, 112), "WEDNESDAY  25  NOVEMBER  2026", font=F_DATE, fill=RED)
    d.text((24, 148), "Four stories that defined the day, from Kyiv to Riyadh.",
           font=F_BODY, fill=GREY)
    # 2x2 grid
    gx, gy, gap = 24, 188, 16
    pw = (W - 2 * gx - gap) // 2
    ph = 380
    for i, story in enumerate(STORIES):
        cx = gx + (i % 2) * (pw + gap)
        cy = gy + (i // 2) * (ph + gap)
        draw_panel(d, (cx, cy, cx + pw, cy + ph), story)
    # footer
    fy = gy + 2 * ph + gap + 12
    d.rectangle([24, fy, 1000, fy + 2], fill=INK)
    d.text((24, fy + 12), "WORLD NEWS  •  25 NOVEMBER 2026  •  ONE DAY, ONE IMAGE",
           font=F_FOOT, fill=INK)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if not out_dir and os.path.isdir("/output"):
        out_dir = "/output"
    if out_dir:
        path = os.path.join(out_dir, OUT_NAME)
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, OUT_NAME)
    img.save(path, format="PNG", optimize=False)
    print("wrote", path)


if __name__ == "__main__":
    main()
