// Browser-only reskin of a CHAMP draft preview for asset-pack screenshots.
// Nothing is saved to CHAMP: it swaps the hero image, logo, copy and colour tokens in the DOM.
window.__skin = function (doc, brand, page) {
  const GH = 'https://raw.githubusercontent.com/ConorEgan1997/demoimages/main/';
  const B = {
    lantern: { name: 'Lantern Trust', vars: null, logo: null, images: null, text: {} },
    willow: {
      name: 'Willowmere Hospice',
      logo: GH + 'hospice-flowers/willowmere-logo-240x80-light.png',
      vars: {
        '--color-primary': '294 26% 25%', '--color-primary-dark': '294 26% 12%', '--color-primary-text': '294 26% 25%',
        '--color-primary-deep': '294 26% 25%', '--color-accent': '44 86% 70%', '--color-button': '44 86% 70%',
        '--color-accent-text': '40 70% 30%', '--color-accent-deep': '40 70% 26%', '--color-success': '127 13% 50%',
        '--color-success-text': '127 15% 32%',
        '--df-primary': 'hsl(294 26% 25%)', '--df-primary-strong': 'hsl(294 26% 12%)', '--df-primary-deep': 'hsl(294 26% 25%)',
        '--df-primary-text': 'hsl(294 26% 25%)', '--df-primary-soft': 'color-mix(in srgb, hsl(294 26% 25%) 8%, white)',
        '--df-primary-soft-2': 'color-mix(in srgb, hsl(294 26% 25%) 14%, white)', '--df-accent': 'hsl(44 86% 70%)',
        '--df-accent-soft': 'color-mix(in srgb, hsl(44 86% 70%) 18%, white)', '--df-accent-line': 'color-mix(in srgb, hsl(44 86% 70%) 32%, white)',
        '--df-accent-strong': 'hsl(40 70% 26%)', '--df-accent-text': 'hsl(40 70% 30%)', '--df-success': 'hsl(127 13% 50%)',
        '--df-success-text': 'hsl(127 15% 32%)', '--df-success-soft': 'color-mix(in srgb, hsl(127 13% 50%) 8%, white)',
        '--df-success-line': 'color-mix(in srgb, hsl(127 13% 50%) 28%, white)', '--df-focus-ring-color': 'hsl(294 26% 25% / .85)',
        '--shadow-primary': '0 1px 2px 0 #0f172a0f, 0 8px 22px -6px hsl(294 26% 25% / .18)'
      },
      images: {
        'christmas-appeal-2026': 'hospice-flowers/classic-memory-garden-1600x600.jpg',
        'warm-meal-fund': 'hospice-flowers/compact-bouquet-1200x480.jpg',
        'a-home-for-every-family': 'hospice-flowers/image-left-windowsill-1120x1280.jpg',
        'winter-coat-drive': 'hospice-flowers/image-right-sunflowers-1120x1280.jpg',
        'lantern-walk-2026': 'hospice-flowers/hero-banner-garden-border-1920x600.jpg',
        'light-a-lantern': 'hospice-flowers/immersive-golden-meadow-1920x1080.jpg'
      },
      text: {
        // headlines + descriptions
        'No family should spend Christmas without a home': 'Light up a life this Christmas',
        'This winter, 1 in 4 families we support will face Christmas in emergency accommodation. Your gift keeps a light on for them, with safe rooms, warm meals and a path home.':
          'Dedicate a blossom in our memory garden for someone you love. Your gift funds specialist hospice care, at home and on our wards.',
        '€10 puts a hot meal on the table tonight': 'Send flowers to someone who needs comfort',
        'Our kitchens serve 600 warm meals every night. A quick gift right now means nobody we support goes to bed hungry.':
          'Every bouquet brightens a room on our ward and funds an hour of care.',
        'Every family deserves a front door of their own': 'Care that lets every moment matter',
        'Last year we helped 312 families move from emergency rooms into homes of their own. Your gift funds the deposit, the keys and the support to stay.':
          'Our nurses care for 1,200 people a year, at home and in our hospice. Your gift gives families comfort, dignity and time together.',
        'Wrap a child in warmth this winter': 'Grow something beautiful in their memory',
        'Hundreds of children we support start winter without a proper coat. €40 buys a brand-new one, so they can walk to school warm and proud.':
          'Plant a sunflower in our remembrance field this summer. Each one stands for someone loved, and funds care for families today.',
        'Walk with us. Light the way home.': 'Walk our garden of remembrance',
        'On 5 December, 1,000 walkers will carry lanterns through Phoenix Park for families without a home. Sponsor a walker or give to the walk today.':
          'Join 800 walkers through the Willowmere gardens on 14 June. Sponsor a walker or give in memory of someone special.',
        'Lantern Walk 2026 goal': 'Garden Walk 2026 goal',
        'Light a lantern. Guide someone home.': 'A meadow of memories',
        "Every lantern you light funds a night of shelter, a warm meal and a caseworker who won't give up. Add yours to our night of hope.":
          'Add a flower to our meadow for someone you remember. Every one helps us care for families when it matters most.',
        // impact text
        'serves Christmas dinner for a family': 'funds an hour of nursing care at home',
        'gives a family a safe, warm night': 'funds a night of specialist hospice care',
        'provides a week of hot meals': 'funds a week of complementary therapies',
        'helps a family move into their own home': 'supports a family through bereavement care',
        'serves one hot, nourishing dinner': 'sends a bouquet to a patient',
        'feeds a family of four tonight': 'funds an hour of care at home',
        "stocks a family's kitchen for a week": 'funds a family support session',
        'buys new bedding for a child\'s first bed': 'brightens a patient\'s room for a week',
        'buys a hat, scarf and gloves set': 'plants one remembrance sunflower',
        'buys a brand-new winter coat for a child': 'plants a sunflower and a named marker',
        'adds waterproof boots to a new coat': 'funds a day of care on the ward',
        'kits out a whole family for winter': 'funds a week of care at home',
        "sponsors one walker's lantern": "sponsors a walker's garden map",
        "sponsors a walker's 5 km": "sponsors a walker's 5 km",
        'sponsors a whole family team': 'sponsors a family team',
        'funds two nights of safe shelter': 'funds two nights of hospice care',
        'lights a lantern on our night of hope': 'adds a flower to the meadow',
        "lights a lantern in a loved one's name": "adds a flower in a loved one's name",
        // testimonials
        'Lantern Trust found us a home two weeks before Christmas. My kids woke up in their own beds.':
          'The nurses gave Mam peace, and gave us time. We will never forget that.',
        'Aoife, Dublin': 'Niamh, Wicklow', 'Mum of three': 'Daughter',
        "The day they handed us our own keys, my daughter ran from room to room shouting 'this one's mine!'":
          'Dad wanted to be at home, with his garden in view. Willowmere made that possible.',
        'Grace, Galway': 'Ciarán, Kildare', 'Moved home in 2025': 'Cared for at home, 2025'
      }
    }
  }[brand];

  const root = doc.documentElement;
  if (B.vars) for (const [k, v] of Object.entries(B.vars)) root.style.setProperty(k, v);
  // charity name (DEMO's global setting shows CHAMP CLOUD)
  const swapText = () => {
    const w = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
    let n; while ((n = w.nextNode())) {
      let t = n.nodeValue, o = t;
      if (t.trim() === 'CHAMP CLOUD') t = t.replace('CHAMP CLOUD', B.name);
      const key = t.trim().replace(/^[“"']|[”"']$/g, '');
      if (B.text[key]) t = t.replace(key, B.text[key]);
      if (t !== o) n.nodeValue = t;
    }
    doc.title = 'Donate to ' + B.name;
  };
  if (B.images && B.images[page]) {
    const url = GH + B.images[page];
    for (const el of doc.querySelectorAll('*')) {
      const bi = getComputedStyle(el).backgroundImage;
      if (bi && /demo-campaign-images\/.*\.jpg/.test(bi)) el.style.backgroundImage = bi.replace(/url\(["']?[^"')]+demo-campaign-images[^"')]+["']?\)/, `url("${url}")`);
    }
  }
  if (B.logo) for (const img of doc.querySelectorAll('img')) if (img.src.includes('lantern-trust-logo')) { img.src = B.logo; img.srcset = ''; }
  // hide the admin-only banners so shots read like the live page
  for (const el of doc.querySelectorAll('div,section')) {
    const t = el.innerText || '';
    if ((t.startsWith('Test mode') || t.startsWith('Draft preview')) && el.children.length <= 3 && t.length < 160) el.style.display = 'none';
  }
  swapText();
  if (!doc.__skinObs) { doc.__skinObs = new MutationObserver(swapText); doc.__skinObs.observe(doc.body, { subtree: true, childList: true, characterData: true }); }
  return 'skinned ' + brand + ' / ' + page;
};
