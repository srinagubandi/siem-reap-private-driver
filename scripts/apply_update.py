#!/usr/bin/env python3
"""Apply final production updates to Angkor Drivers static HTML.

Runs on the original frozen baseline. Idempotent. Preserves all copy.
"""
from pathlib import Path
import re, json

BASE = Path('.')
PAGES = ['index.html', 'fr.html', 'zh.html', 'ko.html', 'ja.html', 'vi.html',
         'th.html', 'de.html', 'es.html', 'it.html', 'pt.html', 'ru.html',
         'nl.html', 'pl.html', 'ar.html', 'id.html', 'sv.html', 'cs.html']

TRIPADVISOR_URL = "https://www.tripadvisor.co.uk/Attraction_Review-g297390-d34664961-Reviews-Angkordrivers-Siem_Reap_Siem_Reap_Province.html"

LOC = {
    'en': {'rating': '5.0/5', 'reviews': '6 reviews', 'verified': 'verified 2026-11-05',
           'read': 'Read reviews on TripAdvisor', 'dialog': 'Mobile navigation'},
    'fr': {'rating': '5,0/5', 'reviews': '6 avis', 'verified': 'vérifié 2026-11-05',
           'read': "Lire les avis sur TripAdvisor", 'dialog': 'Navigation mobile'},
    'zh-Hans': {'rating': '5.0/5', 'reviews': '6条评论', 'verified': '已验证2026-11-05',
                'read': '在TripAdvisor上阅读评论', 'dialog': '移动导航'},
    'ko': {'rating': '5.0/5', 'reviews': '리뷰 6개', 'verified': '2026-11-05 확인됨',
           'read': '트립어드바이저 리뷰 읽기', 'dialog': '모바일 내비게이션'},
    'ja': {'rating': '5.0/5', 'reviews': '6件のレビュー', 'verified': '2026-11-05検証済み',
           'read': 'TripAdvisorでレビューを読む', 'dialog': 'モバイルナビゲーション'},
    'vi': {'rating': '5.0/5', 'reviews': '6 đánh giá', 'verified': 'đã xác minh 2026-11-05',
           'read': 'Đọc đánh giá trên TripAdvisor', 'dialog': 'Điều hướng di động'},
    'th': {'rating': '5.0/5', 'reviews': '6 รีวิว', 'verified': 'ยืนยันแล้ว 2026-11-05',
           'read': 'อ่านรีวิวบน TripAdvisor', 'dialog': 'การนำทางมือถือ'},
    'de': {'rating': '5,0/5', 'reviews': '6 Bewertungen', 'verified': 'verifiziert 2026-11-05',
           'read': 'Bewertungen auf TripAdvisor lesen', 'dialog': 'Mobile Navigation'},
    'es': {'rating': '5,0/5', 'reviews': '6 reseñas', 'verified': 'verificado 2026-11-05',
           'read': 'Leer reseñas en TripAdvisor', 'dialog': 'Navegación móvil'},
    'it': {'rating': '5,0/5', 'reviews': '6 recensioni', 'verified': 'verificato 2026-11-05',
           'read': 'Leggi le recensioni su TripAdvisor', 'dialog': 'Navigazione mobile'},
    'pt': {'rating': '5,0/5', 'reviews': '6 avaliações', 'verified': 'verificado 2026-11-05',
           'read': 'Leia avaliações no TripAdvisor', 'dialog': 'Navegação móvel'},
    'ru': {'rating': '5,0/5', 'reviews': '6 отзывов', 'verified': 'подтверждено 2026-11-05',
           'read': 'Читать отзывы на TripAdvisor', 'dialog': 'Мобильная навигация'},
    'nl': {'rating': '5,0/5', 'reviews': '6 beoordelingen', 'verified': 'geverifieerd 2026-11-05',
           'read': 'Lees beoordelingen op TripAdvisor', 'dialog': 'Mobiele navigatie'},
    'pl': {'rating': '5,0/5', 'reviews': '6 recenzji', 'verified': 'zweryfikowano 2026-11-05',
           'read': 'Przeczytaj recenzje na TripAdvisor', 'dialog': 'Nawigacja mobilna'},
    'ar': {'rating': '5.0/5', 'reviews': '6 تقييمات', 'verified': 'تم التحقق 2026-11-05',
           'read': 'اقرأ التقييمات على TripAdvisor', 'dialog': 'التنقل المحمول'},
    'id': {'rating': '5.0/5', 'reviews': '6 ulasan', 'verified': 'terverifikasi 2026-11-05',
           'read': 'Baca ulasan di TripAdvisor', 'dialog': 'Navigasi seluler'},
    'sv': {'rating': '5,0/5', 'reviews': '6 recensioner', 'verified': 'verifierad 2026-11-05',
           'read': 'Läs recensioner på TripAdvisor', 'dialog': 'Mobilnavigering'},
    'cs': {'rating': '5,0/5', 'reviews': '6 recenzí', 'verified': 'ověřeno 2026-11-05',
           'read': 'Přečtěte si recenze na TripAdvisor', 'dialog': 'Mobilní navigace'}
}

