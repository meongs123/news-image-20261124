#!/usr/bin/env python3
"""Tuesday 24 November 2026 front page for news-image-20261124, painted in code.

A cream-paper newspaper: a large serif masthead carrying the full date,
a strip of headline numbers, a coloured region bar, three large plus ten
small illustrated lead cards, a dotted world map carrying numbered pins,
thirty-one numbered one-line briefs, a red-bordered DATE CHECK box, and a
sources footer. Forty-four stories across seven regions.

Fully deterministic: no clock reads, no randomness, no network access.
Running this file writes entry.png (1024 by 1024, RGB) beside itself.
Loud-failure guards: a headline, deck or brief that would need more
lines than its box allows aborts with SystemExit instead of silently
dropping words, and every illustration paints only inside its own box.
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

# One fill colour per region, shared by the region bar and the lead tags.
REGION_COLOURS = {
    "Americas": (18, 110, 105),
    "Asia": (178, 34, 34),
    "Europe": (24, 42, 78),
    "Africa": (120, 90, 40),
    "Middle East": (198, 142, 32),
    "World/Global": (90, 60, 130),
    "Oceania": (30, 120, 170),
}

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def load_font(filename, size):
    """Load one DejaVu face from the system font directory at a size."""
    return ImageFont.truetype(str(FONT_DIR / filename), size)


def serif_b(size):
    """Bold serif face, used for the masthead and lead headlines."""
    return load_font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    """Regular serif face, used for the sub-headline under the masthead."""
    return load_font("DejaVuSerif.ttf", size)


def sans(size):
    """Regular sans face, used for decks, briefs and footer text."""
    return load_font("DejaVuSans.ttf", size)


def sans_b(size):
    """Bold sans face, used for labels, tags, numbers and pin digits."""
    return load_font("DejaVuSans-Bold.ttf", size)


def wrap(canvas, text, face, max_w):
    """Greedy word wrap. Aborts if one word alone is wider than the box."""
    words = text.split()
    wrapped, current = [], ""
    for word in words:
        candidate = (current + " " + word).strip()
        if canvas.textlength(candidate, font=face) <= max_w:
            current = candidate
        elif current == "":
            raise SystemExit(
                "WORD TOO WIDE for box (%spx): %r in %r"
                % (max_w, word, text))
        else:
            wrapped.append(current)
            current = word
    if current:
        wrapped.append(current)
    return wrapped


def fit(canvas, text, face, max_w, max_lines, what):
    """Wrap text; FAIL LOUDLY when it needs more lines than the box allows."""
    wrapped = wrap(canvas, text, face, max_w)
    if len(wrapped) > max_lines:
        raise SystemExit(
            "OVERFLOW in %s: %d lines > %d: %r" % (what, len(wrapped),
                                                   max_lines, text))
    return wrapped


def draw_lines(canvas, lines, x, y, face, fill, leading):
    """Draw wrapped lines top to bottom; return the y just below the last."""
    cursor = y
    for line in lines:
        canvas.text((x, cursor), line, font=face, fill=fill)
        cursor += leading
    return cursor


def region_counts():
    """Count lead plus brief stories per region, in canonical region order."""
    tally = {region: 0 for region in REGION_ORDER}
    for story in LEADS + BRIEFS:
        tally[story[1]] += 1
    return tally


# ---------------------------------------------------------------- illustrations
# Flat-vector scenes built from simple shapes. Every scene takes a drawing
# canvas plus a box (left, top, width, height) and paints only inside
# that box. All of the geometry below is original to this build.

def art_chip(pen, left, top, wide, tall):
    """Nvidia chip on a dark green circuit board, with a +31% tag."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(16, 60, 40))
    # Horizontal circuit traces running across the board.
    trace_y = top + 8
    while trace_y < top + tall - 4:
        pen.line([left + 4, trace_y, left + wide - 4, trace_y],
                 fill=(30, 110, 70), width=1)
        trace_y += 12
    centre_x, centre_y = left + wide // 2, top + tall // 2
    half = min(wide, tall) // 3
    for offset in (-1, 0, 1):
        pen.rectangle([centre_x - half + offset * 6, centre_y - half - 8,
                       centre_x - half + offset * 6 + 4, centre_y - half],
                      fill=(200, 200, 190))
        pen.rectangle([centre_x - half + offset * 6, centre_y + half,
                       centre_x - half + offset * 6 + 4,
                       centre_y + half + 8], fill=(200, 200, 190))
    pen.rectangle([centre_x - half, centre_y - half,
                   centre_x + half, centre_y + half], fill=(30, 30, 34),
                  outline=(220, 220, 210), width=2)
    pen.rectangle([centre_x - half // 2, centre_y - half // 2,
                   centre_x + half // 2, centre_y + half // 2],
                  fill=(40, 160, 90))
    pen.text((centre_x - 12, centre_y - 6), "NV", font=sans_b(11),
             fill=(255, 255, 255))
    pen.text((left + 6, top + 3), "+31%", font=sans_b(11),
             fill=(120, 230, 140))


def art_awacs(pen, left, top, wide, tall):
    """AWACS surveillance plane in a pale sky, radar disc on its back."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(150, 190, 220))
    cloud_x = left + 10
    while cloud_x < left + wide - 8:
        pen.ellipse([cloud_x, top + tall - 14, cloud_x + 16, top + tall - 6],
                    fill=(255, 255, 255))
        cloud_x += 34
    mid_y = top + tall // 2
    # Fuselage, swept wings and the big radar disc on top.
    pen.polygon([(left + 12, mid_y), (left + wide - 30, mid_y - 6),
                 (left + wide - 8, mid_y), (left + wide - 30, mid_y + 6)],
                fill=(240, 240, 238))
    pen.polygon([(left + wide // 2 - 8, mid_y - 4),
                 (left + wide // 2 + 18, mid_y - 16),
                 (left + wide // 2 + 26, mid_y - 14),
                 (left + wide // 2 + 6, mid_y - 2)], fill=(210, 210, 206))
    pen.polygon([(left + wide // 2 - 8, mid_y + 4),
                 (left + wide // 2 + 18, mid_y + 16),
                 (left + wide // 2 + 26, mid_y + 14),
                 (left + wide // 2 + 6, mid_y + 2)], fill=(210, 210, 206))
    pen.ellipse([left + wide // 2 - 16, mid_y - 16,
                 left + wide // 2 + 16, mid_y - 8],
                fill=(255, 255, 255), outline=(120, 120, 120), width=1)
    pen.line([left + wide // 2, mid_y - 8, left + wide // 2, mid_y - 4],
             fill=(120, 120, 120), width=2)
    pen.text((left + 6, top + 3), "AWACS", font=sans_b(10), fill=NAVY)


def art_jets(pen, left, top, wide, tall):
    """Two jets over a green island mound, with a red alert triangle."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(196, 216, 232))
    pen.rectangle([left, top + tall - 12, left + wide, top + tall],
                  fill=(60, 120, 90))
    # Island (Ulleungdo) as a low green mound with a lighthouse dot.
    pen.pieslice([left + wide // 2 - 34, top + tall - 22,
                  left + wide // 2 + 34, top + tall + 6],
                 180, 360, fill=(50, 110, 70))
    pen.rectangle([left + wide // 2 - 2, top + tall - 26,
                   left + wide // 2 + 2, top + tall - 16],
                  fill=(255, 255, 255))
    # Two jet silhouettes crossing the sky, the second one smaller.
    for jet_x, jet_y, scale in [(left + 18, top + 10, 1.0),
                                (left + wide - 52, top + 22, 0.8)]:
        pen.polygon([(jet_x, jet_y + 6),
                     (jet_x + int(34 * scale), jet_y),
                     (jet_x + int(40 * scale), jet_y + 6),
                     (jet_x + int(34 * scale), jet_y + 10)],
                    fill=(60, 60, 70))
        pen.polygon([(jet_x + int(14 * scale), jet_y + 4),
                     (jet_x + int(22 * scale), jet_y - 4),
                     (jet_x + int(26 * scale), jet_y - 2),
                     (jet_x + int(20 * scale), jet_y + 6)],
                    fill=(60, 60, 70))
    # Red alert triangle in the top-right corner.
    tri_x, tri_y = left + wide - 26, top + 4
    pen.polygon([(tri_x, tri_y + 12), (tri_x + 12, tri_y),
                 (tri_x + 24, tri_y + 12)], fill=RED)
    pen.text((tri_x + 10, tri_y + 2), "!", font=sans_b(9),
             fill=(255, 255, 255))


def art_fire(pen, left, top, wide, tall):
    """Factory building with flames on its sawtooth roof and drifting smoke."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(232, 214, 180))
    roof_h = min(14, tall // 3)
    base_y = top + tall - 6
    roof_y = base_y - 20
    pen.rectangle([left + 10, roof_y, left + wide - 10, base_y],
                  fill=(120, 116, 104))
    pen.polygon([(left + 10, roof_y), (left + 30, roof_y - roof_h),
                 (left + 50, roof_y), (left + 70, roof_y - roof_h),
                 (left + 90, roof_y), (left + wide - 10, roof_y)],
                fill=(90, 86, 76))
    if tall >= 44:
        pen.rectangle([left + wide - 26, top + 10, left + wide - 16, roof_y],
                      fill=(140, 130, 116))
    flame_h = min(22, tall // 2)
    for flame_x in (left + 26, left + 46, left + 66):
        pen.polygon([(flame_x - 8, roof_y), (flame_x, roof_y - flame_h),
                     (flame_x + 8, roof_y)], fill=(255, 140, 30))
        pen.polygon([(flame_x - 4, roof_y), (flame_x, roof_y - flame_h + 8),
                     (flame_x + 4, roof_y)], fill=(255, 200, 60))
    for smoke_x, smoke_y, smoke_r in [(left + 40, top + 8, 6),
                                      (left + 56, top + 14, 8),
                                      (left + 70, top + 8, 5)]:
        if smoke_y - smoke_r >= top:
            pen.ellipse([smoke_x - smoke_r, smoke_y - smoke_r,
                         smoke_x + smoke_r, smoke_y + smoke_r],
                        fill=(110, 108, 102))


def art_cricket(pen, left, top, wide, tall):
    """Cricket pitch seen from above: creases, a bat, a red ball, stumps."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(34, 110, 60))
    stripe_count = max(1, (tall - 12) // 14)
    for stripe in range(stripe_count):
        stripe_y = top + 6 + stripe * 14
        pen.line([left + 6, stripe_y, left + wide - 6, stripe_y],
                 fill=(255, 255, 255), width=1)
    pen.rectangle([left + 10, top + 8, left + wide - 10, top + tall - 8],
                  outline=(255, 255, 255), width=2)
    pen.line([left + 10, top + tall // 2, left + wide - 10, top + tall // 2],
             fill=(255, 255, 255), width=2)
    pen.rectangle([left + wide // 2 - 22, top + 10,
                   left + wide // 2 - 12, top + tall - 22],
                  fill=(220, 180, 120))
    pen.rectangle([left + wide // 2 - 20, top + 6,
                   left + wide // 2 - 14, top + 10], fill=(120, 80, 40))
    pen.ellipse([left + wide // 2 + 8, top + tall // 2 - 7,
                 left + wide // 2 + 22, top + tall // 2 + 7],
                fill=(200, 40, 40))
    for stump_x in (left + wide - 26, left + wide - 20, left + wide - 14):
        pen.rectangle([stump_x, top + tall - 18, stump_x + 3, top + tall - 8],
                      fill=(255, 220, 90))
    pen.rectangle([left + 12, top + tall - 14, left + 52, top + tall - 1],
                  fill=(34, 110, 60))
    pen.text((left + 14, top + tall - 13), "720/9", font=sans_b(9),
             fill=(255, 255, 255))

def art_flags(pen, left, top, wide, tall):
    """India tricolour beside the Nepal pennant, hands clasped below."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(196, 222, 240))
    dot_x = left + 8
    while dot_x < left + wide - 4:
        pen.ellipse([dot_x, top + 8, dot_x + 4, top + 12],
                    fill=(255, 255, 255))
        dot_x += 22
    # India tricolour, left; Nepal crimson pennant, right.
    pen.rectangle([left + 10, top + 16, left + 58, top + 22],
                  fill=(255, 153, 51))
    pen.rectangle([left + 10, top + 22, left + 58, top + 28],
                  fill=(255, 255, 255))
    pen.rectangle([left + 10, top + 28, left + 58, top + 34],
                  fill=(19, 136, 8))
    pen.ellipse([left + 30, top + 22, left + 38, top + 30], outline=NAVY,
                width=1)
    pen.polygon([(left + wide - 58, top + 16), (left + wide - 10, top + 16),
                 (left + wide - 10, top + 34), (left + wide - 58, top + 34)],
                fill=(220, 20, 60))
    pen.polygon([(left + wide - 58, top + 16), (left + wide - 34, top + 16),
                 (left + wide - 58, top + 28)], fill=(220, 20, 60))
    # Handshake: two clasped hands as interlocked arcs.
    pen.ellipse([left + wide // 2 - 16, top + tall - 26,
                 left + wide // 2 + 16, top + tall - 6],
                fill=(240, 200, 160))
    pen.line([left + wide // 2 - 12, top + tall - 16,
              left + wide // 2 + 12, top + tall - 16],
             fill=(180, 120, 80), width=2)


def art_talks(pen, left, top, wide, tall):
    """Four chairs around a round table: four flags, one table."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(226, 222, 208))
    table_x, table_y = left + wide // 2, top + tall // 2 + 4
    pen.ellipse([table_x - 30, table_y - 12, table_x + 30, table_y + 12],
                fill=(120, 70, 40))
    pen.ellipse([table_x - 30, table_y - 12, table_x + 30, table_y + 4],
                fill=(150, 95, 55))
    for flag_x, flag_y, colour in [(table_x - 38, table_y - 22, (0, 90, 180)),
                                   (table_x + 26, table_y - 22, (255, 210, 0)),
                                   (table_x - 38, table_y + 12, (220, 40, 40)),
                                   (table_x + 26, table_y + 12, (30, 120, 60))]:
        pen.rectangle([flag_x, flag_y, flag_x + 12, flag_y + 8], fill=colour,
                      outline=(255, 255, 255), width=1)
    pen.text((left + 6, top + 3), "4-WAY", font=sans_b(10), fill=NAVY)


def art_blast(pen, left, top, wide, tall):
    """Governor's office facade at night, windows lit, blast star at the door."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(40, 38, 52))
    pen.rectangle([left + 14, top + 10, left + wide - 14, top + tall - 6],
                  fill=(150, 140, 125))
    win_y = top + 16
    while win_y < top + tall - 10:
        for win_x in (left + 20, left + 34, left + 48):
            pen.rectangle([win_x, win_y, win_x + 8, win_y + 7],
                          fill=(255, 220, 120))
        win_y += 12
    star_x, star_y = left + wide // 2, top + tall - 14
    star_r = 9 if tall < 44 else 16
    for spoke in range(8):
        angle = math.pi * 2 * spoke / 8
        pen.line([star_x, star_y,
                  star_x + int(star_r * math.cos(angle)),
                  star_y + int(star_r * math.sin(angle))],
                 fill=(255, 180, 40), width=3)
    pen.ellipse([star_x - 6, star_y - 6, star_x + 6, star_y + 6],
                fill=(255, 220, 90))
    for puff_x, puff_y, puff_r in [(left + 30, top + 6, 6),
                                   (left + 46, top + 12, 8)]:
        pen.ellipse([puff_x - puff_r, puff_y - puff_r,
                     puff_x + puff_r, puff_y + puff_r],
                    fill=(110, 108, 102))


def art_picket(pen, left, top, wide, tall):
    """Factory silhouette behind, three picket signs in front."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(222, 226, 232))
    pen.rectangle([left + 8, top + tall - 22, left + wide - 8, top + tall - 4],
                  fill=(90, 90, 96))
    pen.rectangle([left + wide - 30, top + 8, left + wide - 20,
                   top + tall - 22], fill=(120, 120, 126))
    for sign_x in (left + 16, left + 44, left + 72):
        pen.line([sign_x + 6, top + 12, sign_x + 6, top + tall - 8],
                 fill=(120, 90, 60), width=2)
        pen.rectangle([sign_x, top + 6, sign_x + 14, top + 18],
                      fill=(255, 255, 255), outline=RED, width=1)
        pen.text((sign_x + 3, top + 8), "5%", font=sans_b(8), fill=RED_DK)


def art_jet(pen, left, top, wide, tall):
    """F-35 seen from above: delta body, swept wings, twin tail, 41.9% tag."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(150, 190, 220))
    cloud_x = left + 10
    while cloud_x < left + wide - 8:
        pen.ellipse([cloud_x, top + tall - 14, cloud_x + 16, top + tall - 6],
                    fill=(255, 255, 255))
        cloud_x += 34
    centre_x, centre_y = left + wide // 2, top + tall // 2
    pen.polygon([(centre_x - 34, centre_y - 4),
                 (centre_x + 34, centre_y - 8), (centre_x + 40, centre_y),
                 (centre_x + 34, centre_y + 8),
                 (centre_x - 34, centre_y + 4)], fill=(90, 95, 105))
    pen.polygon([(centre_x - 6, centre_y - 4),
                 (centre_x + 8, centre_y - 20),
                 (centre_x + 16, centre_y - 18),
                 (centre_x + 6, centre_y - 2)], fill=(70, 75, 85))
    pen.polygon([(centre_x - 6, centre_y + 4),
                 (centre_x + 8, centre_y + 20),
                 (centre_x + 16, centre_y + 18),
                 (centre_x + 6, centre_y + 2)], fill=(70, 75, 85))
    pen.polygon([(centre_x - 34, centre_y - 6),
                 (centre_x - 26, centre_y - 12),
                 (centre_x - 20, centre_y - 4)], fill=(70, 75, 85))
    pen.polygon([(centre_x - 34, centre_y + 6),
                 (centre_x - 26, centre_y + 12),
                 (centre_x - 20, centre_y + 4)], fill=(70, 75, 85))
    pen.ellipse([centre_x - 4, centre_y - 4, centre_x + 4, centre_y + 4],
                fill=(200, 210, 220))
    pen.text((left + 6, top + 3), "41.9%", font=sans_b(10), fill=NAVY)


def art_ban(pen, left, top, wide, tall):
    """A chip inside a red prohibition circle with a diagonal bar."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(240, 236, 224))
    centre_x, centre_y = left + wide // 2, top + tall // 2
    half = min(wide, tall) // 3
    pen.rectangle([centre_x - half, centre_y - half,
                   centre_x + half, centre_y + half], fill=(30, 30, 34),
                  outline=(120, 120, 115), width=2)
    pen.rectangle([centre_x - half // 2, centre_y - half // 2,
                   centre_x + half // 2, centre_y + half // 2],
                  fill=(40, 160, 90))
    radius = min(wide, tall) // 2 - 4
    pen.ellipse([centre_x - radius, centre_y - radius,
                 centre_x + radius, centre_y + radius], outline=RED, width=4)
    pen.line([centre_x - radius + 4, centre_y + radius - 4,
              centre_x + radius - 4, centre_y - radius + 4], fill=RED,
             width=4)


def art_flats(pen, left, top, wide, tall):
    """Five-storey block at night, one corner blown out, flame at the top."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(40, 38, 52))
    star_x = left + 8
    while star_x < left + wide - 6:
        pen.ellipse([star_x, top + 6, star_x + 2, top + 8],
                    fill=(255, 255, 255))
        star_x += 20
    pen.rectangle([left + 14, top + 12, left + wide - 14, top + tall - 6],
                  fill=(150, 140, 125))
    win_y = top + 18
    while win_y < top + tall - 10:
        for win_x in (left + 20, left + 34, left + 48):
            pen.rectangle([win_x, win_y, win_x + 8, win_y + 7],
                          fill=(255, 220, 120))
        win_y += 12
    pen.polygon([(left + wide - 14, top + 12), (left + wide - 14, top + 34),
                 (left + wide - 34, top + 12)], fill=(30, 28, 40))
    pen.polygon([(left + wide - 40, top + 12), (left + wide - 14, top + 12),
                 (left + wide - 30, top + 30)], fill=(200, 120, 60))
    pen.polygon([(left + 8, top + 6), (left + 22, top + 6),
                 (left + 15, top + 14)], fill=(255, 90, 40))
    pen.text((left + 8, top + tall - 12), "DYMER", font=sans_b(8),
             fill=(255, 255, 255))


def art_plane(pen, left, top, wide, tall):
    """Airliner in flight over a runway strip, with a red DEC 16 banner."""
    pen.rectangle([left, top, left + wide, top + tall], fill=(150, 190, 220))
    cloud_x = left + 10
    while cloud_x < left + wide - 8:
        pen.ellipse([cloud_x, top + 6, cloud_x + 16, top + 12],
                    fill=(255, 255, 255))
        cloud_x += 34
    pen.rectangle([left, top + tall - 10, left + wide, top + tall - 4],
                  fill=(70, 70, 78))
    mid_y = top + tall // 2 - 4
    pen.polygon([(left + 12, mid_y), (left + wide - 30, mid_y - 6),
                 (left + wide - 8, mid_y), (left + wide - 30, mid_y + 6)],
                fill=(240, 240, 238))
    pen.polygon([(left + wide // 2 - 8, mid_y - 4),
                 (left + wide // 2 + 18, mid_y - 16),
                 (left + wide // 2 + 26, mid_y - 14),
                 (left + wide // 2 + 6, mid_y - 2)], fill=(210, 210, 206))
    pen.ellipse([left + wide // 2 - 10, mid_y - 12,
                 left + wide // 2 + 10, mid_y - 4],
                fill=(255, 255, 255), outline=(120, 120, 120), width=1)
    pen.rectangle([left + 6, top + tall - 22, left + 52, top + tall - 12],
                  fill=RED)
    pen.text((left + 8, top + tall - 21), "DEC 16", font=sans_b(9),
             fill=(255, 255, 255))


ART = {"chip": art_chip, "awacs": art_awacs, "jets": art_jets,
       "fire": art_fire, "cricket": art_cricket, "flags": art_flags,
       "talks": art_talks, "blast": art_blast, "picket": art_picket,
       "jet": art_jet, "ban": art_ban, "flats": art_flats,
       "plane": art_plane}

# ---------------------------------------------------------------- world map
# A coarse land grid given as column ranges per row (60 columns by 24
# rows, equirectangular: longitude -180 to 180, latitude 75 to -55).
# Ranges, not typed art, define the land, so no row can be miscounted.
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

# (lead number, longitude, latitude) — approximate places for the 13 leads.
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


def map_xy(map_x, map_y, map_w, map_h, lon, lat):
    """Convert longitude/latitude to pixel coordinates inside the map box."""
    frac_x = (lon + 180.0) / 360.0
    frac_y = (75.0 - lat) / 130.0
    return map_x + frac_x * map_w, map_y + frac_y * map_h


def land_dots(map_x, map_y, map_w, map_h):
    """Expand the land ranges into the centre point of every land cell."""
    dots = []
    for row, ranges in LAND_RANGES.items():
        for col_start, col_end in ranges:
            col = col_start
            while col <= col_end:
                dots.append((map_x + (col + 0.5) * map_w / 60.0,
                             map_y + (row + 0.5) * map_h / 24.0))
                col += 1
    return dots


def nearest_land(dots, px, py):
    """Find the land dot closest to a point, plus its distance in pixels."""
    closest, closest_dist_sq = None, 1e9
    for dot_x, dot_y in dots:
        dist_sq = (dot_x - px) ** 2 + (dot_y - py) ** 2
        if dist_sq < closest_dist_sq:
            closest, closest_dist_sq = (dot_x, dot_y), dist_sq
    return closest, closest_dist_sq ** 0.5


def paint_map(canvas, map_x, map_y, map_w, map_h):
    """Paint the dotted world map and its thirteen numbered red pins."""
    canvas.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                     fill=(228, 236, 240))
    canvas.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                     outline=NAVY, width=2)
    dots = land_dots(map_x, map_y, map_w, map_h)
    for dot_x, dot_y in dots:
        canvas.ellipse([dot_x - 1.6, dot_y - 1.6, dot_x + 1.6, dot_y + 1.6],
                       fill=(90, 110, 95))
    placed = {}
    for num, (lon, lat) in PINS.items():
        px, py = map_xy(map_x, map_y, map_w, map_h, lon, lat)
        (land_x, land_y), dist = nearest_land(dots, px, py)
        if dist > 14:
            raise SystemExit("MAP PIN %d too far from land: %.1fpx"
                             % (num, dist))
        # Keep the disc fully inside the map: a true spot near an edge
        # (Wellington) is pulled in and joined with a leader line.
        target_x = min(max(land_x, map_x + 9), map_x + map_w - 9)
        target_y = min(max(land_y, map_y + 9), map_y + map_h - 9)
        moved = (target_x, target_y) != (land_x, land_y)
        if any(((target_x - old_x) ** 2 + (target_y - old_y) ** 2) ** 0.5 < 19
               for old_x, old_y in placed.values()):
            found = None
            for radius in (13, 17, 21, 25, 29):
                for step in range(12):
                    angle = math.pi * 2 * step / 12
                    cand_x = land_x + radius * math.cos(angle)
                    cand_y = land_y + radius * math.sin(angle)
                    if not (map_x + 9 <= cand_x <= map_x + map_w - 9
                            and map_y + 9 <= cand_y <= map_y + map_h - 9):
                        continue
                    if all(((cand_x - old_x) ** 2
                            + (cand_y - old_y) ** 2) ** 0.5 >= 19
                           for old_x, old_y in placed.values()):
                        found = (cand_x, cand_y)
                        break
                if found:
                    break
            if not found:
                raise SystemExit("MAP PIN %d: no free disc spot near land"
                                 % num)
            target_x, target_y = found
            moved = True
        if moved:
            canvas.line([land_x, land_y, target_x, target_y], fill=RED,
                        width=1)
            canvas.ellipse([land_x - 2, land_y - 2, land_x + 2, land_y + 2],
                           fill=RED)
        placed[num] = (target_x, target_y)
        canvas.ellipse([target_x - 8, target_y - 8,
                        target_x + 8, target_y + 8], fill=RED,
                       outline=(255, 255, 255), width=1)
        canvas.text((target_x - 3, target_y - 6), str(num), font=sans_b(8),
                    fill=(255, 255, 255))
    return placed


# ---------------------------------------------------------------- page layout
# Page margins: a 12-pixel frame around a 1000-pixel content column.
MARGIN = 12
CONTENT_W = W - 2 * MARGIN


def paint_header(canvas):
    """Navy top bar, centred serif masthead, sub-headline and story strip."""
    canvas.rectangle([0, 0, W, 26], fill=NAVY)
    canvas.text((MARGIN, 5), "ONE DAY, EVERYWHERE", font=sans_b(13),
                fill=(255, 255, 255))
    edition = "TUESDAY EDITION  \u2022  No. 328"
    canvas.text((W - MARGIN - canvas.textlength(edition, font=sans_b(11)), 7),
                edition, font=sans_b(11), fill=(200, 200, 200))
    masthead = "Tuesday 24 November 2026"
    mast_font = serif_b(54)
    canvas.text(((W - canvas.textlength(masthead, font=mast_font)) / 2, 30),
                masthead, font=mast_font, fill=INK)
    canvas.line([MARGIN, 92, W - MARGIN, 92], fill=INK, width=2)
    subhead = ("Huang returns to Nvidia, +31% (Mon)  \u2022  NATO sends AWACS "
               "to Poland (Mon)  \u2022  Russian jets spark shelter alert off "
               "Ulleungdo")
    sub_font = serif(15)
    canvas.text(((W - canvas.textlength(subhead, font=sub_font)) / 2, 98),
                subhead, font=sub_font, fill=(60, 60, 60))
    strip = "44 STORIES  \u2022  7 REGIONS  \u2022  13 ILLUSTRATED"
    strip_font = sans_b(14)
    canvas.text(((W - canvas.textlength(strip, font=strip_font)) / 2, 120),
                strip, font=strip_font, fill=RED_DK)
    canvas.line([MARGIN, 140, W - MARGIN, 140], fill=LINE, width=1)


def paint_numbers(canvas):
    """Six headline figures in a row, separated by thin vertical rules."""
    cells = [
        ("+31%", "Nvidia shares, Monday"),
        ("AWACS", "deployed to Poland"),
        ("26", "confirmed dead, Cikande fire"),
        ("24,000 cr", "Nepal aid package (NPR)"),
        ("11", "killed in Dymer, Kyiv region"),
        ("Nikkei +3.9%", "Tue close; Nvidia -5% pre-mkt"),
    ]
    top_y, bottom_y = 146, 194
    cell_w = CONTENT_W / 6.0
    for index, (big, small) in enumerate(cells):
        cell_x = MARGIN + index * cell_w
        if index:
            canvas.line([cell_x, top_y + 4, cell_x, bottom_y - 4],
                        fill=LINE, width=1)
        big_font = sans_b(19)
        canvas.text((cell_x + (cell_w - canvas.textlength(big, font=big_font)) / 2,
                     top_y + 2), big, font=big_font, fill=RED_DK)
        small_font = sans(10)
        canvas.text((cell_x + (cell_w - canvas.textlength(small, font=small_font)) / 2,
                     top_y + 27), small, font=small_font, fill=(70, 70, 70))
    canvas.line([MARGIN, bottom_y, W - MARGIN, bottom_y], fill=LINE, width=1)


def paint_region_bar(canvas, counts):
    """One coloured segment per region, sized by its story count."""
    top_y, bottom_y = 200, 224
    total = sum(counts.values())
    widths = {region: CONTENT_W * counts[region] / total
              for region in REGION_ORDER}
    # Minimum segment width so the smallest label ("Oceania 1", ~50px at
    # 9px bold) fits; the deficit comes off the largest segment.
    min_width = 56.0
    for region in REGION_ORDER:
        if widths[region] < min_width:
            biggest = max(widths, key=lambda key: widths[key])
            widths[biggest] -= min_width - widths[region]
            widths[region] = min_width
    cursor_x = MARGIN
    for region in REGION_ORDER:
        count = counts[region]
        segment = widths[region]
        canvas.rectangle([cursor_x, top_y, cursor_x + segment, bottom_y],
                         fill=REGION_COLOURS[region])
        label = "%s %d" % (REGION_SHORT.get(region, region), count)
        label_font = sans_b(9)
        label_w = canvas.textlength(label, font=label_font)
        if label_w <= segment - 2:
            canvas.text((cursor_x + (segment - label_w) / 2, top_y + 7),
                        label, font=label_font, fill=(255, 255, 255))
        else:
            # Segment too narrow for its name: draw the count only; the
            # full counts line runs in the footer.
            canvas.text((cursor_x + (segment - 6) / 2, top_y + 7), str(count),
                        font=label_font, fill=(255, 255, 255))
        cursor_x += segment
    canvas.rectangle([MARGIN, top_y, W - MARGIN, bottom_y], outline=INK,
                     width=1)


def paint_lead_card(canvas, item, left, top, wide, tall, big):
    """One lead card: illustration on top, tag + number, headline, deck."""
    left, top, wide, tall = int(left), int(top), int(wide), int(tall)
    num, region, field, tag, headline, deck, source, art = item
    canvas.rectangle([left, top, left + wide, top + tall], fill=CARD,
                     outline=LINE, width=1)
    art_h = 88 if big else 34
    ART[art](canvas, left + 1, top + 1, wide - 2, art_h)
    tag_font = sans_b(10 if big else 8)
    tag_w = canvas.textlength(tag, font=tag_font)
    canvas.rectangle([left + 6, top + art_h + 5,
                      left + 10 + tag_w, top + art_h + 20],
                     fill=REGION_COLOURS[region])
    canvas.text((left + 8, top + art_h + 6), tag, font=tag_font,
                fill=(255, 255, 255))
    canvas.ellipse([left + wide - 24, top + art_h + 4,
                    left + wide - 6, top + art_h + 22], fill=RED)
    canvas.text((left + wide - 19, top + art_h + 7), str(num),
                font=sans_b(10), fill=(255, 255, 255))
    headline_y = top + art_h + 24
    headline_font = serif_b(19 if big else 13)
    headline_lines = fit(canvas, headline, headline_font, wide - 12, 2,
                         "lead %d headline" % num)
    headline_lead = 21 if big else 14
    draw_lines(canvas, headline_lines, left + 6, headline_y, headline_font,
               INK, headline_lead)
    deck_y = headline_y + len(headline_lines) * headline_lead + 1
    deck_font = sans(11 if big else 9)
    deck_lines = fit(canvas, deck, deck_font, wide - 12, 2,
                     "lead %d deck" % num)
    deck_lead = 11 if big else 10
    draw_lines(canvas, deck_lines, left + 6, deck_y, deck_font,
               (60, 60, 60), deck_lead)
    if deck_y + len(deck_lines) * deck_lead > top + tall - 13:
        raise SystemExit("OVERFLOW in lead %d: deck runs into source line"
                         % num)
    source_font = sans(8 if big else 7)
    canvas.text((left + 6, top + tall - 11), source.upper(),
                font=source_font, fill=GREY)


def paint_leads(canvas):
    """Three big lead cards on top, then two rows of five small cards."""
    top_y = 230
    big_w, big_h = 322, 196
    gap = (CONTENT_W - 3 * big_w) / 2.0
    for index, item in enumerate(LEADS[:3]):
        paint_lead_card(canvas, item, MARGIN + index * (big_w + gap),
                        top_y, big_w, big_h, True)
    small_w, small_h = 192, 122
    small_gap = (CONTENT_W - 5 * small_w) / 4.0
    for row in range(2):
        for col in range(5):
            item = LEADS[3 + row * 5 + col]
            paint_lead_card(canvas, item, MARGIN + col * (small_w + small_gap),
                            top_y + big_h + 6 + row * (small_h + 6),
                            small_w, small_h, False)


def paint_briefs(canvas, box_x, box_y, box_w, box_h):
    """Thirty-one numbered one-line briefs in two columns."""
    canvas.text((box_x, box_y), "ALSO ON THIS PAGE", font=sans_b(12),
                fill=NAVY)
    canvas.line([box_x, box_y + 16, box_x + box_w, box_y + 16], fill=NAVY,
                width=2)
    col_w = (box_w - 14) / 2.0
    per_col = 16
    brief_font = sans(8)
    row_h = 10.5
    for index, item in enumerate(BRIEFS):
        num, region, field, text = item
        col = index // per_col
        row = index % per_col
        item_x = box_x + col * (col_w + 14)
        item_y = box_y + 20 + row * row_h
        if item_y + 10 > box_y + box_h:
            raise SystemExit("BRIEFS overflow at item %d" % num)
        canvas.text((item_x, item_y), "%d." % num, font=sans_b(8),
                    fill=RED_DK)
        wrapped = fit(canvas, text, brief_font, col_w - 18, 1,
                      "brief %d" % num)
        canvas.text((item_x + 18, item_y), wrapped[0], font=brief_font,
                    fill=INK)


def paint_date_check(canvas, left, top, wide, tall):
    """Red-bordered box listing stale stories that are NOT 24 November news."""
    canvas.rectangle([left, top, left + wide, top + tall], outline=RED,
                     width=2)
    canvas.text((left + 8, top + 4), "DATE CHECK \u2014 NOT 24 NOVEMBER NEWS",
                font=sans_b(11), fill=RED_DK)
    body_font = sans(9)
    cursor_y = top + 21
    for name, when in DATE_CHECK:
        canvas.text((left + 8, cursor_y), "X  %s \u2014 %s" % (name, when),
                    font=body_font, fill=INK)
        cursor_y += 11


def paint_footer(canvas, top_y):
    """Footer: dating note, sources line, region counts, map key."""
    canvas.line([MARGIN, top_y, W - MARGIN, top_y], fill=LINE, width=1)
    canvas.text((MARGIN, top_y + 4),
                "Tuesday 24 November 2026 \u2014 today's biggest stories plus "
                "the weekend's developments; earlier events are dated in the deck.",
                font=sans(10), fill=INK)
    canvas.text((MARGIN, top_y + 16), SOURCES_LINE, font=sans(9),
                fill=(70, 70, 70))
    canvas.text((MARGIN, top_y + 28),
                "Regions: Americas 10 \u00b7 Asia 10 \u00b7 Europe 9 \u00b7 Africa 6 \u00b7 "
                "Middle East 5 \u00b7 World/Global 3 \u00b7 Oceania 1 \u2014 Original "
                "flat-vector drawings, no photographs.",
                font=sans_b(9), fill=(70, 70, 70))
    canvas.text((MARGIN, top_y + 40),
                "Map: 1 Santa Clara \u00b7 2 Warsaw \u00b7 3 Ulleungdo \u00b7 4 Cikande "
                "\u00b7 5 Wellington \u00b7 6 New Delhi \u00b7 7 Berlin \u00b7 8 "
                "Villavicencio \u00b7 9 Hamburg \u00b7 10 Washington DC \u00b7 11 "
                "Singapore \u00b7 12 Dymer \u00b7 13 Dhaka.",
                font=sans(9), fill=(70, 70, 70))


def build():
    """Assemble the whole page and return the finished PIL image."""
    counts = region_counts()
    assert sum(counts.values()) == 44, counts
    assert len(counts) == 7, counts
    assert len(LEADS) == 13 and len(BRIEFS) == 31
    assert [lead[0] for lead in LEADS] == list(range(1, 14))
    assert [brief[0] for brief in BRIEFS] == list(range(14, 45))
    img = Image.new("RGB", (W, H), PAPER)
    canvas = ImageDraw.Draw(img)
    paint_header(canvas)
    paint_numbers(canvas)
    paint_region_bar(canvas, counts)
    paint_leads(canvas)
    # Bottom band: map left, briefs right.
    band_y = 688
    canvas.text((MARGIN, band_y), "WHERE IT HAPPENED", font=sans_b(12),
                fill=NAVY)
    canvas.line([MARGIN, band_y + 16, MARGIN + 470, band_y + 16], fill=NAVY,
                width=2)
    paint_map(canvas, MARGIN, band_y + 22, 470, 124)
    canvas.text((MARGIN, band_y + 152),
                "Pins 1-13 = the illustrated leads above.",
                font=sans(9), fill=(70, 70, 70))
    paint_briefs(canvas, MARGIN + 486, band_y, CONTENT_W - 486, 190)
    paint_date_check(canvas, MARGIN, 850, 470, 102)
    paint_footer(canvas, 962)
    return img


def main():
    """Render the page and write entry.png beside this file."""
    img = build()
    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print("wrote %s %d bytes" % (out, out.stat().st_size))


if __name__ == "__main__":
    main()
