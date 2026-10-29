"""CHAMP Donation Page Asset Pack — HTML laid out for A4 landscape, printed to PDF with Playwright."""
import pathlib, html
from playwright.sync_api import sync_playwright

A = pathlib.Path('/home/claude/assetpack')
R = pathlib.Path('/home/claude/demoimages')
GH = 'https://raw.githubusercontent.com/ConorEgan1997/demoimages/main/'
u = lambda p: 'file://' + str(p)
e = html.escape

LAYOUTS = [
    dict(key='classic', name='Classic', tag='Multi-step wizard · good for higher-value campaigns',
         size='1600 × 600 px', ratio='8:3 wide', maxkb='2 MB', fmt='JPG or PNG',
         how='A wide banner across the top of a step-by-step form. CHAMP trims the top and bottom edges, and trims more on a phone, where the banner becomes almost square.',
         subject='Keep the key subject in the middle of the frame. Treat the top and bottom ~15% as bleed.',
         covered='Logo, charity name, headline and description sit over the left and middle of the image. CHAMP adds a dark overlay so the white text stays readable.',
         dos=['A calm scene with one clear focal point in the centre', 'Simple sky or background behind where the headline sits', 'Subject still recognisable when cropped to a square'],
         donts=['Faces or detail near the top or bottom edge', 'Text, logos or dates inside the image', 'Very busy scenes, which fight the headline'],
         lantern='demo-campaign-images/classic-christmas-appeal-1600x600.jpg', willow='hospice-flowers/classic-memory-garden-1600x600.jpg',
         lname='Christmas Appeal 2026', wname='Light up a life this Christmas'),
    dict(key='compact', name='Compact', tag='Single-page form · best for embeds and quick gifts',
         size='1200 × 480 px', ratio='5:2 wide', maxkb='1.5 MB', fmt='JPG or PNG',
         how='A compact banner above a narrow, single-page form. It shows at about 400 × 180 px on desktop and phone alike.',
         subject='Centre the subject and keep it in the upper half. The lower-left quarter must stay clear.',
         covered='Logo and charity name sit top-left. The headline sits across the lower-left, which is why that corner needs to be quiet.',
         dos=['A single object or close-up (a bouquet, a meal, a hand)', 'Plain or softly textured lower-left corner', 'Strong colour that still reads at small sizes'],
         donts=['Anything important in the lower-left', 'Wide landscapes with small detail, which disappear at this size', 'Re-using a 1600 × 600 Classic image, which crops badly'],
         lantern='demo-campaign-images/compact-warm-meal-1200x480.jpg', willow='hospice-flowers/compact-bouquet-1200x480.jpg',
         lname='Warm Meal Fund', wname='Send flowers to someone who needs comfort'),
    dict(key='imageleft', name='Image left', tag='Hero image left, form right · story-driven',
         size='1120 × 1280 px', ratio='7:8 near-square portrait', maxkb='2.5 MB', fmt='JPG or PNG',
         how='Fills a portrait column beside the form on a laptop (about 560 × 640 px, so supply it at 2×). On a phone it becomes a short banner above the form.',
         subject='Put the subject in the centre. It has to survive both the tall desktop column and the short phone banner.',
         covered='Logo, headline and description cover the top half of the column. Rotating testimonials sit in the lower half, over the image.',
         dos=['Portrait or near-square photo', 'Subject centred, with some breathing room', 'Darker or mid-tone image, so white text and quotes read well'],
         donts=['A wide 1600 × 600 banner, which is the wrong shape', 'Subject at the very top, where the headline sits', 'Bright white images, which make the quote text hard to read'],
         lantern='demo-campaign-images/image-left-a-home-1120x1280.jpg', willow='hospice-flowers/image-left-windowsill-1120x1280.jpg',
         lname='A Home for Every Family', wname='Care that lets every moment matter'),
    dict(key='imageright', name='Image right', tag='Form left, hero image right',
         size='1120 × 1280 px', ratio='7:8 near-square portrait', maxkb='2.5 MB', fmt='JPG or PNG',
         how='The mirror of Image left on desktop. On a phone the image moves below the form, so donors see the form first and the image last.',
         subject='CHAMP says to centre the subject. In practice the headline covers the top half here, so place faces just below centre.',
         covered='Logo, headline and description cover the top half. There are no testimonials over the image in this layout.',
         dos=['Subject slightly below centre', 'Open sky or plain background in the top half', 'Image that works as a closing visual on a phone'],
         donts=['Faces in the top half, where they end up under the headline', 'Relying on the image as the first thing a phone visitor sees', 'Wide landscape banners'],
         lantern='demo-campaign-images/image-right-winter-coats-1120x1280.jpg', willow='hospice-flowers/image-right-sunflowers-1120x1280.jpg',
         lname='Winter Coat Drive', wname='Grow something beautiful in their memory'),
    dict(key='herobanner', name='Hero banner', tag='Full-width banner above a centred form',
         size='1920 × 600 px', ratio='16:5 extra-wide', maxkb='2.5 MB', fmt='JPG or PNG',
         how='A thin strip across the full width of the page, about 126 px tall on desktop. Most of the image height is cut off. CHAMP anchors the crop slightly above centre (40% down).',
         subject='Run the subject across the horizontal middle. On desktop only roughly rows 190–320 of a 600 px-tall image are visible.',
         covered='Logo, charity name, headline and description sit in one line across the strip.',
         dos=['A repeating or panoramic subject (a crowd, a skyline, a flower border)', 'Detail concentrated in the middle band', 'Even tone across the width, so text reads everywhere'],
         donts=['A single subject in the centre, which ends up behind the headline', 'Any detail near the top or bottom', 'Busy high-contrast patterns behind the text'],
         lantern='demo-campaign-images/hero-banner-lantern-walk-1920x600.jpg', willow='hospice-flowers/hero-banner-garden-border-1920x600.jpg',
         lname='Lantern Walk 2026', wname='Walk our garden of remembrance'),
    dict(key='immersive', name='Immersive', tag='Form card floated over a full-page hero image',
         size='1920 × 1080 px', ratio='16:9 full-screen', maxkb='3 MB', fmt='JPG or PNG',
         how='Fills the whole screen behind the form, which floats over the centre. On a phone the card covers most of the image and only the top shows.',
         subject='Place the main subject to the left or right. A centred subject is hidden behind the card. Keep the top of the image attractive, because that is all phones see.',
         covered='The logo, headline and description sit above the card, centred at the top. The card covers the middle third.',
         dos=['Atmospheric, full-bleed scene', 'Subject on the left or right third', 'Interest at the top of the frame for phones'],
         donts=['A centred subject, which ends up behind the card', 'Words or logos in the photo, which get sliced at different screen sizes', 'Low-resolution images, which are stretched to fill the screen'],
         lantern='demo-campaign-images/immersive-light-a-lantern-1920x1080.jpg', willow='hospice-flowers/immersive-golden-meadow-1920x1080.jpg',
         lname='Light a Lantern', wname='A meadow of memories'),
]

