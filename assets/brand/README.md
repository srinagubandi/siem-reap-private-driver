# Angkor Drivers — approved Option A

The owner chose Option A on 6 November 2026 after two Nano Banana Pro loops: concept generation and focused refinement. `source/option-a-approved.png` preserves that approved original. `source/option-a-transparent-master.png` is a native-alpha preparation of the same design, not a replacement concept. Both are retained unchanged as source files.

`angkor-drivers-logo.svg` is a true path-based vector traced from the approved silhouette, not an SVG wrapper containing a bitmap. PNG derivatives are transparent. The main dark navigation presents the same SVG silhouette in a light color via CSS; light headers use the green original. The browser favicon SVG separately adapts to light/dark browser chrome. No white rectangle is added to the header logo.

`asset-manifest.json` lists all 37 generated production files, dimensions, purposes, and SHA-256 hashes. Browser PNG sizes are 16, 24, 32, 48, 64, 96, 128, and 256px. ICO resolutions are 16, 24, 32, 48, and 64px. Apple touch sizes are 57, 60, 72, 76, 114, 120, 144, 152, 167, and 180px. Android/PWA any and maskable icons are 192 and 512px. Windows tiles include 70, 144, 150, and 310px squares and a 310×150px wide tile. A monochrome Safari pinned-tab SVG and the static manifest/config files are included.

Maskable symbols stay inside the central 40%-radius safe circle, with opaque ivory surroundings. Apple, Android, Windows, and legacy ICO files use opaque ivory backgrounds to avoid inappropriate device-generated black backgrounds. Ordinary browser PNGs and website-logo PNGs preserve transparency.

Development regeneration:

```bash
python3 scripts/generate_option_a_brand_assets.py
python3 scripts/apply_option_a_branding.py
```

Pillow and Potrace are development-only tools. Production serves committed files directly from GitHub Pages. Do not regenerate artwork, change its design, or add external runtime image services without approval. Do not touch the unrelated official Tripadvisor logo.
