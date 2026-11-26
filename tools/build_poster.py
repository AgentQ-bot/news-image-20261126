#!/usr/bin/env python3
"""Render a one-page poster summing up Thursday 26 November 2026.

Pure Pillow build: a navy masthead, six story cards in a 2x3 grid,
and a footer strip. Output is a 1024x1024 PNG written next to the
repository root as entry.png.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "entry.png"

W = H = 1024
MARGIN = 28
GAP = 16
MASTHEAD_H = 168
FOOTER_H = 64

NAVY = (13, 27, 52)
PAPER = (247, 244, 238)
CARD = (255, 255, 255)
INK = (24, 28, 36)
MUTED = (92, 99, 112)
RULE = (214, 208, 196)
GOLD = (201, 149, 44)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

STORIES = [
    (
        "NORTH KOREA",
        (178, 34, 52),
        "Kim orders wider tactical nuclear deployment",
        "State media said Thursday that Kim Jong Un ordered "
        "battlefield nuclear weapons spread across more missions, "
        "with fissile-material output still expanding.",
    ),
    (
        "UKRAINE",
        (31, 95, 168),
        "Dawn drone strike kills two in Kharkiv",
        "A Russian drone hit a Kharkiv high-rise before dawn, "
        "killing two people. Kyiv's overnight missile-strike "
        "injury toll rose to seven.",
    ),
    (
        "EUROPEAN UNION",
        (38, 110, 84),
        "EU leaders open budget and Ukraine-loan talks",
        "The 27 leaders met in Brussels on Thursday to narrow gaps "
        "over the 2028-2034 budget and a 45 billion euro loan "
        "for Ukraine.",
    ),
    (
        "TRADE",
        (140, 82, 20),
        "Pacific bloc meets ASEAN and EU in Hanoi",
        "CPTPP ministers met ASEAN counterparts and the EU trade "
        "chief on Thursday, backing open trade and resilient "
        "supply chains.",
    ),
    (
        "MARKETS",
        (104, 62, 140),
        "Asian shares rally, shrugging off US tariffs",
        "Stocks rose across Asia on Thursday as investors judged "
        "the new US tariff plan less damaging than feared. "
        "Tokyo and Seoul led gains.",
    ),
    (
        "INDONESIA",
        (160, 84, 24),
        "Mine death toll rises to 13 in West Java",
        "Rescuers resumed searching a flooded illegal gold mine "
        "on Thursday. Thirteen workers were dead and thirteen "
        "still missing.",
    ),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_masthead(draw):
    draw.rectangle([0, 0, W, MASTHEAD_H], fill=NAVY)
    draw.rectangle([0, MASTHEAD_H - 6, W, MASTHEAD_H], fill=GOLD)
    title_f = font(SERIF_BOLD, 58)
    date_f = font(SANS_BOLD, 34)
    sub_f = font(SANS, 21)
    title = "THE WORLD IN A DAY"
    tw = draw.textlength(title, font=title_f)
    draw.text(((W - tw) / 2, 22), title, font=title_f, fill=(255, 255, 255))
    date = "Thursday, 26 November 2026"
    dw = draw.textlength(date, font=date_f)
    draw.text(((W - dw) / 2, 92), date, font=date_f, fill=(240, 205, 120))
    sub = "Six stories that shaped the day"
    sw = draw.textlength(sub, font=sub_f)
    draw.text(((W - sw) / 2, 132), sub, font=sub_f, fill=(196, 205, 220))


def draw_card(draw, x, y, w, h, story):
    kicker, accent, headline, summary = story
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, outline=RULE, width=2)
    draw.rectangle([x, y + 14, x + 8, y + h - 14], fill=accent)
    pad = 26
    inner_w = w - pad - 20
    kicker_f = font(SANS_BOLD, 20)
    head_f = font(SERIF_BOLD, 29)
    body_f = font(SANS, 20)
    cy = y + 16
    draw.text((x + pad, cy), kicker, font=kicker_f, fill=accent)
    cy += 29
    for line in wrap(draw, headline, head_f, inner_w):
        draw.text((x + pad, cy), line, font=head_f, fill=INK)
        cy += 34
    cy += 5
    draw.line([x + pad, cy, x + pad + 54, cy], fill=accent, width=3)
    cy += 11
    for line in wrap(draw, summary, body_f, inner_w):
        draw.text((x + pad, cy), line, font=body_f, fill=(52, 58, 68))
        cy += 25


def draw_footer(draw):
    y = H - FOOTER_H
    draw.rectangle([0, y, W, H], fill=NAVY)
    f = font(SANS, 20)
    text = "Compiled from reports published on 26 November 2026  |  One image, one day"
    tw = draw.textlength(text, font=f)
    draw.text(((W - tw) / 2, y + 20), text, font=f, fill=(220, 226, 238))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    grid_top = MASTHEAD_H + 18
    grid_bottom = H - FOOTER_H - 18
    card_w = (W - 2 * MARGIN - GAP) // 2
    card_h = (grid_bottom - grid_top - 2 * GAP) // 3
    for i, story in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (card_w + GAP)
        y = grid_top + row * (card_h + GAP)
        draw_card(draw, x, y, card_w, card_h, story)
    draw_footer(draw)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