CSS = """
@page { size: A4 landscape; margin: 0; }
* { box-sizing: border-box; }
:root { --ink:#14233C; --ink2:#3A4A63; --mute:#6B7689; --line:#E3E7EE; --teal:#18A096; --coral:#E8604C; --amber:#F2A93B; --plum:#4B2E4F; --bg:#F6F7FA; }
html, body { margin:0; padding:0; font-family: Inter, sans-serif; color: var(--ink); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 297mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always; padding: 14mm 16mm 12mm; background: #fff; }
.page:last-child { page-break-after: auto; }
h1 { font-family: 'Inter Display', Inter; font-weight: 800; letter-spacing: -0.02em; margin: 0; }
h2 { font-family: 'Inter Display', Inter; font-weight: 800; font-size: 26pt; letter-spacing: -0.02em; margin: 0 0 1mm; }
h3 { font-size: 10.5pt; font-weight: 700; margin: 0 0 1.5mm; letter-spacing: .01em; }
p, li, td { font-size: 9pt; line-height: 1.45; color: var(--ink2); }
.kicker { font-size: 8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--teal); margin-bottom: 2mm; }
.tag { font-size: 10.5pt; color: var(--mute); margin: 0 0 5mm; }
.foot { position: absolute; left: 16mm; right: 16mm; bottom: 6mm; display: flex; justify-content: space-between; font-size: 7pt; color: #9AA3B2; }
.chip { display:inline-block; font-size:7.5pt; font-weight:700; padding:1mm 2.6mm; border-radius: 99px; color:#fff; }
.chip.l { background: var(--ink); } .chip.w { background: var(--plum); }
.spec { display:grid; grid-template-columns: 1fr 1fr; gap: 2mm; margin: 0 0 4mm; }
.spec div { background: var(--bg); border-radius: 3mm; padding: 2.4mm 3mm; }
.spec b { display:block; font-size: 6.8pt; letter-spacing:.12em; text-transform:uppercase; color: var(--mute); font-weight:700; margin-bottom: .6mm; }
.spec span { font-size: 11pt; font-weight: 700; color: var(--ink); }
ul { margin: 0; padding-left: 4.2mm; } li { margin: 0 0 .9mm; }
.do li::marker { content: '✓  '; color: var(--teal); font-weight: 800; }
.dont li::marker { content: '✕  '; color: var(--coral); font-weight: 800; }
.cols2 { display:grid; grid-template-columns: 1fr 1fr; gap: 4mm; }
img { display:block; max-width:100%; }
.shot { border-radius: 2.5mm; box-shadow: 0 0.6mm 2.4mm rgba(20,35,60,.18); border: .3mm solid var(--line); }
.cap { font-size: 7.5pt; color: var(--mute); margin-top: 1.4mm; }
.legend { display:flex; gap: 4mm; font-size: 7.5pt; color: var(--ink2); margin-top: 2mm; }
.legend i { display:inline-block; width: 3mm; height: 3mm; border-radius: .6mm; margin-right: 1.2mm; vertical-align: -0.4mm; }
table.ref { width:100%; border-collapse: collapse; }
table.ref th { text-align:left; font-size: 7pt; letter-spacing:.1em; text-transform:uppercase; color: var(--mute); padding: 2mm 2mm; border-bottom: .4mm solid var(--ink); }
table.ref td { padding: 2.4mm 2mm; border-bottom: .3mm solid var(--line); vertical-align: top; font-size: 8.6pt; }
table.ref td:first-child { font-weight: 700; color: var(--ink); }
.box { background: var(--bg); border-radius: 3.5mm; padding: 4mm 5mm; }
.tipgrid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }
.tip h3 { display:flex; align-items:center; gap: 2mm; }
.tip h3 em { font-style: normal; display:inline-grid; place-items:center; width: 6mm; height: 6mm; border-radius: 1.6mm; background: var(--ink); color:#fff; font-size: 8pt; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 7.2pt; background: var(--bg); padding: .2mm 1mm; border-radius: .8mm; color: var(--ink); word-break: break-all; }
"""

