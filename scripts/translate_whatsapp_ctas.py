#!/usr/bin/env python3
"""Localize the visible hero and Jeep-tour WhatsApp CTAs across all 18 pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = {
    "index.html": ("Message on WhatsApp", "Book a Jeep Tour on WhatsApp"),
    "fr.html": ("Message sur WhatsApp", "Réserver une visite en Jeep sur WhatsApp"),
    "zh.html": ("WhatsApp 留言", "在 WhatsApp 上预订吉普车旅游"),
    "ko.html": ("WhatsApp으로 메시지 보내기", "WhatsApp으로 지프 투어 예약"),
    "ja.html": ("WhatsAppでメッセージ", "WhatsAppでジープツアーを予約"),
    "vi.html": ("Nhắn tin trên WhatsApp", "Đặt tour Jeep trên WhatsApp"),
    "th.html": ("ส่งข้อความทาง WhatsApp", "จองทัวร์รถจี๊ปผ่าน WhatsApp"),
    "de.html": ("Nachricht auf WhatsApp", "Jeep-Tour auf WhatsApp buchen"),
    "es.html": ("Mensaje en WhatsApp", "Reserva un tour en Jeep en WhatsApp"),
    "it.html": ("Messaggio su WhatsApp", "Prenota un tour in Jeep su WhatsApp"),
    "pt.html": ("Mensagem no WhatsApp", "Reserve um passeio de Jeep no WhatsApp"),
    "ru.html": ("Сообщение в WhatsApp", "Забронировать тур на джипе в WhatsApp"),
    "nl.html": ("Bericht op WhatsApp", "Boek een Jeep-tour op WhatsApp"),
    "pl.html": ("Wiadomość na WhatsApp", "Zarezerwuj wycieczkę Jeepem na WhatsApp"),
    "ar.html": ("رسالة على WhatsApp", "احجز جولة بجيب على WhatsApp"),
    "id.html": ("Pesan di WhatsApp", "Pesan Tur Jeep di WhatsApp"),
    "sv.html": ("Meddelande på WhatsApp", "Boka en Jeep-tur på WhatsApp"),
    "cs.html": ("Zpráva na WhatsApp", "Rezervujte si jízdu džípem na WhatsApp"),
}

for filename, (hero, jeep) in TRANSLATIONS.items():
    path = ROOT / filename
    text = path.read_text(encoding="utf-8")
    old_hero = "Message on WhatsApp"
    old_jeep = "Book a Jeep Tour on WhatsApp"
    # The English strings occur exactly once in each main language page.
    if text.count(old_hero) != 1 or text.count(old_jeep) != 1:
        raise SystemExit(f"Unexpected WhatsApp CTA counts in {filename}: {text.count(old_hero)}, {text.count(old_jeep)}")
    path.write_text(text.replace(old_hero, hero).replace(old_jeep, jeep), encoding="utf-8")
    print(f"{filename}: {hero} / {jeep}")
