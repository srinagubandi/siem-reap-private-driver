#!/usr/bin/env python3
"""Version shared gallery assets so GitHub Pages refreshes cached controls."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    'index.html', 'fr.html', 'zh.html', 'ko.html', 'ja.html', 'vi.html', 'th.html',
    'de.html', 'es.html', 'it.html', 'pt.html', 'ru.html', 'nl.html', 'pl.html',
    'ar.html', 'id.html', 'sv.html', 'cs.html',
]
VERSION = '20261110-gallery-2'

for filename in PAGES:
    path = ROOT / filename
    text = path.read_text(encoding='utf-8')
    text = text.replace('/assets/css/tripadvisor-reviews.css"', f'/assets/css/tripadvisor-reviews.css?v={VERSION}"')
    text = text.replace('/assets/js/enhancements.js"', f'/assets/js/enhancements.js?v={VERSION}"')
    path.write_text(text, encoding='utf-8')
print(f'versioned gallery assets on {len(PAGES)} pages as {VERSION}')
