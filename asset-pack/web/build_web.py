"""Charity-facing image guide as a WordPress-ready HTML snippet.

Paste into a Custom HTML block. No JavaScript. All CSS is scoped under .cdg (doubled for
specificity so theme styles such as `.entry-content table td` don't override it).
Images are served from jsDelivr, pinned to a commit of github.com/ConorEgan1997/demoimages.
"""
import html, pathlib, re, sys

SHA = sys.argv[1] if len(sys.argv) > 1 else 'main'
CDN = f'https://cdn.jsdelivr.net/gh/ConorEgan1997/demoimages@{SHA}/'
IMG = CDN + 'asset-pack/web/img/'
e = html.escape

LAYOUTS = [
    dict(key='classic', name='Classic', best='Bigger gifts and flagship appeals',
         why='A step-by-step form with a donation summary and rotating supporter quotes beside it.',
         size='1600 × 600 px', ratio='8:3 wide', maxf='2 MB',
         how='A wide banner across the top of a step-by-step donation form. The top and bottom edges are trimmed, and trimmed more on a phone, where the banner becomes almost square.',
         subject='Keep the main subject in the middle of the frame. Treat the top and bottom 15% or so as edges that may be cut off.',
         covered='Your logo, charity name, headline and description sit over the left and middle of the image. A soft dark overlay keeps the white text readable.',
         dos=['A calm scene with one clear focal point in the centre', 'Simple sky or background where the headline sits', 'A subject that is still recognisable when cropped to a square'],
         donts=['Faces or detail near the top or bottom edge', 'Words, logos or dates in the image (unless you use Banner style)', 'Very busy scenes, which fight the headline'],
         banner=True, lname='Christmas Appeal 2026', wname='Light up a life this Christmas'),
    dict(key='compact', name='Compact', best='Quick gifts and website embeds',
         why='Everything on one short page, ideal inside your own website or for simple appeals.',
         size='1200 × 480 px', ratio='5:2 wide', maxf='1.5 MB',
         how='A compact banner above a narrow, single-page donation form. It looks the same size on a computer and on a phone.',
         subject='Centre the subject and keep it in the upper half. The lower-left quarter must stay clear.',
         covered='Your logo sits top-left. The headline sits across the lower-left, which is why that corner needs to stay quiet.',
         dos=['A single object or close-up (a bouquet, a meal, a hand)', 'Plain or softly textured lower-left corner', 'Strong colour that still reads at a small size'],
         donts=['Anything important in the lower-left', 'Wide landscapes with small detail, which disappear at this size', 'Re-using a Classic 1600 × 600 image, which crops badly'],
         banner=True, lname='Warm Meal Fund', wname='Send flowers to someone who needs comfort'),
    dict(key='imageleft', name='Image left', best='Story-led appeals',
         why='A strong portrait photo carries the story, with supporter quotes over the image.',
         size='1120 × 1280 px', ratio='7:8 near-square portrait', maxf='2.5 MB',
         how='Fills a tall column beside the donation form on a computer. On a phone it becomes a short banner above the form.',
         subject='Put the subject in the centre, so it works in both the tall computer column and the short phone banner.',
         covered='Logo, headline and description cover the top half. Rotating supporter quotes sit over the lower half.',
         dos=['A portrait or near-square photo', 'Subject centred, with some breathing room', 'Mid to dark tones, so white text and quotes read well'],
         donts=['A wide banner image, which is the wrong shape', 'Subject at the very top, where the headline sits', 'Bright white images, which make the quotes hard to read'],
         lname='A Home for Every Family', wname='Care that lets every moment matter'),
    dict(key='imageright', name='Image right', best='Donors who are ready to give',
         why='The form comes first, and the image supports it.',
         size='1120 × 1280 px', ratio='7:8 near-square portrait', maxf='2.5 MB',
         how='Like Image left, but the image sits on the right. On a phone the image moves below the form, so donors see the form first.',
         subject='Place faces and the main subject just below the centre, because the headline covers the top half of the image.',
         covered='Logo, headline and description cover the top half. There are no supporter quotes over the image in this layout.',
         dos=['Subject slightly below centre', 'Open sky or plain background in the top half', 'An image that works as a closing visual on a phone'],
         donts=['Faces in the top half, where they end up under the headline', 'Relying on the image as the first thing a phone visitor sees', 'Wide landscape banners'],
         lname='Winter Coat Drive', wname='Grow something beautiful in their memory'),
    dict(key='herobanner', name='Hero banner', best='Events and fundraising goals',
         why='A wide panoramic strip with a centred form, and a goal thermometer if you want one.',
         size='1920 × 600 px', ratio='16:5 extra-wide', maxf='2.5 MB',
         how='A thin strip across the full width of the page. Only a narrow band through the middle of the image is visible on a computer screen.',
         subject='Run your subject across the horizontal middle. Treat the top and bottom thirds as background that will mostly be hidden.',
         covered='Your logo, charity name, headline and description sit in one line across the strip.',
         dos=['A repeating or panoramic subject (a crowd, a skyline, a flower border)', 'Detail concentrated in the middle band', 'Even tone across the width, so text reads everywhere'],
         donts=['A single subject in the centre, which ends up behind the headline', 'Any detail near the top or bottom', 'Busy high-contrast patterns behind the text'],
         lname='Lantern Walk 2026', wname='Walk our garden of remembrance'),
    dict(key='immersive', name='Immersive', best='Seasonal and in-memory campaigns',
         why='A full-screen, atmospheric image with the form floating on top. Our most emotive layout.',
         size='1920 × 1080 px', ratio='16:9 full-screen', maxf='3 MB',
         how='Fills the whole screen behind the donation form, which floats over the centre. On a phone the form covers most of the image and only the top shows.',
         subject='Place the main subject to the left or right. A centred subject is hidden behind the form. Keep the top of the image attractive, because that is all phones see.',
         covered='Logo, headline and description sit above the form, centred at the top. The form covers the middle third.',
         dos=['An atmospheric, full-bleed scene', 'Subject on the left or right third', 'Interest at the top of the frame for phones'],
         donts=['A centred subject, which ends up behind the form', 'Words or logos in the photo, which get sliced at different screen sizes', 'Low-resolution images, which look soft when stretched to full screen'],
         lname='Light a Lantern', wname='A meadow of memories'),
]
THUMB = {'classic': 'lantern', 'compact': 'willow', 'imageleft': 'willow', 'imageright': 'lantern', 'herobanner': 'willow', 'immersive': 'lantern'}