ICONS = '''
<link rel="icon" type="image/x-icon" href="/favicon.ico"/>
<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"/>
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"/>
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"/>
<link rel="manifest" href="/site.webmanifest"/>
'''

def get_lang(html):
    m = re.search(r'<html[^>]*\blang="([^"]+)"', html, re.I)
    if m:
        lang = m.group(1)
        # Normalize zh-Hans
        if lang.lower().startswith('zh'):
            lang = 'zh-Hans' if 'hans' in lang.lower() else 'zh-Hans'
        return lang
    return 'en'

def balanced_tag(html, start_tag):
    """Return (start, end) indices of the balanced tag beginning at start_tag."""
    depth = 0
    i = start_tag
    while i < len(html):
        if html.startswith('<div', i):
            depth += 1
            i = html.find('>', i) + 1
        elif html.startswith('</div', i):
            depth -= 1
            if depth == 0:
                end = html.find('>', i) + 1
                return start_tag, end
            i += 6
        else:
            i += 1
    return start_tag, len(html)

def remove_favicons(html):
    # Remove all link tags with rel=icon/manifest/apple-touch-icon
    pattern = r'<link\b[^>]*\brel="(?:icon|apple-touch-icon|manifest)"[^>]*>'
    html = re.sub(pattern, '', html, flags=re.I)
    return html

def ensure_viewport(html, page):
    if 'thank-you' in page or '404' in page or 'code' in page:
        if not re.search(r'<meta[^>]*name="viewport"', html, re.I):
            # Insert after charset if present, else after <head>
            if '<meta charset' in html:
                pos = html.find('<meta charset')
                end = html.find('>', pos) + 1
                html = html[:end] + '\n<meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>' + html[end:]
            else:
                html = html.replace('<head>', '<head>\n<meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>', 1)
    return html

def add_css_js(html):
    # Add CSS before </head>
    css_block = '<link rel="stylesheet" href="/assets/css/enhancements.css">\n<link rel="stylesheet" href="/assets/css/release-fixes.css">'
    if '/assets/css/enhancements.css' not in html:
        html = html.replace('</head>', css_block + '\n</head>', 1)
    # Add JS before </body>
    if '/assets/js/enhancements.js' not in html:
        html = html.replace('</body>', '<script src="/assets/js/enhancements.js" defer></script>\n</body>', 1)
    return html

def replace_tailwind(html):
    # Remove Tailwind CDN script and tailwind-config block
    html = re.sub(r'<script\s+src="https://cdn\.tailwindcss\.com[^"]*"[^>]*></script>',
                  '<link rel="stylesheet" href="/assets/tailwind.css">', html, flags=re.I)
    # Remove tailwind-config script block
    pattern = r'<script\s+id="tailwind-config">.*?</script>'
    html = re.sub(pattern, '', html, flags=re.DOTALL)
    return html

