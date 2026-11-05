# Changelog

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
