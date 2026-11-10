#!/usr/bin/env python3
"""Preserve the first gallery image and apply a Thumbsup-style card grid to the rest."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "index.html", "fr.html", "zh.html", "ko.html", "ja.html", "vi.html", "th.html",
    "de.html", "es.html", "it.html", "pt.html", "ru.html", "nl.html", "pl.html",
    "ar.html", "id.html", "sv.html", "cs.html",
]
MOMENTS_START = "<!-- Masonry-style 5-photo grid -->"
MOMENTS_END = '<div id="tripadvisor-traveler-photos"'
IMG_RE = re.compile(r'<img\b([^>]*?)\bsrc=["\']([^"\']+)["\']([^>]*)/?>', re.S)
CARD_RE = re.compile(r'<div class="[^"]*guest-gallery-card[^"]*">', re.S)


def wrap_moments_cards(section: str) -> str:
    if 'data-gallery-template="thumbsup-cards"' not in section:
        section = section.replace(
            '<div class="grid grid-cols-2 md:grid-cols-3 gap-4">',
            '<div class="guest-gallery-cards" data-gallery-template="thumbsup-cards">',
            1,
        )
    if 'class="guest-gallery-card"' in section:
        return section

    def replace_card(match: re.Match[str]) -> str:
        classes, image = match.group(1), match.group(2)
        image_match = IMG_RE.search(image)
        if not image_match:
            return match.group(0)
        attrs_before, src, attrs_after = image_match.groups()
        alt_match = re.search(r'\balt=["\']([^"\']*)["\']', image)
        label = alt_match.group(1) if alt_match else 'Moments with Guests photo'
        img_src = src if src.startswith('/') else '/' + src
        anchor = (
            f'<a href="{html.escape(img_src, quote=True)}" target="_blank" '
            f'rel="noopener noreferrer" aria-label="Open the full-size {html.escape(label, quote=True)}">'
            f'{image}</a>'
        )
        return f'<div class="guest-gallery-card">\n{anchor}\n</div>'

    return re.sub(
        r'<div class="([^"]+)">\n((?:<!--.*?-->\n)*<img\b.*?/>)\n</div>',
        replace_card,
        section,
        flags=re.S,
    )


def main() -> int:
    changed = 0
    for filename in PAGES:
        path = ROOT / filename
        text = path.read_text(encoding="utf-8")
        if MOMENTS_START not in text or MOMENTS_END not in text:
            raise SystemExit(f"Moments section not found in {filename}")
        start = text.index(MOMENTS_START)
        end = text.index(MOMENTS_END, start)
        section = text[start:end]
        updated = wrap_moments_cards(section)
        grid_marker = 'class="ta-traveler-photo-grid"'
        if 'data-gallery-template="thumbsup-cards"' not in text[end:]:
            tail = text[end:]
            tail = tail.replace(grid_marker, grid_marker + ' data-gallery-template="thumbsup-cards"', 1)
            text = text[:end] + tail
        if updated != section or text != path.read_text(encoding="utf-8"):
            path.write_text(text[:start] + updated + text[end:], encoding="utf-8")
            changed += 1
    print(f"thumbsup card migration changed {changed} pages")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
