"""Willowmere Hospice — flower-themed demo image set for CHAMP campaign layouts.
Fictional charity. Sizes and composition follow CHAMP's per-layout guidance
("How your image sits in this layout"). Renders SVG scenes with Playwright Chromium."""
import math, random, pathlib
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).parent

PLUM = "#4B2E4F"; PLUM2 = "#6B4570"; SAGE = "#6E8F72"; SAGE_D = "#4E6E54"; SAGE_L = "#A9C1A3"
PINK = "#E8A0B4"; ROSE = "#D9667F"; BUTTER = "#F4D06F"; CREAM = "#FBF7F0"; LAV = "#A99BD1"
BLUE = "#7FA7D9"; PEACH = "#F6C6A8"; WHITE = "#FFFFFF"; LEAF = "#5E8C5A"; LEAF_D = "#3F6B44"

# ---------------------------------------------------------------- primitives
def flower5(cx, cy, r, petal, centre=BUTTER, rot=0, n=5, op=1):
    s = f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.0f})" opacity="{op:.2f}">'
    for i in range(n):
        a = 360 / n * i
        s += f'<ellipse cx="0" cy="{-r*0.55:.1f}" rx="{r*0.42:.1f}" ry="{r*0.6:.1f}" fill="{petal}" transform="rotate({a:.0f})"/>'
    return s + f'<circle r="{r*0.3:.1f}" fill="{centre}"/></g>'

def daisy(cx, cy, r, petal=WHITE, centre=BUTTER, rot=0, op=1):
    s = f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.0f})" opacity="{op:.2f}">'
    for i in range(14):
        s += f'<ellipse cx="0" cy="{-r*0.62:.1f}" rx="{r*0.16:.1f}" ry="{r*0.45:.1f}" fill="{petal}" transform="rotate({i*360/14:.0f})"/>'
    return s + f'<circle r="{r*0.3:.1f}" fill="{centre}"/></g>'

def sunflower(cx, cy, r, rot=0):
    s = f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.0f})">'
    for ring, (col, k) in enumerate([("#E9A93A", 1.0), (BUTTER, 0.86)]):
        for i in range(22):
            a = i * 360 / 22 + ring * 8
            s += f'<ellipse cx="0" cy="{-r*0.72*k:.1f}" rx="{r*0.14:.1f}" ry="{r*0.38*k:.1f}" fill="{col}" transform="rotate({a:.1f})"/>'
    s += f'<circle r="{r*0.42:.1f}" fill="#6B4226"/><circle r="{r*0.3:.1f}" fill="#4E2F1B"/>'
    rr = random.Random(int(cx * 7 + cy))
    for _ in range(26):
        a, d = rr.uniform(0, 6.28), rr.uniform(0, r * 0.38)
        s += f'<circle cx="{d*math.cos(a):.1f}" cy="{d*math.sin(a):.1f}" r="{r*0.025:.1f}" fill="#8A5A34"/>'
    return s + '</g>'

def tulip(x, y, h, col, lean=0):
    hx, hy = x + lean, y - h
    s = f'<path d="M{x} {y} Q{x+lean*0.3} {y-h*0.5} {hx} {hy}" stroke="{LEAF}" stroke-width="{max(2,h*0.04):.1f}" fill="none"/>'
    s += f'<path d="M{x} {y-h*0.15} Q{x-h*0.18} {y-h*0.45} {x-h*0.05} {y-h*0.62} Q{x-h*0.02} {y-h*0.35} {x} {y-h*0.15}Z" fill="{LEAF}"/>'
    w = h * 0.16
    s += f'<path d="M{hx-w} {hy} Q{hx-w} {hy-w*1.9} {hx} {hy-w*1.6} Q{hx+w} {hy-w*1.9} {hx+w} {hy} Q{hx} {hy+w*0.7} {hx-w} {hy}Z" fill="{col}"/>'
    s += f'<path d="M{hx-w*0.35} {hy-w*0.2} Q{hx} {hy-w*2.1} {hx+w*0.35} {hy-w*0.2}Z" fill="{WHITE}" opacity=".18"/>'
    return s

