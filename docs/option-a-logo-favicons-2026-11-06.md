# Option A logo and favicon release — 6 November 2026

## Authorization and scope

The owner selected Option A and authorized the recommended header/favicon publication. The artwork follows two Nano Banana Pro concept/refinement loops. Approved original artwork and native-alpha preparation are retained under `assets/brand/source/`; SVG paths are traced from the approved silhouette. No new logo concept replaces the selection.

The main-site logo is physically upper-left on all 18 languages, including Arabic. It uses a light presentation on dark green navigation so the mark is visible without a white box. Light AI/FAQ and thank-you headers use the green asset. All 23 public HTML files receive a shared, cache-versioned favicon set. Production remains GitHub Pages, with no Railway, external rendering asset, runtime image call, service worker, or public Manus badge.

## Icon inventory

`assets/brand/asset-manifest.json` contains 37 generated files and SHA-256 hashes. The package includes:

- Browser PNG: 16/24/32/48/64/96/128/256px.
- ICO: embedded 16/24/32/48/64px resolutions.
- True path-based SVG browser favicon with light/dark color adaptation; monochrome Safari pinned mask.
- Apple touch: 57/60/72/76/114/120/144/152/167/180px and a default 180px alias.
- Android/PWA any: 192/512px; separate maskable 192/512px variants inside the central 40%-radius safe circle.
- Windows: 70/144/150/310px squares and 310×150px wide tile.
- Transparent website-logo PNG: 96/192/512px and a true vector SVG.
- Static `site.webmanifest` and `browserconfig.xml`.

Device-specific icons use ivory backgrounds where appropriate; the header logo, browser PNGs, and vector logo remain transparent. Future maintenance uses `scripts/generate_option_a_brand_assets.py`, `scripts/apply_option_a_branding.py`, and shared `scripts/brand_common.py`. AI/FAQ and legacy migration templates are synchronized with the new declarations.

## Acceptance evidence

Local production-equivalent static preview, Chromium, 6 November 2026:

- 18 languages × 24 widths = **432 header layout cases**, 320–1920px; zero final page-width overflow, logo/text collision, or misplaced Arabic logo findings.
- AI, FAQ, thank-you, and error pages checked at 320px; icon declarations and resource targets checked on all 23 HTML pages.
- Icon file hashes, dimensions, SVG/XML syntax, native transparency, ICO resolutions, maskable safe area, and manifest references validated.
- Keyboard-focus/logo accessible-name checks passed on 320px English, 820px Arabic, and 1024px French. Existing menu open/Escape behavior passed on phone and tablet.
- Native-alpha maximum opacity normalized from254 to255; only pre-existing transparent padding is trimmed. The visible approved silhouette is preserved.
- A tablet collision found during the initial test was fixed by retaining the existing menu below1024px. Final retest passed.
- Branding updater is repeatable without HTML drift.
- Non-brand page copy, original photo bytes, review/source data, Tripadvisor artwork, booking form, CNAME, robots, sitemap, and no-Jekyll control preserved. Google remains hidden as previously requested.

This is a scoped engineering evaluation, not a full accessibility conformance claim. Real Safari/iOS/Android/Windows installation and native icon selection are not device-tested; file/config compatibility is validated. Browser-managed favicon caches may persist longer than normal page cache despite versioned declarations.

## Publication procedure

Commit on `updates/option-a-logo-favicons-2026-11-06`, preserve previous production `13f698457b0a9f7dc4626f1872368c63233c55ed` on a rollback branch, and fast-forward existing `deploy` with an atomic push. Check the actual live HTML, favicon/logo files, manifest, and GitHub Pages build before delivery. No forced overwrite or hosting migration is needed.
