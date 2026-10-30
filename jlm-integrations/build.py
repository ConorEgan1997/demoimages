"""Build the JLM 'CHAMP Donate integrations' hub page + one page per integration (classic-editor HTML)."""
import json, html, re, io, pathlib
import qrcode, qrcode.image.svg

S = json.load(open('/home/claude/jlm/snippets.json'))
e = html.escape
OUT = pathlib.Path('/home/claude/jlm/pages'); OUT.mkdir(exist_ok=True)
HUB = 'champ-donate-integrations'
BASE = 'https://www.charitycompliance.net/jlm/' + HUB + '/'

CSS = """<style>.cdi{--ink:#1e1b3a;--ink2:#4a4766;--mute:#7a7794;--line:#e6e4f0;--bg:#f7f6fb;--brand:#5b2d90;--brand2:#7a3fc0;--accent:#f5b31b;font-family:inherit;color:var(--ink2);line-height:1.6;max-width:1080px;margin:0 auto;text-align:left}
.cdi *{box-sizing:border-box}.cdi h1,.cdi h2,.cdi h3{color:var(--ink);line-height:1.2;margin:0 0 10px;text-transform:none;letter-spacing:-.01em}
.cdi h1{font-size:clamp(28px,4vw,42px);font-weight:800}.cdi h2{font-size:24px;font-weight:800;margin-top:6px}.cdi h3{font-size:18px;font-weight:700}
.cdi p{margin:0 0 14px}.cdi a{color:var(--brand)}
.cdi .hero{background:linear-gradient(135deg,#3b1d63,#5b2d90 55%,#7a3fc0);color:#fff;border-radius:20px;padding:clamp(24px,5vw,48px);margin:0 0 34px}
.cdi .hero h1{color:#fff}.cdi .hero p{color:#e9e1f7;font-size:18px;max-width:720px;margin:0}
.cdi .kick{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:0 0 8px}
.cdi .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;margin:0 0 36px}
.cdi a.card{display:flex;flex-direction:column;gap:6px;text-decoration:none;background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:0 1px 2px rgba(30,27,58,.04);transition:transform .15s,box-shadow .15s,border-color .15s;color:var(--ink2)}
.cdi a.card:hover{transform:translateY(-3px);box-shadow:0 10px 26px rgba(91,45,144,.14);border-color:#cdbfe6}
.cdi .ic{width:44px;height:44px;border-radius:12px;display:grid;place-items:center;font-size:22px;background:var(--bg);margin-bottom:6px}
.cdi .card b{color:var(--ink);font-size:17px}.cdi .card span{font-size:14.5px}.cdi .card em{font-style:normal;font-size:12.5px;color:var(--mute);margin-top:auto;padding-top:8px}
.cdi .go{font-size:13px;font-weight:700;color:var(--brand)}
.cdi .tag{display:inline-block;font-size:11.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;border-radius:99px;padding:3px 10px;background:#efe7fb;color:var(--brand);margin-right:6px}
.cdi .tag.w{background:#fff4d6;color:#8a5a00}
.cdi .back{display:inline-block;margin:0 0 18px;font-size:14px;font-weight:600;text-decoration:none}
.cdi .box{background:var(--bg);border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin:0 0 22px}
.cdi .demo{background:#fff;border:2px dashed #cdbfe6;border-radius:16px;padding:24px;margin:0 0 22px}
.cdi .two{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}
.cdi pre{background:#1e1b3a;color:#e9e6ff;border-radius:12px;padding:16px;overflow:auto;font-size:12.5px;line-height:1.5;white-space:pre-wrap;word-break:break-all;margin:0}
.cdi code{font-size:13px;background:#efe7fb;color:var(--brand);padding:1px 6px;border-radius:5px;word-break:break-all}
.cdi .btn{display:inline-block;background:var(--brand);color:#fff!important;text-decoration:none;font-weight:700;padding:12px 22px;border-radius:99px}
.cdi ul.steps{margin:0 0 6px;padding-left:20px}.cdi ul.steps li{margin:0 0 6px}
.cdi .mail{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;max-width:560px}
.cdi .mail .bar{background:#f1f0f6;padding:10px 14px;font-size:13px;color:var(--mute);border-bottom:1px solid var(--line)}
.cdi .mail .body{padding:22px}
.cdi .phone{max-width:300px;border:10px solid #1e1b3a;border-radius:34px;padding:16px 12px;background:#f2f2f7;margin:0 auto}
.cdi .bubble{background:#34c759;color:#fff;border-radius:18px 18px 4px 18px;padding:10px 13px;font-size:14px;margin-left:30px;word-break:break-word}
.cdi .bubble a{color:#fff;text-decoration:underline}
.cdi .post{background:#fff;border:1px solid var(--line);border-radius:14px;max-width:480px;overflow:hidden}
.cdi .post .hd{display:flex;gap:10px;align-items:center;padding:12px 14px}.cdi .post .av{width:38px;height:38px;border-radius:50%;background:#4b2e4f}
.cdi .post img{display:block;width:100%;height:auto;margin:0;border:0}
.cdi .post .lk{padding:10px 14px;background:#f4f4f8;font-size:13px;color:var(--mute)}
.cdi .flyer{display:flex;gap:22px;align-items:center;flex-wrap:wrap;background:linear-gradient(135deg,#0f1f38,#23406b);color:#fff;border-radius:16px;padding:26px}
.cdi .flyer h3{color:#fff;font-size:24px}.cdi .flyer p{color:#cfdcf0}
.cdi .qr{background:#fff;border-radius:12px;padding:10px;width:190px;height:190px}.cdi .qr svg{width:100%;height:100%}
.cdi .note{font-size:13.5px;color:var(--mute)}
.cdi .story p{font-size:17px}
.cdi span[data-champ-donate]{background:#fff4d6;border-bottom:2px solid #f5b31b;padding:0 3px;border-radius:3px;cursor:pointer;color:#5a3d00;font-weight:600}
.cdi a.champ-donate{display:inline-block;background:#4b2e4f;color:#fff!important;font-weight:700;text-decoration:none;padding:12px 24px;border-radius:12px;margin:4px 8px 4px 0}
.cdi a.champ-donate.alt{background:#f4d06f;color:#3a2a00!important}
</style>"""

