#!/usr/bin/env python3
"""Add the supplied guest group photo to the shared traveler-photo gallery."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "index.html", "fr.html", "zh.html", "ko.html", "ja.html", "vi.html",
    "th.html", "de.html", "es.html", "it.html", "pt.html", "ru.html",
    "nl.html", "pl.html", "ar.html", "id.html", "sv.html", "cs.html",
]
SOURCE = Path("/home/ubuntu/upload/WhatsAppImage2026-11-06at16.44.38.webp")
DEST = ROOT / "images/guest-group-siem-reap.webp"
MARKER = '<div class="ta-traveler-photo-grid">'
CARD = '''<figure class="ta-traveler-photo guest-group-photo">
<img src="/images/guest-group-siem-reap.webp" width="1152" height="2048" alt="Guest group enjoying a day in Siem Reap" lang="en" loading="lazy" decoding="async">
<figcaption>Guest group enjoying Siem Reap</figcaption>
</figure>'''

if not SOURCE.is_file():
    raise SystemExit(f"Missing supplied photo: {SOURCE}")
DEST.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE, DEST)

for name in PAGES:
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    if text.count("/images/guest-group-siem-reap.webp"):
        raise SystemExit(f"Photo already present in {name}")
    if text.count(MARKER) != 1:
        raise SystemExit(f"Expected one traveler grid in {name}")
    text = text.replace(MARKER, MARKER + "\n" + CARD, 1)
    path.write_text(text, encoding="utf-8")
    print(f"updated {name}")
print(f"copied {DEST.relative_to(ROOT)}")