def lavender(x, y, h, col=LAV):
    s = f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y-h}" stroke="{SAGE}" stroke-width="{max(1.5,h*0.025):.1f}"/>'
    for i in range(7):
        yy = y - h + i * h * 0.06
        s += f'<ellipse cx="{x-h*0.025}" cy="{yy:.1f}" rx="{h*0.03:.1f}" ry="{h*0.045:.1f}" fill="{col}"/><ellipse cx="{x+h*0.025}" cy="{yy+h*0.02:.1f}" rx="{h*0.03:.1f}" ry="{h*0.045:.1f}" fill="{col}"/>'
    return s

def leaf(x, y, l, ang, col=LEAF):
    return f'<path d="M0 0 Q{l*0.5} {-l*0.28} {l} 0 Q{l*0.5} {l*0.28} 0 0Z" fill="{col}" transform="translate({x:.1f},{y:.1f}) rotate({ang:.0f})"/>'

def grass(x, y, h, col=SAGE_D):
    return f'<path d="M{x} {y} Q{x+h*0.15} {y-h*0.6} {x+h*0.35} {y-h}" stroke="{col}" stroke-width="{max(1.2,h*0.05):.1f}" fill="none" stroke-linecap="round"/>'

def meadow(w, top, bottom, n, seed, palette, minr=3, maxr=16, density_x=None):
    """Depth-scattered wildflowers between rows top..bottom (small at the back)."""
    r = random.Random(seed); items = []
    for _ in range(n):
        y = r.uniform(top, bottom)
        d = (y - top) / max(1, bottom - top)
        x = density_x(r) if density_x else r.uniform(-10, w + 10)
        rad = minr + (maxr - minr) * d * r.uniform(0.7, 1.15)
        items.append((y, x, rad, r.random(), r.choice(palette), r.uniform(0, 70)))
    s = ""
    for y, x, rad, kind, col, rot in sorted(items):
        if rad > 6:
            s += f'<line x1="{x:.1f}" y1="{y+rad*0.3:.1f}" x2="{x+rad*0.1:.1f}" y2="{y+rad*2.4:.1f}" stroke="{LEAF}" stroke-width="{rad*0.12:.1f}"/>'
        if kind < 0.45:
            s += flower5(x, y, rad, col, rot=rot)
        elif kind < 0.75:
            s += daisy(x, y, rad, rot=rot)
        else:
            s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad*0.5:.1f}" fill="{col}"/>'
    return s

def petals_float(w, h, n, seed, maxy=None, cols=(PINK, WHITE, "#F3C1CF")):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x, y = r.uniform(0, w), r.uniform(0, maxy or h)
        sz = r.uniform(4, 11)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{sz:.1f}" ry="{sz*0.55:.1f}" fill="{r.choice(cols)}" opacity="{r.uniform(.45,.9):.2f}" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    return s

def butterfly(x, y, s, col=LAV):
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="-9" cy="-6" rx="10" ry="8" fill="{col}"/>'
            f'<ellipse cx="9" cy="-6" rx="10" ry="8" fill="{col}"/><ellipse cx="-7" cy="7" rx="7" ry="6" fill="{col}" opacity=".85"/>'
            f'<ellipse cx="7" cy="7" rx="7" ry="6" fill="{col}" opacity=".85"/><rect x="-1.5" y="-10" width="3" height="20" rx="1.5" fill="{PLUM}"/></g>')

def blossom_tree(x, base, s, trunk="#6B4F43", bloom=(PINK, "#F3C1CF", WHITE), seed=1):
    r = random.Random(seed)
    out = f'<g transform="translate({x},{base}) scale({s})">'
    out += f'<path d="M-14 0 Q-10 -90 -4 -160 Q-40 -200 -90 -215 M-4 -160 Q20 -210 70 -235 M-6 -120 Q30 -140 60 -150 M-8 0 Q-2 -80 2 -160 L14 0Z" stroke="{trunk}" stroke-width="16" fill="none" stroke-linecap="round"/>'
    out += f'<path d="M-16 0 Q-10 -80 -6 -160 L8 -160 Q12 -80 18 0Z" fill="{trunk}"/>'
    for _ in range(46):
        a, d = r.uniform(0, 6.28), r.uniform(0, 1)
        cx, cy = math.cos(a) * 150 * d, -230 + math.sin(a) * 90 * d
        out += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r.uniform(26,48):.0f}" fill="{r.choice(bloom)}" opacity="{r.uniform(.75,1):.2f}"/>'
    for _ in range(40):
        a, d = r.uniform(0, 6.28), r.uniform(0.2, 1.1)
        out += flower5(math.cos(a) * 150 * d, -230 + math.sin(a) * 95 * d, r.uniform(5, 9), WHITE, centre=ROSE, rot=r.uniform(0, 70))
    return out + '</g>'

