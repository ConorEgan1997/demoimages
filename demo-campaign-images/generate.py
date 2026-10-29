"""Lantern Trust demo image set for CHAMP campaign layouts.
Renders SVG scenes to JPG/PNG with Playwright Chromium."""
import random, math, pathlib
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).parent / "demo-campaign-images"
OUT.mkdir(exist_ok=True)

NAVY = "#14233C"; NAVY2 = "#1E3456"; INDIGO = "#2B3F6B"
AMBER = "#F2A93B"; GOLD = "#FFD27A"; CREAM = "#FBF4E8"
CORAL = "#E2725B"; TEAL = "#2F7F79"; SNOW = "#F4F7FB"

def stars(w, h, n, seed, maxy=None):
    r = random.Random(seed); maxy = maxy or h
    out = []
    for _ in range(n):
        x, y = r.uniform(0, w), r.uniform(0, maxy)
        s = r.choice([0.8, 1, 1.2, 1.6, 2.2])
        o = r.uniform(0.35, 0.95)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s}" fill="#fff" opacity="{o:.2f}"/>')
    return "".join(out)

def snow(w, h, n, seed):
    r = random.Random(seed); out = []
    for _ in range(n):
        x, y = r.uniform(0, w), r.uniform(0, h)
        s = r.uniform(1.5, 4.5)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s:.1f}" fill="#fff" opacity="{r.uniform(.5,.95):.2f}"/>')
    return "".join(out)

def lantern_glyph(cx, cy, s, body=AMBER, frame=CREAM, flame=GOLD, glow=True):
    """Brand lantern mark centred at cx,cy; s = height."""
    k = s / 100
    g = f'<circle cx="{cx}" cy="{cy+8*k}" r="{46*k}" fill="url(#glow)"/>' if glow else ""
    return f'''{g}<g transform="translate({cx-50*k},{cy-50*k}) scale({k})">
      <path d="M42 6 a8 8 0 0 1 16 0" fill="none" stroke="{frame}" stroke-width="5" stroke-linecap="round"/>
      <path d="M30 18 h40 l-6 -10 h-28 z" fill="{frame}"/>
      <rect x="26" y="18" width="48" height="8" rx="3" fill="{frame}"/>
      <rect x="30" y="26" width="40" height="56" rx="10" fill="{body}"/>
      <rect x="30" y="26" width="40" height="56" rx="10" fill="none" stroke="{frame}" stroke-width="4"/>
      <line x1="50" y1="26" x2="50" y2="82" stroke="{frame}" stroke-width="2" opacity=".45"/>
      <path d="M50 40 C58 50 58 60 50 68 C42 60 42 50 50 40 Z" fill="{flame}"/>
      <path d="M50 52 C54 57 54 62 50 66 C46 62 46 57 50 52 Z" fill="#fff" opacity=".85"/>
      <rect x="26" y="82" width="48" height="9" rx="3" fill="{frame}"/>
    </g>'''

GLOW_DEFS = f'''<radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".75"/>
<stop offset=".45" stop-color="{AMBER}" stop-opacity=".25"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>'''

def person(x, y, h, color, child=False, lantern=False, facing=1):
    """Simple silhouette, feet at (x,y)."""
    k = h / 100
    hr = 9 if not child else 10
    body = f'''<g transform="translate({x},{y}) scale({k*facing},{k})" fill="{color}">
      <circle cx="0" cy="-88" r="{hr}"/>
      <path d="M-13 -76 Q0 -80 13 -76 L17 -36 L10 -36 L8 0 L2 0 L0 -30 L-2 0 L-8 0 L-10 -36 L-17 -36 Z"/>'''
    if lantern:
        body += f'''<path d="M13 -70 L26 -46" stroke="{color}" stroke-width="5" stroke-linecap="round"/>
        <circle cx="28" cy="-34" r="22" fill="url(#glow)"/>
        <line x1="28" y1="-46" x2="28" y2="-40" stroke="{color}" stroke-width="2"/>
        <rect x="22" y="-40" width="12" height="15" rx="3" fill="{GOLD}"/>'''
    return body + "</g>"

