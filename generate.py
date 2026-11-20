#!/usr/bin/env python3
"""Draw Friday 20 November 2026 as a one-page newspaper front page.

Reads stories.json beside this file (a masthead date, one lead story,
four grid stories, two bottom stories and a footer line) and paints
entry.png at 1024x1024 with Pillow. Each story gets a small flat
illustration drawn with basic shapes, so the whole day can be taken
in from the single image. This is a local build step only; the entry
program (main.py) ships the finished PNG unchanged.

Run from this folder:  python3 generate.py
"""

import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
SIDE = 1024
EDGE = 42
GAP = 22
COLUMN = (SIDE - 2 * EDGE - GAP) // 2

INK = (22, 22, 22)
SOFT = (78, 76, 70)
FAINT = (150, 146, 138)
PAPER = (252, 250, 244)
CARD = (255, 255, 255)
ACCENT = (166, 30, 30)
WASH = (240, 236, 226)
SKY = (205, 226, 240)
SEA = (110, 158, 196)
LEAF = (74, 140, 74)
AMBER = (214, 150, 32)
NIGHT = (28, 34, 64)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def typeface(points, bold=False, serif=False):
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), points)
    except OSError:
        return ImageFont.load_default()


def split_lines(pen, text, face, limit):
    """Greedy wrap: pack words onto a line while the line still fits."""
    out, line = [], ""
    for word in text.split():
        candidate = word if not line else line + " " + word
        if line and pen.textlength(candidate, font=face) > limit:
            out.append(line)
            line = word
        else:
            line = candidate
    if line:
        out.append(line)
    return out


def paint_lines(pen, x, y, lines, face, colour, step):
    for chunk in lines:
        pen.text((x, y), chunk, font=face, fill=colour)
        y += step
    return y


def centred(pen, y, text, face, colour):
    width = pen.textlength(text, font=face)
    pen.text(((SIDE - width) / 2, y), text, font=face, fill=colour)
    return y + face.size


# ------------------------------------------------------------------ art
def art_calendar(pen, box):
    """Lead art: a torn-off calendar page marked 2027 beside a clock."""
    x0, y0, x1, y1 = box
    pen.rectangle(box, fill=SKY)
    pen.rectangle([x0, y1 - 28, x1, y1], fill=SEA)
    page_x0, page_y0 = x0 + 40, y0 + 34
    page_x1, page_y1 = x0 + 230, y1 - 44
    pen.rectangle([page_x0, page_y0, page_x1, page_y1], fill=CARD,
                  outline=INK, width=4)
    pen.rectangle([page_x0, page_y0, page_x1, page_y0 + 40], fill=ACCENT)
    for ring_x in (page_x0 + 32, page_x0 + 92, page_x0 + 152):
        pen.ellipse([ring_x - 9, page_y0 - 14, ring_x + 9, page_y0 + 12],
                    outline=INK, width=4)
    big = typeface(58, bold=True)
    label = "2027"
    tw = pen.textlength(label, font=big)
    pen.text((page_x0 + (page_x1 - page_x0 - tw) / 2, page_y0 + 54),
             label, font=big, fill=INK)
    small = typeface(24, bold=True)
    sub = "JAN 1"
    tw = pen.textlength(sub, font=small)
    pen.text((page_x0 + (page_x1 - page_x0 - tw) / 2, page_y0 + 124),
             sub, font=small, fill=ACCENT)
    cx, cy, r = x0 + 296, y0 + 104, 46
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CARD,
                outline=INK, width=4)
    pen.line([cx, cy, cx, cy - r + 12], fill=INK, width=5)
    pen.line([cx, cy, cx + r - 18, cy + 14], fill=ACCENT, width=5)
    pen.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=INK)


def art_cyclone(pen, box):
    x0, y0, x1, y1 = box
    pen.rectangle(box, fill=(226, 238, 246))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    for turn in range(3):
        radius = 16 + turn * 15
        pen.arc([cx - radius, cy - radius, cx + radius, cy + radius],
                start=turn * 70, end=turn * 70 + 270,
                fill=(70, 110, 160), width=7)
    pen.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(70, 110, 160))
    pen.rectangle([x0, y1 - 26, x1, y1], fill=SEA)
    for wave_x in range(x0 + 10, x1 - 24, 34):
        pen.arc([wave_x, y1 - 34, wave_x + 26, y1 - 14], 180, 360,
                fill=CARD, width=3)