TIPS = [
    ('One subject, one feeling', 'Choose a photo with one clear focal point and an emotion that matches your appeal: hope, warmth, dignity. Busy collages fight the headline.'),
    ('Think about the crop', 'Check the crop diagram for your layout. The same image looks very different on a computer and a phone, so keep the important part inside both outlines.'),
    ('Leave room for the words', 'Your headline sits on the image. Photos with sky, a wall or a soft background where the text goes work best.'),
    ('Mid to dark tones', 'White text sits on your image under a soft dark overlay. Very pale or very busy photos make text harder to read. We can adjust the overlay if needed.'),
    ('Real people, with consent', 'Your own people and places beat stock photos. Get written consent from anyone recognisable, and take extra care with children and patients.'),
    ('Sensitive causes', 'For hospice, bereavement or health causes, show hope rather than illness: gardens, light, hands, family moments. Flowers and nature suit in-memory giving.'),
    ('Colours from your brand', 'Send your brand colours as hex codes, such as #4B2E4F. We use your main colour for links and highlights and your accent colour for the donate button.'),
    ('Export at full size', 'Send images at the size listed for your layout. They are already double-size so they stay sharp on modern screens. JPG at high quality is ideal.'),
    ('Send the files themselves', 'Attach the files or send a download link. If you replace an image later, give it a new filename so the update shows straight away.'),
]

