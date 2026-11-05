#!/usr/bin/env python3
import re, html
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
CSS_HREF = '/assets/css/tripadvisor-hero-badge.css'
CSS_LINK = f'''<link rel='stylesheet' href='{CSS_HREF}'>'''
BADGE_ID = 'tripadvisor-hero-badge'
GOOGLE_ID = 'google-reviews-section'
PLACEHOLDER_MARK = 'id="google-reviews-placeholder"'
WRAPPER_RE = re.compile(r'<div\b[^>]*\bclass="[^"]*\bmb-16\b[^"]*"[^>]*>', re.I)
SCRIPT_RE = re.compile(r'\s*<script\b[^>]*src="https://static\.elfsight\.com/platform/platform\.js"[^>]*>\s*</script>\s*', re.I)
APP_DIV_RE = re.compile(r'\s*<div\b[^>]*class="[^"]*elfsight-app-YOUR_ELFSIGHT_APP_ID[^"]*"[^>]*>\s*</div>\s*', re.I | re.S)
MAXW_RE = re.compile(r'<div\b[^>]*\bclass="[^"]*\bmax-w-2xl\b[^"]*"[^>]*>', re.I)
BADGE_RE = re.compile(r"""<a\b[^>]*\bid=['"]tripadvisor-hero-badge['"][^>]*>.*?</a>""", re.I | re.S)

LOCALES = {
    'index.html': ('Rating as of', '5 Nov 2026', 'TripAdvisor rating 5 out of 5 based on 6 reviews. Rating as of {date}. Opens the official TripAdvisor listing.'),
    'ar.html': ('تقييم بتاريخ', '5 نوفمبر 2026', 'TripAdvisor: التقييم 5 من 5 بناءً على 6 تقييمات. التقييم بتاريخ {date}. يفتح قائمة TripAdvisor الرسمية.'),
    'cs.html': ('Hodnocení k datu', '5. 11. 2026', 'TripAdvisor: hodnocení 5 z 5 na základě 6 recenzí. Hodnocení k datu {date}. Otevře oficiální stránku TripAdvisor.'),
    'de.html': ('Bewertung vom', '5. Nov. 2026', 'TripAdvisor: Bewertung 5 von 5 basierend auf 6 Bewertungen. Bewertung vom {date}. Öffnet die offizielle TripAdvisor-Seite.'),
    'es.html': ('Valoración a fecha de', '5 nov 2026', 'TripAdvisor: valoración 5 de 5 basada en 6 reseñas. Valoración a fecha de {date}. Abre la página oficial de TripAdvisor.'),
    'fr.html': ('Note au', '5 nov. 2026', 'TripAdvisor : note 5 sur 5 basée sur 6 avis. Note au {date}. Ouvre la page officielle TripAdvisor.'),
    'id.html': ('Rating per', '5 Nov 2026', 'TripAdvisor: rating 5 dari 5 berdasarkan 6 ulasan. Rating per {date}. Membuka halaman resmi TripAdvisor.'),
    'it.html': ('Valutazione al', '5 nov 2026', 'TripAdvisor: valutazione 5 su 5 basata su 6 recensioni. Valutazione al {date}. Apre la pagina ufficiale di TripAdvisor.'),
    'ja.html': ('評価日', '2026年11月5日', 'TripAdvisor: 6件のレビューに基づく5つ星中5.0の評価。評価日{date}。TripAdvisor公式ページを開きます。'),
    'ko.html': ('평가 기준일', '2026년 11월 5일', 'TripAdvisor: 리뷰 6개 기준 5점 만점에 5.0점. 평가 기준일 {date}. 공식 TripAdvisor 페이지를 엽니다.'),
    'nl.html': ('Beoordeling per', '5 nov. 2026', 'TripAdvisor: beoordeling 5 van 5 op basis van 6 beoordelingen. Beoordeling per {date}. Opent de officiële TripAdvisor-pagina.'),
    'pl.html': ('Ocena na dzień', '5 lis 2026', 'TripAdvisor: ocena 5 na 5 na podstawie 6 recenzji. Ocena na dzień {date}. Otwiera oficjalną stronę TripAdvisor.'),
    'pt.html': ('Avaliação em', '5 de nov. de 2026', 'TripAdvisor: avaliação 5 de 5 com base em 6 avaliações. Avaliação em {date}. Abre a página oficial do TripAdvisor.'),
    'ru.html': ('Оценка на', '5 нояб. 2026 г.', 'TripAdvisor: оценка 5 из 5 на основе 6 отзывов. Оценка на {date}. Открывает официальную страницу TripAdvisor.'),
    'sv.html': ('Betyg per', '5 nov. 2026', 'TripAdvisor: betyg 5 av 5 baserat på 6 recensioner. Betyg per {date}. Öppnar den officiella TripAdvisor-sidan.'),
    'th.html': ('คะแนน ณ วันที่', '5 พ.ย. 2026', 'TripAdvisor: คะแนน 5 จาก 5 จากรีวิว 6 รายการ คะแนน ณ วันที่ {date} เปิดหน้ารายการ TripAdvisor อย่างเป็นทางการ'),
    'vi.html': ('Đánh giá vào ngày', '5 thg 11, 2026', 'TripAdvisor: đánh giá 5 trên 5 dựa trên 6 đánh giá. Đánh giá vào ngày {date}. Mở trang TripAdvisor chính thức.'),
    'zh.html': ('评分截至', '2026年11月5日', 'TripAdvisor：基于6条评论获得5分（满分5分）。评分截至{date}。打开TripAdvisor官方页面。'),
}