def art_market(pen, box):
    x0, y0, x1, y1 = box
    pen.rectangle(box, fill=CARD)
    pen.line([x0 + 16, y0 + 12, x0 + 16, y1 - 16], fill=INK, width=3)
    pen.line([x0 + 16, y1 - 16, x1 - 10, y1 - 16], fill=INK, width=3)
    points = [(x0 + 24, y1 - 34), (x0 + 52, y1 - 52), (x0 + 78, y1 - 46),
              (x0 + 102, y0 + 52), (x0 + 122, y0 + 26)]
    pen.line(points, fill=LEAF, width=5, joint="curve")
    for px, py in points:
        pen.ellipse([px - 5, py - 5, px + 5, py + 5], fill=LEAF)
    tip_x, tip_y = points[-1]
    pen.polygon([(tip_x, tip_y - 14), (tip_x - 9, tip_y + 4),
                 (tip_x + 9, tip_y + 4)], fill=LEAF)


def art_talks(pen, box):
    x0, y0, x1, y1 = box
    pen.rectangle(box, fill=(234, 238, 246))
    table_y = y0 + 96
    pen.rectangle([x0 + 18, table_y, x1 - 18, table_y + 12], fill=INK)
    pen.rectangle([x0 + 28, table_y + 12, x0 + 36, y1 - 16], fill=INK)
    pen.rectangle([x1 - 36, table_y + 12, x1 - 28, y1 - 16], fill=INK)
    for flag_x, colour in ((x0 + 26, (40, 90, 170)), (x1 - 58, ACCENT)):
        pen.rectangle([flag_x, y0 + 30, flag_x + 28, y0 + 58],
                      fill=colour, outline=INK, width=2)
        pen.line([flag_x, y0 + 30, flag_x, table_y], fill=INK, width=3)
    dove_x, dove_y = (x0 + x1) // 2, y0 + 40
    pen.ellipse([dove_x - 17, dove_y - 9, dove_x + 17, dove_y + 10],
                fill=CARD, outline=INK, width=2)
    pen.polygon([(dove_x + 14, dove_y - 3), (dove_x + 26, dove_y),
                 (dove_x + 14, dove_y + 3)], fill=AMBER)
    pen.arc([dove_x - 12, dove_y - 24, dove_x + 10, dove_y - 2],
            200, 340, fill=INK, width=3)


def art_probe(pen, box):
    x0, y0, x1, y1 = box
    pen.rectangle(box, fill=NIGHT)
    for sx, sy in ((x0 + 18, y0 + 20), (x0 + 96, y0 + 14),
                   (x1 - 26, y0 + 34), (x0 + 30, y1 - 30),
                   (x1 - 18, y1 - 44), (x0 + 70, y0 + 44)):
        pen.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=CARD)
    cx, cy = (x0 + x1) // 2 - 8, (y0 + y1) // 2
    pen.rectangle([cx - 16, cy - 12, cx + 16, cy + 12], fill=AMBER,
                  outline=INK, width=2)
    pen.rectangle([cx - 62, cy - 6, cx - 18, cy + 6], fill=(90, 130, 200),
                  outline=INK, width=2)
    pen.rectangle([cx + 18, cy - 6, cx + 62, cy + 6], fill=(90, 130, 200),
                  outline=INK, width=2)
    pen.line([cx, cy - 12, cx + 26, cy - 40], fill=CARD, width=3)
    pen.pieslice([cx + 10, cy - 62, cx + 48, cy - 24], 300, 60,
                 outline=CARD, width=3)
    for ring in (10, 18, 26):
        pen.arc([cx + 26 - ring, cy - 44 - ring, cx + 26 + ring,
                 cy - 44 + ring], 300, 60, fill=(160, 200, 240), width=2)


ART = [art_cyclone, art_market, art_talks, art_probe]