SEND = [
    ('Your chosen layout', 'Or send your best photo and ask us to suggest one'),
    ('Main image', 'At the size for your layout (see the table in Step 2)'),
    ('Logo, light version', '240 × 80 px transparent PNG or SVG, with white or light text'),
    ('Logo, dark version', 'Optional, for white backgrounds and Banner style'),
    ('Brand colours', 'Main colour and accent colour, as hex codes'),
    ('Font', 'A Google Font name, or leave it to us'),
    ('Charity number', 'As registered'),
    ('Headline and description', 'Headline up to ~60 characters, plus two short sentences'),
    ('Amounts and impact lines', '3–4 amounts, each with a short "what it does" line, and which one to pre-select'),
    ('Supporter quotes', 'Up to 5, with first name, role or county, and consent to use them'),
    ('Fundraising goal (optional)', 'Target amount, label, start and end dates'),
]
CHECK = ['The image is the right size for your layout', 'The main subject sits inside both crop outlines', 'No words, logos or dates in the image (unless you chose Banner style)',
         'You have consent from anyone who can be recognised', 'Your logo has a transparent background and light text', 'Each file is under the size limit']

CSS = """
.cdg{--ink:#14233C;--ink2:#3A4A63;--mute:#6B7689;--line:#E3E7EE;--bg:#F6F7FA;--teal:#18A096;--coral:#E8604C;--gold:#D9A21F;--plum:#4B2E4F;
  color:var(--ink2);font-size:16px;line-height:1.6;width:100%;max-width:1100px;margin:0 auto;text-align:left;contain:inline-size;min-width:0}
.cdg *{box-sizing:border-box}
.cdg h2,.cdg h3,.cdg h4{color:var(--ink);font-family:inherit;line-height:1.2;letter-spacing:-.01em;margin:0;padding:0;text-transform:none;border:0;background:none}
.cdg h2{font-size:28px;font-weight:800;margin:0 0 6px}
.cdg h3{font-size:20px;font-weight:750;margin:0 0 4px}
.cdg h4{font-size:15px;font-weight:700;margin:0 0 4px}
.cdg p{margin:0 0 12px;padding:0;color:var(--ink2);font-size:16px}
.cdg a{color:var(--teal);text-decoration:underline;text-underline-offset:2px}
.cdg img{display:block;max-width:100%;height:auto;margin:0;padding:0;border:0;box-shadow:none;border-radius:0}
.cdg ul{margin:0 0 12px;padding:0 0 0 20px;list-style:disc outside}
.cdg li{margin:0 0 6px;padding:0;color:var(--ink2);font-size:15px;background:none;list-style:inherit;border:0}
.cdg li::before{content:none}
.cdg figure{margin:0;padding:0;border:0;background:none;width:auto;max-width:100%}
.cdg figcaption{font-size:13px;color:var(--mute);margin:8px 0 0;line-height:1.4;text-align:left;font-style:normal}
.cdg table{width:100%;table-layout:auto;border-collapse:collapse;margin:0;border:0;background:#fff;font-size:15px}
.cdg th,.cdg td{border:0;border-bottom:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top;background:none;color:var(--ink2)}
.cdg th{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);font-weight:700;border-bottom:2px solid var(--ink)}
.cdg td:first-child{font-weight:700;color:var(--ink)}
.cdg .cdg-tbl{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);border-radius:12px;margin:0 0 16px}
.cdg .cdg-tbl table{min-width:640px}
.cdg .cdg-kicker{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin:0 0 6px}
.cdg .cdg-lead{font-size:18px;color:var(--ink2);margin:0 0 20px}
.cdg .cdg-sec{margin:0 0 56px;scroll-margin-top:90px}
.cdg .cdg-hero{position:relative;border-radius:18px;overflow:hidden;margin:0 0 36px;background:#2A1A2E}
.cdg .cdg-hero img{width:100%;aspect-ratio:16/7;object-fit:cover}
.cdg .cdg-hero-txt{position:absolute;inset:0;padding:clamp(18px,4vw,44px);display:flex;flex-direction:column;justify-content:flex-end;
  background:linear-gradient(0deg,rgba(30,16,34,.88) 0%,rgba(30,16,34,.45) 55%,rgba(30,16,34,0) 100%)}
.cdg .cdg-hero-txt h2{color:#fff;font-size:clamp(24px,4.2vw,42px);margin:0 0 8px}
.cdg .cdg-hero-txt p{color:#EEE3EE;font-size:clamp(14px,1.7vw,18px);margin:0;max-width:640px}
.cdg .cdg-toc{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 40px}
.cdg .cdg-toc a{display:inline-block;text-decoration:none;font-size:14px;font-weight:600;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:99px;padding:6px 14px}
.cdg .cdg-toc a:hover{border-color:var(--teal);color:var(--teal)}
.cdg .cdg-grid3{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
.cdg .cdg-grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}
.cdg .cdg-card{background:var(--bg);border-radius:14px;padding:16px;border:1px solid var(--line)}
.cdg .cdg-card a.cdg-cardlink{text-decoration:none;color:inherit;display:block}
.cdg .cdg-thumb{border-radius:10px;overflow:hidden;border:1px solid var(--line);background:#fff;aspect-ratio:16/10;margin:0 0 12px}
.cdg .cdg-thumb img{width:100%;height:100%;object-fit:cover;object-position:top}
.cdg .cdg-best{font-weight:700;color:var(--ink);font-size:14px;margin:0 0 4px}
.cdg .cdg-small{font-size:14px;margin:0 0 6px}
.cdg .cdg-meta{font-size:13px;color:var(--mute);margin:0}
.cdg .cdg-specs{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:14px 0 18px}
.cdg .cdg-specs div{background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:10px 14px}
.cdg .cdg-specs b{display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);font-weight:700}
.cdg .cdg-specs span{font-size:17px;font-weight:750;color:var(--ink)}
.cdg .cdg-layout{border-top:1px solid var(--line);padding-top:32px;margin-top:32px}
.cdg .cdg-two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:28px;align-items:start}
.cdg .cdg-do,.cdg .cdg-dont{list-style:none;padding:0;margin-left:0}
.cdg .cdg-do li,.cdg .cdg-dont li{padding-left:24px;position:relative;list-style:none}
.cdg .cdg-do li::before,.cdg .cdg-dont li::before{position:absolute;left:0;top:0;font-weight:800}
.cdg .cdg-do li::before{content:"✓";color:var(--teal)}
.cdg .cdg-dont li::before{content:"✕";color:var(--coral)}
.cdg .cdg-legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:13px;color:var(--ink2);margin:0 0 12px}
.cdg .cdg-legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px}
.cdg .cdg-shot{border-radius:10px;overflow:hidden;border:1px solid var(--line);box-shadow:0 2px 10px rgba(20,35,60,.12);background:#fff}
.cdg .cdg-chip{display:inline-block;font-size:12px;font-weight:700;color:#fff;border-radius:99px;padding:3px 10px;margin:0 0 8px}
.cdg .cdg-chip.l{background:var(--ink)} .cdg .cdg-chip.w{background:var(--plum)}
.cdg .cdg-finished{display:grid;grid-template-columns:minmax(0,1fr) 150px;gap:14px;align-items:start}
.cdg .cdg-note{background:#FFF8E6;border:1px solid #F3D98C;border-radius:14px;padding:16px 18px;margin:18px 0 0}
.cdg .cdg-note h4{color:#6B4E06}
.cdg .cdg-note p,.cdg .cdg-note li{color:#5A4A22;font-size:15px}
.cdg .cdg-logos{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.cdg .cdg-logos div{border-radius:12px;display:flex;align-items:center;justify-content:center;padding:26px 16px;border:1px solid var(--line)}
.cdg .cdg-logos img{height:56px;width:auto}
.cdg .cdg-tip{background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:16px}
.cdg .cdg-tip h4{display:flex;gap:10px;align-items:center}
.cdg .cdg-tip h4 em{font-style:normal;flex:none;display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:7px;background:var(--ink);color:#fff;font-size:13px}
.cdg .cdg-tip p{font-size:15px;margin:0}
.cdg .cdg-check td:first-child{width:32px;color:var(--teal);font-size:18px}
.cdg .cdg-next{background:var(--plum);border-radius:14px;padding:18px 20px;color:#fff}
.cdg .cdg-next h4{color:#fff} .cdg .cdg-next p{color:#EADFEA;margin:0}
.cdg .cdg-top{font-size:13px;margin:16px 0 0}
.cdg .cdg-foot{font-size:13px;color:var(--mute);border-top:1px solid var(--line);padding-top:14px;margin-top:20px}
@media (max-width:760px){
  .cdg .cdg-two{grid-template-columns:1fr}
  .cdg .cdg-finished{grid-template-columns:minmax(0,1fr) 110px}
  .cdg h2{font-size:24px}
}
"""
# double the scope class so we out-rank typical theme selectors like `.entry-content table td`
CSS = re.sub(r'(^|[,{}]\s*)\.cdg\b', lambda m: m.group(1) + '.cdg.cdg', CSS.strip())
CSS = re.sub(r'\n\s*', '', CSS)

