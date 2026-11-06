# Angkor Drivers

Angkor Drivers is a standalone multilingual static website. GitHub Pages publishes the root of the `deploy` branch at https://angkordrivers.com/. The `main` branch is older source and must not overwrite production.

**Project policy: GitHub Pages only. Never deploy this project to Railway.** All production rendering resources must remain in the repository and be served by GitHub Pages. Do not add Manus badges, branding scripts, or runtime dependencies to the public site. Development tools and private previews are not production hosting.

## Production

The 18 language pages remain ordinary HTML. Production needs no package install or build service. CSS, JavaScript, working photographs, fonts, SVG/PNG/ICO favicons, and touch icons are committed to Git and served directly by GitHub Pages. Booking still uses the original Formspree endpoint; WhatsApp and telephone links retain the original contacts.

## Tripadvisor

The website links to the supplied Angkordrivers listing:

https://www.tripadvisor.co.uk/Attraction_Review-g297390-d34664961-Reviews-Angkordrivers-Siem_Reap_Siem_Reap_Province.html

A dated snapshot shows **5.0/5 from 6 reviews, verified 2026-11-05**. It does not update automatically. Update the visible value and verification date together after rechecking the public listing. No AggregateRating rich-result markup is added. The owner approved publishing this static plan without a live widget.

The testimonial cards now use verified public display names, actual source avatars, review dates, and short verbatim excerpts from three real reviews. Every card links to its individual Tripadvisor review. Original quotations stay in English with `lang="en"`; surrounding UI labels are localized into the site's 18 languages. Public handles are never expanded into invented legal names. The listing's single traveler tip is labelled as a tip, not an invented question.

`data/tripadvisor-reviews.json`, `data/tripadvisor-ui-labels.json`, and `images/tripadvisor/SOURCES.json` preserve source attribution and owner-confirmed reuse permission. `scripts/apply_genuine_tripadvisor_reviews.py` is an idempotent migration, not a live feed or CMS; deliberate content updates require reviewing both the source records and existing generated cards. Do not silently substitute generated faces or rewrite quotations as though they were verbatim.

## Photographs

The five original CloudFront guest-gallery URLs no longer work. At the owner's request, the gallery now reuses the five genuine photographs already committed under `images/`: the couple, driver, temple guest, forest Jeeps, and Jeep fleet. Their existing localized descriptions are reused so the images are not mislabeled as airport or hotel photographs. The original image bytes and the Jeep section are preserved. No generated people or neutral placeholders are used.

Three additional original photographs supplied on 5 November 2026 are kept under `images/`: `guest-family-airport-departures.jpg` is featured in Moments with Guests, `private-van-angkor-gate.jpg` appears with private transport/tour content rather than the Jeep section, and `leng-cheaheng-private-driver.jpg` replaces the profile image in Meet Leng Cheaheng. Image content and original bytes are preserved; the supplied mobile screenshot is only a reference and is not published.

The van-at-Angkor image is now paired with Leng's profile image inside Meet Leng rather than displayed as an isolated tour-area tile. Its original bytes and natural aspect ratio remain unchanged. Five source avatars and eight full-size traveler photos are committed under `images/tripadvisor/`. Two credited, optimized traveler photos are featured in Moments with Guests; the remaining originals are retained without being indiscriminately added to the gallery.

Other working legacy CDN images and the Google Fonts files have been copied into `assets/local/`. `asset-localisation-report.json` records their original URLs and local mapping. Production does not need the original media CDNs or Google Fonts endpoints.

## Public AI information and FAQ

The English-only `/ai/` hub, `/faq/`, `llms.txt`, and JSON/text/Markdown resources are ordinary committed files. The owner approved English for this new information section after reviewing language guidance; all 18 existing main-site translations remain intact and are linked from the hub. These optional files do not guarantee AI citations or search rankings.

`ai/faq.json` contains 18 source-linked English answers. Individual JSON records are under `ai/faq/`. `ai/business.json` contains only public business contacts and location; `ai/manifest.json` is a static resource catalogue, not an MCP or A2A discovery card. `ai/agent.md`, `ai/agent.txt`, `ai/faq.md`, and `ai/faq.txt` provide equivalent readable guidance. HTML pages have exact Markdown counterparts at `/ai/index.md` and `/faq/index.md`.

There is no live AI server, POST question endpoint, model call, booking confirmation, private customer access, or site-level question queue in this section. Ordinary hosting access logs may exist. Model-assisted development and test tools do not run in production. Do not place API keys or account credentials in these public files.

To maintain the information, edit the source-linked English answers and snapshot date in `ai/data.json`, then run:

```bash
python3 scripts/build_ai_section.py
python3 scripts/apply_accessibility_seo.py
```

Both scripts use Python's standard library and make no network calls. Review the generated HTML and JSON before committing. If Tripadvisor changes, update its visible values/date and the dated FAQ answer together; the snapshot is not a live feed.

## Accessibility and language-specific SEO

The shared fixes add localized skip links and landmark labels, hide decorative icon text from assistive technology, correct heading order, improve identified contrast failures, and allow the footer resource link to wrap. `ai/ui-labels.json` contains only the small translated accessibility/navigation labels; it is not a translated AI dataset.

Each of the 18 main pages keeps its existing localized title and description. Open Graph, Twitter, and structured-data names/descriptions use that page's language, with its own canonical URL and one reciprocal 19-entry hreflang family, including `x-default`. The new AI/FAQ pages are labelled English and have no non-existent translation alternates. Unsupported inventory-style offer markup is removed. The XML sitemap lists the 20 canonical HTML routes; the existing `robots.txt` allow/crawl policy is preserved. Legacy design, thank-you, and 404 pages are marked `noindex, follow` and excluded from the sitemap.

Automated checks and keyboard/reflow sampling are release evidence, not a full WCAG conformance claim, legal certification, or proof of indexing. Live booking submissions, real screen-reader testing, and Search Console indexing verification require separate checks.

`assets/css/device-breakpoints.css` adds content-driven phone, tablet, landscape, desktop, and wide-display refinements and loads after the existing fixes. It preserves natural photo ratios, source links, long-language wrapping, RTL order, touch targets, and booking controls. Reviews use one/two/three columns at 640px and 1024px transition points; the tablet's third card spans the full row. Three post-breakpoint Qwen high open-weight review loops and the 18-language, 22-width acceptance matrix are documented under `docs/genuine-reviews-device-refinement-2026-11-06.md`.

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

The real **Angkor Driver** Google Business Profile has been verified against its website, phone, and street address. Its actual Google Maps place URL is recorded in `data/google-business-profile.json`, with localized link labels in `data/google-profile-ui-labels.json`. A static profile card and truthful profile-opening CTA replace the old unconfigured Elfsight block and broken Google review link. There is no Google rating claim, copied Google review content, live sync, iframe, or API dependency. `scripts/link_verified_google_profile.py` records this migration. The dated Tripadvisor rating badge remains unchanged above the hero heading.

**Current display state: Google is temporarily hidden at the owner's request.** Both the profile/reviews card and Google CTAs are hidden without reserving layout space. Keep the verified information in Git. To restore it later with owner approval, set `display_on_site` to `true` in `data/google-business-profile.json` and run `python3 scripts/link_verified_google_profile.py`; then verify and publish the resulting HTML.

The decorative, pointer-styled aerial image in the contact panel was removed because it was not a useful working map. Real contact links and all inquiry form controls and submission settings are unchanged.

The legacy `code.html` design page is not part of the canonical-language release tests, but its rendering resources, together with those on the thank-you and 404 pages, are also localized to GitHub Pages. No live booking request or third-party form submission is made by validation.
