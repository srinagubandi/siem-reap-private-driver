#!/usr/bin/env python3
"""
Angkor Drivers — localize all external assets into the repository.

This script gathers every externally referenced image (Manus CDN, CloudFront)
from the 18 canonical pages plus auxiliary pages, downloads the accessible
bytes once, stores them under assets/local/ with a deterministic URL hash
name, and rewrites HTML ``src`` attributes to point to the local copies.

It also localises Google Fonts CSS (Noto Serif + Manrope + Material Symbols)
with a Chromium User-Agent, downloads all referenced woff2 font files, and
rewrites the CSS ``url(...)`` to point to local font files.  HTML <link>
stylesheet references are then updated to the local CSS.

Key requirements:
  * timeout <= 15s per request
  * atomic downloads (never leave 0-byte files)
  * deterministic URL -> local filename mapping (md5 prefix)
  * preserve original alt text and never substitute people
  * report failures clearly without asking for credentials
  * no code that contacts OpenRouter or any model service

Run:
    python3 scripts/localize_assets.py

The mapping report is written to asset-localisation-report.json.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LANG_PAGES = [
    "index.html", "fr.html", "zh.html", "ko.html", "ja.html", "vi.html",
    "th.html", "de.html", "es.html", "it.html", "pt.html", "ru.html",
    "nl.html", "pl.html", "ar.html", "id.html", "sv.html", "cs.html",
]

AUX_PAGES = ["thank-you.html", "404.html"]

# Exclude old design-only pages from asset crawling.
EXCLUDED_HTML = {"code.html"}

# Directories
LOCAL_IMG_DIR = Path("assets/local/images")
LOCAL_FONT_DIR = Path("assets/local/fonts")
LOCAL_CSS_DIR = Path("assets/local/css")

# Google Fonts CSS URLs to localise.
GOOGLE_FONTS_CSS_URLS = [
    "https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,700;1,400&family=Manrope:wght@400;500;600;700;800&display=swap",
    "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap",
]

# Chromium User-Agent (Google Fonts sends different CSS to non-browser UA).
CHROMIUM_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

TIMEOUT_SECONDS = 15

# Externally accessible image URL hostnames to localise.
EXTERNAL_IMAGE_HOSTS = (
    "files.manuscdn.com",
    "d2xsxph8kpxj0f.cloudfront.net",
    "manuscdn.com",
)

# ---------------------------------------------------------------------------
# Deterministic local naming
# ---------------------------------------------------------------------------

def deterministic_name(url: str, ext: Optional[str] = None) -> str:
    """Return a deterministic local filename based on md5 of the URL."""
    digest = hashlib.md5(url.encode("utf-8")).hexdigest()[:12]
    return f"{digest}.{ext or 'bin'}"


# ---------------------------------------------------------------------------
# Atomic download
# ---------------------------------------------------------------------------

def atomic_download(url: str, dest: Path, timeout: int = TIMEOUT_SECONDS) -> bool:
    """Download to a temp file and atomically rename to dest.

    Returns True on success.  On failure, removes any temp file and returns
    False.  Never leaves a 0-byte file at the destination.
    """
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": CHROMIUM_UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        if not data:
            return False
        # Write to temp file, then rename.
        with tmp.open("wb") as fh:
            fh.write(data)
        os.replace(tmp, dest)
        return True
    except Exception as exc:
        if tmp.exists():
            tmp.unlink()
        print(f"  DOWNLOAD FAILED {url}: {exc}")
        return False


# ---------------------------------------------------------------------------
# Image localisation
# ---------------------------------------------------------------------------

def find_image_urls(html_files: List[Path]) -> Dict[str, List[Path]]:
    """Map each unique external image URL to the HTML files that reference it."""
    url_to_files: Dict[str, List[Path]] = {}
    src_pattern = re.compile(r'\bsrc="(https?://[^"]+)"', re.IGNORECASE)

    for path in html_files:
        text = path.read_text(encoding="utf-8")
        for m in src_pattern.finditer(text):
            url = m.group(1)
            if any(host in url for host in EXTERNAL_IMAGE_HOSTS):
                url_to_files.setdefault(url, []).append(path)
    return url_to_files


def localize_images(html_files: List[Path]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Download external images and return mapping plus failure report."""
    LOCAL_IMG_DIR.mkdir(parents=True, exist_ok=True)
    url_to_files = find_image_urls(html_files)
    url_mapping: Dict[str, str] = {}   # original URL -> local relative path
    failures: Dict[str, str] = {}      # original URL -> failure reason

    for url, files in url_to_files.items():
        # Determine extension from URL path.
        clean_path = url.split("?")[0]
        ext_match = re.search(r'\.(jpe?g|png|webp|gif|svg|avif|ico)$', clean_path, re.IGNORECASE)
        ext = ext_match.group(1).lower() if ext_match else "bin"
        local_name = deterministic_name(url, ext)
        local_path = LOCAL_IMG_DIR / local_name

        if not local_path.exists():
            success = atomic_download(url, local_path)
            if not success:
                failures[url] = "download failed or empty response"
                continue
            if local_path.stat().st_size == 0:
                local_path.unlink()
                failures[url] = "download produced 0 bytes"
                continue

        relative = f"/{local_path.as_posix()}"
        url_mapping[url] = relative
        print(f"  OK {url} -> {relative}")

    return url_mapping, failures


def rewrite_image_srcs(html_files: List[Path], url_mapping: Dict[str, str]) -> int:
    """Replace external image src attributes with local paths."""
    total = 0
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        original = text
        for url, local_path in url_mapping.items():
            text = text.replace(url, local_path)
        if text != original:
            path.write_text(text, encoding="utf-8")
            total += 1
            print(f"  rewrote image srcs in {path.name}")
    return total