def img(name, alt, cls='', lazy=True, extra=''):
    return f'<img src="{IMG}{name}" alt="{e(alt)}"{" loading=\"lazy\"" if lazy else ""} decoding="async"{(" class=" + chr(34) + cls + chr(34)) if cls else ""}{extra}>'

def legend():
    return ('<div class="cdg-legend"><span><i style="background:#18A096"></i>Seen on a computer</span>'
            '<span><i style="background:#E7B53A"></i>Seen on a phone</span>'
            '<span><i style="background:#E8604C"></i>Covered by text or the form</span><span style="color:#6B7689">Faded = cropped off</span></div>')

def section_layout(L):
    k = L['key']
    lis = lambda xs, c: f'<ul class="{c}">' + ''.join(f'<li>{e(x)}</li>' for x in xs) + '</ul>'
    banner = ''
    if L.get('banner'):
        banner = ('<div class="cdg-note"><h4>Prefer your artwork untouched? Use Banner style</h4>'
                  '<p>On this layout we can show your image whole, with no cropping, no darkening and nothing placed over it. Your headline then appears below the image. '
                  'Use it for designed artwork that already includes your logo and title, or if your image is light and your logo is dark.</p>'
                  '<p style="margin:0">Keep any words in the artwork large, because a phone shows it at about a quarter of the size. Tell us what the artwork says, so we can add it for screen-reader users.</p></div>')
    zones = ''.join(f'<figure><div class="cdg-shot">{img(f"{k}-{b}-zones.jpg", f"Crop diagram for the {L["name"]} layout, example {i+1}")}</div>'
                    f'<figcaption><span class="cdg-chip {"l" if b=="lantern" else "w"}" style="margin:0 6px 0 0">Example {i+1}</span>{e(L["lname"] if b=="lantern" else L["wname"])}</figcaption></figure>'
                    for i, b in enumerate(['lantern', 'willow']))
    zgrid = 'cdg-grid2' if k in ('imageleft', 'imageright') else ''
    zones = f'<div class="{zgrid}" style="display:grid;gap:16px">{zones}</div>' if not zgrid else f'<div class="cdg-grid2" style="grid-template-columns:repeat(2,minmax(0,1fr));gap:14px">{zones}</div>'
    def finished(b, i):
        nm = L['lname'] if b == 'lantern' else L['wname']
        note = ' On a phone this image sits below the form (shown scrolled down).' if k == 'imageright' else ''
        return (f'<figure><span class="cdg-chip {"l" if b=="lantern" else "w"}">{"Lantern Trust" if b=="lantern" else "Willowmere Hospice"}</span>'
                f'<div class="cdg-finished"><div class="cdg-shot">{img(f"{k}-{b}-desktop.jpg", f"{L["name"]} layout on a computer: {nm}")}</div>'
                f'<div class="cdg-shot">{img(f"{k}-{b}-phone.jpg", f"{L["name"]} layout on a phone: {nm}")}</div></div>'
                f'<figcaption>“{e(nm)}”. Left: on a computer. Right: on a phone.{note}</figcaption></figure>')
    return f"""<div class="cdg-layout" id="cdg-{k}">
<div class="cdg-kicker">Layout guide</div><h3>{e(L['name'])}</h3><p class="cdg-small" style="color:#6B7689">Best for: {e(L['best'])}</p>
<div class="cdg-specs"><div><b>Image size</b><span>{L['size']}</span></div><div><b>Shape</b><span>{L['ratio']}</span></div><div><b>Format</b><span>JPG or PNG</span></div><div><b>Max file</b><span>{L['maxf']}</span></div></div>
<div class="cdg-two"><div>
<h4>How it sits on the page</h4><p>{e(L['how'])}</p>
<h4>Where to put the subject</h4><p>{e(L['subject'])}</p>
<h4>What covers the image</h4><p>{e(L['covered'])}</p>
<div class="cdg-grid2" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px"><div><h4 style="color:#18A096">Do</h4>{lis(L['dos'],'cdg-do')}</div><div><h4 style="color:#E8604C">Avoid</h4>{lis(L['donts'],'cdg-dont')}</div></div>
{banner}
</div><div><h4>How your image is cropped</h4>{legend()}{zones}</div></div>
<h4 style="margin-top:26px">The finished page</h4>
<div class="cdg-grid2" style="margin-top:10px">{finished('lantern',0)}{finished('willow',1)}</div>
<p class="cdg-top"><a href="#cdg-top">↑ Back to top</a></p>
</div>"""

