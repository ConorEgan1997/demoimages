"""Charity-facing edition of the asset pack: same guidance and examples, no internal/admin detail."""
import copy
import build as B
from build import u, e, A, R, CSS
from playwright.sync_api import sync_playwright

TITLE = 'Preparing images for your donation page'
B.foot = lambda n, title=TITLE: f'<div class="foot"><span>{title}</span><span>{n}</span></div>'

L = {x['key']: copy.deepcopy(x) for x in B.LAYOUTS}
L['classic']['how'] = 'A wide banner across the top of a step-by-step donation form. The top and bottom edges are trimmed, and trimmed more on a phone, where the banner becomes almost square.'
L['classic']['covered'] = 'Your logo, charity name, headline and description sit over the left and middle of the image. A soft dark overlay keeps the white text readable.'
L['imageright']['subject'] = 'Place faces and the main subject just below the centre, because the headline covers the top half of the image.'
L['herobanner']['how'] = 'A thin strip across the full width of the page. Only a narrow band through the middle of the image is visible on a computer screen.'
L['herobanner']['subject'] = 'Run your subject across the horizontal middle of the image. Treat the top and bottom thirds as background that will mostly be hidden.'
L['immersive']['how'] = 'Fills the whole screen behind the donation form, which floats over the centre. On a phone the form covers most of the image and only the top shows.'
L['compact']['how'] = 'A compact banner above a narrow, single-page donation form. It looks the same size on a computer and a phone.'
L['imageleft']['how'] = 'Fills a tall column beside the donation form on a computer. On a phone it becomes a short banner above the form.'
L['imageright']['how'] = 'Like Image left, but the image sits on the right. On a phone the image moves below the form, so donors see the form first.'
ORDER = ['classic', 'compact', 'imageleft', 'imageright', 'herobanner', 'immersive']

BEST = {
    'classic': ('Bigger gifts and flagship appeals', 'A step-by-step form with a donation summary and rotating testimonials beside it.'),
    'compact': ('Quick gifts and website embeds', 'Everything on one short page, ideal inside your own website or for simple appeals.'),
    'imageleft': ('Story-led appeals', 'A strong portrait photo carries the story, with supporter quotes over the image.'),
    'imageright': ('Donors who are ready to give', 'The form comes first, and the image supports it.'),
    'herobanner': ('Events and fundraising goals', 'A wide panoramic strip with a centred form, and a goal thermometer if you want one.'),
    'immersive': ('Seasonal and in-memory campaigns', 'A full-screen, atmospheric image with the form floating on top. Our most emotive layout.'),
}

def cover():
    imL = u(R / 'demo-campaign-images/immersive-light-a-lantern-1920x1080.jpg')
    imW = u(R / 'hospice-flowers/immersive-golden-meadow-1920x1080.jpg')
    return f"""
<section class="page" style="padding:0">
  <div style="position:absolute;inset:0;background:url('{imW}') center/cover"></div>
  <div style="position:absolute;inset:0;background:url('{imL}') center/cover;clip-path:polygon(70% 0,100% 0,100% 100%,54% 100%)"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(40,22,44,.9) 0%,rgba(40,22,44,.6) 45%,rgba(40,22,44,0) 78%)"></div>
  <div style="position:absolute;left:18mm;top:22mm;width:150mm;color:#fff">
    <div class="kicker" style="color:#F4D06F">Your CHAMP donation page</div>
    <h1 style="font-size:44pt;line-height:1.02;color:#fff">Preparing images<br>for your donation page</h1>
    <p style="color:#EADFEA;font-size:12pt;line-height:1.5;margin:6mm 0 0;max-width:132mm">
      A short guide to choosing a page layout, preparing the right images, and what to send us. Follow it and your page will look sharp on every screen.</p>
  </div>
  <div style="position:absolute;left:18mm;bottom:10mm;font-size:7.5pt;color:#CDBFD0">The examples in this guide use two fictional charities, Lantern Trust and Willowmere Hospice, created to show each layout.</div>
</section>"""

