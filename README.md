# Angkor Drivers

Angkor Drivers is a standalone multilingual static website. GitHub Pages publishes the root of the `deploy` branch at https://angkordrivers.com/. The `main` branch is older source and must not overwrite production.

**Project policy: GitHub Pages only. Never deploy this project to Railway.** All production rendering resources must remain in the repository and be served by GitHub Pages. Do not add Manus badges, branding scripts, or runtime dependencies to the public site. Development tools and private previews are not production hosting.

## Production

The 18 language pages remain ordinary HTML. Production needs no package install or build service. CSS, JavaScript, working photographs, fonts, SVG/PNG/ICO favicons, and touch icons are committed to Git and served directly by GitHub Pages. Booking still uses the original Formspree endpoint; WhatsApp and telephone links retain the original contacts.

## Tripadvisor

The website links to the supplied Angkordrivers listing:

https://www.tripadvisor.co.uk/Attraction_Review-g297390-d34664961-Reviews-Angkordrivers-Siem_Reap_Siem_Reap_Province.html

A dated snapshot shows **5.0/5 from 6 reviews, verified 2026-11-05**. It does not update automatically. Update the visible value and verification date together after rechecking the public listing. No AggregateRating rich-result markup is added. The owner approved publishing this static plan without a live widget.

## Photographs

The five original CloudFront guest-gallery URLs no longer work. At the owner's request, the gallery now reuses the five genuine photographs already committed under `images/`: the couple, driver, temple guest, forest Jeeps, and Jeep fleet. Their existing localized descriptions are reused so the images are not mislabeled as airport or hotel photographs. The original image bytes and the Jeep section are preserved. No generated people or neutral placeholders are used.

Three additional original photographs supplied on 5 November 2026 are kept under `images/`: `guest-family-airport-departures.jpg` is featured in Moments with Guests, `private-van-angkor-gate.jpg` appears with private transport/tour content rather than the Jeep section, and `leng-cheaheng-private-driver.jpg` replaces the profile image in Meet Leng Cheaheng. Image content and original bytes are preserved; the supplied mobile screenshot is only a reference and is not published.

Other working legacy CDN images and the Google Fonts files have been copied into `assets/local/`. `asset-localisation-report.json` records their original URLs and local mapping. Production does not need the original media CDNs or Google Fonts endpoints.

## Development tools

`scripts/apply_update.py` and `scripts/localize_assets.py` record the HTML and asset migration. They are migration aids, not a CMS: do not rerun the migration blindly on an edited production page. `scripts/validate_site.py` checks the canonical pages, form labels and endpoint, local resources, icon sizes, Tripadvisor summary, and JSON-LD structure. It is not a full accessibility or search-engine conformance test.

To rebuild the committed static CSS from the repository root, install development-only Tailwind dependencies outside the repository:

```bash
npm install --prefix /tmp/angkor-build-tools --no-audit --no-fund tailwindcss@3.4.19 @tailwindcss/forms @tailwindcss/container-queries
NODE_PATH=/tmp/angkor-build-tools/node_modules /tmp/angkor-build-tools/node_modules/.bin/tailwindcss -c tools/tailwind.config.cjs -i tools/tailwind-input.css -o assets/tailwind.css --minify
python3 scripts/validate_site.py
```

Python migration/validation dependencies are Beautiful Soup and Pillow. Raster icon generation additionally uses CairoSVG. None of these run in the visitor's browser.

## Remaining setup

Google Reviews is intentionally hidden at the owner's request. Its heading and setup copy remain in the hidden `google-reviews-section` wrapper, with no layout space or unconfigured Elfsight request. Restore the wrapper only after a real widget is configured. The dated Tripadvisor rating badge appears before the hero heading on all 18 language pages and links to the supplied listing.

The legacy `code.html` design page is not part of the canonical-language release tests, but its rendering resources, together with those on the thank-you and 404 pages, are also localized to GitHub Pages. No live booking request or third-party form submission is made by validation.
