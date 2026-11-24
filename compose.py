#!/usr/bin/env python3
"""news-image-20261124 — Tuesday 24 November 2026 front page, drawn in code.

Cream-paper newspaper: big serif masthead with the full date, a numbers
strip, a coloured region bar, 3 big + 10 small illustrated lead cards, a
dotted world map with numbered pins, 31 numbered one-line briefs, a
red-bordered DATE CHECK box, and a sources footer. 44 stories, 7 regions.

Deterministic: no clock, no randomness, no network. Writes entry.png
(1024x1024, RGB) next to this file. Loud-failure guards: any headline,
deck or brief that would need more lines than its box allows raises
SystemExit instead of silently dropping words, and every illustration
paints only inside its own box.
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stories import (BRIEFS, DATE_CHECK, LEADS, REGION_ORDER,
                     REGION_SHORT, SOURCES_LINE)

W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (26, 26, 26)
NAVY = (24, 42, 78)
RED = (178, 34, 34)
RED_DK = (140, 22, 22)
GREEN = (34, 139, 34)
GREEN_DK = (22, 100, 22)
GOLD = (198, 142, 32)
TEAL = (18, 110, 105)
GREY = (110, 104, 90)
LINE = (180, 170, 145)
CARD = (255, 252, 244)

REGION_COLOURS = {
    "Americas": (18, 110, 105), "Asia": (178, 34, 34),
    "Europe": (24, 42, 78), "Africa": (120, 90, 40),
    "Middle East": (198, 142, 32), "World/Global": (90, 60, 130),
    "Oceania": (30, 120, 170),
}

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def serif_b(s):
    return font("DejaVuSerif-Bold.ttf", s)


def serif(s):
    return font("DejaVuSerif.ttf", s)


def sans(s):
    return font("DejaVuSans.ttf", s)


def sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy wrap. Raises if any single word is wider than the box."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if not cur:
                raise SystemExit(
                    "WORD TOO WIDE for box (%spx): %r in %r"
                    % (max_w, word, text))
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt, max_w, max_lines, what):
    """Wrap text; FAIL LOUDLY if it needs more lines than the box allows."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        raise SystemExit(
            "OVERFLOW in %s: %d lines > %d: %r" % (what, len(lines),
                                                   max_lines, text))
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=fnt, fill=fill)
    return y + len(lines) * leading


def region_counts():
    counts = {r: 0 for r in REGION_ORDER}
    for item in LEADS + BRIEFS:
        counts[item[1]] += 1
    return counts


# ---------------------------------------------------------------- illustrations
# Flat-vector scenes drawn from simple shapes. Each takes (draw, x, y, w, h)
# and paints only inside that box. All geometry is original to this build.

def art_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 60, 40))
    # Circuit traces.
    for gy in range(y + 8, y + h - 4, 12):
        d.line([x + 4, gy, x + w - 4, gy], fill=(30, 110, 70), width=1)
    cx, cy = x + w // 2, y + h // 2
    s = min(w, h) // 3
    for k in range(-1, 2):
        d.rectangle([cx - s + k * 6, cy - s - 8, cx - s + k * 6 + 4,
                     cy - s], fill=(200, 200, 190))
        d.rectangle([cx - s + k * 6, cy + s, cx - s + k * 6 + 4,
                     cy + s + 8], fill=(200, 200, 190))
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(30, 30, 34),
                outline=(220, 220, 210), width=2)
    d.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                fill=(40, 160, 90))
    d.text((cx - 12, cy - 6), "NV", font=sans_b(11), fill=(255, 255, 255))
    d.text((x + 6, y + 3), "+31%", font=sans_b(11), fill=(120, 230, 140))