def foot(n, title='CHAMP donation page asset pack'):
    return f'<div class="foot"><span>{title}</span><span>{n}</span></div>'

def cover():
    imL = u(R / 'demo-campaign-images/immersive-light-a-lantern-1920x1080.jpg')
    imW = u(R / 'hospice-flowers/immersive-golden-meadow-1920x1080.jpg')
    return f"""
<section class="page" style="padding:0">
  <div style="position:absolute;inset:0;background:url('{imL}') center/cover"></div>
  <div style="position:absolute;inset:0;background:url('{imW}') center/cover;clip-path:polygon(58% 0,100% 0,100% 100%,42% 100%)"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(12,20,36,.88) 0%,rgba(12,20,36,.55) 45%,rgba(12,20,36,0) 75%)"></div>
  <div style="position:absolute;left:18mm;top:20mm;width:150mm;color:#fff">
    <div class="kicker" style="color:#8FE3DA">CHAMP · Donation pages</div>
    <h1 style="font-size:44pt;line-height:1.02;color:#fff">Campaign image<br>asset pack</h1>
    <p style="color:#DCE3EE;font-size:12pt;line-height:1.5;margin:6mm 0 0;max-width:130mm">
      What images each of the six page layouts needs, how CHAMP crops them on desktop and phone, and worked examples for two very different charities.</p>
    <div style="display:flex;gap:6mm;margin-top:12mm">
      <div style="display:flex;align-items:center;gap:3mm;background:rgba(255,255,255,.1);padding:3mm 4mm;border-radius:3mm">
        <img src="{u(R/'demo-campaign-images/lantern-trust-logo-240x80-light.png')}" style="height:13mm">
        <span style="font-size:8pt;color:#C8D2E2;line-height:1.35">Example 1<br><b style="color:#fff">Homelessness charity</b></span></div>
      <div style="display:flex;align-items:center;gap:3mm;background:rgba(255,255,255,.1);padding:3mm 4mm;border-radius:3mm">
        <img src="{u(R/'hospice-flowers/willowmere-logo-240x80-light.png')}" style="height:13mm">
        <span style="font-size:8pt;color:#C8D2E2;line-height:1.35">Example 2<br><b style="color:#fff">Hospice, flower theme</b></span></div>
    </div>
  </div>
  <div style="position:absolute;left:18mm;bottom:10mm;font-size:7.5pt;color:#AEB9CB">Both charities are fictional demo brands. All artwork is original and free to use in CHAMP demos.</div>
</section>"""