def q(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1)
    b = io.BytesIO(); img.save(b); s = b.getvalue().decode()
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    s = re.sub(r'width="[^"]*"\s+height="[^"]*"', '', s, count=1)
    return s

PH = 'https://raw.githubusercontent.com/ConorEgan1997/demoimages/main/photo-pack/'
I = [  # key, slug, icon, group, one-liner, best-for
 ('Donate link','donate-link','🔗','link','A link to the campaign’s donation page. Nothing to install.','Emails, newsletters, posters, social posts, texts.'),
 ('Newsletter button','newsletter-button','📰','link','A branded Donate button for your next email newsletter.','Monthly newsletters and appeal emails.'),
 ('Email signature','email-signature','✉️','link','A short “Support our work” link in every staff email.','Staff and volunteer email footers.'),
 ('QR code for print','qr-code-for-print','▦','link','A QR code that opens the donation page on a phone.','Flyers, posters, collection boxes, event stands.'),
 ('Social media post','social-media-post','💬','link','A tracked link for Facebook, Instagram, LinkedIn or X.','Posts, stories and your profile bio.'),
 ('Text message','text-message','📱','link','A link to send by SMS or WhatsApp.','Supporter texts and WhatsApp groups.'),
 ('Monthly giving link','monthly-giving-link','🔁','link','Opens the form with monthly giving already selected.','Regular-giving appeals.'),
 ('Form on a page','form-on-a-page','🧾','web','The whole donation form sits on a page of your website.','Your Donate page and campaign landing pages.'),
 ('Floating Donate button','floating-donate-button','♥','web','A Donate button in the corner that opens the form over the page.','Giving from anywhere on your site.'),
 ('Sticky bar','sticky-bar','▁','web','A slim bar slides up as visitors scroll.','Stories, news and appeal updates.'),
 ('Amounts in your text','amounts-in-your-text','€','web','Amounts in your copy open the form with that amount chosen.','Copy that already talks about what a gift does.'),
 ('Your own Donate buttons','your-own-donate-buttons','🔘','web','The Donate buttons already on your site open the form.','Sites that already have Donate buttons.'),
 ('Sticky bar after reading','sticky-bar-after-reading','📖','web','Slides up once a visitor has read 70% of the page.','Long stories and impact reports.'),
 ('Ask for an email on close','ask-for-an-email-on-close','🔔','web','If a visitor closes the form without giving, it asks for their email.','Recovering donors who nearly gave.'),
]

