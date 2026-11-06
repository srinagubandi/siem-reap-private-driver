#!/usr/bin/env python3
"""Add the approved We Love Siem Reap footer row to the 18 main locale pages."""
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "index.html", "fr.html", "zh.html", "ko.html", "ja.html", "vi.html",
    "th.html", "de.html", "es.html", "it.html", "pt.html", "ru.html",
    "nl.html", "pl.html", "ar.html", "id.html", "sv.html", "cs.html",
]
ASSET_SOURCE = Path("/home/ubuntu/upload/we-love-siem-reap-cambodia.svg")
ASSET_DEST = ROOT / "assets/brand/we-love-siem-reap-cambodia.svg"

ROW = '''  <div class="siem-reap-love-row" role="group" aria-label="We Love Siem Reap Cambodia">
    <img src="/assets/brand/we-love-siem-reap-cambodia.svg" width="220" height="187" alt="We Love Siem Reap Cambodia" loading="lazy" decoding="async">
    <p>Made with love in Siem Reap, Cambodia</p>
  </div>'''

# The prior localized line is the final child of the main footer flex container.
OLD = re.compile(
    r'''\n\s*<div class="flex items-center gap-2 text-stone-400 text-sm italic">\s*\n\s*<span class="material-symbols-outlined text-sm" data-icon="favorite"(?: aria-hidden="true")?>favorite</span>\s*\n\s*.*?\n\s*</div>\s*\n\s*</div>\s*\n\s*</footer>''',
    re.DOTALL,
)
NEW = "\n" + ROW + "\n</div>\n</footer>"

if not ASSET_SOURCE.is_file():
    raise SystemExit(f"Missing supplied SVG: {ASSET_SOURCE}")
ASSET_DEST.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(ASSET_SOURCE, ASSET_DEST)

for name in PAGES:
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    updated, count = OLD.subn(NEW, text, count=1)
    if count != 1:
        raise SystemExit(f"Expected exactly one old footer slogan in {name}; found {count}")
    if updated.count("Made with love in Siem Reap, Cambodia") != 1:
        raise SystemExit(f"Footer wording check failed in {name}")
    if updated.count("we-love-siem-reap-cambodia.svg") != 1:
        raise SystemExit(f"Footer logo check failed in {name}")
    path.write_text(updated, encoding="utf-8")
    print(f"updated {name}")

print(f"copied {ASSET_DEST.relative_to(ROOT)}")