def choose_page(n):
    cards = ''
    for k in ORDER:
        x = L[k]; best, why = BEST[k]
        shot = u(A / 'shots' / f'{k}-willow-desktop.jpg') if k in ('compact', 'imageleft', 'herobanner') else u(A / 'shots' / f'{k}-lantern-desktop.jpg')
        cards += f"""<div class="box" style="padding:3mm">
          <div style="height:44mm;border-radius:2mm;overflow:hidden;border:.3mm solid var(--line);background:#fff"><img src="{shot}" style="width:100%;height:100%;object-fit:cover;object-position:top"></div>
          <h3 style="margin:2.6mm 0 .6mm;font-size:11pt">{e(x['name'])}</h3>
          <p style="margin:0;font-weight:700;color:var(--ink);font-size:8.6pt">Best for: {e(best)}</p>
          <p style="margin:.8mm 0 0;font-size:8.2pt">{e(why)}</p>
          <p style="margin:1.4mm 0 0;font-size:7.6pt;color:var(--mute)">Image: {x['size']} · {x['ratio']}</p></div>"""
    return f"""
<section class="page">
  <div class="kicker">Step 1</div>
  <h2>Choose a layout</h2>
  <p class="tag" style="margin-bottom:4mm">Each layout uses a different image shape, so pick the layout first. Not sure? Send us your best photo and we'll suggest one.</p>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4mm">{cards}</div>
  {B.foot(n)}
</section>"""

def quickref(n):
    rows = ''.join(f"<tr><td>{L[k]['name']}</td><td>{L[k]['size']}</td><td>{L[k]['ratio']}</td><td>≤ {L[k]['maxkb']}</td><td>{e(L[k]['subject'])}</td></tr>" for k in ORDER)
    rows += "<tr><td>Logo</td><td>240 × 80 px</td><td>3:1</td><td>≤ 200 KB</td><td>Transparent PNG or SVG, in a light version that reads on a dark background. No box or background behind it.</td></tr>"
    return f"""
<section class="page">
  <div class="kicker">Step 2</div>
  <h2>Prepare one image, sized for your layout</h2>
  <p class="tag">Each layout crops the image differently. Supply the size listed and your subject will land in the right place.</p>
  <table class="ref">
    <tr><th style="width:24mm">Layout</th><th style="width:28mm">Image size</th><th style="width:36mm">Shape</th><th style="width:20mm">Max file</th><th>Where to put the subject</th></tr>
    {rows}
  </table>
  <div class="cols2" style="margin-top:6mm">
    <div class="box"><h3>For every image</h3><ul>
      <li>JPG for photos and illustrations, PNG for logos.</li>
      <li>Send the original files, not screenshots or images saved from social media.</li>
      <li>No words, prices or dates in the image. We put your headline on the page as text.</li>
      <li>Only use photos you have the rights to, with consent from anyone who can be recognised.</li></ul></div>
    <div class="box"><h3>How to read the layout pages</h3>
      <p style="margin:0 0 2mm">Each layout has two pages. The first explains the image and shows how it is cropped.</p>
      <div class="legend" style="margin:0 0 2mm"><span><i style="background:var(--teal)"></i>Seen on a computer</span><span><i style="background:#E7B53A"></i>Seen on a phone</span><span><i style="background:var(--coral)"></i>Covered by text or the form</span></div>
      <p style="margin:0">The second shows the finished page on a computer and on a phone.</p></div>
  </div>
  {B.foot(n)}
</section>"""