def minify(h):
    keep = []
    def stash(m): keep.append(m.group(0)); return f'@@KEEP{len(keep)-1}@@'
    h = re.sub(r'<pre>.*?</pre>', stash, h.strip(), flags=re.S)
    h = re.sub(r'>\s+<', '><', h)
    h = re.sub(r'\n\s*', ' ', h)
    for i, k in enumerate(keep): h = h.replace(f'@@KEEP{i}@@', k)
    return h

def page(key, slug, icon, grp, one, best, body, code, steps, live_note=''):
    c = S[key]; camp = c['campaign']
    tag = '<span class="tag">Share a link</span>' if grp == 'link' else '<span class="tag w">On your website</span>'
    codeblock = f'<pre>{e(code)}</pre>'
    stp = ''.join(f'<li>{s}</li>' for s in steps)
    h = f"""{CSS}<div class="cdi">
<a class="back" href="{BASE}">← All CHAMP Donate integrations</a>
<div class="hero"><div class="kick">{tag}</div><h1>{icon} {e(key)}</h1><p>{e(one)}</p></div>
<div class="two"><div class="box"><h3>Best for</h3><p style="margin:0">{e(best)}</p></div>
<div class="box"><h3>Example campaign</h3><p style="margin:0">{e(camp)}<br><span class="note">Created in CHAMP → Campaign → Integration as “JLM demo – {e(key)}”, so every gift from here is tracked separately.</span></p></div></div>
<h2>See it in action</h2>{('<p class="note">'+live_note+'</p>') if live_note else ''}
<div class="demo">{body}</div>
<h2>How to set it up</h2><div class="box"><ul class="steps">{stp}</ul></div>
<h2>The code from CHAMP</h2>{codeblock}
<p style="margin-top:26px"><a class="back" href="{BASE}">← Back to all integrations</a></p></div>"""
    return minify(h)

pages = {}
link_steps = lambda where: ['In CHAMP, open the campaign and go to the <b>Integration</b> tab.', f'Choose <b>{where}</b>, give it a name and click <b>Save as new</b>.', 'Copy the link (or the ready-made HTML button) and paste it where you need it.']
web_steps = lambda where: ['In CHAMP, open the campaign and go to the <b>Integration</b> tab.', f'Choose <b>{where}</b>, give it a name and click <b>Save as new</b>.', 'Copy the snippet and paste it once into your website (in WordPress: a <b>Custom HTML</b> block, or the Text tab of the classic editor).', 'Publish the campaign in CHAMP so the form loads for visitors.']