def replace_tripadvisor_block(html, loc):
    start = html.find('id="tripadvisor-widget-placeholder"')
    if start == -1:
        return html
    # Find the opening div tag
    open_start = html.rfind('<div', 0, start)
    open_end = html.find('>', open_start) + 1
    # Find balanced closing div
    depth = 1
    i = open_end
    while i < len(html):
        if html.startswith('<div', i):
            depth += 1
            i = html.find('>', i) + 1
        elif html.startswith('</div', i):
            depth -= 1
            if depth == 0:
                close_end = html.find('>', i) + 1
                break
            i += 6
        else:
            i += 1
    else:
        return html
    new_block = f'''<div id="tripadvisor-summary" class="bg-white rounded-2xl shadow-sm border border-outline-variant p-10 text-center">
      <p class="text-2xl font-bold text-primary mb-2"><span class="text-emerald-600">{loc['rating']}</span> <span class="text-on-surface-variant font-normal">({loc['reviews']})</span></p>
      <p class="text-sm text-on-surface-variant mb-4">{loc['verified']}</p>
      <a class="inline-block px-6 py-3 bg-emerald-600 text-white rounded-lg font-semibold hover:bg-emerald-700 transition-all" href="{TRIPADVISOR_URL}" target="_blank" rel="noopener">{loc['read']}</a>
    </div>'''
    return html[:open_start] + new_block + html[close_end:]

def remove_bird_svg(html):
    # Remove the decorative TripAdvisor bird SVG (viewBox="0 0 60 60")
    pattern = r'<svg[^>]*viewBox="0 0 60 60"[^>]*>.*?&#128038;.*?</svg>'
    return re.sub(pattern, '', html, flags=re.DOTALL)

def fix_ta_cta(html):
    return html.replace('https://www.tripadvisor.com/REPLACE_WITH_YOUR_TRIPADVISOR_LISTING', TRIPADVISOR_URL)

def update_service_jsonld(html):
    """Update all Service JSON-LD blocks: add provider.sameAs, remove aggregateRating."""
    pattern = r'<script\s+type="application/ld\+json">(.*?)</script>'
    def replace_jsonld(match):
        json_str = match.group(1)
        try:
            data = json.loads(json_str)
            # If it's a Service, modify it
            if isinstance(data, dict) and data.get('@type') == 'Service':
                # Add provider.sameAs if not present
                provider = data.setdefault('provider', {})
                if 'sameAs' not in provider:
                    provider['sameAs'] = TRIPADVISOR_URL
                # Remove aggregateRating if present
                if 'aggregateRating' in data:
                    del data['aggregateRating']
                # Re-serialize with consistent formatting
                new_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
                return f'<script type="application/ld+json">{new_json}</script>'
            # Leave non-Service blocks unchanged
            return match.group(0)
        except json.JSONDecodeError:
            # If JSON parsing fails, leave the block unchanged
            return match.group(0)
    
    # Apply replacement to all JSON-LD script tags
    return re.sub(pattern, replace_jsonld, html, flags=re.DOTALL)