def logo_page(n):
    lg = lambda p: u(R / p)
    return f"""
<section class="page">
  <div class="kicker">Your logo</div>
  <h2>A small, transparent logo that reads on dark</h2>
  <p class="tag">Your logo appears at the top of every donation page, usually on top of your image.</p>
  <div style="display:grid;grid-template-columns:96mm 1fr;gap:8mm">
    <div>
      <div class="spec"><div><b>Size</b><span>240 × 80 px</span></div><div><b>Shape</b><span>3:1</span></div>
        <div><b>Format</b><span>PNG or SVG</span></div><div><b>Max file</b><span>200 KB</span></div></div>
      <h3>Why we ask for a light version</h3>
      <p>Your logo sits over your image, which has a soft dark overlay. A dark logo disappears against it, so please send a version with white or light text. If you have a dark version too, send it as well; we use it on white backgrounds.</p>
      <h3 style="margin-top:4mm">Tips</h3>
      <ul class="do"><li>A symbol plus your name reads best at this small size</li><li>Transparent background, with no white box around it</li><li>If you can, export at 3× (720 × 240) for extra-sharp screens</li></ul>
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
      <p class="cap" style="margin:-2mm 0 0">Left: light version, used on your page · Right: dark version, used on white backgrounds</p>
    </div>
  </div>
  {B.foot(n)}
</section>"""

def spec_page(x, n):
    page = B.spec_page(x, n)
    return page.replace('Desktop view</span>', 'Seen on a computer</span>').replace('Phone view</span>', 'Seen on a phone</span>')

def shots_page(x, n):
    s = lambda b, d: u(A / 'shots' / f"{x['key']}-{b}-{d}.jpg")
    note = ' Scrolled down: on a phone this image sits below the form.' if x['key'] == 'imageright' else ''
    col = lambda b, chip, name: f"""
      <div>
        <div style="margin-bottom:2mm"><span class="chip {chip}">{'Example · Lantern Trust' if chip=='l' else 'Example · Willowmere Hospice'}</span></div>
        <img src="{s(b,'desktop')}" class="shot" style="width:100%">
        <div style="display:grid;grid-template-columns:36mm 1fr;gap:4mm;margin-top:4mm;align-items:start">
          <img src="{s(b,'phone')}" class="shot" style="width:36mm">
          <div><p class="cap" style="margin:0 0 1mm;font-weight:700;color:var(--ink)">“{e(name)}”</p>
            <p class="cap" style="margin:0">Top: on a computer. Left: on a phone.{note}</p></div>
        </div>
      </div>"""
    return f"""
<section class="page" style="padding-top:11mm">
  <div class="kicker">Layout · {e(x['name'])} · the finished page</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:9mm;margin-top:2mm">
    {col('lantern','l',x['lname'])}
    {col('willow','w',x['wname'])}
  </div>
  {B.foot(n)}
</section>"""

def copy_page(n):
    pg = B.copy_page(n)
    return (pg.replace('Star the middle amount as the default. Most donors pick the pre-selected amount or the one next to it.',
                       'Tell us which amount to pre-select. A middle amount works well, because most donors pick it or the one beside it.')
              .replace('Every layout uses the same text fields. These limits keep the text clear of the image and readable on a phone.',
                       'Along with your image, send us these words. The limits keep the text clear of your image and easy to read on a phone.'))

TIPS = [
    ('1', 'One subject, one feeling', 'Choose a photo with one clear focal point and an emotion that matches your appeal: hope, warmth, dignity. Busy collages fight the headline.'),
    ('2', 'Think about the crop', 'Check the crop diagram for your layout. The same image looks very different on a computer and a phone, so keep the important part inside both outlines.'),
    ('3', 'Leave room for the words', 'Your headline sits on the image. Photos with sky, a wall or a soft background where the text goes work best.'),
    ('4', 'Mid to dark tones', 'White text sits on your image under a soft dark overlay. Very pale or very busy photos make text harder to read. We can adjust the overlay if needed.'),
    ('5', 'Real people, with consent', 'Your own people and places beat stock photos. Get written consent from anyone recognisable, and take extra care with children and patients.'),
    ('6', 'Sensitive causes', 'For hospice, bereavement or health causes, show hope rather than illness: gardens, light, hands, family moments. Flowers and nature suit in-memory giving.'),
    ('7', 'Colours from your brand', 'Send your brand colours as hex codes, such as #4B2E4F. We use your main colour for links and highlights and your accent colour for the donate button.'),
    ('8', 'Export at full size', 'Send images at the size listed for your layout. They are already double-size so they stay sharp on modern screens. JPG at high quality is ideal.'),
    ('9', 'Send the files themselves', 'Attach the files or send a download link. If you replace an image later, give it a new filename so the update shows straight away.'),
]