def quickref(n):
    rows = ''.join(f"<tr><td>{L['name']}</td><td>{L['size']}</td><td>{L['ratio']}</td><td>≤ {L['maxkb']}</td><td>{e(L['subject'])}</td></tr>" for L in LAYOUTS)
    rows += "<tr><td>Logo</td><td>240 × 80 px</td><td>3:1</td><td>≤ 200 KB</td><td>Transparent PNG or SVG. It must read on a dark overlay, so supply a light-text version. No baked-in background.</td></tr>"
    return f"""
<section class="page">
  <div class="kicker">Quick reference</div>
  <h2>One image per layout, sized for that layout</h2>
  <p class="tag">Every layout crops the hero image differently. Supply the size listed and the subject will land where CHAMP expects it.</p>
  <table class="ref">
    <tr><th style="width:24mm">Layout</th><th style="width:28mm">Supply at</th><th style="width:36mm">Shape</th><th style="width:20mm">Max file</th><th>Where to put the subject</th></tr>
    {rows}
  </table>
  <div class="cols2" style="margin-top:6mm">
    <div class="box"><h3>For every image</h3><ul>
      <li>JPG for photos and illustrations, PNG only for logos. Use the sRGB colour profile.</li>
      <li>Must be served over <b>https://</b> as a direct image link, ending in .jpg or .png.</li>
      <li>Aim for under 500 KB where you can. Small files make the page load faster on mobile data.</li>
      <li>No words, prices or dates in the image. Type them into the headline instead.</li></ul></div>
    <div class="box"><h3>How to read the layout pages</h3>
      <p style="margin:0 0 2mm">Each layout gets two pages. The first shows the spec and a crop diagram for both examples.</p>
      <div class="legend" style="margin:0 0 2mm"><span><i style="background:var(--teal)"></i>Desktop view</span><span><i style="background:#E7B53A"></i>Phone view</span><span><i style="background:var(--coral)"></i>Covered by text or the form</span></div>
      <p style="margin:0">The second shows real screenshots of the page on desktop (1440 px) and phone (390 px).</p></div>
  </div>
  {foot(n)}
</section>"""