def add_form_ids(html):
    # Add IDs and for attributes to the six form controls
    controls = [
        ('name="name"', 'id="name"', 'autocomplete="name"', 'input'),
        ('name="email"', 'id="email"', 'autocomplete="email"', 'input'),
        ('name="dates"', 'id="dates"', '', 'input'),
        ('name="service"', 'id="service"', '', 'select'),
        ('name="message"', 'id="message"', '', 'textarea'),
        ('name="whatsapp"', 'id="whatsapp"', 'autocomplete="tel" inputmode="tel"', 'input')
    ]
    # We need to find each control and its preceding label sequentially
    # Use regex to find all control positions and label positions
    # We'll work from end to start to preserve indexes
    positions = []
    label_positions = [m.start() for m in re.finditer(r'<label\b', html)]
    for ctrl in controls:
        name_attr = ctrl[0]
        pos = html.find(name_attr)
        if pos == -1:
            continue
        # find the control tag start
        ctrl_start = html.rfind('<', 0, pos)
        ctrl_end = html.find('>', pos) + 1
        ctrl_tag = html[ctrl_start:ctrl_end]
        # If id already present, skip
        if 'id=' in ctrl_tag:
            continue
        # Insert id
        new_tag = re.sub(r'(<\w+)(\s)', r'\1 ' + ctrl[1] + r'\2', ctrl_tag, count=1)
        if ctrl[3] == 'input' and ctrl[2]:
            # Add autocomplete/inputmode if not present
            if 'autocomplete=' not in new_tag:
                new_tag = re.sub(r'\s*/?>$', lambda m: ' ' + ctrl[2] + (' />' if '/>' in m.group(0) else '>'), new_tag)
        # Replace in html
        html = html[:ctrl_start] + new_tag + html[ctrl_end:]
        # Now find label: nearest preceding <label after previous control
        # Determine insertion index for label for attribute
        # We'll search backwards from ctrl_start for a <label
        label_start = html.rfind('<label', 0, ctrl_start)
        if label_start != -1:
            label_end = html.find('>', label_start) + 1
            label_tag = html[label_start:label_end]
            if 'for=' not in label_tag:
                # Add for attribute
                new_label = label_tag.replace('>', ' for="' + ctrl[1].split('"')[1] + '">', 1)
                html = html[:label_start] + new_label + html[label_end:]
    return html

def add_hamburger_attrs(html):
    # Add aria-controls and aria-expanded to hamburger button
    pattern = r'<button\s+class="hamburger"\s+id="hamburger"\s+aria-label="menu">'
    replacement = '<button class="hamburger" id="hamburger" aria-label="menu" aria-controls="mobileDrawer" aria-expanded="false">'
    html = re.sub(pattern, replacement, html, count=1)
    # Add role dialog to mobile drawer
    pattern2 = r'<div\s+class="mobile-drawer"\s+id="mobileDrawer">'
    lang = get_lang(html)
    aria_label = LOC.get(lang, LOC['en'])['dialog']
    replacement2 = f'<div class="mobile-drawer" id="mobileDrawer" role="dialog" aria-modal="true" aria-label="{aria_label}">'
    html = re.sub(pattern2, replacement2, html, count=1)
    return html

def fix_viewport(html):
    # Ensure viewport-fit=cover and zoom enabled
    pattern = r'<meta\s+content="width=device-width,\s*initial-scale=1\.0"\s+name="viewport"/>'
    replacement = '<meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>'
    if re.search(pattern, html):
        html = re.sub(pattern, replacement, html, count=1)
    else:
        # Update any viewport meta
        pattern2 = r'<meta\b[^>]*name="viewport"[^>]*>'
        html = re.sub(pattern2, replacement, html, count=1)
    return html

def remove_testimonial_chevrons(html):
    # Remove the div containing the two chevron buttons in testimonials
    pattern = r'<div\s+class="hidden\s+md:flex\s+gap-4">\s*<button.*?</button>\s*<button.*?</button>\s*</div>'
    return re.sub(pattern, '', html, flags=re.DOTALL)

def remove_obsolete_scripts(html):
    # Remove script blocks that reference mobile-menu-btn or lang-dropdown-wrapper
    pattern = r'<script>.*?(mobile-menu-btn|lang-dropdown-wrapper).*?</script>'
    html = re.sub(pattern, '', html, flags=re.DOTALL)
    # Remove any script that adds langLeft/langRight listeners (duplicate)
    pattern2 = r'<script>.*?langLeft.*?langRight.*?</script>'
    html = re.sub(pattern2, '', html, flags=re.DOTALL)
    return html

def add_noscript_css(html):
    """Add noscript CSS to make nav responsive without JavaScript."""
    noscript_block = '<noscript><style>.nav-links{display:flex!important;flex-wrap:wrap!important;height:auto!important;}.hamburger{display:none!important;}nav{position:static!important;}</style></noscript>'
    if '<noscript>' not in html:
        # Insert after last CSS link or before </head>
        head_end = html.find('</head>')
        if head_end != -1:
            return html[:head_end] + noscript_block + html[head_end:]
    return html

