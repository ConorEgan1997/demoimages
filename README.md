# Lantern Trust – CHAMP demo campaign images

Fictional charity artwork for demoing each CHAMP donation-page layout. Every image matches the size and composition guidance CHAMP shows under "How your image sits in this layout".

| Layout | Image | Size |
|---|---|---|
| Classic | classic-christmas-appeal-1600x600.jpg | 1600×600 |
| Compact | compact-warm-meal-1200x480.jpg | 1200×480 |
| Hero banner | hero-banner-lantern-walk-1920x600.jpg | 1920×600 |
| Image left | image-left-a-home-1120x1280.jpg | 1120×1280 |
| Image right | image-right-winter-coats-1120x1280.jpg | 1120×1280 |
| Immersive | immersive-light-a-lantern-1920x1080.jpg | 1920×1080 |

Logos: lantern-trust-logo-240x80-light.png (for the campaign Logo URL — light text, legible on dark hero scrims), lantern-trust-logo-240x80-dark.png (light backgrounds), lantern-trust-logo-square.png, lantern-trust-logo-wide.png, lantern-trust-logo-wide-light.png.

Regenerate with `python3 demo-campaign-images/generate.py` (needs Playwright + Inter font).

## Asset pack
`asset-pack/CHAMP-Campaign-Image-Asset-Pack.pdf`: which image each CHAMP layout needs, crop diagrams for desktop and phone, on-page screenshots of both example charities, copy guidance, design tips and a charity intake checklist (internal edition).

`asset-pack/Donation-Page-Image-Guide.pdf`: charity-facing edition to send to clients. It has no admin notes or internal links, and adds a layout chooser and a "what to send us" checklist.

## Second example set
`hospice-flowers/`: Willowmere Hospice, a flower-themed set at the same CHAMP sizes (see its README).

## Knowledge base page (WordPress)
`asset-pack/web/donation-page-image-guide-wordpress.html`: charity-facing guide as one HTML snippet. Paste it into a WordPress **Custom HTML** block. It has no JavaScript, and its CSS is scoped under `.cdg`. Images load from jsDelivr, pinned to commit `0b88131`, so later changes to this repo won't alter the live page. Rebuild with `python3 asset-pack/web/build_web.py <commit-sha>`.
