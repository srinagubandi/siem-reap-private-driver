#!/usr/bin/env python3
"""Keep Moments with Guests focused on people and guest experiences."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    'index.html', 'fr.html', 'zh.html', 'ko.html', 'ja.html', 'vi.html', 'th.html',
    'de.html', 'es.html', 'it.html', 'pt.html', 'ru.html', 'nl.html', 'pl.html',
    'ar.html', 'id.html', 'sv.html', 'cs.html',
]
START = '<!-- moments-people-photos:start -->'
END = '<!-- moments-people-photos:end -->'
CARD_RE = re.compile(r'<div class="guest-gallery-card">\s*<a href="([^"]+)"[\s\S]*?</div>', re.S)

WELCOME = '''<figure class="guest-gallery-card guest-welcome-card">
<a href="/images/guest-welcome-siem-reap.webp" target="_blank" rel="noopener noreferrer" aria-label="Open the full-size guest welcome photo">
<picture>
<source srcset="/images/guest-welcome-siem-reap.webp" type="image/webp">
<img src="/images/guest-welcome-siem-reap.jpg" width="1600" height="1200" alt="Guests sharing a warm welcome with their Angkor Drivers guide in Siem Reap" loading="lazy" decoding="async">
</picture>
</a>
<figcaption>Guests sharing a warm welcome in Siem Reap</figcaption>
</figure>'''

GROUP = '''<figure class="guest-gallery-card guest-group-card">
<a href="/images/guest-group-siem-reap.webp" target="_blank" rel="noopener noreferrer" aria-label="Open the full-size guest group photo">
<img src="/images/guest-group-siem-reap.webp" width="1152" height="2048" alt="Guest group enjoying a day in Siem Reap" loading="lazy" decoding="async">
</a>
<figcaption>Guest group enjoying Siem Reap</figcaption>
</figure>'''


def main() -> int:
    changed = 0
    for filename in PAGES:
        path = ROOT / filename
        text = path.read_text(encoding='utf-8')
        start = text.index('<div class="guest-gallery-cards" data-gallery-template="thumbsup-cards">')
        end_marker = '\n</div>\n<div id="tripadvisor-traveler-photos"'
        end = text.index(end_marker, start) + len('\n</div>')
        block = text[start:end]
        block = re.sub(
            r'<div class="guest-gallery-card">\s*<a href="/images/jeep-(?:two-forest|fleet-street)\.jpg"[\s\S]*?</div>',
            '',
            block,
        )
        if START not in block:
            first_card = block.index('<div class="guest-gallery-card">')
            additions = f'\n{START}\n{WELCOME}\n{GROUP}\n{END}\n'
            block = block[:first_card] + additions + block[first_card:]
        text = text[:start] + block + text[end:]
        path.write_text(text, encoding='utf-8')
        changed += 1
    print(f'updated Moments people photos on {changed} pages')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
