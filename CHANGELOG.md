# Changelog

## 2026-11-10 — Matching Moments and Traveler galleries

Updated Moments with Guests to use the same visible toolbar and lightbox treatment as Traveler photo gallery. Both galleries now use the same localized message, photo count, Open gallery control, keyboard guidance, swipe guidance, independent URL hashes, and accessible focus behavior. Moments contains six images and opens at 1 / 6; Traveler photo gallery contains four images and opens at 1 / 4.

The existing first image remains first in both sections: the family-at-airport photo for Moments with Guests and the guest-welcome photo for Traveler photo gallery. The shared multi-gallery controller keeps each gallery scoped independently, preserves no-JavaScript native links, and remains GitHub Pages-only. The regression passed 54 responsive JavaScript states plus 18 no-JavaScript states across all 18 language pages with zero overflow.

## 2026-11-10 — Thumbsup-style gallery cards and safe image prefetch

Applied the GitHub Pages Gallery-inspired card treatment to the remaining photos in both Moments with Guests and Traveler photo gallery across all 18 language pages. The existing first image remains first and unchanged in each section: the family-at-airport photo in Moments with Guests and the guest-welcome photo in Traveler photo gallery. The migration is repeatable and changed 18 pages once, then 0 pages on its second run.

Added connection-aware background prefetching for six later same-origin local images during browser idle time. Prefetching is skipped when Save-Data, 2g, or slow-2g is detected; external Tripadvisor URLs are never prefetched. The verified regression passed 54 responsive page states, 18 lightbox states, exact first-image DOM preservation, six unique local prefetches, connection suppression, no JavaScript errors, and zero horizontal overflow.

## 2026-11-10 — Discoverable multilingual traveler gallery

Added a visible gallery toolbar above the existing traveler-photo grid on all 18 language pages. It provides a localized gallery heading, short description, photo count, Open Gallery action, keyboard guidance, and coarse-pointer swipe guidance. The no-JavaScript view keeps the heading and description plus four native full-image links, while JS-only controls remain hidden until the shared lightbox initializes.

Connected the toolbar to the existing GitHub Pages-safe vanilla-JS lightbox without adding a backend, database, external library, CDN, or runtime image service. The idempotent `scripts/add_gallery_toolbar.py` migration and `data/gallery-toolbar-translations.json` make future photo additions maintainable. The release passed 54 JS responsive states across 18 pages at 320/390/768px, 18 no-JS states, keyboard/hash/focus/inert restoration, Arabic RTL, coarse/fine pointer behavior, zero overflow, native-link fallback, and repeat-run idempotency. Planning and skeptic gates used Claude Opus 5.5; the final independent test gate used Claude Sonnet 5.5; Meta's open `muse-spark-open` supplied the toolbar copy after the preferred `muse-ember` response was unusable. No DeepSeek dependency is present in the site.

## 2026-11-10 — Static traveler gallery controls

Added progressive-enhancement controls to the traveler-photo gallery across all 18 language pages. Each card remains a native local image link without JavaScript; when the shared enhancement script loads, the gallery adds a keyboard- and touch-friendly lightbox with previous/next, close, Escape, focus containment, URL hash deep links, accessible captions, reduced-motion handling, and Arabic-safe layout. No backend, external gallery library, runtime image service, or non-GitHub hosting is required.

The gallery uses stable aspect-ratio frames, local WebP with JPEG fallback, lazy loading, intrinsic dimensions, and a maintainable semantic `figure`/`figcaption` card pattern. Future photos can be added through the repeatable migration scripts under `scripts/`, then validated at the same responsive checkpoints. OpenRouter catalog access was available, but both attempted chat models returned a provider-session `401 User not found` response; no external model dependency was added to the site.

## 2026-11-06 — Approved Option A logo and complete icon package

Applied the owner's selected Option A to the upper-left main-site header in all 18 languages and the public AI/FAQ and thank-you branding. The dark navigation uses a light rendition of the same transparent silhouette; light headers use green. The selected original and native-alpha preparation are retained in Git, and a real vector version is traced from the approved silhouette. Compact phones use a stacked wordmark; tablet navigation retains the existing menu until 1024px to keep translated labels within the viewport.

Regenerated browser PNGs at 16/24/32/48/64/96/128/256px, a five-resolution ICO, a light/dark adaptive SVG favicon, a Safari pinned-tab mask, ten Apple touch sizes from 57px to 180px, Android/PWA 192/512px icons, separate safe-area maskable 192/512px icons, and Windows square/wide tiles. All 23 public HTML files share cache-versioned icon declarations. Static builders import the shared declarations so old favicon tags do not return on future builds. No Railway, runtime image service, service worker, public Manus badge, review/photo changes, or booking-form changes are introduced.

## 2026-11-06 — Google section temporarily hidden

At the owner's request, hid the Google Business Profile/reviews card and Google CTAs across all 18 main-site languages. The hidden components reserve no layout space and are unavailable to keyboard focus. The verified Google profile URL and source records remain in Git for later restoration, controlled by `display_on_site` in `data/google-business-profile.json`. Tripadvisor cards, ratings, original photos, responsive breakpoints, and booking controls are unchanged.