def read_summary_data(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    summary = soup.find(id='tripadvisor-summary')
    if not summary:
        return None
    rating_el = summary.find('span', class_=lambda c: c and 'text-emerald-600' in c)
    count_el = summary.find('span', class_=lambda c: c and 'text-on-surface-variant' in c and 'font-normal' in c)
    date_paras = summary.find_all('p')
    link = summary.find('a', href=True)
    if not (rating_el and count_el and len(date_paras) > 1 and link):
        return None
    return {
        'rating': rating_el.get_text(' ', strip=True),
        'count': count_el.get_text(' ', strip=True),
        'href': link['href'],
    }

def build_badge(data, filename):
    asof_raw, date_raw, aria_tpl = LOCALES.get(filename, LOCALES['index.html'])
    href = html.escape(data['href'], quote=True)
    r = html.escape(data['rating'])
    c = html.escape(data['count'])
    asof_disp = html.escape(asof_raw, quote=True)
    date_disp = html.escape(date_raw, quote=True)
    aria = html.escape(aria_tpl.format(date=date_raw), quote=True)
    badge = (
        f'''<a id='{BADGE_ID}' class='tripadvisor-hero-badge' href='{href}' target='_blank' rel='noopener' aria-label='{aria}'>'''
        '''<span class='tripadvisor-hero-badge__main'><span class='tripadvisor-hero-badge__brand'>TripAdvisor</span>'''
        f'''<span class='tripadvisor-hero-badge__rating'>{r}</span><span class='tripadvisor-hero-badge__count'>{c}</span></span>'''
        f'''<span class='tripadvisor-hero-badge__date'><span class='tripadvisor-hero-badge__date-asof'>{asof_disp}</span> <span class='tripadvisor-hero-badge__date-value' dir='auto'>{date_disp}</span></span>'''
        '''<span class='tripadvisor-hero-badge__arrow' aria-hidden='true'>↗</span></a>'''
    )
    return badge

def replace_or_insert_badge(raw, badge):
    if BADGE_RE.search(raw):
        return BADGE_RE.sub(lambda _: badge, raw, count=1), True
    if f'''id='{BADGE_ID}' ''' in raw:
        return raw, False
    home_idx = raw.find('id="home"')
    if home_idx == -1:
        return raw, False
    m = MAXW_RE.search(raw, home_idx)
    if not m:
        return raw, False
    h1_idx = raw.find('<h1', m.end())
    if h1_idx == -1:
        return raw, False
    return raw[:h1_idx] + badge + raw[h1_idx:], True

def add_css(raw):
    if CSS_HREF in raw:
        return raw, False
    pos = raw.rfind('</head>')
    if pos == -1:
        return raw, False
    return raw[:pos] + CSS_LINK + '\n' + raw[pos:], True

def add_google_hidden(raw):
    pos = raw.find(PLACEHOLDER_MARK)
    if pos == -1:
        return raw, False
    matches = list(WRAPPER_RE.finditer(raw, 0, pos))
    if not matches:
        return raw, False
    m = matches[-1]
    opening = m.group(0)
    has_id = f'id="{GOOGLE_ID}"' in opening
    has_hidden = re.search(r'\bhidden\b', opening) is not None
    if has_id and has_hidden:
        return raw, False
    attrs = ''
    if not has_id:
        attrs += f' id="{GOOGLE_ID}"'
    if not has_hidden:
        attrs += ' hidden'
    new_opening = opening[:-1] + attrs + '>' if opening.endswith('>') else opening + attrs + '>'
    return raw[:m.start()] + new_opening + raw[m.end():], True

def remove_elfsight(raw):
    raw, n = SCRIPT_RE.subn(lambda _: '', raw, count=1)
    raw, m = APP_DIV_RE.subn(lambda _: '', raw, count=1)
    return raw, (n + m) > 0

pages = sorted(ROOT.glob('*.html'))
seen = updated = 0
for path in pages:
    raw = path.read_text(encoding='utf-8')
    if 'id="tripadvisor-summary"' not in raw:
        continue
    seen += 1
    data = read_summary_data(raw)
    if not data:
        continue
    badge = build_badge(data, path.name)
    original = raw
    raw, badge_ok = replace_or_insert_badge(raw, badge)
    raw, css_ok = add_css(raw)
    raw, google_ok = add_google_hidden(raw)
    raw, elfsight_ok = remove_elfsight(raw)
    if raw != original:
        if not raw.endswith('\n'):
            raw += '\n'
        path.write_text(raw, encoding='utf-8', newline='')
        updated += 1
print(f'Processed {seen} pages; updated {updated}.')
