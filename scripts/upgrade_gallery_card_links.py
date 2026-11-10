#!/usr/bin/env python3
"""Wrap the existing local portrait traveler photo in a native image link."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "index.html", "fr.html", "zh.html", "ko.html", "ja.html", "vi.html", "th.html",
    "de.html", "es.html", "it.html", "pt.html", "ru.html", "nl.html", "pl.html",
    "ar.html", "id.html", "sv.html", "cs.html",
]
OLD = '''<figure class="ta-traveler-photo guest-group-photo">
<img src="/images/guest-group-siem-reap.webp" width="1152" height="2048" alt="Guest group enjoying a day in Siem Reap" lang="en" loading="lazy" decoding="async">
<figcaption>Guest group enjoying Siem Reap</figcaption>
</figure>'''
NEW = '''<figure class="ta-traveler-photo guest-group-photo">
<a href="/images/guest-group-siem-reap.webp" target="_blank" rel="noopener noreferrer" aria-label="Open the full-size guest group photo">
<img src="/images/guest-group-siem-reap.webp" width="1152" height="2048" alt="Guest group enjoying a day in Siem Reap" lang="en" loading="lazy" decoding="async">
</a>
<figcaption>Guest group enjoying Siem Reap</figcaption>
</figure>'''
for filename in PAGES:
    path = ROOT / filename
    text = path.read_text(encoding="utf-8")
    if OLD in text:
        text = text.replace(OLD, NEW, 1)
        path.write_text(text, encoding="utf-8")
        print(f"{filename}: wrapped portrait card")
    elif NEW in text:
        print(f"{filename}: already wrapped")
    else:
        raise SystemExit(f"portrait card not found in {filename}")