def svg(w, h, defs, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{GLOW_DEFS}{defs}</defs>{body}</svg>'

# ---------------- LOGOS ----------------
def logo_square():
    w = h = 512
    body = f'''<rect width="512" height="512" rx="112" fill="{NAVY}"/>
    <circle cx="256" cy="268" r="170" fill="url(#glow)" opacity=".6"/>
    {lantern_glyph(256, 256, 300, glow=False)}'''
    return svg(w, h, "", body)

def logo_wide():
    w, h = 1200, 320
    body = f'''<rect width="{w}" height="{h}" fill="none"/>
    <rect x="20" y="20" width="280" height="280" rx="64" fill="{NAVY}"/>
    {lantern_glyph(160, 160, 170, glow=False)}
    <text x="340" y="170" font-family="Inter" font-weight="800" font-size="112" fill="{NAVY}" letter-spacing="-3">Lantern Trust</text>
    <text x="346" y="238" font-family="Inter" font-weight="500" font-size="40" fill="{CORAL}" letter-spacing="1">Lighting the way home</text>'''
    return svg(w, h, "", body)

def logo_wide_light():
    w, h = 1200, 320
    body = f'''<rect x="20" y="20" width="280" height="280" rx="64" fill="{AMBER}"/>
    {lantern_glyph(160, 160, 170, body=NAVY, frame=CREAM, flame=GOLD, glow=False)}
    <text x="340" y="170" font-family="Inter" font-weight="800" font-size="112" fill="{CREAM}" letter-spacing="-3">Lantern Trust</text>
    <text x="346" y="238" font-family="Inter" font-weight="500" font-size="40" fill="{AMBER}" letter-spacing="1">Lighting the way home</text>'''
    return svg(w, h, "", body)

# ---------------- CLASSIC: Christmas appeal street ----------------
def house(x, base, w, h, wall, roof, lit=True, door=CORAL, seed=0):
    r = random.Random(seed)
    s = f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="{wall}"/>'
    s += f'<path d="M{x-8} {base-h} L{x+w/2} {base-h-w*0.42} L{x+w+8} {base-h} Z" fill="{roof}"/>'
    s += f'<path d="M{x-8} {base-h} L{x+w/2} {base-h-w*0.42} L{x+w+8} {base-h} L{x+w-4} {base-h-6} L{x+w/2} {base-h-w*0.42+14} L{x+4} {base-h-6} Z" fill="{SNOW}"/>'
    s += f'<rect x="{x+w*0.68}" y="{base-h-w*0.38}" width="{w*0.12}" height="{w*0.26}" fill="{roof}"/>'
    ww, wh = w*0.2, h*0.2
    for i, (fx, fy) in enumerate([(0.15, 0.22), (0.65, 0.22), (0.15, 0.55)]):
        on = lit and r.random() > 0.15
        c = GOLD if on else "#33476E"
        if on:
            s += f'<circle cx="{x+w*fx+ww/2}" cy="{base-h+h*fy+wh/2}" r="{ww*1.3}" fill="url(#glow)" opacity=".7"/>'
        s += f'<rect x="{x+w*fx}" y="{base-h+h*fy}" width="{ww}" height="{wh}" fill="{c}" stroke="{CREAM}" stroke-width="3"/>'
        s += f'<line x1="{x+w*fx+ww/2}" y1="{base-h+h*fy}" x2="{x+w*fx+ww/2}" y2="{base-h+h*fy+wh}" stroke="{CREAM}" stroke-width="2"/>'
    # door with fanlight
    dx, dw, dh = x+w*0.6, w*0.24, h*0.36
    s += f'<path d="M{dx} {base} v-{dh} a{dw/2} {dw/2} 0 0 1 {dw} 0 v{dh} z" fill="{door}"/>'
    s += f'<path d="M{dx+4} {base-dh} a{dw/2-4} {dw/2-4} 0 0 1 {dw-8} 0 z" fill="{GOLD}"/>'
    s += f'<circle cx="{dx+dw/2}" cy="{base-dh*0.55}" r="{dw*0.22}" fill="none" stroke="{TEAL}" stroke-width="5"/>'  # wreath
    return s

def classic():
    w, h = 1600, 600
    defs = f'''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{NAVY}"/><stop offset=".55" stop-color="{INDIGO}"/>
      <stop offset=".85" stop-color="#7A5A7E"/><stop offset="1" stop-color="{CORAL}"/></linearGradient>'''
    body = f'<rect width="{w}" height="{h}" fill="url(#sky)"/>' + stars(w, h, 140, 1, 300)
    body += f'<circle cx="1290" cy="120" r="46" fill="{CREAM}"/><circle cx="1308" cy="108" r="44" fill="{INDIGO}" opacity=".0"/>'
    body += f'<path d="M0 470 Q400 400 800 450 T1600 430 V600 H0Z" fill="#2E4470"/>'
    base = 520
    cols = [("#C9D3E3", "#2C3E63"), ("#E9C9A8", NAVY2), ("#F3E3CC", "#3A2E4F"), ("#BFD8D3", NAVY2), ("#EED6C4", "#2C3E63")]
    xs = [470, 600, 730, 860, 990]
    for i, x in enumerate(xs):
        wall, roof = cols[i]
        door = [TEAL, CORAL, "#C0392B", NAVY2, AMBER][i]
        body += house(x, base, 124, 190 + (i % 2) * 20, wall, roof, door=door, seed=i+3)
    # lamppost with lantern
    body += f'<rect x="395" y="300" width="8" height="220" fill="{NAVY}"/><circle cx="399" cy="300" r="70" fill="url(#glow)"/>'
    body += f'<rect x="385" y="285" width="28" height="30" rx="4" fill="{GOLD}" stroke="{NAVY}" stroke-width="4"/>'
    body += f'<rect x="1195" y="300" width="8" height="220" fill="{NAVY}"/><circle cx="1199" cy="300" r="70" fill="url(#glow)"/>'
    body += f'<rect x="1185" y="285" width="28" height="30" rx="4" fill="{GOLD}" stroke="{NAVY}" stroke-width="4"/>'
    body += f'<path d="M0 515 Q800 495 1600 515 V600 H0Z" fill="{SNOW}"/>'
    body += f'<path d="M0 545 Q800 530 1600 548 V600 H0Z" fill="#DCE5F0"/>'
    # pine trees
    for tx, ts in [(150, 1.0), (260, .8), (1340, .9), (1460, 1.1)]:
        body += f'<g transform="translate({tx},530) scale({ts})"><path d="M0 -160 L45 -60 L25 -60 L60 0 L-60 0 L-25 -60 L-45 -60Z" fill="#1F5A55"/><path d="M0 -160 L20 -115 L-20 -115Z" fill="{SNOW}"/></g>'
    body += snow(w, h, 220, 7)
    return svg(w, h, defs, body)

# ---------------- COMPACT: Warm meal ----------------
def compact():
    w, h = 1600, 600
    defs = f'''<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7E6CF"/><stop offset="1" stop-color="{CREAM}"/></linearGradient>
    <linearGradient id="bowl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="#1F5A55"/></linearGradient>
    <radialGradient id="soup" cx=".5" cy=".4"><stop offset="0" stop-color="#F6B85A"/><stop offset="1" stop-color="#D9822B"/></radialGradient>'''
    body = f'<rect width="{w}" height="{h}" fill="url(#wall)"/>'
    r = random.Random(4)
    for _ in range(60):
        body += f'<circle cx="{r.uniform(0,w):.0f}" cy="{r.uniform(0,380):.0f}" r="{r.uniform(3,7):.1f}" fill="{AMBER}" opacity=".18"/>'
    body += f'<rect y="400" width="{w}" height="200" fill="#C98B5A"/><rect y="400" width="{w}" height="14" fill="#B5764A"/>'
    for i in range(0, w, 160):
        body += f'<line x1="{i}" y1="414" x2="{i+40}" y2="600" stroke="#B5764A" stroke-width="3" opacity=".5"/>'
    # cloth
    body += f'<path d="M520 470 L1080 470 L1140 600 L460 600Z" fill="{CREAM}"/>'
    for i in range(8):
        body += f'<line x1="{540+i*70}" y1="470" x2="{500+i*82}" y2="600" stroke="{CORAL}" stroke-width="6" opacity=".55"/>'
    body += f'<line x1="500" y1="510" x2="1100" y2="510" stroke="{CORAL}" stroke-width="6" opacity=".55"/><line x1="480" y1="560" x2="1120" y2="560" stroke="{CORAL}" stroke-width="6" opacity=".55"/>'
    # bowl
    body += f'<ellipse cx="800" cy="500" rx="210" ry="26" fill="#000" opacity=".12"/>'
    body += f'<path d="M590 380 Q600 500 800 505 Q1000 500 1010 380 Z" fill="url(#bowl)"/>'
    body += f'<ellipse cx="800" cy="380" rx="210" ry="40" fill="#1F5A55"/><ellipse cx="800" cy="384" rx="190" ry="30" fill="url(#soup)"/>'
    body += f'<path d="M640 420 Q800 440 960 420" stroke="{CREAM}" stroke-width="6" fill="none" opacity=".6"/>'
    for cx, cy in [(740, 380), (820, 372), (860, 392), (770, 396)]:
        body += f'<circle cx="{cx}" cy="{cy}" r="9" fill="#7FB069"/>'
    body += f'<circle cx="800" cy="385" r="7" fill="{CREAM}"/><circle cx="700" cy="388" r="6" fill="{CREAM}"/>'
    # spoon
    body += f'<path d="M930 370 L1080 250" stroke="#C9CED6" stroke-width="12" stroke-linecap="round"/><ellipse cx="915" cy="380" rx="24" ry="14" fill="#C9CED6" transform="rotate(-38 915 380)"/>'
    # bread
    body += f'<path d="M1110 470 Q1120 410 1200 410 Q1280 410 1290 470 Z" fill="#D9963F"/><path d="M1150 430 l20 -10 M1190 425 l20 -10 M1230 430 l20 -10" stroke="#F3C987" stroke-width="6" stroke-linecap="round"/>'
    # steam
    for sx in [730, 800, 870]:
        body += f'<path d="M{sx} 330 C{sx-30} 290 {sx+30} 260 {sx} 220 C{sx-30} 180 {sx+25} 150 {sx} 120" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" opacity=".85"/>'
    # mug left
    body += f'<rect x="330" y="380" width="110" height="100" rx="14" fill="{CORAL}"/><path d="M440 400 a26 26 0 0 1 0 60" stroke="{CORAL}" stroke-width="14" fill="none"/>'
    body += f'<ellipse cx="385" cy="382" rx="55" ry="10" fill="#6B3A2A"/>'
    body += lantern_glyph(385, 435, 52, body=CREAM, frame=NAVY, flame=AMBER, glow=False)
    return svg(w, h, defs, body)

# ---------------- HERO BANNER: Lantern walk ----------------
def hero_banner():
    w, h = 1600, 600
    defs = f'''<linearGradient id="sky2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{NAVY}"/>
    <stop offset=".6" stop-color="#25507A"/><stop offset="1" stop-color="{TEAL}"/></linearGradient>'''
    body = f'<rect width="{w}" height="{h}" fill="url(#sky2)"/>' + stars(w, h, 170, 11, 320)
    body += f'<circle cx="300" cy="120" r="60" fill="{CREAM}" opacity=".95"/><circle cx="300" cy="120" r="120" fill="{CREAM}" opacity=".06"/>'
    body += f'<path d="M0 380 Q300 300 620 350 T1200 320 T1600 340 V600 H0Z" fill="#1C3A57"/>'
    body += f'<path d="M0 450 Q400 380 820 430 T1600 410 V600 H0Z" fill="#162C45"/>'
    # winding path
    body += f'<path d="M-20 600 C300 560 520 520 760 500 S1150 470 1400 440 S1600 425 1640 420" stroke="#2E4E6E" stroke-width="40" fill="none" stroke-linecap="round"/>'
    pts = [(80, 585, 72), (190, 568, 52), (270, 556, 70), (390, 540, 66), (470, 532, 48), (560, 522, 68), (660, 512, 64),
           (740, 504, 46), (830, 498, 62), (930, 490, 60), (1010, 484, 44), (1100, 476, 58), (1190, 466, 56), (1260, 458, 40),
           (1340, 450, 52), (1420, 442, 50), (1500, 434, 46)]
    for i, (x, y, hh) in enumerate(pts):
        child = hh < 50
        body += person(x, y, hh, "#0D1B2E", child=child, lantern=(i % 3 != 2) or child)
    return svg(w, h, defs, body)

# ---------------- IMAGE LEFT: Home for a family ----------------
def image_left():
    w, h = 1120, 1280
    defs = f'''<linearGradient id="sky3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{INDIGO}"/></linearGradient>
    <linearGradient id="spill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".85"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>
    <radialGradient id="room" cx=".5" cy=".3"><stop offset="0" stop-color="#FFE7B0"/><stop offset="1" stop-color="{AMBER}"/></radialGradient>'''
    body = f'<rect width="{w}" height="{h}" fill="url(#sky3)"/>' + stars(w, h, 80, 21, 260)
    # facade: brick wall
    body += f'<rect x="0" y="180" width="{w}" height="900" fill="#8E4A3C"/>'
    r = random.Random(5)
    for row in range(0, 900, 36):
        off = 0 if (row // 36) % 2 == 0 else 50
        for col in range(-50, w, 100):
            shade = r.choice(["#9A5446", "#84433A", "#A35B4A", "#8E4A3C"])
            body += f'<rect x="{col+off+2}" y="{180+row+2}" width="96" height="32" fill="{shade}"/>'
    # Georgian doorway
    body += f'<rect x="300" y="300" width="520" height="780" fill="{CREAM}"/>'
    body += f'<path d="M330 560 a230 230 0 0 1 460 0 Z" fill="{CREAM}" stroke="#E6D8C0" stroke-width="6"/>'
    body += f'<path d="M370 560 a190 190 0 0 1 380 0 Z" fill="{GOLD}"/>'
    for a in range(0, 181, 20):
        rad = math.radians(180 + a)
        body += f'<line x1="560" y1="560" x2="{560+190*math.cos(rad):.1f}" y2="{560+190*math.sin(rad):.1f}" stroke="{CREAM}" stroke-width="5"/>'
    # open door frame with warm room
    body += f'<rect x="370" y="580" width="380" height="500" fill="url(#room)"/>'
    body += f'<path d="M750 580 L870 620 L870 1100 L750 1080 Z" fill="{CORAL}"/>'  # open door
    body += f'<rect x="770" y="660" width="80" height="140" rx="6" fill="none" stroke="#C25A45" stroke-width="6"/><rect x="770" y="840" width="80" height="160" rx="6" fill="none" stroke="#C25A45" stroke-width="6"/>'
    body += f'<circle cx="788" cy="840" r="8" fill="{GOLD}"/>'
    # family in doorway (silhouettes against glow)
    body += person(500, 1075, 330, NAVY, facing=1)
    body += person(620, 1075, 220, NAVY, child=True, facing=-1)
    body += f'<path d="M532 860 Q560 900 590 900" stroke="{NAVY}" stroke-width="18" fill="none" stroke-linecap="round"/>'
    # potted plants + lanterns either side
    for px in [230, 890]:
        body += f'<path d="M{px-45} 1000 L{px+45} 1000 L{px+35} 1080 L{px-35} 1080Z" fill="{TEAL}"/>'
        body += f'<circle cx="{px}" cy="960" r="55" fill="#2F6B3A"/><circle cx="{px-30}" cy="975" r="35" fill="#3C8048"/><circle cx="{px+30}" cy="975" r="35" fill="#3C8048"/>'
    body += lantern_glyph(230, 470, 140)
    body += lantern_glyph(890, 470, 140)
    # steps and light spill
    body += f'<rect x="260" y="1080" width="600" height="40" fill="#C9C2B4"/><rect x="220" y="1120" width="680" height="40" fill="#B8B0A1"/>'
    body += f'<rect x="0" y="1160" width="{w}" height="120" fill="#3A3F4B"/>'
    body += f'<path d="M370 1080 L750 1080 L880 1280 L240 1280Z" fill="url(#spill)" opacity=".55"/>'
    body += f'<rect x="440" y="1124" width="240" height="30" rx="6" fill="{TEAL}"/>'
    return svg(w, h, defs, body)

# ---------------- IMAGE RIGHT: Winter coat / child with lantern ----------------
def image_right():
    w, h = 1120, 1280
    defs = f'''<linearGradient id="sky4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0F1C33"/>
    <stop offset=".55" stop-color="{INDIGO}"/><stop offset="1" stop-color="#5A6F9E"/></linearGradient>
    <radialGradient id="bigglow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".9"/><stop offset=".35" stop-color="{AMBER}" stop-opacity=".35"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>'''
    body = f'<rect width="{w}" height="{h}" fill="url(#sky4)"/>' + stars(w, h, 160, 31, 700)
    body += f'<path d="M0 860 Q280 780 560 830 T1120 800 V1280 H0Z" fill="#DCE5F0"/>'
    body += f'<path d="M0 960 Q300 900 620 950 T1120 930 V1280 H0Z" fill="{SNOW}"/>'
    for tx, ts in [(120, 1.3), (230, 1.0), (930, 1.2), (1030, 1.5)]:
        body += f'<g transform="translate({tx},900) scale({ts})"><path d="M0 -220 L60 -90 L32 -90 L80 0 L-80 0 L-32 -90 L-60 -90Z" fill="#1F4A5A"/><path d="M0 -220 L26 -160 L-26 -160Z M-32 -90 L32 -90 L44 -66 L-44 -66Z" fill="{SNOW}" opacity=".9"/></g>'
    cx, fy = 560, 1080
    body += f'<ellipse cx="{cx}" cy="{fy+8}" rx="150" ry="20" fill="#9FB0C8" opacity=".5"/>'
    body += f'<circle cx="{cx+195}" cy="{fy-180}" r="260" fill="url(#bigglow)"/>'
    # boots
    body += f'<path d="M{cx-60} {fy-60} h44 v60 h-60 q0 -20 16 -20z" fill="{NAVY}"/><path d="M{cx+16} {fy-60} h44 v40 q16 0 16 20 h-60z" fill="{NAVY}"/>'
    # legs
    body += f'<rect x="{cx-56}" y="{fy-170}" width="40" height="115" fill="#34507A"/><rect x="{cx+16}" y="{fy-170}" width="40" height="115" fill="#34507A"/>'
    # coat (amber)
    body += f'<path d="M{cx-120} {fy-150} Q{cx-110} {fy-420} {cx} {fy-440} Q{cx+110} {fy-420} {cx+120} {fy-150} Z" fill="{AMBER}"/>'
    body += f'<line x1="{cx}" y1="{fy-430}" x2="{cx}" y2="{fy-150}" stroke="#D88A1E" stroke-width="5"/>'
    for by in range(fy-390, fy-180, 60):
        body += f'<circle cx="{cx+18}" cy="{by}" r="8" fill="{NAVY}"/>'
    body += f'<rect x="{cx-90}" y="{fy-260}" width="56" height="40" rx="8" fill="#D88A1E"/><rect x="{cx+34}" y="{fy-260}" width="56" height="40" rx="8" fill="#D88A1E"/>'
    # left arm down, right arm raised holding lantern
    body += f'<path d="M{cx-100} {fy-400} Q{cx-150} {fy-300} {cx-130} {fy-220}" stroke="{AMBER}" stroke-width="48" fill="none" stroke-linecap="round"/>'
    body += f'<circle cx="{cx-130}" cy="{fy-205}" r="22" fill="{CORAL}"/>'
    body += f'<path d="M{cx+100} {fy-400} Q{cx+175} {fy-360} {cx+195} {fy-300}" stroke="#E39A2E" stroke-width="46" fill="none" stroke-linecap="round"/>'
    body += f'<line x1="{cx+195}" y1="{fy-290}" x2="{cx+195}" y2="{fy-250}" stroke="{NAVY}" stroke-width="5"/>'
    body += lantern_glyph(cx+195, fy-175, 170, glow=False)
    body += f'<circle cx="{cx+195}" cy="{fy-288}" r="22" fill="{CORAL}"/>'
    # scarf
    body += f'<path d="M{cx-70} {fy-440} Q{cx} {fy-405} {cx+70} {fy-440} L{cx+70} {fy-415} Q{cx} {fy-380} {cx-70} {fy-415}Z" fill="{CORAL}"/>'
    body += f'<path d="M{cx-50} {fy-420} L{cx-70} {fy-320} L{cx-35} {fy-320} L{cx-25} {fy-415}Z" fill="{CORAL}"/>'
    for sx in range(-66, -36, 10):
        body += f'<line x1="{cx+sx}" y1="{fy-322}" x2="{cx+sx}" y2="{fy-305}" stroke="{CORAL}" stroke-width="4"/>'
    # head, looking up
    body += f'<circle cx="{cx}" cy="{fy-505}" r="70" fill="#E8B48F"/>'
    body += f'<path d="M{cx-74} {fy-515} Q{cx} {fy-640} {cx+74} {fy-515} Q{cx+60} {fy-560} {cx} {fy-565} Q{cx-60} {fy-560} {cx-74} {fy-515}Z" fill="{TEAL}"/>'
    body += f'<rect x="{cx-78}" y="{fy-530}" width="156" height="26" rx="13" fill="{CREAM}"/>'
    body += f'<circle cx="{cx}" cy="{fy-628}" r="22" fill="{CREAM}"/>'
    body += f'<path d="M{cx-30} {fy-495} q8 -8 16 0 M{cx+14} {fy-495} q8 -8 16 0" stroke="{NAVY}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    body += f'<path d="M{cx-14} {fy-465} q14 12 28 0" stroke="{NAVY}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    body += f'<circle cx="{cx-40}" cy="{fy-475}" r="10" fill="{CORAL}" opacity=".5"/><circle cx="{cx+40}" cy="{fy-475}" r="10" fill="{CORAL}" opacity=".5"/>'
    body += snow(w, h, 160, 33)
    return svg(w, h, defs, body)

# ---------------- IMMERSIVE: Light a Lantern night ----------------
def sky_lantern(x, y, s, o=1):
    return f'''<g transform="translate({x},{y}) scale({s})" opacity="{o:.2f}">
      <circle cx="0" cy="0" r="70" fill="url(#glow)"/>
      <path d="M-18 -26 Q0 -34 18 -26 L13 24 Q0 28 -13 24 Z" fill="{AMBER}"/>
      <path d="M-10 -24 Q0 -28 10 -24 L7 20 Q0 22 -7 20 Z" fill="{GOLD}"/>
      <ellipse cx="0" cy="18" rx="5" ry="6" fill="#fff"/></g>'''

def immersive():
    w, h = 1920, 1080
    defs = f'''<linearGradient id="sky5" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0A1426"/>
    <stop offset=".5" stop-color="{NAVY2}"/><stop offset=".72" stop-color="#3E3F6E"/><stop offset=".78" stop-color="#7D5C78"/></linearGradient>
    <linearGradient id="lake" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2D3459"/><stop offset="1" stop-color="#0A1426"/></linearGradient>'''
    body = f'<rect width="{w}" height="{h}" fill="url(#sky5)"/>' + stars(w, h, 380, 41, 760)
    body += f'<circle cx="1560" cy="190" r="70" fill="{CREAM}"/><circle cx="1560" cy="190" r="160" fill="{CREAM}" opacity=".05"/>'
    horizon = 820
    body += f'<path d="M0 {horizon} L0 760 Q160 700 320 740 Q520 660 760 735 Q980 690 1180 745 Q1420 680 1640 735 Q1800 710 1920 750 L1920 {horizon} Z" fill="#141E36"/>'
    body += f'<rect y="{horizon}" width="{w}" height="{h-horizon}" fill="url(#lake)"/>'
    r = random.Random(42)
    lanterns = []
    for _ in range(58):
        x = r.uniform(40, w-40)
        y = r.uniform(80, horizon-40)
        depth = (y / horizon)
        s = 0.35 + depth * 0.95 * r.uniform(.7, 1.1)
        lanterns.append((y, x, s))
    for y, x, s in sorted(lanterns):
        body += sky_lantern(x, y, s, 0.55 + 0.45*(y/horizon))
    # reflections
    for y, x, s in lanterns:
        ry = horizon + (horizon - y) * 0.22
        if ry < h:
            body += f'<ellipse cx="{x:.0f}" cy="{ry:.0f}" rx="{10*s:.1f}" ry="{3*s:.1f}" fill="{GOLD}" opacity=".35"/>'
    for i in range(18):
        yy = horizon + 20 + i*14
        body += f'<line x1="{r.uniform(0,w):.0f}" y1="{yy}" x2="{r.uniform(0,w):.0f}" y2="{yy}" stroke="#fff" stroke-width="1.5" opacity=".06"/>'
    # people on jetty releasing lanterns (left foreground)
    body += f'<rect x="0" y="960" width="560" height="22" fill="#0B1222"/>'
    for px in [80, 200, 340, 470]:
        body += f'<rect x="{px}" y="980" width="12" height="100" fill="#0B1222"/>'
    body += person(180, 962, 150, "#070D1A")
    body += person(260, 962, 100, "#070D1A", child=True, facing=-1)
    body += sky_lantern(232, 760, 1.6)
    body += f'<path d="M205 840 L225 800 M282 875 L240 800" stroke="#070D1A" stroke-width="10" stroke-linecap="round"/>'
    body += person(420, 962, 140, "#070D1A", facing=-1)
    body += sky_lantern(380, 700, 1.3)
    return svg(w, h, defs, body)

JOBS = [
    ("lantern-trust-logo-square.png", logo_square, 512, 512, "png"),
    ("lantern-trust-logo-wide.png", logo_wide, 1200, 320, "png"),
    ("lantern-trust-logo-wide-light.png", logo_wide_light, 1200, 320, "png"),
    ("classic-christmas-appeal-1600x600.jpg", classic, 1600, 600, "jpeg"),
    ("compact-warm-meal-1600x600.jpg", compact, 1600, 600, "jpeg"),
    ("hero-banner-lantern-walk-1600x600.jpg", hero_banner, 1600, 600, "jpeg"),
    ("image-left-a-home-1120x1280.jpg", image_left, 1120, 1280, "jpeg"),
    ("image-right-winter-coats-1120x1280.jpg", image_right, 1120, 1280, "jpeg"),
    ("immersive-light-a-lantern-1920x1080.jpg", immersive, 1920, 1080, "jpeg"),
]

if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, fn, w, h, fmt in JOBS:
            pg = b.new_page(viewport={"width": w, "height": h})
            bg = "transparent" if fmt == "png" else "#000"
            pg.set_content(f'<html><body style="margin:0;background:{bg}">{fn()}</body></html>')
            kw = {"type": fmt, "full_page": False, "omit_background": fmt == "png"}
            if fmt == "jpeg": kw["quality"] = 88
            pg.screenshot(path=str(OUT / name), **kw)
            (OUT / name.rsplit(".", 1)[0]).with_suffix(".svg").write_text(fn())
            pg.close()
        b.close()
    for f in sorted(OUT.glob("*")):
        if f.suffix != ".svg": print(f.name, f.stat().st_size // 1024, "KB")