## 2026-11-06 — Additional device breakpoints and three refinement loops

Added scoped spacing and layout refinements for compact phones, ordinary phones, large phones, tablets, desktops, wide displays, and short landscape viewports. Reviews use one column below 640px, two columns with a full-row third card from 640px to 1023px, and three columns from 1024px. Contact panel padding adapts without changing the form's display structure; original profile and van images remain paired and uncropped. The shared stylesheet is served locally from Git and loaded after the existing fixes.

Completed exactly three requested post-breakpoint review loops using Qwen3 VL 235B A22B Instruct, with Qwen3 Coder 480B for implementation; no DeepSeek was used. The first model suggestion was constrained to a safe tablet-only rule after measured evidence showed the original third card already spanned the row. The second and third reviews passed with no further justified changes. All 18 language pages were measured at 22 widths from 320px to 1920px in every loop. Final 396 width-language cases show no page/review/badge overflow and correct review columns; keyboard/text-spacing checks passed 10 additional device sizes. Evidence and limits are recorded in `docs/genuine-reviews-device-refinement-2026-11-06.md`.

## 2026-11-06 — Genuine Tripadvisor reviews and source photos

Replaced unsupported testimonial names and quotes with short, verbatim excerpts from Sam C, BigMac666, and Fearless64391184385. Each card records the public display name, actual review date, five-bubble rating, original source avatar, and a permalink to that specific Tripadvisor review. Review quotations remain in English and are marked with their language; surrounding labels are localized for all 18 main-site languages. No reviewer handles are expanded into invented legal names, and default source avatars are not presented as photographs of the reviewers.

Stored five available reviewer-avatar images and eight original review-attached traveler photos under `images/tripadvisor/`, alongside source URLs, creator display names, hashes, and explicit owner-confirmed reuse permission. Featured two appropriately selected traveler photos with credits and review links in Moments with Guests, using optimized, aspect-ratio-preserving WebP copies. Other original downloads remain available in Git but are not added indiscriminately to the marketing gallery. The source listing has no traveler questions; its single tip is explicitly labelled as BigMac666's tip, not presented as a Q&A post.

Removed the decorative pointer-styled aerial image from the contact area; it was not a functioning map. The real contact links, booking fields, labels, and submission endpoint remain unchanged. Removed unsupported testimonial names from the noindex legacy design HTML as well.

Resolved the supplied Google share link to the real Angkor Driver Google Maps profile and verified its matching website, phone, and street address. Replaced the unconfigured Elfsight area and broken Google review URL with localized, truthful profile links across all 18 languages. No Google ratings, review text, live syncing, new script, API, or iframe is added. Source identity and the actual Maps URL are recorded in `data/google-business-profile.json`.

Moved the original van-at-Angkor image out of the tour-card area and into the Meet Leng photo group across all 18 languages. Preserved its original file and complete image, localized its new caption, and kept the existing driver photo and experience badge. Qwen3 Coder 480B supplied layout implementation guidance, localized labels, and scoped card styling; integration repairs preserve HTML and ensure repeatable builds. Production remains plain GitHub Pages with no new external runtime requests, backend, or public Manus branding.

## 2026-11-06 — Static AI resources, accessibility, and localized SEO

Added an English `/ai/` information hub, readable `/faq/`, 18 source-linked JSON FAQ records, business facts, a static resource catalogue, Markdown/plain-text FAQ and agent guides, and `llms.txt`. All 18 existing main-site language versions remain available and are linked from the new resources. English-only AI resources were approved after primary-source research found no requirement to translate these files into every website language. There is no new backend, hosted API, model call, private data access, or automated booking service.

Added localized skip links and landmark labels, decorative icon ARIA, semantic heading-order fixes, scoped contrast corrections, robust photo-text underlays, and wrapping footer resource links. Preserved original main copy, photographs, contacts, and booking settings.

Preserved each language page's own title and description while aligning its Open Graph, Twitter, and structured-data text/URLs. Consolidated reciprocal hreflang annotations to one 19-entry family per main page, removed unsupported inventory-style offer markup, and regenerated the sitemap for 20 canonical HTML routes. Kept the existing robots policy unchanged; marked ancillary design, thank-you, and error pages noindex. Added `.nojekyll` so Markdown and other static files are served verbatim.

Completed two open-weight review-and-fix loops: Qwen3 Coder 480B for the first review and initial implementation, and Qwen3 VL 235B for the second visual/content review. Integration corrections made repeated builds stable and cleaned the plain-text guide. Scoped image-overlay contrast calculations cover the manually reviewed variable-photo contexts. Final automated checks report no axe rule violations on the 20 indexable pages; keyboard and responsive checks cover the existing language pages and new resource pages. These checks are not a full accessibility conformance claim or a guarantee of indexing, ranking, or AI citations.

## 2026-11-05 — All identified language-audit issues repaired

Resolved the 320px Spanish, Portuguese, and Swedish bio benefit-label overflow with a shared, scoped shrink-and-wrap rule. Labels remain fully readable without hidden overflow, ellipses, or smaller text; icons retain their size.