def process_floating_whatsapp(html):
    # Find the fixed whatsapp anchor and add class, remove inline handlers
    # It's the anchor with href="https://wa.me/855976453855" that has style with position:fixed
    pattern = r'<a\s+href="https://wa\.me/855976453855"[^>]*?(?:style="[^"]*position:\s*fixed[^"]*"|style=[^>]*position:\s*fixed)[^>]*>'
    m = re.search(pattern, html, re.DOTALL)
    if m:
        tag = m.group(0)
        # Add class if not present
        if 'floating-whatsapp' not in tag:
            if 'class=' in tag:
                tag = re.sub(r'class="([^"]*)"', r'class="\1 floating-whatsapp"', tag, count=1)
            else:
                tag = tag.replace('>', ' class="floating-whatsapp">', 1)
        # Remove onmouseover/onmouseout
        tag = re.sub(r'\s+onmouseover="[^"]*"', '', tag)
        tag = re.sub(r'\s+onmouseout="[^"]*"', '', tag)
        html = html[:m.start()] + tag + html[m.end():]
    return html

def add_hero_actions(html):
    # Add hero-actions class to the CTA parent in hero (the div with flex-wrap gap-4 containing whatsapp button)
    # Find the div that contains href="https://wa.me/855976453855" in hero section
    hero_start = html.find('id="home"')
    if hero_start == -1:
        return html
    hero_end = html.find('</section>', hero_start)
    if hero_end == -1:
        hero_end = len(html)
    hero_html = html[hero_start:hero_end]
    # Find the div with class containing "flex flex-wrap gap-4"
    pattern = r'<div\s+class="([^"]*\bflex\s+flex-wrap\s+gap-4[^"]*)"'
    m = re.search(pattern, hero_html)
    if m and 'hero-actions' not in m.group(1):
        new_class = m.group(1) + ' hero-actions'
        hero_html = hero_html[:m.start()] + f'<div class="{new_class}"' + hero_html[m.end():]
        html = html[:hero_start] + hero_html + html[hero_end:]
    return html

def update_comments(html):
    # Update obsolete TA comments
    html = html.replace('Replace the placeholder below with your official TripAdvisor widget code.',
                        'TripAdvisor summary replaced with static verified rating block.')
    return html

def process_file(page):
    """Process a single HTML file with all enhancements."""
    path = BASE / page
    if not path.exists():
        return
    html = path.read_text(encoding='utf-8')
    
    # Early return for special pages
    if 'thank-you' in page or '404' in page or 'code' in page:
        html = ensure_viewport(html, page)
        # Only add essential elements for these pages
        if '<link rel="icon"' not in html and ICONS.strip() not in html:
            html = html.replace('</head>', ICONS + '</head>', 1)
        path.write_text(html, encoding='utf-8')
        print(f"Updated {page}")
        return
    
    lang = get_lang(html)
    loc = LOC.get(lang, LOC['en'])
    
    # Apply transformations in order
    html = remove_favicons(html)
    if ICONS.strip() not in html:
        html = html.replace('</head>', ICONS + '</head>', 1)
    html = ensure_viewport(html, page)
    html = add_css_js(html)
    html = replace_tailwind(html)
    html = replace_tripadvisor_block(html, loc)
    html = remove_bird_svg(html)
    html = fix_ta_cta(html)
    html = update_service_jsonld(html)
    html = add_form_ids(html)
    html = add_hamburger_attrs(html)
    html = fix_viewport(html)
    html = remove_testimonial_chevrons(html)
    html = remove_obsolete_scripts(html)
    html = add_noscript_css(html)
    html = process_floating_whatsapp(html)
    html = add_hero_actions(html)
    html = update_comments(html)
    
    path.write_text(html, encoding='utf-8')
    print(f"Updated {page}")

if __name__ == '__main__':
    for page in PAGES + ['thank-you.html', '404.html', 'code.html']:
        process_file(page)
