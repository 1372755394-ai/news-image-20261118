#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261118 entry.

Renders a newspaper front page for Wednesday 18 November 2026 with PIL
(crisp vector text, no garbled AI text) around the AI-generated hero
illustration in assets/. Run once locally; the committed entry.png is what
the entry program copies to /output/entry.png.

Facts (all reported on 18 Nov 2026, checked against live news that day):
- Nvidia Q3 (reported Tue evening): revenue $115.8bn +103% YoY, EPS $2.68
  vs $2.47 expected; Q4 guide $130bn (+/-3%) vs ~$125.3bn; data-centre
  $107.6bn; board ruled out reinstating Jensen Huang; H200 shipments to
  China stopped; shares ~+4.8% after hours.
- Anthropic IPO prices Wed evening: $70-$78 range, ~825m shares, up to
  ~$64bn raise, valuation up to ~$1.4tn; first trade Thu 19 Nov as ANT.
- FOMC minutes (Oct 27-28 meeting, rates held 3.75-4.00%) released 2pm ET
  Wed; December hike ~95% priced.
- APEC Shenzhen: Xi and Putin met Wed, denounced Western protectionism /
  sanctions; Trump-Xi-Putin trilateral Thu; Trump in Manila, met Marcos;
  Quad leaders met.
- Gulf: Iran widened attacks on US bases (incl. Kuwait); US struck Qeshm
  Island; UAE tanker hit in Hormuz.
- Ukraine: Crimea bridge crippled Tue (follow-up Wed); UK GBP240m missile
  package (>1,000 short-range air-defence missiles); Germany new aid.
- Gaza: Israel launched a ground operation in central Gaza; WHO called for
  unobstructed aid; hypothermia deaths feared.
- Markets Tue: S&P 500 -1.03% (4th straight fall), Nasdaq -0.74%;
  10-yr ~5.10%; gold below $3,800 (lowest in >1 yr); dollar near 19-mo high.
- UK inflation 3.6%; UK sanctioned 8 firms over West Bank settlements.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO = os.path.join(
    HERE, "assets",
    "media-generation-hero-chip-globe-0-2c33e3b5-dc3c-45b9-9e57-59bd1ae14b06.webp")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
M = 30  # margin
PAPER = (246, 241, 231)
INK = (17, 17, 17)
RED = (155, 28, 28)
NAVY = (16, 32, 64)
GREY = (90, 86, 78)

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centered(draw, y, text, fnt, fill=INK):
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")
    return y + fnt.size


def rule(draw, y, w=2, x0=M, x1=W - M):
    draw.line([(x0, y), (x1, y)], fill=INK, width=w)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
y = 16
centered(d, y, "O N E   D A Y  ·  O N E   P A G E", font(F_SANS_B, 15), GREY)
y = 38
centered(d, y, "THE WORLD", font(F_SERIF, 96))
y = 138
rule(d, y, 3)
rule(d, y + 5, 1)
y = 152
centered(d, y, "WEDNESDAY,  18 NOVEMBER 2026", font(F_SERIF, 31), RED)
y = 190
rule(d, y, 1)

# ---- lead headline + deck ----
y = 202
centered(d, y, "NVIDIA BEATS AND RAISES", font(F_SERIF, 56))
y = 262
deck = ("Revenue $115.8bn, up 103% — and a $130bn guide lifts the shares, "
        "as Anthropic prices its record IPO tonight")
for line in wrap(d, deck, font(F_SANS, 20), W - 2 * M - 40):
    centered(d, y, line, font(F_SANS, 20))
    y += 26

# ---- hero image ----
hero = Image.open(HERO).convert("RGB")  # 1920x1280
# crop a wide band: chip + horizon + lit map (centre ~42% down)
cw, ch = hero.size
band_h = int(cw * 290 / (W - 2 * M))  # match target aspect
top = int(ch * 0.10)
hero = hero.crop((0, top, cw, top + band_h))
hero = hero.resize((W - 2 * M, 290), Image.LANCZOS)
img.paste(hero, (M, y + 8))
y = y + 8 + 290 + 8
d.text((M, y), "A golden chip over a world lit by markets: AI earnings set the tone "
       "for a day of summits, war and rate-watch.  (Illustration)",
       font=font(F_SERIF_I, 15), fill=GREY)
y += 24

# ---- markets ticker ----
d.rectangle([M, y, W - M, y + 34], fill=NAVY)
d.text((W // 2, y + 17),
       "S&P 500  −1.03% Tue  ·  NASDAQ  −0.74%  ·  10-YR  5.10%  ·  "
       "GOLD below $3,800  ·  DOLLAR near 19-mo high",
       font=font(F_SANS_B, 16), fill=(255, 255, 255), anchor="mm")
y += 34 + 10

# ---- story grid: 2 cols x 3 rows ----
stories = [
    ("ANTHROPIC IPO",
     "Claude-maker prices record IPO tonight",
     "$70–$78 a share, ~825m shares, value up to ~$1.4tn; first trade "
     "Thursday as ANT on Nasdaq."),
    ("THE FED",
     "Minutes land at 2pm ET; Dec hike ~95% priced",
     "October meeting held rates at 3.75–4.00%; markets read the minutes "
     "for what comes in January."),
    ("APEC · SHENZHEN",
     "Xi and Putin meet; Trump trilateral Thursday",
     "Both denounce Western sanctions and protectionism; Trump in Manila "
     "as Quad leaders meet."),
    ("THE GULF",
     "Iran widens attacks on US bases",
     "US strikes Qeshm Island; a tanker is hit in Hormuz; the Navy warns "
     "the war is straining stocks."),
    ("UKRAINE",
     "Crimea bridge crippled; allies rush arms",
     "UK sends £240m of missiles; Germany pledges air defences and "
     "F-16 ammunition."),
    ("GAZA",
     "Israel launches Gaza ground operation",
     "WHO urges unobstructed aid; hypothermia deaths feared as winter "
     "bites in the enclave."),
]
col_w = (W - 2 * M - 24) // 2
row_h = 84
gx0 = M
for i, (kick, head, body) in enumerate(stories):
    cx = gx0 + (i % 2) * (col_w + 24)
    cy = y + (i // 2) * row_h
    d.text((cx, cy), kick, font=font(F_SANS_B, 14), fill=RED)
    hl = wrap(d, head, font(F_SERIF, 23), col_w)
    hy = cy + 19
    for line in hl[:1]:
        d.text((cx, hy), line, font=font(F_SERIF, 23), fill=INK)
        hy += 27
    by = hy + 1
    for line in wrap(d, body, font(F_SANS, 15), col_w)[:2]:
        d.text((cx, by), line, font=font(F_SANS, 15), fill=(51, 51, 51))
        by += 19
    if i % 2 == 0:
        d.line([(cx + col_w + 12, cy), (cx + col_w + 12, cy + row_h - 12)],
               fill=(200, 192, 175), width=1)

y = y + 3 * row_h + 2
rule(d, y, 1)
y += 8
d.text((M, y), "ALSO:  UK inflation 3.6%  ·  Britain sanctions 8 firms over West Bank "
       "building  ·  Jeffries wins Speaker nomination  ·  Target and Lowe’s slide",
       font=font(F_SANS_B, 14), fill=INK)
y += 24
d.text((W // 2, y), "Every story above happened or was first reported on "
       "Wednesday 18 November 2026.",
       font=font(F_SERIF_I, 14), fill=GREY, anchor="ma")

img.save(OUT, "JPEG", quality=88, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