def logo_page(n):
    lg = lambda p: u(R / p)
    return f"""
<section class="page">
  <div class="kicker">Logo</div>
  <h2>A small, transparent logo that reads on dark</h2>
  <p class="tag">Set per campaign under Branding → Override default branding → Logo URL, or charity-wide in Settings.</p>
  <div style="display:grid;grid-template-columns:96mm 1fr;gap:8mm">
    <div>
      <div class="spec"><div><b>Supply at</b><span>240 × 80 px</span></div><div><b>Shape</b><span>3:1</span></div>
        <div><b>Format</b><span>PNG or SVG</span></div><div><b>Max file</b><span>200 KB</span></div></div>
      <h3>Why a light version</h3>
      <p>The logo sits on top of the hero image, under CHAMP's dark overlay, or on a branded panel. A dark wordmark disappears on that, so give each charity a light-text version for the Logo URL. Keep the dark version for emails and white backgrounds.</p>
      <h3 style="margin-top:4mm">Tips</h3>
      <ul class="do"><li>A square symbol plus a short wordmark reads best at this size</li><li>Transparent background, with no white box around it</li><li>Export at 3× (720 × 240) if the platform allows, for sharp retina screens</li></ul>
    </div>
    <div style="display:grid;grid-template-rows:1fr 1fr;gap:5mm">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm">
        <div style="background:#14233C;border-radius:3mm;display:grid;place-items:center;padding:6mm"><img src="{lg('demo-campaign-images/lantern-trust-logo-240x80-light.png')}" style="height:20mm"></div>
        <div style="background:#fff;border:.3mm solid var(--line);border-radius:3mm;display:grid;place-items:center;padding:6mm"><img src="{lg('demo-campaign-images/lantern-trust-logo-240x80-dark.png')}" style="height:20mm"></div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm">
        <div style="background:#4B2E4F;border-radius:3mm;display:grid;place-items:center;padding:6mm"><img src="{lg('hospice-flowers/willowmere-logo-240x80-light.png')}" style="height:20mm"></div>
        <div style="background:#fff;border:.3mm solid var(--line);border-radius:3mm;display:grid;place-items:center;padding:6mm"><img src="{lg('hospice-flowers/willowmere-logo-240x80-dark.png')}" style="height:20mm"></div>
      </div>
      <p class="cap" style="margin:-2mm 0 0">Light version (use for Logo URL) · Dark version (emails, white backgrounds)</p>
    </div>
  </div>
  {foot(n)}
</section>"""

def spec_page(L, n):
    z = lambda b: u(A / 'zones' / f"{L['key']}-{b}-zones.jpg")
    portrait = L['key'] in ('imageleft', 'imageright')
    if portrait:
        zones = f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm;align-items:start">
          <div><img src="{z('lantern')}" class="shot" style="height:118mm;width:auto;margin:0 auto"><div class="cap"><span class="chip l">Example 1</span>&nbsp; {e(L['lname'])}</div></div>
          <div><img src="{z('willow')}" class="shot" style="height:118mm;width:auto;margin:0 auto"><div class="cap"><span class="chip w">Example 2</span>&nbsp; {e(L['wname'])}</div></div></div>"""
    else:
        h = 'max-height:62mm' if L['key'] != 'immersive' else 'max-height:66mm'
        zones = f"""<div style="display:grid;gap:4mm">
          <div><img src="{z('lantern')}" class="shot" style="{h};width:auto"><div class="cap"><span class="chip l">Example 1</span>&nbsp; {e(L['lname'])}</div></div>
          <div><img src="{z('willow')}" class="shot" style="{h};width:auto"><div class="cap"><span class="chip w">Example 2</span>&nbsp; {e(L['wname'])}</div></div></div>"""
    lis = lambda xs: ''.join(f'<li>{e(x)}</li>' for x in xs)
    return f"""
<section class="page">
  <div style="display:grid;grid-template-columns:96mm 1fr;gap:9mm;height:100%">
    <div>
      <div class="kicker">Layout · {e(L['name'])}</div>
      <h2>{e(L['name'])}</h2>
      <p class="tag" style="margin-bottom:4mm">{e(L['tag'])}</p>
      <div class="spec"><div><b>Supply at</b><span>{L['size']}</span></div><div><b>Shape</b><span>{L['ratio']}</span></div>
        <div><b>Format</b><span>{L['fmt']}</span></div><div><b>Max file</b><span>{L['maxkb']}</span></div></div>
      <h3>How it sits on the page</h3><p style="margin:0 0 2.6mm">{e(L['how'])}</p>
      <h3>Where to put the subject</h3><p style="margin:0 0 2.6mm">{e(L['subject'])}</p>
      <h3>What covers the image</h3><p style="margin:0 0 3mm">{e(L['covered'])}</p>
      <div class="cols2" style="gap:3mm"><div><h3 style="color:var(--teal)">Do</h3><ul class="do">{lis(L['dos'])}</ul></div>
        <div><h3 style="color:var(--coral)">Avoid</h3><ul class="dont">{lis(L['donts'])}</ul></div></div>
    </div>
    <div>
      <div class="legend" style="margin:0 0 3mm"><span><i style="background:var(--teal)"></i>Desktop view</span><span><i style="background:#E7B53A"></i>Phone view</span><span><i style="background:var(--coral)"></i>Covered by text or form</span><span style="color:var(--mute)">Faded = cropped off</span></div>
      {zones}
    </div>
  </div>
  {foot(n)}
