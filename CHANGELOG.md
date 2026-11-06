# Changelog

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