Localized the remaining City Discovery tour heading in Japanese, Vietnamese, Thai, German, Spanish, Italian, Portuguese, Russian, Dutch, Polish, Arabic, Indonesian, Swedish, and Czech. Existing French, Chinese, Korean, and English headings remain unchanged. Added an idempotent source-preserving repair script.

Qwen3 Coder 480B implemented the repairs and Qwen3-VL 235B reviewed repaired 320px grids and all 18 tour headings. Preview checks passed all 18 languages at 320px, 390px, and 1440px: no horizontal page overflow, no badge/date/count overlap, preserved vertical centering and above-fold position, loaded original photos with natural aspect ratios, and Google Reviews still hidden. The three original photo files, other copy, prices, contacts, booking forms, metadata, and Tripadvisor snapshot remain unchanged. GitHub Pages-only hosting and no public Manus branding are retained.

## 2026-11-05 — Tripadvisor badge vertical centering

Vertically centered the official logo, rating, and review count within the badge's main row using a narrowly scoped alignment rule from Qwen3 Coder 480B. Preserved the dated snapshot, date/arrow alignment, desktop one-row and mobile two-row layouts, RTL behavior, all content and photos, and GitHub Pages-only hosting. A fresh open-weight vision review checks the corrected badge with all 18 language pages.

## 2026-11-05 — New original photos and Tripadvisor icon

Featured the supplied airport-family photograph in Moments with Guests and placed the supplied van-at-Angkor photograph with private transport/tour content. Replaced the Meet Leng Cheaheng profile photo with the supplied photograph of Leng beside his Hyundai van across all 18 language pages. Original files are committed under `images/`, without AI edits or changed pixels. The reference screenshot is not published.

Added Tripadvisor's original owl-and-wordmark SVG to the above-the-fold rating badge, self-hosted under `assets/icons/` with source documentation. The badge retains its dated 5.0/5-from-6-reviews snapshot and official listing link. Scoped narrow-screen grid rules keep the date and review count readable, including long-language and RTL layouts.

DeepSeek V4 Pro maximum reasoning produced the photo update, with Qwen3 Coder 480B used for focused coding repairs. Preserved all existing marketing copy, prices, contacts, booking settings, genuine Jeep photos, hidden Google Reviews state, and GitHub Pages-only hosting. The photo-update script has stable markers to avoid duplicate images when run again.

## 2026-11-05 — Hero rating badge refinement

Added an above-the-fold, localized Tripadvisor rating badge linking to the supplied listing. It shows the verified 5.0/5 rating from 6 reviews with a dated snapshot label, not a live-widget claim. The unconfigured Google Reviews heading and setup area are intentionally hidden, with their copy retained for later configuration and the inactive Elfsight request removed.

The owner explicitly requires GitHub Pages only for this project, never Railway. All rendering assets, including those used by the legacy design document, thank-you page, and 404 page, are now committed local resources. No Manus branding script or visible “Made with Manus” text is present in the public site. Existing booking services, contacts, photographs, and marketing copy are preserved.

The badge change is developed with two DeepSeek V4 Pro 0813 maximum-reasoning passes and two design-only reviews. Scoped mobile/desktop and RTL checks verify above-the-fold placement, overflow, Google-section hiding, and public-site branding.

## 2026-11-05

### Tripadvisor

Replaced the unconfigured Tripadvisor placeholder with a dated 5.0/5 summary from 6 reviews, verified 2026-11-05, and linked the summary and review action to the supplied Angkordrivers listing. This is the owner-approved static plan, not a live widget. Service provider JSON-LD includes the real listing URL; no AggregateRating rich-result markup is added.

### Photos and assets

Reused the five genuine photographs from `images/` in the broken guest-gallery slots across all 18 language pages, using their existing localized descriptions. Original image files are unchanged. No generated people or placeholder photo tiles are used. Other working images, fonts, production CSS, JavaScript, and favicons are served from Git instead of legacy external media or runtime Tailwind/Google Fonts requests. Added matching SVG, PNG, ICO, Apple touch, and manifest icons.

### Mobile and desktop

Improved mobile hero readability and full-width actions, section spacing, headings, responsive cards, and booking fields. Added shared mobile drawer behavior with focus trapping, Escape/overlay dismissal, focus restoration, state attributes, and scroll locking. Language-strip scrolling respects RTL and reduced motion. Removed nonfunctional testimonial arrows and the incorrect decorative Tripadvisor bird. Added a no-JavaScript navigation fallback and viewport safe-area support.

### Copy and booking

Preserved visible marketing and translated copy outside the authorized Tripadvisor area. Removed only decorative icon text from inactive controls. Associated all six visible booking labels with their controls; retained the original Formspree endpoint, contact information, prices, and booking options. Google/Elfsight setup text remains unchanged and is documented as pending setup.

### Release checks

Structural checks cover all 18 canonical language pages. Chromium checks cover image loading, mobile drawer states, keyboard Escape/focus restoration, booking-label associations, representative narrow/desktop widths, and navigation without JavaScript. JSON-LD syntax is parsed separately. These checks do not claim legal accessibility compliance or guaranteed search-engine visibility.