</section>"""

def shots_page(L, n):
    s = lambda b, d: u(A / 'shots' / f"{L['key']}-{b}-{d}.jpg")
    col = lambda b, chip, name: f"""
      <div>
        <div style="margin-bottom:2mm"><span class="chip {chip}">{'Example 1 · Lantern Trust' if chip=='l' else 'Example 2 · Willowmere Hospice'}</span></div>
        <img src="{s(b,'desktop')}" class="shot" style="width:100%">
        <div style="display:grid;grid-template-columns:36mm 1fr;gap:4mm;margin-top:4mm;align-items:start">
          <img src="{s(b,'phone')}" class="shot" style="width:36mm">
          <div><p class="cap" style="margin:0 0 1mm;font-weight:700;color:var(--ink)">{e(name)}</p>
            <p class="cap" style="margin:0">Top: desktop at 1440 px wide. Left: phone at 390 px wide{' (scrolled to the image, which sits below the form)' if L['key']=='imageright' else ''}.</p>
            <p class="cap" style="margin:2mm 0 0">Image file:<br><code>{GH}{L['lantern'] if chip=='l' else L['willow']}</code></p></div>
        </div>
      </div>"""
    return f"""
<section class="page" style="padding-top:11mm">
  <div class="kicker">Layout · {e(L['name'])} · on the page</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:9mm;margin-top:2mm">
    {col('lantern','l',L['lname'])}
    {col('willow','w',L['wname'])}
  </div>
  {foot(n)}
</section>"""

def copy_page(n):
    return f"""
<section class="page">
  <div class="kicker">Words on the page</div>
  <h2>The image sets the mood. The words do the asking.</h2>
  <p class="tag">Every layout uses the same text fields. These limits keep the text clear of the image and readable on a phone.</p>
  <table class="ref">
    <tr><th style="width:34mm">Field</th><th style="width:40mm">Length</th><th>Guidance</th><th style="width:78mm">Example (hospice)</th></tr>
    <tr><td>Headline</td><td>Up to ~60 characters</td><td>One idea, written to the donor. Specific beats generic.</td><td>“Care that lets every moment matter”</td></tr>
    <tr><td>Description</td><td>Two short sentences</td><td>Sentence 1: the need, with a real number. Sentence 2: what the gift does.</td><td>“Our nurses care for 1,200 people a year… Your gift gives families comfort, dignity and time together.”</td></tr>
    <tr><td>Amounts</td><td>3–4 amounts + Other</td><td>Star the middle amount as the default. Most donors pick the pre-selected amount or the one next to it.</td><td>€25 · <b>€50</b> · €100 · €250</td></tr>
    <tr><td>Impact text</td><td>Under ~40 characters</td><td>Concrete and tangible. Start with a verb.</td><td>“funds a night of specialist hospice care”</td></tr>
    <tr><td>Testimonials</td><td>Up to 5 · under ~120 characters</td><td>Real voices, with consent. First name and county or role. Keep the tone warm and avoid graphic detail.</td><td>“The nurses gave Mam peace, and gave us time.” Niamh, Wicklow · Daughter</td></tr>
    <tr><td>Charity number</td><td>As registered</td><td>Shown beside the logo and in the trust line under the button. It builds confidence.</td><td>Reg. Charity 20212026</td></tr>
    <tr><td>Fundraising goal</td><td>Target + label + dates</td><td>Best for events and time-limited appeals. A visible goal with progress lifts urgency.</td><td>“Garden Walk 2026 goal · €25,000”</td></tr>
  </table>
  {foot(n)}
