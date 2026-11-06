#!/usr/bin/env python3
"""Localize the Phone and Reviews links in the shared footer."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = {
    "index.html": ("Phone", "Reviews"),
    "fr.html": ("Téléphone", "Avis"),
    "zh.html": ("电话", "评论"),
    "ko.html": ("전화", "리뷰"),
    "ja.html": ("電話", "レビュー"),
    "vi.html": ("Điện thoại", "Đánh giá"),
    "th.html": ("โทรศัพท์", "รีวิว"),
    "de.html": ("Telefon", "Bewertungen"),
    "es.html": ("Teléfono", "Reseñas"),
    "it.html": ("Telefono", "Recensioni"),
    "pt.html": ("Telefone", "Avaliações"),
    "ru.html": ("Телефон", "Отзывы"),
    "nl.html": ("Telefoon", "Beoordelingen"),
    "pl.html": ("Telefon", "Opinie"),
    "ar.html": ("الهاتف", "المراجعات"),
    "id.html": ("Telepon", "Ulasan"),
    "sv.html": ("Telefon", "Recensioner"),
    "cs.html": ("Telefon", "Recenze"),
}
FOOTER = re.compile(r"(<footer\b[\s\S]*?</footer>)", re.IGNORECASE)
PHONE = re.compile(r'(<a[^>]*href="tel:\+855976453855"[^>]*>)([^<]*)(</a>)', re.IGNORECASE)
REVIEWS = re.compile(r'(<a[^>]*href="#reviews"[^>]*>)([^<]*)(</a>)', re.IGNORECASE)

for filename, (phone, reviews) in TRANSLATIONS.items():
    path = ROOT / filename
    text = path.read_text(encoding="utf-8")
    match = FOOTER.search(text)
    if not match:
        raise SystemExit(f"Footer missing in {filename}")
    footer = match.group(1)
    footer, phone_count = PHONE.subn(lambda m: m.group(1) + phone + m.group(3), footer, count=1)
    footer, reviews_count = REVIEWS.subn(lambda m: m.group(1) + reviews + m.group(3), footer, count=1)
    if phone_count != 1 or reviews_count != 1:
        raise SystemExit(f"Expected one Phone and Reviews link in {filename}; found {phone_count}, {reviews_count}")
    path.write_text(text[:match.start()] + footer + text[match.end():], encoding="utf-8")
    print(f"{filename}: {phone} · {reviews}")