def art_awacs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 220))
    for cx in range(x + 10, x + w - 8, 34):
        d.ellipse([cx, y + h - 14, cx + 16, y + h - 6],
                  fill=(255, 255, 255))
    cy = y + h // 2
    # Fuselage, swept wings and the big radar disc on top.
    d.polygon([(x + 12, cy), (x + w - 30, cy - 6), (x + w - 8, cy),
               (x + w - 30, cy + 6)], fill=(240, 240, 238))
    d.polygon([(x + w // 2 - 8, cy - 4), (x + w // 2 + 18, cy - 16),
               (x + w // 2 + 26, cy - 14), (x + w // 2 + 6, cy - 2)],
              fill=(210, 210, 206))
    d.polygon([(x + w // 2 - 8, cy + 4), (x + w // 2 + 18, cy + 16),
               (x + w // 2 + 26, cy + 14), (x + w // 2 + 6, cy + 2)],
              fill=(210, 210, 206))
    d.ellipse([x + w // 2 - 16, cy - 16, x + w // 2 + 16, cy - 8],
              fill=(255, 255, 255), outline=(120, 120, 120), width=1)
    d.line([x + w // 2, cy - 8, x + w // 2, cy - 4], fill=(120, 120, 120),
           width=2)
    d.text((x + 6, y + 3), "AWACS", font=sans_b(10), fill=NAVY)


def art_jets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 216, 232))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(60, 120, 90))
    # Island (Ulleungdo) as a low green mound with a lighthouse dot.
    d.pieslice([x + w // 2 - 34, y + h - 22, x + w // 2 + 34, y + h + 6],
               180, 360, fill=(50, 110, 70))
    d.rectangle([x + w // 2 - 2, y + h - 26, x + w // 2 + 2, y + h - 16],
                fill=(255, 255, 255))
    # Two jet silhouettes crossing the sky.
    for jx, jy, s in [(x + 18, y + 10, 1.0), (x + w - 52, y + 22, 0.8)]:
        d.polygon([(jx, jy + 6), (jx + int(34 * s), jy),
                   (jx + int(40 * s), jy + 6), (jx + int(34 * s), jy + 10)],
                  fill=(60, 60, 70))
        d.polygon([(jx + int(14 * s), jy + 4), (jx + int(22 * s), jy - 4),
                   (jx + int(26 * s), jy - 2), (jx + int(20 * s), jy + 6)],
                  fill=(60, 60, 70))
    # Red alert triangle.
    tx, ty = x + w - 26, y + 4
    d.polygon([(tx, ty + 12), (tx + 12, ty), (tx + 24, ty + 12)],
              fill=RED)
    d.text((tx + 10, ty + 2), "!", font=sans_b(9), fill=(255, 255, 255))


def art_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 180))
    roof = min(14, h // 3)
    base = y + h - 6
    top = base - 20
    d.rectangle([x + 10, top, x + w - 10, base], fill=(120, 116, 104))
    d.polygon([(x + 10, top), (x + 30, top - roof), (x + 50, top),
               (x + 70, top - roof), (x + 90, top), (x + w - 10, top)],
              fill=(90, 86, 76))
    if h >= 44:
        d.rectangle([x + w - 26, y + 10, x + w - 16, top],
                    fill=(140, 130, 116))
    fh = min(22, h // 2)
    for fx in (x + 26, x + 46, x + 66):
        d.polygon([(fx - 8, top), (fx, top - fh), (fx + 8, top)],
                  fill=(255, 140, 30))
        d.polygon([(fx - 4, top), (fx, top - fh + 8), (fx + 4, top)],
                  fill=(255, 200, 60))
    for sx, sy, sr in [(x + 40, y + 8, 6), (x + 56, y + 14, 8),
                       (x + 70, y + 8, 5)]:
        if sy - sr >= y:
            d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                      fill=(110, 108, 102))


def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(34, 110, 60))
    for i in range(max(1, (h - 12) // 14)):
        yy = y + 6 + i * 14
        d.line([x + 6, yy, x + w - 6, yy], fill=(255, 255, 255), width=1)
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], outline=(255, 255, 255),
                width=2)
    d.line([x + 10, y + h // 2, x + w - 10, y + h // 2],
           fill=(255, 255, 255), width=2)
    d.rectangle([x + w // 2 - 22, y + 10, x + w // 2 - 12, y + h - 22],
                fill=(220, 180, 120))
    d.rectangle([x + w // 2 - 20, y + 6, x + w // 2 - 14, y + 10],
                fill=(120, 80, 40))
    d.ellipse([x + w // 2 + 8, y + h // 2 - 7, x + w // 2 + 22, y + h // 2 + 7],
              fill=(200, 40, 40))
    for sx in (x + w - 26, x + w - 20, x + w - 14):
        d.rectangle([sx, y + h - 18, sx + 3, y + h - 8], fill=(255, 220, 90))
    d.rectangle([x + 12, y + h - 14, x + 52, y + h - 1], fill=(34, 110, 60))
    d.text((x + 14, y + h - 13), "720/9", font=sans_b(9), fill=(255, 255, 255))

def art_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 222, 240))
    for cx in range(x + 8, x + w - 4, 22):
        d.ellipse([cx, y + 8, cx + 4, y + 12], fill=(255, 255, 255))
    # India tricolour, left; Nepal crimson pennant, right.
    d.rectangle([x + 10, y + 16, x + 58, y + 22], fill=(255, 153, 51))
    d.rectangle([x + 10, y + 22, x + 58, y + 28], fill=(255, 255, 255))
    d.rectangle([x + 10, y + 28, x + 58, y + 34], fill=(19, 136, 8))
    d.ellipse([x + 30, y + 22, x + 38, y + 30], outline=NAVY, width=1)
    d.polygon([(x + w - 58, y + 16), (x + w - 10, y + 16),
               (x + w - 10, y + 34), (x + w - 58, y + 34)],
              fill=(220, 20, 60))
    d.polygon([(x + w - 58, y + 16), (x + w - 34, y + 16),
               (x + w - 58, y + 28)], fill=(220, 20, 60))
    # Handshake: two clasped hands as interlocked arcs.
    d.ellipse([x + w // 2 - 16, y + h - 26, x + w // 2 + 16, y + h - 6],
              fill=(240, 200, 160))
    d.line([x + w // 2 - 12, y + h - 16, x + w // 2 + 12, y + h - 16],
           fill=(180, 120, 80), width=2)


def art_talks(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 208))
    # Four chairs around a round table: four flags, one table.
    cx, cy = x + w // 2, y + h // 2 + 4
    d.ellipse([cx - 30, cy - 12, cx + 30, cy + 12], fill=(120, 70, 40))
    d.ellipse([cx - 30, cy - 12, cx + 30, cy + 4], fill=(150, 95, 55))
    for fx, fy, col in [(cx - 38, cy - 22, (0, 90, 180)),
                        (cx + 26, cy - 22, (255, 210, 0)),
                        (cx - 38, cy + 12, (220, 40, 40)),
                        (cx + 26, cy + 12, (30, 120, 60))]:
        d.rectangle([fx, fy, fx + 12, fy + 8], fill=col,
                    outline=(255, 255, 255), width=1)
    d.text((x + 6, y + 3), "4-WAY", font=sans_b(10), fill=NAVY)


def art_blast(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 38, 52))
    # Governor's office facade, windows lit, blast star at the door.
    d.rectangle([x + 14, y + 10, x + w - 14, y + h - 6], fill=(150, 140, 125))
    for fy in range(y + 16, y + h - 10, 12):
        for fx in (x + 20, x + 34, x + 48):
            d.rectangle([fx, fy, fx + 8, fy + 7], fill=(255, 220, 120))
    cx, cy = x + w // 2, y + h - 14
    rstar = 9 if h < 44 else 16
    for k in range(8):
        a = math.pi * 2 * k / 8
        d.line([cx, cy, cx + int(rstar * math.cos(a)),
                cy + int(rstar * math.sin(a))], fill=(255, 180, 40), width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 220, 90))
    for sx, sy, sr in [(x + 30, y + 6, 6), (x + 46, y + 12, 8)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 108, 102))


def art_picket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 226, 232))
    # Factory silhouette behind, picket signs in front.
    d.rectangle([x + 8, y + h - 22, x + w - 8, y + h - 4], fill=(90, 90, 96))
    d.rectangle([x + w - 30, y + 8, x + w - 20, y + h - 22],
                fill=(120, 120, 126))
    for sx in (x + 16, x + 44, x + 72):
        d.line([sx + 6, y + 12, sx + 6, y + h - 8], fill=(120, 90, 60),
               width=2)
        d.rectangle([sx, y + 6, sx + 14, y + 18], fill=(255, 255, 255),
                    outline=RED, width=1)
        d.text((sx + 3, y + 8), "5%", font=sans_b(8), fill=RED_DK)


def art_jet(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 220))
    for cx in range(x + 10, x + w - 8, 34):
        d.ellipse([cx, y + h - 14, cx + 16, y + h - 6],
                  fill=(255, 255, 255))
    # F-35 top view: delta body, swept wings, twin tail.
    cx, cy = x + w // 2, y + h // 2
    d.polygon([(cx - 34, cy - 4), (cx + 34, cy - 8), (cx + 40, cy),
               (cx + 34, cy + 8), (cx - 34, cy + 4)], fill=(90, 95, 105))
    d.polygon([(cx - 6, cy - 4), (cx + 8, cy - 20), (cx + 16, cy - 18),
               (cx + 6, cy - 2)], fill=(70, 75, 85))
    d.polygon([(cx - 6, cy + 4), (cx + 8, cy + 20), (cx + 16, cy + 18),
               (cx + 6, cy + 2)], fill=(70, 75, 85))
    d.polygon([(cx - 34, cy - 6), (cx - 26, cy - 12), (cx - 20, cy - 4)],
              fill=(70, 75, 85))
    d.polygon([(cx - 34, cy + 6), (cx - 26, cy + 12), (cx - 20, cy + 4)],
              fill=(70, 75, 85))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(200, 210, 220))
    d.text((x + 6, y + 3), "41.9%", font=sans_b(10), fill=NAVY)


def art_ban(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 236, 224))
    cx, cy = x + w // 2, y + h // 2
    s = min(w, h) // 3
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(30, 30, 34),
                outline=(120, 120, 115), width=2)
    d.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                fill=(40, 160, 90))
    r = min(w, h) // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=4)
    d.line([cx - r + 4, cy + r - 4, cx + r - 4, cy - r + 4], fill=RED,
           width=4)