# ------------------------------------------------------------------ page
class Page:
    def __init__(self, data):
        self.data = data
        self.canvas = Image.new("RGB", (SIDE, SIDE), PAPER)
        self.pen = ImageDraw.Draw(self.canvas)
        self.y = 24

    def rule(self, weight=2, before=0, after=0):
        self.y += before
        self.pen.line([(EDGE, self.y), (SIDE - EDGE, self.y)],
                      fill=INK, width=weight)
        self.y += weight + after

    def masthead(self):
        eyebrow = typeface(19, bold=True)
        self.y = centred(self.pen, self.y,
                         "ONE DAY · ONE PAGE · WORLD NEWS", eyebrow, SOFT) + 8
        title = typeface(52, bold=True, serif=True)
        self.y = centred(self.pen, self.y, "THE WORLD IN ONE PAGE",
                         title, INK) + 10
        stamp = typeface(23, bold=True)
        self.y = centred(self.pen, self.y, self.data["date"], stamp,
                         ACCENT) + 10
        self.rule(weight=4, after=3)
        self.rule(weight=1, after=12)

    def kicker(self, x, y, text):
        face = typeface(19, bold=True)
        pad = 9
        width = self.pen.textlength(text, font=face)
        self.pen.rounded_rectangle([x, y, x + width + 2 * pad, y + 28],
                                   radius=4, fill=ACCENT)
        self.pen.text((x + pad, y + 4), text, font=face, fill=CARD)
        return y + 36

    def lead(self):
        story = self.data["lead"]
        top, height = self.y, 272
        self.pen.rectangle([EDGE, top, SIDE - EDGE, top + height],
                           fill=CARD, outline=INK, width=2)
        art_calendar(self.pen, (EDGE + 2, top + 2, EDGE + 378,
                                top + height - 2))
        self.pen.line([EDGE + 380, top, EDGE + 380, top + height],
                      fill=INK, width=2)
        tx = EDGE + 402
        limit = SIDE - EDGE - tx - 18
        y = self.kicker(tx, top + 16, story["kicker"])
        head = typeface(40, bold=True)
        y = paint_lines(self.pen, tx, y,
                        split_lines(self.pen, story["headline"], head,
                                    limit)[:3], head, INK, 47)
        body = typeface(24)
        paint_lines(self.pen, tx, y + 4,
                    split_lines(self.pen, story["summary"], body,
                                limit)[:4], body, SOFT, 30)
        self.y = top + height + 18

    def cell(self, x, top, story, art):
        height = 182
        self.pen.rectangle([x, top, x + COLUMN, top + height],
                           fill=CARD, outline=INK, width=2)
        art(self.pen, (x + 2, top + 2, x + 126, top + height - 2))
        self.pen.line([x + 128, top, x + 128, top + height],
                      fill=(205, 200, 190), width=1)
        tx = x + 140
        limit = x + COLUMN - tx - 12
        y = self.kicker(tx, top + 10, story["kicker"])
        head = typeface(25, bold=True)
        y = paint_lines(self.pen, tx, y,
                        split_lines(self.pen, story["headline"], head,
                                    limit)[:2], head, INK, 29)
        body = typeface(19)
        paint_lines(self.pen, tx, y + 2,
                    split_lines(self.pen, story["summary"], body,
                                limit)[:3], body, SOFT, 23)
        return top + height

    def grid(self):
        stories = self.data["grid"]
        bottom = self.cell(EDGE, self.y, stories[0], ART[0])
        self.cell(EDGE + COLUMN + GAP, self.y, stories[1], ART[1])
        self.y = bottom + 18
        bottom = self.cell(EDGE, self.y, stories[2], ART[2])
        self.cell(EDGE + COLUMN + GAP, self.y, stories[3], ART[3])
        self.y = bottom + 18

    def bottom_pair(self):
        stories = self.data["bottom"]
        top = self.y
        self.pen.rectangle([EDGE, top, SIDE - EDGE, top + 118],
                           fill=WASH, outline=INK, width=1)
        for index, story in enumerate(stories):
            x = EDGE + 18 + index * (COLUMN + GAP)
            head = typeface(24, bold=True)
            y = paint_lines(
                self.pen, x, top + 12,
                split_lines(self.pen, story["headline"], head,
                            COLUMN - 24)[:2], head, INK, 28)
            body = typeface(19)
            paint_lines(self.pen, x, y + 2,
                        split_lines(self.pen, story["summary"], body,
                                    COLUMN - 24)[:2], body, SOFT, 23)
        self.y = top + 118 + 10

    def footer(self):
        face = typeface(18)
        centred(self.pen, self.y, self.data["footer"], face, FAINT)

    def render(self, path):
        self.masthead()
        self.lead()
        self.grid()
        self.bottom_pair()
        self.footer()
        self.pen.rectangle([5, 5, SIDE - 6, SIDE - 6], outline=INK,
                           width=2)
        self.canvas.save(path, "PNG", optimize=True)


def main():
    with open(os.path.join(ROOT, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    out = os.path.join(ROOT, "entry.png")
    Page(data).render(out)
    print("entry.png written:", os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