for key, slug, icon, grp, one, best in I:
    caps = S[key]['caps']; url = caps[0]
    if key == 'Donate link':
        body = f'<p>Click the button or the link to open the <b>Christmas Appeal 2026</b> page on CHAMP.</p><p>{caps[1]}</p><p class="note">Link: <code>{e(url)}</code></p>'
        code = url + '\n\n' + caps[1]; steps = link_steps('Donate link')
    elif key == 'Newsletter button':
        btn = f'<a href="{e(url)}" style="display:inline-block;background:#4b2e4f;color:#fff;font-weight:700;padding:14px 28px;border-radius:50px;text-decoration:none">Light up a life →</a>'
        body = f'<div class="mail"><div class="bar"><b>From:</b> Willowmere Hospice &nbsp;·&nbsp; <b>Subject:</b> Our Christmas memory garden is open</div><div class="body"><img src="{PH}willowmere-hospice/classic-blossom-park-1600x600.jpg" alt="" style="width:100%;border-radius:10px;margin:0 0 16px;display:block"><h3>Dedicate a blossom this Christmas</h3><p>This year, you can dedicate a blossom in our memory garden for someone you love. Every dedication funds specialist hospice care, at home and on our wards.</p><p>{btn}</p></div></div>'
        code = url + '\n\n' + btn; steps = link_steps('Newsletter button')
    elif key == 'Email signature':
        body = f'<div class="mail"><div class="bar">Staff email footer</div><div class="body"><p>Kind regards,</p><p style="margin:0"><b>Mary Byrne</b><br>Family Support Coordinator, Willowmere Hospice<br><span class="note">01 555 0123 · willowmere.example</span></p><p style="margin:14px 0 0;padding-top:12px;border-top:1px solid #e6e4f0">💜 <a href="{e(url)}" style="color:#4b2e4f;font-weight:700">Support our work</a> – care that lets every moment matter.</p></div></div>'
        code = url + f'\n\n<a href="{url}">Support our work</a>'; steps = link_steps('Email signature')
    elif key == 'QR code for print':
        body = f'<div class="flyer"><div class="qr">{q(url)}</div><div style="flex:1;min-width:220px"><div class="kick">Lantern Walk 2026</div><h3>Walk with us. Light the way home.</h3><p>Scan to sponsor a walker or give to the walk.</p><p class="note" style="color:#9fb3d1">Try it: scan with your phone camera.</p></div></div>'
        code = url; steps = link_steps('QR code for print')[:2] + ['Download the <b>PNG</b> QR code and add it to your flyer, poster or collection box.']
    elif key == 'Social media post':
        body = f'<div class="post"><div class="hd"><div class="av"></div><div><b style="color:#1e1b3a">Willowmere Hospice</b><br><span class="note">Sponsored · 🌍</span></div></div><p style="padding:0 14px">Add a flower to our meadow for someone you remember 🌸 Every one helps us care for families when it matters most.<br><a href="{e(url)}">{e(url.split("?")[0])}</a></p><a href="{e(url)}"><img src="{PH}willowmere-hospice/immersive-wildflower-meadow-1920x1080.jpg" alt=""></a><div class="lk">GIVING.PMSVAULT.COM<br><b style="color:#1e1b3a">A meadow of memories – Willowmere Hospice</b></div></div>'
        code = url; steps = link_steps('Social media post')
    elif key == 'Text message':
        body = f'<div class="phone"><p class="note" style="text-align:center;margin:0 0 10px">Lantern Trust</p><div class="bubble">Hi Sarah 👋 €10 puts a hot meal on the table tonight for someone we support. Can you help? <a href="{e(url)}">Give now</a> 💛</div><p class="note" style="text-align:right;margin:6px 0 0">Delivered</p></div>'
        code = url; steps = link_steps('Text message')
    elif key == 'Monthly giving link':
        body = f'<p>This link opens <b>A Home for Every Family</b> with <b>Monthly</b> already selected.</p><p><a class="btn" href="{e(url)}">Give monthly →</a></p><p class="note">Link: <code>{e(url)}</code></p>'
        code = url; steps = link_steps('Monthly giving link')
    elif key == 'Form on a page':
        body = '<div style="display:flex;justify-content:center">' + caps[1].replace('\n', '') + '</div>'
        code = caps[1]; steps = web_steps('Form on a page')
    elif key == 'Floating Donate button':
        body = '<p>Look in the <b>bottom corner of this page</b>: a Donate button floats there. Click it to open the <b>Light a Lantern</b> form over the page.</p>' + caps[1]
        code = caps[1]; steps = web_steps('Floating Donate button')
    elif key in ('Sticky bar', 'Sticky bar after reading'):
        camp = 'Remembrance Sunflowers' if key == 'Sticky bar' else 'Every Moment Matters'
        img = 'image-right-sunflowers-1120x1280.jpg' if key == 'Sticky bar' else 'image-left-windowsill-1120x1280.jpg'
        paras = ''.join(f'<p>{t}</p>' for t in [
            'When Mam came to Willowmere, the first thing she noticed was the garden. The nurses wheeled her bed to the window every morning so she could see the flowers.',
            'Over those weeks, the team cared for all of us: Mam, Dad, my brothers and me. They answered our questions at 3am, made endless cups of tea, and helped us say the things we needed to say.',
            'Every summer since, we have planted a sunflower in the Willowmere remembrance field. It is our way of saying thank you, and of keeping her close.',
            'Care like this is only possible because of people who give. Every gift funds nurses, family support and the quiet moments that matter most.',
            'This year, more families than ever need that care. Your support means no family has to face the end of life alone.',
            'Thank you for reading our story. If it moved you, please consider giving today.'] * 2)
        body = f'<p class="note">Scroll down. {"A slim bar slides up as you go." if key=="Sticky bar" else "Once you have read 70% of this page, a bar slides up: “Moved by what you read? Support us.”"}</p><div class="story"><h3>“The garden was the first thing she saw each morning”</h3><img src="{PH}willowmere-hospice/{img}" alt="" style="max-width:360px;width:100%;border-radius:14px;float:right;margin:0 0 16px 20px">{paras}<div style="clear:both"></div></div>' + caps[1]
        code = caps[1]; steps = web_steps(key)
    elif key == 'Amounts in your text':
        body = f'<div class="story"><h3>Wrap a child in warmth this winter</h3><img src="{PH}lantern-trust/image-right-child-in-snow-1120x1280.jpg" alt="" style="max-width:300px;width:100%;border-radius:14px;float:right;margin:0 0 16px 20px"><p>Hundreds of children we support start winter without a proper coat. You can change that today.</p><p><span data-champ-donate="20">€20 buys a hat, scarf and gloves set</span> to keep the cold out on the walk to school.</p><p><span data-champ-donate="40">€40 buys a brand-new winter coat</span>, chosen by the child, in their favourite colour.</p><p><span data-champ-donate="150">€150 kits out a whole family for winter</span>, with coats, boots and warm layers for everyone.</p><p class="note">Click any highlighted amount: the form opens with that amount already chosen.</p><div style="clear:both"></div></div>' + caps[1]
        code = '<span data-champ-donate="40">€40 buys a brand-new winter coat</span>\n\n' + caps[1]; steps = web_steps('Amounts in your text')[:3] + ['Wrap each amount in your text in <code>&lt;span data-champ-donate="40"&gt;…&lt;/span&gt;</code>.', 'Publish the campaign in CHAMP so the form loads for visitors.']
    elif key == 'Your own Donate buttons':
        body = '<p>These are ordinary buttons on this page. Each has the class <code>champ-donate</code>, so clicking one opens the <b>Garden Walk 2026</b> form over the page.</p><p><a class="champ-donate" href="https://giving.pmsvault.com/DEMO/c/willowmere-garden-walk-2026-realistic">Sponsor a walker</a><a class="champ-donate alt" href="https://giving.pmsvault.com/DEMO/c/willowmere-garden-walk-2026-realistic">Donate</a></p>' + caps[1]
        code = '<a href="https://giving.pmsvault.com/DEMO/c/willowmere-garden-walk-2026-realistic" class="champ-donate">Donate</a>\n\n' + caps[1]; steps = web_steps('Your own Donate buttons')[:3] + ['Add <code>class="champ-donate"</code> to the Donate buttons or links you already have.', 'Publish the campaign in CHAMP so the form loads for visitors.']
    elif key == 'Ask for an email on close':
        body = '<p>A Donate button sits in the bottom corner of this page. Open the form, then <b>close it without giving</b>: you are asked for your email so the charity can send a gentle reminder.</p>' + caps[1]
        code = caps[1]; steps = web_steps('Ask for an email on close')
    pages[slug] = dict(title=key, html=page(key, slug, icon, grp, one, best, body, code, steps))

