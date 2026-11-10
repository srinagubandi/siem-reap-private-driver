#!/usr/bin/env python3
"""Add or remove the discoverable traveler-photo gallery toolbar on all 18 pages."""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = ROOT / "data/gallery-toolbar-translations.json"
PAGES = [
    "index.html", "fr.html", "zh.html", "ko.html", "ja.html", "vi.html", "th.html",
    "de.html", "es.html", "it.html", "pt.html", "ru.html", "nl.html", "pl.html",
    "ar.html", "id.html", "sv.html", "cs.html",
]
START = "<!-- gallery-toolbar:start -->"
END = "<!-- gallery-toolbar:end -->"
BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def render(t: dict) -> str:
    return f'''{START}
<div class="gallery-toolbar" data-gallery-toolbar role="region" aria-labelledby="gallery-toolbar-heading">
  <div class="gallery-toolbar__copy">
    <h4 id="gallery-toolbar-heading">{esc(t['heading'])}</h4>
    <p>{esc(t['lead'])}.</p>
  </div>
  <div class="gallery-toolbar__actions">
    <span class="gallery-toolbar__count" data-gallery-count-group hidden><span>{esc(t['photos'])}</span> <span data-gallery-count>0</span></span>
    <button type="button" class="gallery-toolbar__open" data-gallery-open hidden aria-haspopup="dialog">{esc(t['open'])}</button>
  </div>
  <p class="gallery-toolbar__hint" data-gallery-keyboard hidden>{esc(t['keyboard'])}.</p>
  <p class="gallery-toolbar__hint gallery-toolbar__touch-hint" data-gallery-touch hidden>{esc(t['swipe'])}.</p>
</div>
{END}
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--remove', action='store_true')
    args = parser.parse_args()
    translations = {x['filename']: x for x in json.loads(TRANSLATIONS.read_text(encoding='utf-8'))}
    if set(translations) != set(PAGES):
        raise SystemExit('translation filenames must match all 18 pages exactly')
    changed = []
    errors = []
    for filename in PAGES:
        path = ROOT / filename
        text = path.read_text(encoding='utf-8')
        matches = list(BLOCK_RE.finditer(text))
        if args.remove:
            if len(matches) > 1:
                errors.append(f'{filename}: duplicate toolbar markers')
            elif matches:
                path.write_text(BLOCK_RE.sub('', text, count=1), encoding='utf-8')
                changed.append(filename)
            continue
        if len(matches) > 1:
            errors.append(f'{filename}: duplicate toolbar markers')
            continue
        if matches:
            continue
        grid = '<div class="ta-traveler-photo-grid">'
        if text.count(grid) != 1:
            errors.append(f'{filename}: expected one traveler-photo grid')
            continue
        block = render(translations[filename])
        text = text.replace(grid, block + grid, 1)
        if not args.check:
            path.write_text(text, encoding='utf-8')
            changed.append(filename)
    if errors:
        raise SystemExit('\n'.join(errors))
    if args.check:
        print(f'gallery toolbar check passed for {len(PAGES)} pages')
    else:
        print(f'gallery toolbar migration changed {len(changed)} pages')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