</section>"""

TIPS = [
    ('1', 'One subject, one feeling', 'Choose images with a single clear focal point and an emotion that matches the appeal: hope, warmth, dignity. Busy collages fight the headline.'),
    ('2', 'Design for the crop', 'Check the crop diagram before choosing an image. The same file is shown very differently on desktop and phone. Keep important detail inside both boxes.'),
    ('3', 'Leave room for the words', 'Headlines sit on the image. Pick photos with sky, wall or soft background where the text lands, and never bake text or logos into the image.'),
    ('4', 'Mind the contrast', 'CHAMP darkens the image so white text reads. For pale or busy images, raise "Image overlay darkness" in the Hero banner settings and re-check the preview.'),
    ('5', 'Real, consented people', 'Authentic photos of the charity\'s own people outperform stock. Get written consent for anyone recognisable, and be extra careful with children and patients.'),
    ('6', 'Sensitive causes', 'For hospice, bereavement or health causes, show hope rather than illness: gardens, light, hands, family moments. Flowers and nature suit in-memory giving.'),
    ('7', 'Colour that matches', 'Pick the campaign colours from the image. Choose a primary dark enough for white text (CHAMP warns you if it isn\'t). Use the accent for the donate button.'),
    ('8', 'Export properly', 'Supply at the listed size, which is already 2× for sharp screens. Use JPG at 80–85% quality in sRGB. Logos go in as transparent PNG or SVG.'),
    ('9', 'Host it well', 'Use a direct https link to the image file. Google Drive, Dropbox and social links are not direct image links. To swap an image, upload it under a new filename, because the old one can stay cached.'),
]

def tips_page(n):
    cards = ''.join(f'<div class="tip box"><h3><em>{i}</em>{e(t)}</h3><p style="margin:0">{e(d)}</p></div>' for i, t, d in TIPS)
    return f"""
<section class="page">
  <div class="kicker">Design tips</div>
  <h2>Nine habits of donation pages that convert</h2>
  <p class="tag">Apply these on top of each layout's spec.</p>
  <div class="tipgrid">{cards}</div>
  {foot(n)}
</section>"""

def checklist_page(n):
    items = [
        ('Hero image', 'One per campaign, at the size for the chosen layout (see the quick reference)'),
        ('Logo, light version', '240 × 80 px transparent PNG or SVG, light text, for the Logo URL'),
        ('Logo, dark version', 'For emails and white backgrounds'),
        ('Brand colours', 'Primary, accent and success, as hex codes'),
        ('Font', 'A Google Font name, or "use CHAMP default"'),
        ('Charity number', 'As registered with the Charities Regulator / Commission'),
        ('Headline + description', 'Headline up to ~60 characters, plus two short sentences'),
        ('Amounts + impact lines', '3–4 amounts, each with a short "what it does" line, and the default amount'),
        ('Testimonials', 'Up to 5 quotes, with name, role and consent confirmed'),
        ('Goal (optional)', 'Target, label, start and end dates'),
    ]
    rows = ''.join(f'<tr><td style="width:6mm;font-size:12pt;color:var(--teal)">☐</td><td style="width:52mm">{e(a)}</td><td>{e(b)}</td></tr>' for a, b in items)
    gotchas = [
        ('Drafts vs published', 'Edits save as a Draft. The campaign list and public page keep showing the last published version, and a never-published campaign shows as Classic. Click Publish, or preview with ?draft=true while logged in.'),
        ('Duplicates start paused', 'Duplicating a campaign switches Campaign active off on the copy, and the page shows "This campaign is on hold". Switch it back on.'),
        ('Pre-filled fields', 'The Logo URL and goal Target amount can come pre-filled. Clear them before pasting, or the new value is appended to the old one.'),
        ('Charity name', 'The name beside the logo and in the donation summary comes from the charity-wide Settings, not from the campaign.'),
        ('Image right on phones', 'The image moves below the form, so the first thing a phone donor sees is the form.'),
    ]
    g = ''.join(f'<div style="margin-bottom:3mm"><h3 style="margin:0 0 .6mm">{e(a)}</h3><p style="margin:0">{e(b)}</p></div>' for a, b in gotchas)
    return f"""
