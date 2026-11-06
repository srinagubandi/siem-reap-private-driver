# Static AI information, accessibility, and locale SEO release

## Approved scope

The new information section is English-only. All 18 existing main-site language pages remain in place, with their original main copy, photos, contacts, and booking details preserved. Every production resource is committed to the existing GitHub Pages `deploy` branch. No Railway service, new backend, external runtime dependency, AI question endpoint, private data access, or automatic booking is introduced.

The reference's static capabilities are provided at `/ai/`, `/faq/`, `/ai/faq.json`, individual `/ai/faq/faq-NNN.json` records, `/ai/business.json`, `/ai/manifest.json`, `/ai/agent.md`, `/ai/agent.txt`, `/ai/faq.md`, `/ai/faq.txt`, and `/llms.txt`. Markdown counterparts for the HTML pages are `/ai/index.md` and `/faq/index.md`. `.nojekyll` keeps these files unchanged during publishing.

## Why English-only

The owner approved English AI resources after research. Google's AI Search guidance does not require special AI files or translations of them; the `llms.txt` community proposal does not require a separate file for every website language. The resource directory links to all 18 existing main-page languages. Future translated FAQs should be added for actual visitor needs, with reviewed translations, not merely to manufacture AI-search pages.

Sources: [Google AI features](https://developers.google.com/search/docs/appearance/ai-features), [Google AI optimization guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [llms.txt proposal](https://llmstxt.org/), and [Google multilingual-site guidance](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites).

## Two review-and-fix loops

**Loop 1:** Qwen3 Coder 480B reviewed the initial accessibility and SEO evidence and the source-bounded FAQ draft. The baseline axe scan found color-contrast, heading-order, and landmark findings across the 18 main pages. Repairs added localized skip links and landmark labels, hid decorative icon text from assistive technology, corrected the heading hierarchy, fixed identified contrast failures, and allowed the resource footer link to wrap. The draft FAQ was corrected to avoid invented availability/lead-time policies, a claim that 18 translations imply 18 spoken tour languages, and ambiguous live-rating wording.

**Loop 2:** Qwen3 VL 235B reviewed the completed hub and FAQ screenshots, static documentation, source records, locale metadata, and test evidence. It identified unstable repeated builds, Markdown markers left in the plain-text guide, and image-overlay contrast contexts that automation could not determine. The build ordering/whitespace was corrected, plain-text exports were cleaned, and scoped photograph-text underlays were manually reviewed and tested with conservative contrast calculations. No third model review loop was used.

## Verification

| Check | Scope | Result |
|---|---|---|
| Automated accessibility | axe-core 4.14.0; WCAG A/AA tags and best-practice rules; 18 main pages plus AI hub and FAQ | 0 reported rule violations on all 20 pages after fixes |
| Keyboard skip link | First Tab and Enter on all 20 pages | Localized skip link receives focus and moves focus to main content |
| Main mobile menu | English main page; keyboard activation, Escape dismissal, focus restoration | Passed |
| Responsive page layout | All 20 pages at 320, 390, 768, and 1440px | No horizontal page overflow or missing images |
| New-page text spacing | AI hub and FAQ at 320px | No page overflow with WCAG-style text spacing |
| Rendering resources | All 20 pages | No console exceptions or external stylesheet/script/font/image requests in tested views |
| Main content and photos | All 18 main pages compared with the prior Git revision | Main text and image source/alt pairs unchanged |
| Metadata | All 18 main pages | Preserved localized titles/descriptions; localized social/structured-data text and correct own URLs |
| Locale alternates | All 18 main pages | One 19-entry reciprocal/self hreflang family, including x-default |
| AI page language | New hub and FAQ | English, self-canonical, no non-existent translated alternates |
| Sitemap and crawler policy | Root files | 20 unique canonical HTML URLs; existing robots policy unchanged |
| Static JSON | All new JSON files | Parsed successfully; 18 source-linked FAQ records |
| Build repeatability | Run both standard-library build scripts twice | No changed output files on second run |
| Text export | Agent plain-text guide | No Markdown heading markers |
| Production safety | Public HTML/resources and environment-secret checks | No public Made with Manus branding or credential values detected |

Image-overlay calculations use WCAG relative luminance for the declared underlays with black/white photo extremes. The lowest evaluated hero-text ratio is **5.65:1** and the lowest evaluated tour-text ratio is **6.54:1**, above the normal-text 4.5:1 threshold. Hero, tour-card, and Jeep-caption text underlays are scoped CSS changes; no photo files are edited.

The original dated Tripadvisor snapshot is retained as 5.0/5 from 6 reviews checked on 5 November 2026, not a live widget or automatic data feed. Confirm current values on the official listing before updating the visible site and FAQ data together.

## Limits

This is scoped accessibility engineering and release evidence, not a complete WCAG conformance claim or legal certification. Some automated image/native-control contrast tests can remain inconclusive; the reviewed photo contexts are supplemented by visual inspection and explicit underlay calculations. Real screen-reader testing, live booking form submission, native-device coverage, Google/Bing console indexing checks, social-network cache previews, and independent authentication of business claims were not performed. Successful publication does not prove indexing, rankings, rich-result display, or AI citations.

The new information files introduce no question logging or review queue. Ordinary hosting access logs may exist. Uncovered questions, prices, booking availability, vehicle requirements, and operational policies must be confirmed directly with Leng.
