# Locale audit remediation — 5 November 2026

## Issues repaired

The 18-language audit identified narrow-screen overflow in the `about` benefit list on Spanish (1px), Portuguese (7px), and Swedish (11px) pages at 320px. `assets/css/locale-layout-fixes.css` fixes the root cause: two equal grid columns with zero minimum widths, shrinkable flex labels, natural wrapping when needed, and non-shrinking icons. It does not hide overflow, truncate text, reduce font size, or alter photo framing.

The English `City Discovery` tour heading was retained on 14 non-English pages. `scripts/fix_locale_audit.py` localizes it in Japanese, Vietnamese, Thai, German, Spanish, Italian, Portuguese, Russian, Dutch, Polish, Arabic, Indonesian, Swedish, and Czech. Existing French, Chinese, Korean, and English headings remain unchanged. The script is idempotent and changes source narrowly without reserializing the documents.

## Open-weight model work

Qwen3 Coder 480B implemented the fixes and reviewed source escaping and tour-heading wording. Qwen3-VL 235B reviewed actual repaired 320px benefit-grid screenshots for Spanish, Portuguese, Swedish, and Arabic, plus the actual tour headings for all 18 languages. It approved the identified repairs with no remaining issues reported in that scope. This is a bounded engineering and model-assisted translation review, not certified native proofreading or a full accessibility-conformance audit.

## Pre-publication acceptance results

All 18 canonical language pages passed Chromium checks at 320 × 844, 390 × 844, and 1440 × 1000: **54 of 54 viewport checks passed**.

- No horizontal document overflow.
- Benefit labels fit their cells and remain readable.
- Centered Tripadvisor logo/rating/count row and above-the-fold badge position preserved.
- No date/rating/count/arrow overlap or date clipping.
- The official listing link and local logo remain intact.
- All three new original photographs load once and retain their natural aspect ratios.
- Google Reviews remains intentionally hidden.
- No public Manus branding or page-script errors were observed.

Source comparisons verified that the three original photo bytes, other image references, Tripadvisor markup, booking forms, prices, contacts, and all other visible copy remain unchanged outside the 14 authorized tour headings. Structural validation also passed all 18 pages. No customer booking or form submission was performed.

## Hosting and release controls

Production remains GitHub Pages-only, never Railway. All production CSS, images, fonts, scripts, icons, and HTML are committed to Git. Development model calls are not production dependencies.

The repair release is maintained on `updates/final-language-fixes-2026-11-05` and published from `deploy`. The predecessor is retained in `backups/production-before-final-locale-fixes-2026-11-05`. Live post-deployment checks repeat the same 18-language/54-viewport acceptance gate before final delivery.