def art_flats(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 38, 52))
    for sx in range(x + 8, x + w - 6, 20):
        d.ellipse([sx, y + 6, sx + 2, y + 8], fill=(255, 255, 255))
    # Five-storey block, one corner blown out.
    d.rectangle([x + 14, y + 12, x + w - 14, y + h - 6], fill=(150, 140, 125))
    for fy in range(y + 18, y + h - 10, 12):
        for fx in (x + 20, x + 34, x + 48):
            d.rectangle([fx, fy, fx + 8, fy + 7], fill=(255, 220, 120))
    d.polygon([(x + w - 14, y + 12), (x + w - 14, y + 34),
               (x + w - 34, y + 12)], fill=(30, 28, 40))
    d.polygon([(x + w - 40, y + 12), (x + w - 14, y + 12),
               (x + w - 30, y + 30)], fill=(200, 120, 60))
    d.polygon([(x + 8, y + 6), (x + 22, y + 6), (x + 15, y + 14)],
              fill=(255, 90, 40))
    d.text((x + 8, y + h - 12), "DYMER", font=sans_b(8), fill=(255, 255, 255))


def art_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 220))
    for cx in range(x + 10, x + w - 8, 34):
        d.ellipse([cx, y + 6, cx + 16, y + 12], fill=(255, 255, 255))
    d.rectangle([x, y + h - 10, x + w, y + h - 4], fill=(70, 70, 78))
    cy = y + h // 2 - 4
    d.polygon([(x + 12, cy), (x + w - 30, cy - 6), (x + w - 8, cy),
               (x + w - 30, cy + 6)], fill=(240, 240, 238))
    d.polygon([(x + w // 2 - 8, cy - 4), (x + w // 2 + 18, cy - 16),
               (x + w // 2 + 26, cy - 14), (x + w // 2 + 6, cy - 2)],
              fill=(210, 210, 206))
    d.ellipse([x + w // 2 - 10, cy - 12, x + w // 2 + 10, cy - 4],
              fill=(255, 255, 255), outline=(120, 120, 120), width=1)
    d.rectangle([x + 6, y + h - 22, x + 52, y + h - 12], fill=RED)
    d.text((x + 8, y + h - 21), "DEC 16", font=sans_b(9),
           fill=(255, 255, 255))


ART = {"chip": art_chip, "awacs": art_awacs, "jets": art_jets,
       "fire": art_fire, "cricket": art_cricket, "flags": art_flags,
       "talks": art_talks, "blast": art_blast, "picket": art_picket,
       "jet": art_jet, "ban": art_ban, "flats": art_flats,
       "plane": art_plane}

# ---------------------------------------------------------------- world map
# Coarse land grid as column ranges per row (60 cols x 24 rows, equirect
# angles: lon -180..180, lat 75..-55). Built from ranges, not typed art,
# so no row can be miscounted.
LAND_RANGES = {
    0: [(3, 16), (28, 52)], 1: [(2, 17), (27, 55)],
    2: [(3, 18), (26, 56)], 3: [(4, 19), (25, 57)],
    4: [(5, 19), (27, 38), (40, 56)], 5: [(6, 20), (27, 37), (40, 55)],
    6: [(7, 21), (28, 36), (41, 54)],
    7: [(8, 21), (28, 38), (39, 43), (45, 53)],
    8: [(9, 20), (29, 39), (40, 43), (45, 48), (50, 53)],
    9: [(10, 16), (30, 40), (46, 48), (50, 53)],
    10: [(11, 15), (30, 40), (46, 47), (51, 54)],
    11: [(12, 15), (31, 40), (52, 55)], 12: [(13, 17), (31, 40), (52, 56)],
    13: [(13, 18), (32, 39), (44, 51), (53, 57)],
    14: [(14, 18), (32, 38), (45, 51), (54, 58)],
    15: [(14, 18), (32, 37), (46, 50), (54, 58)],
    16: [(15, 18), (33, 37), (47, 50), (53, 59)],
    17: [(15, 18), (33, 36), (53, 58)], 18: [(15, 17), (33, 36), (54, 58)],
    19: [(16, 17), (34, 35), (55, 58)], 20: [(16, 16), (55, 57), (59, 59)],
    21: [(16, 16), (59, 59)], 22: [(16, 16)], 23: [(16, 16)],
}

# (lead num, lon, lat) — approximate places for the 13 leads.
PINS = {
    1: (-122, 37), 2: (21, 52), 3: (131, 37), 4: (106, -6),
    5: (175, -41), 6: (77, 28), 7: (13, 52), 8: (-73, 4),
    9: (10, 53), 10: (-77, 39), 11: (104, 1), 12: (30, 51),
    13: (90, 24),
}

MAP_PLACES = {1: "Santa Clara (Nvidia)", 2: "Warsaw", 3: "Ulleungdo",
              4: "Cikande", 5: "Wellington", 6: "New Delhi",
              7: "Berlin", 8: "Villavicencio", 9: "Hamburg",
              10: "Washington DC", 11: "Singapore", 12: "Dymer",
              13: "Dhaka"}


def map_xy(mx, my, mw, mh, lon, lat):
    fx = (lon + 180.0) / 360.0
    fy = (75.0 - lat) / 130.0
    return mx + fx * mw, my + fy * mh


def land_dots(mx, my, mw, mh):
    dots = []
    for r, ranges in LAND_RANGES.items():
        for c0, c1 in ranges:
            for c in range(c0, c1 + 1):
                dots.append((mx + (c + 0.5) * mw / 60.0,
                             my + (r + 0.5) * mh / 24.0))
    return dots


def nearest_land(dots, px, py):
    best, bd = None, 1e9
    for dx, dy in dots:
        dd = (dx - px) ** 2 + (dy - py) ** 2
        if dd < bd:
            best, bd = (dx, dy), dd
    return best, bd ** 0.5


def paint_map(d, mx, my, mw, mh):
    d.rectangle([mx, my, mx + mw, my + mh], fill=(228, 236, 240))
    d.rectangle([mx, my, mx + mw, my + mh], outline=NAVY, width=2)
    dots = land_dots(mx, my, mw, mh)
    for dx, dy in dots:
        d.ellipse([dx - 1.6, dy - 1.6, dx + 1.6, dy + 1.6], fill=(90, 110, 95))
    placed = {}
    for num, (lon, lat) in PINS.items():
        px, py = map_xy(mx, my, mw, mh, lon, lat)
        (lx, ly), dist = nearest_land(dots, px, py)
        if dist > 14:
            raise SystemExit("MAP PIN %d too far from land: %.1fpx"
                             % (num, dist))
        # Keep the disc fully inside the map: a true spot near an edge
        # (Wellington) is pulled in and joined with a leader line.
        tx = min(max(lx, mx + 9), mx + mw - 9)
        ty = min(max(ly, my + 9), my + mh - 9)
        moved = (tx, ty) != (lx, ly)
        if any(((tx - ox) ** 2 + (ty - oy) ** 2) ** 0.5 < 19
               for ox, oy in placed.values()):
            found = None
            for radius in (13, 17, 21, 25, 29):
                for k in range(12):
                    a = math.pi * 2 * k / 12
                    cx, cy = lx + radius * math.cos(a), ly + radius * math.sin(a)
                    if not (mx + 9 <= cx <= mx + mw - 9
                            and my + 9 <= cy <= my + mh - 9):
                        continue
                    if all(((cx - ox) ** 2 + (cy - oy) ** 2) ** 0.5 >= 19
                           for ox, oy in placed.values()):
                        found = (cx, cy)
                        break
                if found:
                    break
            if not found:
                raise SystemExit("MAP PIN %d: no free disc spot near land"
                                 % num)
            tx, ty = found
            moved = True
        if moved:
            d.line([lx, ly, tx, ty], fill=RED, width=1)
            d.ellipse([lx - 2, ly - 2, lx + 2, ly + 2], fill=RED)
        placed[num] = (tx, ty)
        d.ellipse([tx - 8, ty - 8, tx + 8, ty + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((tx - 3, ty - 6), str(num), font=sans_b(8),
               fill=(255, 255, 255))
    return placed


# ---------------------------------------------------------------- page layout
MARGIN = 12
CONTENT_W = W - 2 * MARGIN


def paint_header(d):
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((MARGIN, 5), "ONE DAY, EVERYWHERE", font=sans_b(13),
           fill=(255, 255, 255))
    right = "TUESDAY EDITION  \u2022  No. 328"
    d.text((W - MARGIN - d.textlength(right, font=sans_b(11)), 7), right,
           font=sans_b(11), fill=(200, 200, 200))
    mast = "Tuesday 24 November 2026"
    f = serif_b(54)
    d.text(((W - d.textlength(mast, font=f)) / 2, 30), mast, font=f, fill=INK)
    d.line([MARGIN, 92, W - MARGIN, 92], fill=INK, width=2)
    sub = ("Huang returns to Nvidia, +31% (Mon)  \u2022  NATO sends AWACS "
           "to Poland (Mon)  \u2022  Russian jets spark shelter alert off "
           "Ulleungdo")
    f2 = serif(15)
    d.text(((W - d.textlength(sub, font=f2)) / 2, 98), sub, font=f2,
           fill=(60, 60, 60))
    strip = "44 STORIES  \u2022  7 REGIONS  \u2022  13 ILLUSTRATED"
    f3 = sans_b(14)
    d.text(((W - d.textlength(strip, font=f3)) / 2, 120), strip, font=f3,
           fill=RED_DK)
    d.line([MARGIN, 140, W - MARGIN, 140], fill=LINE, width=1)


def paint_numbers(d):
    cells = [
        ("+31%", "Nvidia shares, Monday"),
        ("AWACS", "deployed to Poland"),
        ("26", "confirmed dead, Cikande fire"),
        ("24,000 cr", "Nepal aid package (NPR)"),
        ("11", "killed in Dymer, Kyiv region"),
        ("Nikkei +3.9%", "Tue: Nvidia -5% pre-market"),
    ]
    y0, y1 = 146, 194
    cw = CONTENT_W / 6.0
    for i, (big, small) in enumerate(cells):
        x = MARGIN + i * cw
        if i:
            d.line([x, y0 + 4, x, y1 - 4], fill=LINE, width=1)
        fb = sans_b(19)
        d.text((x + (cw - d.textlength(big, font=fb)) / 2, y0 + 2), big,
               font=fb, fill=RED_DK)
        fs = sans(10)
        d.text((x + (cw - d.textlength(small, font=fs)) / 2, y0 + 27), small,
               font=fs, fill=(70, 70, 70))
    d.line([MARGIN, y1, W - MARGIN, y1], fill=LINE, width=1)


def paint_region_bar(d, counts):
    y0, y1 = 200, 224
    total = sum(counts.values())
    widths = {r: CONTENT_W * counts[r] / total for r in REGION_ORDER}
    # Minimum segment width so the smallest label ("Oceania 1", ~50px at
    # 9px bold) fits; the deficit comes off the largest segment.
    min_w = 56.0
    for r in REGION_ORDER:
        if widths[r] < min_w:
            widths[max(widths, key=lambda k: widths[k])] -= min_w - widths[r]
            widths[r] = min_w
    x = MARGIN
    for region in REGION_ORDER:
        n = counts[region]
        seg = widths[region]
        d.rectangle([x, y0, x + seg, y1], fill=REGION_COLOURS[region])
        label = "%s %d" % (REGION_SHORT.get(region, region), n)
        f = sans_b(9)
        tw = d.textlength(label, font=f)
        if tw <= seg - 2:
            d.text((x + (seg - tw) / 2, y0 + 7), label, font=f,
                   fill=(255, 255, 255))
        else:
            # Segment too narrow for its name: draw the count only; the
            # full counts line runs in the footer.
            d.text((x + (seg - 6) / 2, y0 + 7), str(n), font=f,
                   fill=(255, 255, 255))
        x += seg
    d.rectangle([MARGIN, y0, W - MARGIN, y1], outline=INK, width=1)


def paint_lead_card(d, item, x, y, w, h, big):
    x, y, w, h = int(x), int(y), int(w), int(h)
    num, region, field, tag, headline, deck, source, art = item
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    art_h = 88 if big else 34
    ART[art](d, x + 1, y + 1, w - 2, art_h)
    tag_f = sans_b(10 if big else 8)
    tw = d.textlength(tag, font=tag_f)
    d.rectangle([x + 6, y + art_h + 5, x + 10 + tw, y + art_h + 20],
                fill=REGION_COLOURS[region])
    d.text((x + 8, y + art_h + 6), tag, font=tag_f, fill=(255, 255, 255))
    d.ellipse([x + w - 24, y + art_h + 4, x + w - 6, y + art_h + 22], fill=RED)
    d.text((x + w - 19, y + art_h + 7), str(num), font=sans_b(10),
           fill=(255, 255, 255))
    hy = y + art_h + 24
    hf = serif_b(19 if big else 13)
    hl = fit(d, headline, hf, w - 12, 2, "lead %d headline" % num)
    lead = 21 if big else 14
    draw_lines(d, hl, x + 6, hy, hf, INK, lead)
    dy = hy + len(hl) * lead + 1
    df = sans(11 if big else 9)
    dl = fit(d, deck, df, w - 12, 2, "lead %d deck" % num)
    dlead = 11 if big else 10
    draw_lines(d, dl, x + 6, dy, df, (60, 60, 60), dlead)
    if dy + len(dl) * dlead > y + h - 13:
        raise SystemExit("OVERFLOW in lead %d: deck runs into source line"
                         % num)
    sf = sans(8 if big else 7)
    d.text((x + 6, y + h - 11), source.upper(), font=sf, fill=GREY)


def paint_leads(d):
    y0 = 230
    big_w, big_h = 322, 196
    gap = (CONTENT_W - 3 * big_w) / 2.0
    for i, item in enumerate(LEADS[:3]):
        paint_lead_card(d, item, MARGIN + i * (big_w + gap), y0, big_w, big_h,
                        True)
    small_w, small_h = 192, 122
    sgap = (CONTENT_W - 5 * small_w) / 4.0
    for row in range(2):
        for col in range(5):
            item = LEADS[3 + row * 5 + col]
            paint_lead_card(d, item, MARGIN + col * (small_w + sgap),
                            y0 + big_h + 6 + row * (small_h + 6),
                            small_w, small_h, False)


def paint_briefs(d, bx, by, bw, bh):
    d.text((bx, by), "ALSO ON THIS PAGE", font=sans_b(12), fill=NAVY)
    d.line([bx, by + 16, bx + bw, by + 16], fill=NAVY, width=2)
    col_w = (bw - 14) / 2.0
    per_col = 16
    df = sans(8)
    row_h = 10.5
    for idx, item in enumerate(BRIEFS):
        num, region, field, text = item
        col = idx // per_col
        row = idx % per_col
        x = bx + col * (col_w + 14)
        y = by + 20 + row * row_h
        if y + 10 > by + bh:
            raise SystemExit("BRIEFS overflow at item %d" % num)
        d.text((x, y), "%d." % num, font=sans_b(8), fill=RED_DK)
        lines = fit(d, text, df, col_w - 18, 1, "brief %d" % num)
        d.text((x + 18, y), lines[0], font=df, fill=INK)


def paint_date_check(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    d.text((x + 8, y + 4), "DATE CHECK \u2014 NOT 24 NOVEMBER NEWS",
           font=sans_b(11), fill=RED_DK)
    f = sans(9)
    yy = y + 21
    for name, when in DATE_CHECK:
        d.text((x + 8, yy), "X  %s \u2014 %s" % (name, when), font=f, fill=INK)
        yy += 11


def paint_footer(d, y):
    d.line([MARGIN, y, W - MARGIN, y], fill=LINE, width=1)
    d.text((MARGIN, y + 4),
           "Tuesday 24 November 2026 \u2014 today's biggest stories plus "
           "the weekend's developments; earlier events are dated in the deck.",
           font=sans(10), fill=INK)
    d.text((MARGIN, y + 16), SOURCES_LINE, font=sans(9), fill=(70, 70, 70))
    d.text((MARGIN, y + 28),
           "Regions: Americas 10 \u00b7 Asia 10 \u00b7 Europe 9 \u00b7 Africa 6 \u00b7 "
           "Middle East 5 \u00b7 World/Global 3 \u00b7 Oceania 1 \u2014 Original "
           "flat-vector drawings, no photographs.",
           font=sans_b(9), fill=(70, 70, 70))
    d.text((MARGIN, y + 40),
           "Map: 1 Santa Clara \u00b7 2 Warsaw \u00b7 3 Ulleungdo \u00b7 4 Cikande "
           "\u00b7 5 Wellington \u00b7 6 New Delhi \u00b7 7 Berlin \u00b7 8 "
           "Villavicencio \u00b7 9 Hamburg \u00b7 10 Washington DC \u00b7 11 "
           "Singapore \u00b7 12 Dymer \u00b7 13 Dhaka.",
           font=sans(9), fill=(70, 70, 70))


def build():
    counts = region_counts()
    assert sum(counts.values()) == 44, counts
    assert len(counts) == 7, counts
    assert len(LEADS) == 13 and len(BRIEFS) == 31
    assert [i[0] for i in LEADS] == list(range(1, 14))
    assert [i[0] for i in BRIEFS] == list(range(14, 45))
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    paint_header(d)
    paint_numbers(d)
    paint_region_bar(d, counts)
    paint_leads(d)
    # Bottom band: map left, briefs right.
    by = 688
    d.text((MARGIN, by), "WHERE IT HAPPENED", font=sans_b(12), fill=NAVY)
    d.line([MARGIN, by + 16, MARGIN + 470, by + 16], fill=NAVY, width=2)
    paint_map(d, MARGIN, by + 22, 470, 124)
    d.text((MARGIN, by + 152),
           "Pins 1-13 = the illustrated leads above.",
           font=sans(9), fill=(70, 70, 70))
    paint_briefs(d, MARGIN + 486, by, CONTENT_W - 486, 190)
    paint_date_check(d, MARGIN, 850, 470, 102)
    paint_footer(d, 962)
    return img


def main():
    img = build()
    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print("wrote %s %d bytes" % (out, out.stat().st_size))


if __name__ == "__main__":
    main()