def tips_page(n):
    cards = ''.join(f'<div class="tip box"><h3><em>{i}</em>{e(t)}</h3><p style="margin:0">{e(d)}</p></div>' for i, t, d in TIPS)
    return f"""
<section class="page">
  <div class="kicker">Tips</div>
  <h2>Nine tips for a page that inspires giving</h2>
  <p class="tag">Use these alongside the guidance for your layout.</p>
  <div class="tipgrid">{cards}</div>
  {B.foot(n)}
</section>"""

def send_page(n):
    items = [
        ('Your chosen layout', 'Or send your best photo and ask us to suggest one'),
        ('Main image', 'At the size for your layout (see Step 2)'),
        ('Logo, light version', '240 × 80 px transparent PNG or SVG, with white or light text'),
        ('Logo, dark version', 'Optional, for white backgrounds'),
        ('Brand colours', 'Main colour and accent colour, as hex codes'),
        ('Font', 'A Google Font name, or leave it to us'),
        ('Charity number', 'As registered'),
        ('Headline + description', 'Headline up to ~60 characters, plus two short sentences'),
        ('Amounts + impact lines', '3–4 amounts, each with a short "what it does" line, and which one to pre-select'),
        ('Supporter quotes', 'Up to 5, with first name, role or county, and consent to use them'),
        ('Fundraising goal (optional)', 'Target amount, label, start and end dates'),
    ]
    rows = ''.join(f'<tr><td style="width:6mm;font-size:12pt;color:var(--teal)">☐</td><td style="width:54mm">{e(a)}</td><td>{e(b)}</td></tr>' for a, b in items)
    checks = ['Image is the right size for the layout', 'Main subject sits inside both crop outlines', 'No text, logos or dates inside the image',
              'Consent from anyone who can be recognised', 'Logo has a transparent background and light text', 'Each file is under the size limit']
    c = ''.join(f'<li>{e(x)}</li>' for x in checks)
    return f"""
<section class="page">
  <div style="display:grid;grid-template-columns:1.2fr 1fr;gap:9mm">
    <div>
      <div class="kicker">Step 3</div>
      <h2>What to send us</h2>
      <p class="tag">Send everything together to your CHAMP contact, as attachments or a download link. With all of this, we can usually set up your page in one go.</p>
      <table class="ref">{rows}</table>
    </div>
    <div style="display:grid;gap:5mm;align-self:start">
      <div class="box"><div class="kicker" style="color:var(--plum)">Before you send</div>
        <h3 style="font-size:13pt;margin-bottom:2.5mm">A 30-second check</h3><ul class="do">{c}</ul></div>
      <div class="box" style="background:#4B2E4F;color:#fff"><h3 style="color:#fff;font-size:13pt">What happens next</h3>
        <p style="color:#EADFEA;margin:0">We build your page and send you a private preview link to check it on your computer and phone. Once you're happy, we make it live.</p></div>
    </div>
  </div>
  {B.foot(n)}
</section>"""

def build():
    pages = [cover(), choose_page(2), quickref(3), logo_page(4)]
    n = 5
    for k in ORDER:
        pages.append(spec_page(L[k], n)); n += 1
        pages.append(shots_page(L[k], n)); n += 1
    pages += [copy_page(n), tips_page(n + 1), send_page(n + 2)]
    doc = f'<!doctype html><html><head><meta charset="utf-8"><title>{TITLE}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    (A / 'charity-guide.html').write_text(doc)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto(u(A / 'charity-guide.html')); pg.wait_for_load_state('networkidle')
        pg.pdf(path=str(A / 'Donation-Page-Image-Guide.pdf'), format='A4', landscape=True, print_background=True,
               margin=dict(top='0', bottom='0', left='0', right='0'))
        b.close()

if __name__ == '__main__':
    build(); print('ok')
