#!/usr/bin/env python3
"""Remove the locally supplied guest photos from the Tripadvisor traveler gallery."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    'index.html', 'fr.html', 'zh.html', 'ko.html', 'ja.html', 'vi.html', 'th.html',
    'de.html', 'es.html', 'it.html', 'pt.html', 'ru.html', 'nl.html', 'pl.html',
    'ar.html', 'id.html', 'sv.html', 'cs.html',
]
FIGURE_RE = re.compile(r'\s*<figure class="ta-traveler-photo (?:guest-welcome-photo|guest-group-photo)"[\s\S]*?</figure>', re.S)


def main() -> int:
    changed = 0
    for filename in PAGES:
        path = ROOT / filename
        text = path.read_text(encoding='utf-8')
        section_start = text.index('<div id="tripadvisor-traveler-photos"')
        section_end = text.index('</div>\n</div>\n</div>\n</section>', section_start)
        before, section, after = text[:section_start], text[section_start:section_end], text[section_end:]
        section = FIGURE_RE.sub('', section)
        path.write_text(before + section + after, encoding='utf-8')
        changed += 1
    print(f'checked Traveler photo gallery on {changed} pages')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
