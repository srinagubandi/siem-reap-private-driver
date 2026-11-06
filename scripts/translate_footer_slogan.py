#!/usr/bin/env python3
"""Localize the footer slogan while keeping the English page in English."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = {
    "index.html": "Made with love in Siem Reap, Cambodia",
    "fr.html": "Fait avec amour à Siem Reap, Cambodge",
    "zh.html": "在柬埔寨暹粒，用爱制作",
    "ko.html": "캄보디아 씨엠립에서 사랑을 담아 만들었습니다",
    "ja.html": "カンボジアのシェムリアップから、愛を込めて",
    "vi.html": "Được tạo nên bằng tình yêu tại Siem Reap, Campuchia",
    "th.html": "สร้างด้วยความรักที่เสียมราฐ ประเทศกัมพูชา",
    "de.html": "Mit Liebe in Siem Reap, Kambodscha gemacht",
    "es.html": "Hecho con amor en Siem Reap, Camboya",
    "it.html": "Fatto con amore a Siem Reap, Cambogia",
    "pt.html": "Feito com amor em Siem Reap, Camboja",
    "ru.html": "Сделано с любовью в Сиемреапе, Камбоджа",
    "nl.html": "Met liefde gemaakt in Siem Reap, Cambodja",
    "pl.html": "Zrobione z miłością w Siem Reap w Kambodży",
    "ar.html": "صُنع بحب في سيم ريب، كمبوديا",
    "id.html": "Dibuat dengan cinta di Siem Reap, Kamboja",
    "sv.html": "Gjord med kärlek i Siem Reap, Kambodja",
    "cs.html": "Vyrobeno s láskou v Siem Reapu v Kambodži",
}
PATTERN = re.compile(r'(<div class="siem-reap-love-row"[\s\S]*?<p>)(.*?)(</p>)')
for filename, slogan in TRANSLATIONS.items():
    path = ROOT / filename
    text = path.read_text(encoding="utf-8")
    updated, count = PATTERN.subn(lambda m: m.group(1) + slogan + m.group(3), text, count=1)
    if count != 1:
        raise SystemExit(f"Expected exactly one footer slogan in {filename}; found {count}")
    path.write_text(updated, encoding="utf-8")
    print(f"{filename}: {slogan}")
