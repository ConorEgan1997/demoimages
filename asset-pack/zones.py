"""Crop-zone diagrams: draw on each source image the region CHAMP actually shows.

CHAMP renders every hero with background-size: cover. Positions and container sizes
were measured from the live DEMO pages (desktop 1440x900, phone 390x844):
  classic      50% 50%  desktop 691x210   phone 391x306
  compact      50% 50%  desktop 403x180   phone 391x180
  image left   50% 50%  desktop 517x481   phone 391x310
  image right  50% 50%  desktop 517x376   phone 391x330
  hero banner  50% 40%  desktop 1440x126  phone 420x192
  immersive    50% 50%  desktop 1440x900  phone 390x844 (form card covers the middle)
"""
from PIL import Image, ImageDraw, ImageFont
import pathlib

ROOT = pathlib.Path('/home/claude/demoimages')
OUT = pathlib.Path('/home/claude/assetpack/zones'); OUT.mkdir(exist_ok=True)
F = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'

def cover_rect(iw, ih, cw, ch, px=.5, py=.5):
    """Region of the source image visible in a cw x ch box with cover + position px/py."""
    s = max(cw / iw, ch / ih)
    vw, vh = cw / s, ch / s
    x = (iw - vw) * px; y = (ih - vh) * py
    return x, y, x + vw, y + vh

LAYOUTS = {
    'classic':     dict(pos=(.5, .5), desk=(691, 210), phone=(391, 306)),
    'compact':     dict(pos=(.5, .5), desk=(403, 180), phone=(391, 180), clear='lowerleft'),
    'imageleft':   dict(pos=(.5, .5), desk=(517, 481), phone=(391, 310), text='top'),
    'imageright':  dict(pos=(.5, .5), desk=(517, 376), phone=(391, 330), text='top'),
    'herobanner':  dict(pos=(.5, .4), desk=(1440, 126), phone=(420, 192), wide=(1920, 126)),
    'immersive':   dict(pos=(.5, .5), desk=(1440, 900), phone=(390, 844), card=True),
}
FILES = {
    'lantern': {'classic': 'demo-campaign-images/classic-christmas-appeal-1600x600.jpg',
                'compact': 'demo-campaign-images/compact-warm-meal-1200x480.jpg',
                'imageleft': 'demo-campaign-images/image-left-a-home-1120x1280.jpg',
                'imageright': 'demo-campaign-images/image-right-winter-coats-1120x1280.jpg',
                'herobanner': 'demo-campaign-images/hero-banner-lantern-walk-1920x600.jpg',
                'immersive': 'demo-campaign-images/immersive-light-a-lantern-1920x1080.jpg'},
    'willow': {'classic': 'hospice-flowers/classic-memory-garden-1600x600.jpg',
               'compact': 'hospice-flowers/compact-bouquet-1200x480.jpg',
               'imageleft': 'hospice-flowers/image-left-windowsill-1120x1280.jpg',
               'imageright': 'hospice-flowers/image-right-sunflowers-1120x1280.jpg',
               'herobanner': 'hospice-flowers/hero-banner-garden-border-1920x600.jpg',
               'immersive': 'hospice-flowers/immersive-golden-meadow-1920x1080.jpg'},
}
TEAL = (24, 160, 150); CORAL = (232, 96, 76); WHITE = (255, 255, 255)

def label(d, xy, text, col, size):
    f = ImageFont.truetype(F, size)
    x, y = xy
    tw, th = d.textbbox((0, 0), text, font=f)[2:]
    d.rounded_rectangle((x, y, x + tw + size * .9, y + th + size * .6), radius=size * .35, fill=col)
    d.text((x + size * .45, y + size * .22), text, font=f, fill=WHITE)

def zone(brand, key):
    L = LAYOUTS[key]
    src = Image.open(ROOT / FILES[brand][key]).convert('RGB')
    iw, ih = src.size
    k = 1100 / iw  # normalise width for the PDF
    im = src.resize((1100, round(ih * k)), Image.LANCZOS)
    W, H = im.size
    sc = lambda r: tuple(v * k for v in r)

    # dim everything, then reveal what desktop shows
    dim = Image.new('RGBA', im.size, (20, 24, 35, 150))
    base = im.convert('RGBA')
    desk = sc(cover_rect(iw, ih, *L['desk'], *L['pos']))
    if 'wide' in L:  # also mark the widest common desktop (1920 px)
        wide = sc(cover_rect(iw, ih, *L['wide'], *L['pos']))
    phone = sc(cover_rect(iw, ih, *L['phone'], *L['pos']))
    mask = Image.new('L', im.size, 255)
    md = ImageDraw.Draw(mask)
    md.rectangle([round(v) for v in desk], fill=0)
    md.rectangle([round(v) for v in phone], fill=0)
    veil = Image.new('RGBA', im.size, (255, 255, 255, 0))
    veil.putalpha(mask.point(lambda v: 150 if v else 0))
    base = Image.alpha_composite(base, veil)
    d = ImageDraw.Draw(base)
    lw = max(4, W // 220)
    fs = max(20, W // 42)

    if L.get('card'):
        # immersive: card floats over the centre at ~430 px of 1440 desktop, top ~150..880
        cw = 430 / 1440 * W; cx0 = (W - cw) / 2
        d.rounded_rectangle((cx0, H * .19, cx0 + cw, H * .83), radius=18, outline=CORAL, width=lw)
        label(d, (cx0 + 10, H * .19 + 10), 'Form card (hidden)', CORAL, fs)
        ph = phone
        d.rectangle(ph, outline=(255, 210, 90), width=lw)
        label(d, (ph[0] + 10, ph[1] + 10), 'Phone: only the top shows', (190, 140, 30), fs)
        label(d, (14, 14), 'Desktop: full image', TEAL, fs)
    else:
        d.rectangle(desk, outline=TEAL, width=lw)
        d.rectangle(phone, outline=(255, 210, 90), width=lw)
        if 'wide' in L:
            d.rectangle(wide, outline=TEAL, width=max(2, lw // 2))
        # labels: desktop on top-left of its box, phone on bottom-right of its box
        label(d, (desk[0] + 10, desk[1] + 10), 'Desktop view', TEAL, fs)
        pf = ImageFont.truetype(F, fs)
        tw = d.textbbox((0, 0), 'Phone view', font=pf)[2]
        label(d, (phone[2] - tw - fs * 1.4, phone[3] - fs * 2.1), 'Phone view', (190, 140, 30), fs)
        if L.get('clear') == 'lowerleft':
            x0, y0 = desk[0], desk[1] + (desk[3] - desk[1]) * .5
            d.rectangle((x0 + lw, y0, x0 + (desk[2] - desk[0]) * .55, desk[3] - lw), outline=CORAL, width=lw)
            label(d, (x0 + 16, desk[3] - fs * 2.4), 'Logo + headline', CORAL, fs)
        if L.get('text') == 'top':
            y1 = desk[1] + (desk[3] - desk[1]) * .52
            d.rectangle((desk[0] + lw, desk[1] + fs * 2.6, desk[2] - lw, y1), outline=CORAL, width=lw)
            label(d, (desk[0] + 16, y1 - fs * 2.2), 'Headline + text', CORAL, fs)
    out = OUT / f'{key}-{brand}-zones.jpg'
    base.convert('RGB').save(out, quality=88)
    return out

if __name__ == '__main__':
    for b in FILES:
        for k in LAYOUTS:
            print(zone(b, k))
