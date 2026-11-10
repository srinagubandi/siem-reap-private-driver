#!/usr/bin/env python3
"""Add the shared localized toolbar to the Moments with Guests gallery."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/gallery-toolbar-translations.json'
PAGES = [
    'index.html', 'fr.html', 'zh.html', 'ko.html', 'ja.html', 'vi.html', 'th.html',
    'de.html', 'es.html', 'it.html', 'pt.html', 'ru.html', 'nl.html', 'pl.html',
    'ar.html', 'id.html', 'sv.html', 'cs.html',
]
START = '<!-- moments-gallery-toolbar:start -->'
END = '<!-- moments-gallery-toolbar:end -->'
FEATURED_RE = re.compile(r"(<figure class='guest-featured-photo' id='guest-family-photo'>\s*)(<img\b[^>]+>)(\s*</figure>)", re.S)


def e(value: str) -> str:
    return html.escape(value, quote=True)


def render(t: dict) -> str:
    return f'''{START}
<div class="gallery-toolbar" data-gallery-toolbar="moments" role="region" aria-labelledby="moments-gallery-toolbar-heading">
  <div class="gallery-toolbar__copy">
    <h4 id="moments-gallery-toolbar-heading">{e(t['heading'])}</h4>
    <p>{e(t['lead'])}.</p>
  </div>
  <div class="gallery-toolbar__actions">
    <span class="gallery-toolbar__count" data-gallery-count-group hidden><span>{e(t['photos'])}</span> <span data-gallery-count>0</span></span>
    <button type="button" class="gallery-toolbar__open" data-gallery-open hidden aria-haspopup="dialog">{e(t['open'])}</button>
  </div>
  <p class="gallery-toolbar__hint" data-gallery-keyboard hidden>{e(t['keyboard'])}.</p>
  <p class="gallery-toolbar__hint gallery-toolbar__touch-hint" data-gallery-touch hidden>{e(t['swipe'])}.</p>
</div>
{END}
'''


def main() -> int:
    translations = {item['filename']: item for item in json.loads(DATA.read_text(encoding='utf-8'))}
    changed = 0
    for filename in PAGES:
        path = ROOT / filename
        text = path.read_text(encoding='utf-8')
        text = text.replace(
            'data-gallery-toolbar role="region" aria-labelledby="gallery-toolbar-heading"',
            'data-gallery-toolbar="traveler" role="region" aria-labelledby="traveler-gallery-toolbar-heading"',
            1,
        ).replace('id="gallery-toolbar-heading"', 'id="traveler-gallery-toolbar-heading"', 1)
        if START not in text:
            marker = '<!-- guest-gallery-family-photo (idempotent marker) -->'
            if marker not in text:
                raise SystemExit(f'Moments marker not found in {filename}')
            text = text.replace(marker, render(translations[filename]) + marker, 1)
        featured = FEATURED_RE.search(text)
        if featured and '<a ' not in featured.group(0):
            image = featured.group(2)
            text = text[:featured.start()] + (
                featured.group(1)
                + '<a href="/images/guest-family-airport-departures.jpg" target="_blank" '
                + 'rel="noopener noreferrer" aria-label="Open the full-size guest family photo">\n'
                + image + '\n</a>'
                + featured.group(3)
            ) + text[featured.end():]
        path.write_text(text, encoding='utf-8')
        changed += 1
    print(f'Moments toolbar migration checked {changed} pages')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