def build():
    choose = ''.join(f"""<div class="cdg-card"><a class="cdg-cardlink" href="#cdg-{L['key']}"><div class="cdg-thumb">{img(f"{L['key']}-{THUMB[L['key']]}-desktop.jpg", f"Example of the {L['name']} layout")}</div>
<h4>{e(L['name'])}</h4><p class="cdg-best">Best for: {e(L['best'])}</p><p class="cdg-small">{e(L['why'])}</p><p class="cdg-meta">Image: {L['size']} · {L['ratio']}</p></a></div>""" for L in LAYOUTS)
    qrows = ''.join(f"<tr><td><a href=\"#cdg-{L['key']}\">{e(L['name'])}</a></td><td>{L['size']}</td><td>{L['ratio']}</td><td>≤ {L['maxf']}</td><td>{e(L['subject'])}</td></tr>" for L in LAYOUTS)
    qrows += '<tr><td><a href="#cdg-logo">Logo</a></td><td>240 × 80 px</td><td>3:1</td><td>≤ 200 KB</td><td>Transparent PNG or SVG, in a light version that reads on a dark background.</td></tr>'
    tips = ''.join(f'<div class="cdg-tip"><h4><em>{i+1}</em>{e(t)}</h4><p>{e(d)}</p></div>' for i, (t, d) in enumerate(TIPS))
    send = ''.join(f'<tr><td>☐</td><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in SEND)
    check = ''.join(f'<li>{e(c)}</li>' for c in CHECK)
    logo = lambda p, alt: f'<img src="{CDN}{p}" alt="{e(alt)}" loading="lazy">'
    body = f"""<div class="cdg" id="cdg-top">
<div class="cdg-hero"><img src="{IMG.replace('asset-pack/web/img/','hospice-flowers/')}immersive-golden-meadow-1920x1080.jpg" alt="Illustrated meadow of wildflowers at golden hour" decoding="async"><div class="cdg-hero-txt"><h2>Preparing images for your donation page</h2><p>How to choose a page layout, prepare the right images, and what to send us, so your page looks sharp on every screen.</p></div></div>
<nav class="cdg-toc" aria-label="On this page"><a href="#cdg-step1">1. Choose a layout</a><a href="#cdg-step2">2. Prepare your image</a><a href="#cdg-logo">Your logo</a><a href="#cdg-layouts">Layout guides</a><a href="#cdg-words">Words on the page</a><a href="#cdg-tips">Tips</a><a href="#cdg-step3">3. What to send us</a></nav>

<section class="cdg-sec" id="cdg-step1"><div class="cdg-kicker">Step 1</div><h2>Choose a layout</h2>
<p class="cdg-lead">Each layout uses a different image shape, so pick the layout first. Not sure? Send us your best photo and we'll suggest one.</p>
<div class="cdg-grid3">{choose}</div></section>

<section class="cdg-sec" id="cdg-step2"><div class="cdg-kicker">Step 2</div><h2>Prepare one image, sized for your layout</h2>
<p class="cdg-lead">Each layout crops the image differently. Supply the size listed and your subject will land in the right place.</p>
<div class="cdg-tbl"><table><thead><tr><th>Layout</th><th>Image size</th><th>Shape</th><th>Max file</th><th>Where to put the subject</th></tr></thead><tbody>{qrows}</tbody></table></div>
<div class="cdg-card"><h4>For every image</h4><ul>
<li>JPG for photos and illustrations, PNG for logos.</li>
<li>Send the original files, not screenshots or images saved from social media.</li>
<li>No words, prices or dates in the image. We add your headline to the page as text. The one exception is Banner style, explained below.</li>
<li>Only use photos you have the rights to, with consent from anyone who can be recognised.</li></ul></div></section>

<section class="cdg-sec" id="cdg-logo"><div class="cdg-kicker">Your logo</div><h2>A small, transparent logo that reads on dark</h2>
<p class="cdg-lead">Your logo appears at the top of every donation page, usually on top of your image.</p>
<div class="cdg-two"><div>
<div class="cdg-specs" style="margin-top:0"><div><b>Size</b><span>240 × 80 px</span></div><div><b>Shape</b><span>3:1</span></div><div><b>Format</b><span>PNG or SVG</span></div><div><b>Max file</b><span>200 KB</span></div></div>
<h4>Why we ask for a light version</h4><p>On most layouts your logo sits over your image, which has a soft dark overlay so white text stays readable. That overlay is there even when your photo is light, so a dark logo would disappear against it. Please send a version with white or light text.</p>
<ul class="cdg-do"><li>A symbol plus your name reads best at this small size</li><li>Transparent background, with no white box around it</li><li>If you can, export at 3× (720 × 240) for extra-sharp screens</li></ul>
</div><div>
<div class="cdg-logos"><div style="background:#14233C">{logo('demo-campaign-images/lantern-trust-logo-240x80-light.png','Lantern Trust logo, light version')}</div><div style="background:#fff">{logo('demo-campaign-images/lantern-trust-logo-240x80-dark.png','Lantern Trust logo, dark version')}</div>
<div style="background:#4B2E4F">{logo('hospice-flowers/willowmere-logo-240x80-light.png','Willowmere Hospice logo, light version')}</div><div style="background:#fff">{logo('hospice-flowers/willowmere-logo-240x80-dark.png','Willowmere Hospice logo, dark version')}</div></div>
<p class="cdg-meta" style="margin-top:8px">Left: light version, used on your page. Right: dark version, used on white backgrounds.</p>
</div></div>
<div class="cdg-note"><h4>Only have a dark logo, or a light image?</h4>
<ul><li><b>Classic or Compact layout:</b> choose <b>Banner style</b>. Your image is shown whole and untouched, with no overlay, and your headline goes below it. Your artwork can then carry your dark logo itself.</li>
<li><b>Any other layout:</b> the overlay is always on, so a light logo is needed. If you only have a dark version, send it and we can create a white version for you.</li></ul></div>
</section>

<section class="cdg-sec" id="cdg-layouts"><div class="cdg-kicker">Layout guides</div><h2>Each layout, in detail</h2>
<p class="cdg-lead" style="margin-bottom:0">For each layout: what to supply, how it is cropped on a computer and a phone, and the finished page for our two example charities.</p>
{''.join(section_layout(L) for L in LAYOUTS)}</section>

<section class="cdg-sec" id="cdg-words"><div class="cdg-kicker">Words on the page</div><h2>The image sets the mood. The words do the asking.</h2>
<p class="cdg-lead">Along with your image, send us these words. The limits keep the text clear of your image and easy to read on a phone.</p>
<div class="cdg-tbl"><table><thead><tr><th>Field</th><th>Length</th><th>Guidance</th><th>Example (hospice)</th></tr></thead><tbody>
<tr><td>Headline</td><td>Up to ~60 characters</td><td>One idea, written to the donor. Specific beats generic.</td><td>“Care that lets every moment matter”</td></tr>
<tr><td>Description</td><td>Two short sentences</td><td>First sentence: the need, with a real number. Second sentence: what the gift does.</td><td>“Our nurses care for 1,200 people a year, at home and in our hospice. Your gift gives families comfort, dignity and time together.”</td></tr>
<tr><td>Amounts</td><td>3–4 amounts, plus Other</td><td>Tell us which amount to pre-select. A middle amount works well, because most donors pick it or the one beside it.</td><td>€25 · <b>€50</b> · €100 · €250</td></tr>
<tr><td>Impact text</td><td>Under ~40 characters</td><td>Concrete and tangible. Start with a verb.</td><td>“funds a night of specialist hospice care”</td></tr>
<tr><td>Supporter quotes</td><td>Up to 5, under ~120 characters each</td><td>Real voices, with consent. First name and county or role. Keep the tone warm and avoid graphic detail.</td><td>“The nurses gave Mam peace, and gave us time.” Niamh, Wicklow, Daughter</td></tr>
<tr><td>Charity number</td><td>As registered</td><td>Shown beside your logo and under the donate button. It builds trust.</td><td>Reg. Charity 20212026</td></tr>
<tr><td>Fundraising goal</td><td>Target, label and dates</td><td>Best for events and time-limited appeals. A visible goal adds urgency.</td><td>“Garden Walk 2026 goal · €25,000”</td></tr>
</tbody></table></div></section>

<section class="cdg-sec" id="cdg-tips"><div class="cdg-kicker">Tips</div><h2>Nine tips for a page that inspires giving</h2>
<p class="cdg-lead">Use these alongside the guidance for your layout.</p>
<div class="cdg-grid3">{tips}</div></section>

<section class="cdg-sec" id="cdg-step3"><div class="cdg-kicker">Step 3</div><h2>What to send us</h2>
<p class="cdg-lead">Send everything together to your CHAMP contact, as attachments or a download link. With all of this, we can usually set up your page in one go.</p>
<div class="cdg-two" style="grid-template-columns:minmax(0,1.3fr) minmax(0,1fr)">
<div class="cdg-tbl cdg-check" style="margin:0"><table style="min-width:0"><tbody>{send}</tbody></table></div>
<div style="display:grid;gap:16px"><div class="cdg-card"><h4>Before you send: a 30-second check</h4><ul class="cdg-do">{check}</ul></div>
<div class="cdg-next"><h4>What happens next</h4><p>We build your page and send you a private preview link to check it on your computer and phone. Once you're happy, we make it live.</p></div></div>
</div></section>

<p class="cdg-foot">The examples on this page use two fictional charities, Lantern Trust and Willowmere Hospice, created to show each layout.</p>
</div>"""
    body = re.sub(r'\n\s*\n', '\n', body)
    snippet = f'<!-- CHAMP donation page image guide. Paste into a WordPress "Custom HTML" block. -->\n<style>{CSS}</style>\n{body}\n'
    out = pathlib.Path('/home/claude/assetpack/donation-page-image-guide-wordpress.html')
    out.write_text(snippet)
    return out

if __name__ == '__main__':
    p = build(); print(p, p.stat().st_size // 1024, 'KB')