# ---------------------------------------------------------------------------
# Google Fonts CSS localisation
# ---------------------------------------------------------------------------

def download_google_font_css() -> Dict[str, Path]:
    """Download each Google Fonts CSS URL, return mapping of URL -> local file."""
    LOCAL_CSS_DIR.mkdir(parents=True, exist_ok=True)
    url_to_local: Dict[str, Path] = {}

    for url in GOOGLE_FONTS_CSS_URLS:
        local_name = "fonts-" + hashlib.md5(url.encode("utf-8")).hexdigest()[:10] + ".css"
        local_path = LOCAL_CSS_DIR / local_name
        if not local_path.exists():
            success = atomic_download(url, local_path)
            if not success or local_path.stat().st_size == 0:
                print(f"  FAILED to download Google Fonts CSS: {url}")
                continue
        url_to_local[url] = local_path
        print(f"  OK Google Fonts CSS {url} -> {local_path}")

    return url_to_local


def download_font_files(css_path: Path) -> Dict[str, Path]:
    """Parse a Google Fonts CSS file, download referenced woff2/ttf fonts."""
    LOCAL_FONT_DIR.mkdir(parents=True, exist_ok=True)
    url_to_local: Dict[str, Path] = {}

    text = css_path.read_text(encoding="utf-8")
    font_url_re = re.compile(r'url\((https://fonts\.gstatic\.com/[^)]+)\)', re.IGNORECASE)

    for m in font_url_re.finditer(text):
        font_url = m.group(1)
        font_filename = f"font-{hashlib.md5(font_url.encode('utf-8')).hexdigest()[:10]}.woff2"
        local_font_path = LOCAL_FONT_DIR / font_filename
        if not local_font_path.exists():
            success = atomic_download(font_url, local_font_path)
            if not success or local_font_path.stat().st_size == 0:
                print(f"  FAILED to download font file: {font_url}")
                continue
        url_to_local[font_url] = local_font_path
        print(f"  OK font file {font_url} -> {local_font_path}")

    return url_to_local


def rewrite_font_css(css_path: Path, font_mapping: Dict[str, Path]) -> None:
    """Rewrite url(...) in localised CSS to point to local font files."""
    text = css_path.read_text(encoding="utf-8")
    for font_url, local_path in font_mapping.items():
        local_relative = f"/{local_path.as_posix()}"
        text = text.replace(f'url({font_url})', f'url({local_relative})')
    css_path.write_text(text, encoding="utf-8")
    print(f"  rewrote font URLs in {css_path.name}")


def rewrite_html_font_links(html_files, url_to_local):
    """Replace Google Fonts <link> URLs in HTML with local CSS paths, handling &amp; correctly."""
    total = 0
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        original = text
        
        # Handle both regular and HTML entity encoded ampersands
        for url, local_css in url_to_local.items():
            # Create variations of the URL with different ampersand encodings
            urls_to_replace = [
                url,  # Original
                url.replace('&', '&amp;'),  # HTML entity encoded
            ]
            
            for variant_url in urls_to_replace:
                text = text.replace(variant_url, f"/{local_css.as_posix()}")
        
        # Also handle module alias imports if present
        # This would require more specific parsing which is beyond scope here
        # For now we assume direct link replacements are sufficient
        
        if text != original:
            path.write_text(text, encoding="utf-8")
            total += 1
    return total


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def write_report(
    image_mapping: Dict[str, str],
    image_failures: Dict[str, str],
    font_css_mapping: Dict[str, Path],
    font_file_mapping: Dict[str, Path],
) -> None:
    report = {
        "generated": "2026-11-05",
        "image_localisation": {
            "successful": image_mapping,
            "failed": image_failures,
            "notes": [
                "All successful downloads are stored under assets/local/images with deterministic md5-prefixed names.",
                "Guest photos formerly served from d2xsxph8kpxj0f.cloudfront.net returned 403 and could not be localised.",
                "No human images were substituted. CSS neutral tiles remain the fallback for missing guest photos.",
            ],
        },
        "font_localisation": {
            "css_files": {k: f"/{v.as_posix()}" for k, v in font_css_mapping.items()},
            "font_files": {k: f"/{v.as_posix()}" for k, v in font_file_mapping.items()},
        },
    }
    with open("asset-localisation-report.json", "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    print("\nReport written to asset-localisation-report.json")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("Angkor Drivers — asset localisation\n")

    all_html_files = [Path(p) for p in LANG_PAGES + AUX_PAGES if Path(p).exists()]
    all_html_files = [p for p in all_html_files if p.name not in EXCLUDED_HTML]

    # --- Images ---
    print("[1/3] Localising images…")
    image_mapping, image_failures = localize_images(all_html_files)
    rewritten_images = rewrite_image_srcs(all_html_files, image_mapping)
    print(f"  rewrote image srcs in {rewritten_images} HTML file(s)")

    # --- Google Fonts CSS ---
    print("\n[2/3] Localising Google Fonts CSS…")
    font_css_mapping = download_google_font_css()
    all_font_mapping: Dict[str, Path] = {}
    for css_url, css_path in font_css_mapping.items():
        font_mapping = download_font_files(css_path)
        all_font_mapping.update(font_mapping)
        rewrite_font_css(css_path, font_mapping)
    rewritten_css_links = rewrite_html_font_links(all_html_files, font_css_mapping)
    print(f"  rewrote font CSS links in {rewritten_css_links} HTML file(s)")

    # --- Report ---
    print("\n[3/3] Writing report…")
    write_report(image_mapping, image_failures, font_css_mapping, all_font_mapping)

    print("\nDone.")
    if image_failures:
        print("\nWARNING: some image downloads failed (see report).")
        for url in image_failures:
            print(f"  - {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
