#!/usr/bin/env python3
"""Add the supplied welcome photo to every localized traveler-photo gallery."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "index.html", "fr.html", "zh.html", "ko.html", "ja.html", "vi.html", "th.html",
    "de.html", "es.html", "it.html", "pt.html", "ru.html", "nl.html", "pl.html",
    "ar.html", "id.html", "sv.html", "cs.html",
]
CARD = '''<figure class="ta-traveler-photo guest-welcome-photo" id="guest-welcome-photo">
<a href="/images/guest-welcome-siem-reap.webp" target="_blank" rel="noopener noreferrer" aria-label="Open the full-size guest welcome photo">
<picture>
<source srcset="/images/guest-welcome-siem-reap.webp" type="image/webp">
<img src="/images/guest-welcome-siem-reap.jpg" width="1600" height="1200" alt="Guests sharing a warm welcome with their Angkor Drivers guide in Siem Reap" loading="lazy" decoding="async">
</picture>
</a>
<figcaption>Guests sharing a warm welcome in Siem Reap</figcaption>
</figure>'''

for filename in PAGES:
    path = ROOT / filename
    text = path.read_text(encoding="utf-8")
    if 'id="guest-welcome-photo"' in text or 'guest-welcome-siem-reap.webp' in text:
        print(f"{filename}: already present")
        continue
    marker = '<div id="tripadvisor-traveler-photos"'
    start = text.index(marker)
    grid_start = text.index('<div class="ta-traveler-photo-grid">', start)
    insert_at = grid_start + len('<div class="ta-traveler-photo-grid">')
    text = text[:insert_at] + '\n' + CARD + text[insert_at:]
    path.write_text(text, encoding="utf-8")
    print(f"{filename}: added")