def bench(x, y, s, col="#8A6A55"):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="{col}">'
            f'<rect x="-70" y="-46" width="140" height="10" rx="3"/><rect x="-70" y="-62" width="140" height="8" rx="3"/>'
            f'<rect x="-74" y="-30" width="148" height="10" rx="3"/><rect x="-64" y="-30" width="8" height="30"/>'
            f'<rect x="56" y="-30" width="8" height="30"/><rect x="-66" y="-66" width="7" height="40"/><rect x="59" y="-66" width="7" height="40"/></g>')

def svg(w, h, defs, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{defs}</defs>{body}</svg>'

def sun(cx, cy, r, col="#FFF1C9"):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r*4}" fill="url(#sunhalo)"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>')

SUN_DEFS = (f'<radialGradient id="sunhalo"><stop offset="0" stop-color="#FFF4D6" stop-opacity=".8"/>'
            f'<stop offset=".35" stop-color="#FFE3A8" stop-opacity=".3"/><stop offset="1" stop-color="#FFE3A8" stop-opacity="0"/></radialGradient>')

# ---------------------------------------------------------------- logos
def mark(cx, cy, s, tile, petal, centre):
    """Willowmere mark: a forget-me-not (remembrance) on a rounded tile."""
    k = s / 100
    return (f'<rect x="{cx-50*k:.1f}" y="{cy-50*k:.1f}" width="{100*k:.1f}" height="{100*k:.1f}" rx="{24*k:.1f}" fill="{tile}"/>'
            + flower5(cx, cy - 2 * k, 30 * k, petal, centre=centre, n=5)
            + f'<path d="M{cx} {cy+26*k} Q{cx+4*k} {cy+38*k} {cx+14*k} {cy+42*k}" stroke="{SAGE_L}" stroke-width="{4*k:.1f}" fill="none" stroke-linecap="round"/>'
            + leaf(cx + 10 * k, cy + 38 * k, 16 * k, -30, SAGE_L))

def logo_3x1(text, tag, tile, petal, centre):
    body = (mark(120, 120, 216, tile, petal, centre)
            + f'<text x="256" y="122" font-family="Inter" font-weight="800" font-size="70" fill="{text}" letter-spacing="-2">Willowmere</text>'
            + f'<text x="259" y="190" font-family="Inter" font-weight="600" font-size="46" fill="{tag}" letter-spacing="7">HOSPICE</text>')
    return svg(720, 240, "", body)

def logo_square():
    return svg(512, 512, "", f'<rect width="512" height="512" rx="112" fill="{PLUM}"/>' + mark(256, 256, 400, PLUM, CREAM, BUTTER))

def logo_wide():
    body = (mark(160, 160, 280, PLUM, CREAM, BUTTER)
            + f'<text x="340" y="168" font-family="Inter" font-weight="800" font-size="104" fill="{PLUM}" letter-spacing="-3">Willowmere</text>'
            + f'<text x="346" y="236" font-family="Inter" font-weight="500" font-size="40" fill="{SAGE_D}" letter-spacing="1">Hospice · Care that blooms</text>')
    return svg(1200, 320, "", body)

# ---------------------------------------------------------------- CLASSIC 1600x600 — memory garden at dawn
# CHAMP: wide banner, top and bottom trimmed (more on phones) -> subject in the middle.
def classic():
    w, h = 1600, 600
    defs = (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B9A6D6"/>'
            f'<stop offset=".45" stop-color="#F3C8C8"/><stop offset=".75" stop-color="{PEACH}"/></linearGradient>' + SUN_DEFS)
    b = f'<rect width="{w}" height="{h}" fill="url(#sky)"/>' + sun(800, 330, 46)
    b += f'<path d="M0 360 Q300 300 620 340 T1200 320 T1600 335 V600 H0Z" fill="{SAGE_L}"/>'
    b += f'<path d="M0 410 Q400 360 820 395 T1600 380 V600 H0Z" fill="{SAGE}"/>'
    b += blossom_tree(800, 420, 0.92, seed=3)
    b += bench(800, 422, 1.0)
    b += f'<path d="M640 600 Q760 470 800 425 Q840 470 960 600Z" fill="#D9C7AE"/>'
    b += meadow(w, 420, 600, 520, 5, [PINK, LAV, BLUE, ROSE, BUTTER, WHITE], 3, 18,
                density_x=lambda r: r.choice([r.uniform(-10, 640), r.uniform(960, 1610), r.uniform(-10, 1610)]))
    b += butterfly(560, 300, 1.2) + butterfly(1060, 270, 1.0, BLUE)
    b += petals_float(w, h, 40, 7, 380)
    return svg(w, h, defs, b)

# ---------------------------------------------------------------- COMPACT 1200x480 — a bouquet for someone
# CHAMP: subject centred; logo and headline overlay the lower-left, so that corner stays clear.
def compact():
    w, h = 1200, 480
    defs = (f'<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6EDF3"/><stop offset="1" stop-color="{CREAM}"/></linearGradient>'
            f'<linearGradient id="vase" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8FB3D9"/><stop offset=".5" stop-color="#B9D1EA"/><stop offset="1" stop-color="#7FA7D9"/></linearGradient>')
    b = f'<rect width="{w}" height="{h}" fill="url(#wall)"/>'
    for i in range(0, w, 60):
        b += f'<line x1="{i}" y1="0" x2="{i}" y2="300" stroke="#EADCE6" stroke-width="2"/>'
    T = 300
    b += f'<rect y="{T}" width="{w}" height="{h-T}" fill="#E7D8C6"/><rect y="{T}" width="{w}" height="10" fill="#D8C5AF"/>'
    cx = 600
    # bouquet (centred, upper-middle): stems, leaves, flowers
    r = random.Random(11)
    for i in range(16):
        a = -55 + i * 7.3
        b += f'<line x1="{cx}" y1="{T-20}" x2="{cx+math.sin(math.radians(a))*190:.0f}" y2="{T-20-math.cos(math.radians(a))*190:.0f}" stroke="{LEAF}" stroke-width="4"/>'
    for i in range(14):
        a = r.uniform(-70, 70)
        b += leaf(cx + math.sin(math.radians(a)) * 120, T - 30 - math.cos(math.radians(a)) * 120, r.uniform(50, 70), a - 90 + r.uniform(-30, 30), r.choice([LEAF, LEAF_D, SAGE]))
    blooms = []
    for _ in range(26):
        a, d = r.uniform(-1.25, 1.25), r.uniform(70, 200)
        blooms.append((cx + math.sin(a) * d, T - 30 - math.cos(a) * d * 0.95))
    for x, y in sorted(blooms, key=lambda p: -p[1]):
        k = r.random()
        if k < .35: b += flower5(x, y, r.uniform(22, 30), r.choice([PINK, ROSE, "#F3C1CF"]), rot=r.uniform(0, 70))
        elif k < .6: b += daisy(x, y, r.uniform(20, 26), rot=r.uniform(0, 30))
        elif k < .8: b += tulip(x, y + 30, 46, r.choice([ROSE, PINK, BUTTER]))
        else: b += lavender(x, y + 40, 80)
    # vase
    b += f'<ellipse cx="{cx}" cy="{T+12}" rx="105" ry="12" fill="#000" opacity=".1"/>'
    b += f'<path d="M{cx-60} {T-70} Q{cx-95} {T-20} {cx-70} {T+10} L{cx+70} {T+10} Q{cx+95} {T-20} {cx+60} {T-70}Z" fill="url(#vase)"/>'
    b += f'<rect x="{cx-64}" y="{T-82}" width="128" height="16" rx="8" fill="#9CBDE0"/>'
    b += f'<path d="M{cx-40} {T-40} Q{cx-50} {T-10} {cx-36} {T+2}" stroke="{WHITE}" stroke-width="6" fill="none" opacity=".45" stroke-linecap="round"/>'
    # right side: candle + small framed photo (keeps the lower-left clear)
    b += f'<rect x="900" y="{T-120}" width="110" height="128" rx="6" fill="{PLUM2}"/><rect x="910" y="{T-110}" width="90" height="108" fill="#F3E5EC"/>'
    b += flower5(955, T - 56, 22, PINK) + f'<rect x="1040" y="{T-62}" width="34" height="70" rx="5" fill="{CREAM}" stroke="#E2D2C0" stroke-width="2"/>'
    b += f'<path d="M1057 {T-90} Q1066 {T-76} 1057 {T-64} Q1048 {T-76} 1057 {T-90}Z" fill="{BUTTER}"/><circle cx="1057" cy="{T-74}" r="30" fill="#FFE7A8" opacity=".25"/>'
    b += petals_float(w, 300, 14, 4)
    return svg(w, h, defs, b)

# ---------------------------------------------------------------- HERO BANNER 1920x600 — the hospice garden border
# CHAMP: thin full-width strip, most height cut off -> subject across the horizontal middle.
# Strip is cover at 50% 40%: rows ~190-320 on wide desktops, so the flower border lives in ~200-330.
def hero_banner():
    w, h = 1920, 600
    defs = (f'<linearGradient id="sky2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C7B8E0"/>'
            f'<stop offset=".33" stop-color="#F2D3D3"/><stop offset=".42" stop-color="{PEACH}"/></linearGradient>' + SUN_DEFS)
    b = f'<rect width="{w}" height="{h}" fill="url(#sky2)"/>' + sun(1500, 170, 30)
    b += f'<path d="M0 225 Q400 190 860 214 T1920 205 V600 H0Z" fill="{SAGE_L}"/>'
    b += f'<rect y="330" width="{w}" height="270" fill="{SAGE_D}"/>'
    b += f'<path d="M0 318 L1920 296 L1920 330 L0 340Z" fill="#E4D6C2"/>'  # garden path
    r = random.Random(21)
    cols = [ROSE, PINK, BUTTER, WHITE, "#C85A73", LAV]
    # back row: lavender hedge; middle: tulips; front: daisies — all within rows ~205-320
    for x in range(0, w, 14):
        b += lavender(x + r.uniform(-4, 4), 262 - x * 0.006, r.uniform(42, 56))
    for x in range(10, w, 26):
        b += tulip(x + r.uniform(-5, 5), 300 - x * 0.008, r.uniform(46, 62), r.choice(cols), lean=r.uniform(-5, 5))
    for x in range(0, w, 22):
        b += daisy(x + r.uniform(-6, 6), 312 - x * 0.009 + r.uniform(-4, 4), r.uniform(7, 10))
    b += butterfly(700, 205, 0.8) + butterfly(1260, 215, 0.7, BLUE)
    for x in range(0, w, 9):
        b += grass(x, 600, r.uniform(30, 90), LEAF_D)
    return svg(w, h, defs, b)

# ---------------------------------------------------------------- IMAGE LEFT 1120x1280 — flowers on the windowsill
# CHAMP: portrait column on desktop, short banner on a phone -> subject centred.
def image_left():
    w, h = 1120, 1280
    defs = (f'<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CFE0F0"/><stop offset=".6" stop-color="#F7E3D3"/><stop offset="1" stop-color="{PEACH}"/></linearGradient>'
            f'<linearGradient id="room" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EFE3EA"/><stop offset="1" stop-color="#E4D3DE"/></linearGradient>'
            f'<linearGradient id="vase2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PLUM2}"/><stop offset=".5" stop-color="#8D6492"/><stop offset="1" stop-color="{PLUM}"/></linearGradient>'
            f'<linearGradient id="beam" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF4D6" stop-opacity=".55"/><stop offset="1" stop-color="#FFF4D6" stop-opacity="0"/></linearGradient>')
    b = f'<rect width="{w}" height="{h}" fill="url(#room)"/>'
    # window
    b += f'<rect x="150" y="120" width="820" height="760" rx="18" fill="{CREAM}"/>'
    b += f'<rect x="185" y="155" width="750" height="690" fill="url(#glass)"/>'
    b += f'<path d="M185 560 Q400 500 560 535 T935 520 V845 H185Z" fill="{SAGE_L}"/>'
    b += f'<path d="M185 640 Q450 590 700 620 T935 610 V845 H185Z" fill="{SAGE}"/>'
    b += blossom_tree(330, 650, 0.75, seed=8) + blossom_tree(820, 640, 0.6, seed=9)
    b += f'<rect x="552" y="155" width="16" height="690" fill="{CREAM}"/><rect x="185" y="492" width="750" height="16" fill="{CREAM}"/>'
    b += f'<path d="M185 155 L700 155 L1120 1000 L1120 1280 L520 1280Z" fill="url(#beam)"/>'
    # sill
    b += f'<rect x="110" y="880" width="900" height="40" rx="6" fill="#F4ECE2"/><rect x="130" y="920" width="860" height="22" fill="#E2D5C5"/>'
    # vase + bouquet centred on the sill
    cx, base = 560, 880
    r = random.Random(17)
    for i in range(18):
        a = -50 + i * 6
        b += f'<line x1="{cx}" y1="{base-120}" x2="{cx+math.sin(math.radians(a))*260:.0f}" y2="{base-120-math.cos(math.radians(a))*260:.0f}" stroke="{LEAF}" stroke-width="5"/>'
    for _ in range(18):
        a = r.uniform(-60, 60)
        b += leaf(cx + math.sin(math.radians(a)) * 170, base - 130 - math.cos(math.radians(a)) * 170, r.uniform(60, 90), a - 90 + r.uniform(-25, 25), r.choice([LEAF, LEAF_D, SAGE]))
    pts = []
    for _ in range(30):
        a, d = r.uniform(-1.1, 1.1), r.uniform(110, 300)
        pts.append((cx + math.sin(a) * d, base - 130 - math.cos(a) * d * 0.9))
    for x, y in sorted(pts, key=lambda p: -p[1]):
        k = r.random()
        if k < .4: b += flower5(x, y, r.uniform(30, 40), r.choice([PINK, ROSE, "#F3C1CF", WHITE]), rot=r.uniform(0, 70))
        elif k < .65: b += daisy(x, y, r.uniform(26, 34), rot=r.uniform(0, 30))
        elif k < .85: b += tulip(x, y + 40, 64, r.choice([ROSE, PINK, BUTTER]))
        else: b += lavender(x, y + 60, 120)
    b += f'<path d="M{cx-80} {base-150} Q{cx-130} {base-60} {cx-90} {base} L{cx+90} {base} Q{cx+130} {base-60} {cx+80} {base-150}Z" fill="url(#vase2)"/>'
    b += f'<rect x="{cx-86}" y="{base-166}" width="172" height="22" rx="11" fill="#8D6492"/>'
    b += f'<path d="M{cx-52} {base-110} Q{cx-70} {base-50} {cx-50} {base-14}" stroke="{WHITE}" stroke-width="8" fill="none" opacity=".3" stroke-linecap="round"/>'
    # card propped against the vase
    b += f'<g transform="rotate(-8 790 860)"><rect x="740" y="800" width="110" height="80" rx="4" fill="{WHITE}"/>' + flower5(795, 838, 16, BLUE) + '</g>'
    b += petals_float(w, h, 18, 13, 860)
    return svg(w, h, defs, b)

# ---------------------------------------------------------------- IMAGE RIGHT 1120x1280 — sunflowers turning to the light
# CHAMP: subject centred. Its headline overlay covers roughly the top half of this column on
# desktop, so the sunflower heads sit just below centre (still inside the phone's short-banner crop).
def image_right():
    w, h = 1120, 1280
    defs = (f'<linearGradient id="sky4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9FC3E8"/>'
            f'<stop offset=".55" stop-color="#DCEBF5"/><stop offset=".8" stop-color="#FCE9C8"/></linearGradient>' + SUN_DEFS)
    b = f'<rect width="{w}" height="{h}" fill="url(#sky4)"/>' + sun(860, 300, 60)
    b += f'<path d="M0 860 Q300 800 620 840 T1120 820 V1280 H0Z" fill="{SAGE_L}"/>'
    r = random.Random(23)
    # back row of small sunflowers
    for x in range(-20, w + 40, 70):
        y = 850 + r.uniform(-10, 10)
        b += f'<line x1="{x}" y1="{y}" x2="{x}" y2="1280" stroke="{LEAF_D}" stroke-width="6"/>' + sunflower(x, y, r.uniform(26, 32), r.uniform(0, 30))
    b += f'<rect y="960" width="{w}" height="320" fill="{SAGE}"/>'
    # three hero sunflowers, centred, heads just below the middle
    for x, y, rad, lean in [(420, 760, 92, -30), (700, 700, 110, 25), (560, 880, 80, 0)]:
        b += f'<path d="M{x} {y} Q{x+lean} {y+260} {x+lean*0.6} 1280" stroke="{LEAF_D}" stroke-width="16" fill="none"/>'
        b += leaf(x + lean * 0.5, y + 220, 110, -20, LEAF) + leaf(x + lean * 0.6, y + 300, 100, 200, LEAF_D)
        b += sunflower(x, y, rad, r.uniform(0, 20))
    for x in range(0, w, 8):
        b += grass(x, 1280, r.uniform(60, 160), LEAF_D)
    b += butterfly(300, 560, 1.4, PINK) + butterfly(860, 610, 1.1)
    return svg(w, h, defs, b)

# ---------------------------------------------------------------- IMMERSIVE 1920x1080 — golden-hour meadow
# CHAMP: form card floats over the CENTRE; on a phone only the top shows; no words in the image.
# Subject (blossom tree + memorial bench) on the left, sun on the right, petals across the top.
def immersive():
    w, h = 1920, 1080
    defs = (f'<linearGradient id="sky5" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E7BB8"/>'
            f'<stop offset=".35" stop-color="#D7A6B7"/><stop offset=".6" stop-color="#F6C29A"/><stop offset=".72" stop-color="#FBDDA8"/></linearGradient>' + SUN_DEFS)
    b = f'<rect width="{w}" height="{h}" fill="url(#sky5)"/>' + sun(1560, 560, 70)
    b += f'<path d="M0 640 Q360 580 780 625 T1500 600 T1920 615 V1080 H0Z" fill="#B7A27E" opacity=".55"/>'
    b += f'<path d="M0 690 Q420 640 900 675 T1920 660 V1080 H0Z" fill="{SAGE_L}"/>'
    b += f'<path d="M0 760 Q520 710 1040 745 T1920 735 V1080 H0Z" fill="{SAGE}"/>'
    b += blossom_tree(360, 800, 1.55, seed=31)
    b += bench(470, 806, 1.3, "#6E5444")
    b += meadow(w, 700, 1080, 900, 33, [PINK, LAV, BUTTER, WHITE, ROSE, BLUE], 2.5, 22)
    b += petals_float(w, h, 90, 35, 560)
    b += butterfly(640, 360, 1.3, BLUE) + butterfly(1250, 330, 1.1, LAV)
    return svg(w, h, defs, b)

# (filename, scene, output width, output height, format) — CHAMP's recommended sizes
JOBS = [
    ("willowmere-logo-240x80-light.png", lambda: logo_3x1(CREAM, BUTTER, PLUM2, CREAM, BUTTER), 240, 80, "png"),
    ("willowmere-logo-240x80-dark.png", lambda: logo_3x1(PLUM, SAGE_D, PLUM, CREAM, BUTTER), 240, 80, "png"),
    ("willowmere-logo-square.png", logo_square, 512, 512, "png"),
    ("willowmere-logo-wide.png", logo_wide, 1200, 320, "png"),
    ("classic-memory-garden-1600x600.jpg", classic, 1600, 600, "jpeg"),
    ("compact-bouquet-1200x480.jpg", compact, 1200, 480, "jpeg"),
    ("hero-banner-garden-border-1920x600.jpg", hero_banner, 1920, 600, "jpeg"),
    ("image-left-windowsill-1120x1280.jpg", image_left, 1120, 1280, "jpeg"),
    ("image-right-sunflowers-1120x1280.jpg", image_right, 1120, 1280, "jpeg"),
    ("immersive-golden-meadow-1920x1080.jpg", immersive, 1920, 1080, "jpeg"),
]

if __name__ == "__main__":
    with sync_playwright() as p:
        br = p.chromium.launch()
        for name, fn, w, h, fmt in JOBS:
            pg = br.new_page(viewport={"width": w, "height": h})
            bg = "transparent" if fmt == "png" else "#fff"
            pg.set_content(f'<html><head><style>svg{{display:block;width:{w}px;height:{h}px}}</style></head>'
                           f'<body style="margin:0;background:{bg}">{fn()}</body></html>')
            kw = {"type": fmt, "omit_background": fmt == "png"}
            if fmt == "jpeg": kw["quality"] = 88
            pg.screenshot(path=str(OUT / name), **kw)
            pg.close()
        br.close()
    for f in sorted(OUT.glob("*.*")):
        if f.suffix in (".jpg", ".png"): print(f.name, f.stat().st_size // 1024, "KB")