<section class="page">
  <div style="display:grid;grid-template-columns:1.15fr 1fr;gap:9mm">
    <div>
      <div class="kicker">Checklist</div>
      <h2>What to ask the charity for</h2>
      <p class="tag">Send this list at kick-off. With everything here, a campaign can be set up in one sitting.</p>
      <table class="ref">{rows}</table>
    </div>
    <div class="box" style="align-self:start">
      <div class="kicker" style="color:var(--coral)">Admin notes</div>
      <h3 style="font-size:13pt;margin-bottom:3mm">Things we learned setting these up</h3>
      {g}
    </div>
  </div>
  {foot(n)}
</section>"""

def files_page(n):
    rows = ''
    for L in LAYOUTS:
        rows += f"<tr><td>{L['name']}</td><td><code>{L['lantern'].split('/')[-1]}</code></td><td><code>{L['willow'].split('/')[-1]}</code></td></tr>"
    rows += "<tr><td>Logo (light)</td><td><code>lantern-trust-logo-240x80-light.png</code></td><td><code>willowmere-logo-240x80-light.png</code></td></tr>"
    rows += "<tr><td>Logo (dark)</td><td><code>lantern-trust-logo-240x80-dark.png</code></td><td><code>willowmere-logo-240x80-dark.png</code></td></tr>"
    return f"""
<section class="page">
  <div class="kicker">Files</div>
  <h2>Where the example images live</h2>
  <p class="tag">All files are in <b>github.com/ConorEgan1997/demoimages</b>. Paste the raw link straight into CHAMP's Hero image URL or Logo URL field.</p>
  <table class="ref">
    <tr><th style="width:30mm">Layout</th><th>Example 1 · Lantern Trust<br><span style="text-transform:none;letter-spacing:0">…/main/demo-campaign-images/</span></th><th>Example 2 · Willowmere Hospice<br><span style="text-transform:none;letter-spacing:0">…/main/hospice-flowers/</span></th></tr>
    {rows}
  </table>
  <div class="cols2" style="margin-top:6mm">
    <div class="box"><h3>Brand colours used</h3>
      <p style="margin:0"><b>Lantern Trust</b> · Primary #14233C navy · Accent #F2A93B amber · Success #2F7F79 teal · Poppins + Playfair Display</p>
      <p style="margin:2mm 0 0"><b>Willowmere Hospice</b> · Primary #4B2E4F plum · Accent #F4D06F butter · Success #6E8F72 sage</p></div>
    <div class="box"><h3>About the screenshots</h3>
      <p style="margin:0">Lantern Trust screenshots are the live DEMO draft campaigns. The Willowmere screenshots use the same DEMO pages with the hospice images, logo, colours and copy applied in the browser for illustration. They are not saved in CHAMP.</p></div>
  </div>
  {foot(n)}
</section>"""

def build():
    pages = [cover(), quickref(2), logo_page(3)]
    n = 4
    for L in LAYOUTS:
        pages.append(spec_page(L, n)); n += 1
        pages.append(shots_page(L, n)); n += 1
    pages += [copy_page(n), tips_page(n + 1), checklist_page(n + 2), files_page(n + 3)]
    doc = f'<!doctype html><html><head><meta charset="utf-8"><title>CHAMP campaign image asset pack</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    (A / 'assetpack.html').write_text(doc)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto(u(A / 'assetpack.html')); pg.wait_for_load_state('networkidle')
        pg.pdf(path=str(A / 'CHAMP-Campaign-Image-Asset-Pack.pdf'), format='A4', landscape=True, print_background=True,
               margin=dict(top='0', bottom='0', left='0', right='0'))
        b.close()

if __name__ == '__main__':
    build()
    print('ok')