def hubcards(g):
    return ''.join(f'<a class="card" href="{BASE}{slug}/"><div class="ic">{icon}</div><b>{e(k)}</b><span>{e(one)}</span><em>Example: {e(S[k]["campaign"].replace(" (Realistic)",""))}</em><div class="go">See it live →</div></a>' for k, slug, icon, grp, one, best in I if grp == g)
hub = minify(f"""{CSS}<div class="cdi"><div class="hero"><div class="kick">CHAMP Donate</div><h1>Every way to take donations with CHAMP</h1><p>Fourteen ways to put a CHAMP campaign in front of donors, each set up for real. Open any one to see it working, how it was set up, and the code to copy.</p></div>
<h2>Share a link</h2><p>Nothing to install. A tracked link to the campaign page that works in emails, posts, texts and print.</p><div class="grid">{hubcards('link')}</div>
<h2>On your website</h2><p>Paste a snippet once, and donors give without leaving your site, on a page or in a pop-up over it.</p><div class="grid">{hubcards('web')}</div>
<div class="box"><h3>Not sure where to start?</h3><p style="margin:0">Start with a <a href="{BASE}donate-link/">Donate link</a>: nothing to install, and it works in emails, QR codes, posts and texts. Add a website option when your web person can paste a snippet.</p></div></div>""")
json.dump({'hub': {'title': 'CHAMP Donate Integrations', 'slug': HUB, 'html': hub}, 'pages': [{'slug': s, **v} for s, v in pages.items()]}, open('/home/claude/jlm/pages.json', 'w'), ensure_ascii=False)
for s, v in pages.items(): (OUT / f'{s}.html').write_text(v['html'])
(OUT / 'hub.html').write_text(hub)
print(len(pages), 'pages; hub', len(hub), 'chars; largest', max(len(v['html']) for v in pages.values()))
