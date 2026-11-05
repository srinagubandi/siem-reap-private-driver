#!/usr/bin/env python3
import re, html as html_lib
from pathlib import Path

FAMILY_SRC='/images/guest-family-airport-departures.jpg'
VAN_SRC='/images/private-van-angkor-gate.jpg'
PROFILE_SRC='/images/leng-cheaheng-private-driver.jpg'
OLD_PROFILE_SRC='/assets/local/images/e94e002bd1ea.jpeg'
CSS_HREF='/assets/css/guest-vehicle-photos.css'

PAGES = {'index.html': ('Guest family with their driver at international departures', 'Private van parked beside an Angkor temple gate'), 'fr.html': ('Famille invitée avec son chauffeur aux départs internationaux', 'Van privé garé près d’une porte de temple d’Angkor'), 'zh.html': ('客人家庭与国际出发区的司机', '私人面包车停在吴哥寺庙大门旁'), 'ko.html': ('국제선 출발 구역에서 기사님과 함께한 게스트 가족', '앙코르 사원 문 옆에 주차된 전용 밴'), 'ja.html': ('国際線出発ロビーでドライバーと一緒のゲスト家族', 'アンコール寺院の門のそばに駐車したプライベートバン'), 'vi.html': ('Gia đình khách cùng tài xế tại khu vực khởi hành quốc tế', 'Xe van riêng đỗ cạnh cổng đền Angkor'), 'th.html': ('ครอบครัวผู้เข้าพักพร้อมคนขับที่อาคารผู้โดยสารขาออกระหว่างประเทศ', 'รถตู้ส่วนตัวจอดใกล้ประตูโบราณในอังกอร์'), 'de.html': ('Gästefamilie mit ihrem Fahrer am internationalen Abflug', 'Privater Van neben einem Angkor-Tempelportal geparkt'), 'es.html': ('Familia huésped con su conductor en salidas internacionales', 'Van privado aparcado junto a una puerta de templo de Angkor'), 'it.html': ('Famiglia ospite con il proprio autista alle partenze internazionali', 'Van privato parcheggiato accanto a una porta del tempio di Angkor'), 'pt.html': ('Família hóspede com seu motorista nas partidas internacionais', 'Van privado estacionado ao lado de um portão de templo de Angkor'), 'ru.html': ('Семья гостей с водителем в зоне международных вылетов', 'Частный минивэн припаркован у ворот ангкорского храма'), 'nl.html': ('Gastgezin met hun chauffeur bij internationale vertrekhal', 'Privébus geparkeerd naast een Angkortempelpoort'), 'pl.html': ('Rodzina gości z kierowcą przy międzynarodowych odlotach', 'Prywatny van zaparkowany obok bramy świątyni Angkor'), 'ar.html': ('عائلة ضيفة مع سائقها في صالة المغادرة الدولية', 'فان خاص متوقف بجانب بوابة معبد أنغكور'), 'id.html': ('Keluarga tamu bersama sopir mereka di area keberangkatan internasional', 'Van pribadi terparkir di samping gerbang kuil Angkor'), 'sv.html': ('Gästfamilj med förare vid internationella avfärden', 'Privat minibuss parkerad intill en tempelport i Angkor'), 'cs.html': ('Rodina hostů s řidičem v oblasti mezinárodního odletu', 'Soukromý minibus zaparkovaný vedle brány chrámu Angkor')}

def matching_end(s, start, tag):
    depth=0
    i=start
    ot=f'<{tag}'
    ct=f'</{tag}'
    while i < len(s):
        if s.startswith('<!--', i):
            end=s.find('-->', i)
            i = end+3 if end!=-1 else i+1
            continue
        if s[i:i+len(ot)].lower() == ot:
            nxt=s[i+len(ot):i+len(ot)+1]
            if nxt == '' or nxt.isspace() or nxt == '>':
                depth += 1
                i += len(ot)
                continue
        if s[i:i+len(ct)].lower() == ct:
            if s[i+len(ct):i+len(ct)+1] == '>':
                depth -= 1
                if depth == 0:
                    return s.find('>', i)+1
                i += len(ct)
                continue
        i += 1
    return len(s)

def iter_sections(html):
    for m in re.finditer(r'<section\b[^>]*>', html, re.I):
        st=m.start()
        en=matching_end(html, st, 'section')
        yield st, en, html[st:en]

def find_by_id(html, wanted):
    pat = re.compile(r'\bid\s*=\s*[\x22\x27]?' + re.escape(wanted) + r'[\x22\x27]?(?=\s|/?>)', re.I)
    for st, en, s in iter_sections(html):
        opening_end=s.find('>')+1
        if pat.search(s[:opening_end]):
            return st, en, s
    return None

def find_by_needle(html, needle):
    for st, en, s in iter_sections(html):
        if needle in s:
            return st, en, s
    return None

def add_css(html):
    if CSS_HREF in html:
        return html
    link = f'''\n<link rel='stylesheet' href='{CSS_HREF}'>'''
    return re.sub(r'</head\s*>', lambda m: link + m.group(0), html, count=1, flags=re.I)

def add_section_id_if_missing(s):
    opening_end=s.find('>')+1
    opening=s[:opening_end]
    if re.search(r'\bid\s*=', opening, re.I):
        return s
    return re.sub(r'<section\b', '<section id=\'guest-gallery\'', s, count=1)

def update_gallery(html, alt):
    if 'id=\'guest-family-photo\'' in html:
        return html
    found = find_by_needle(html, 'jeep-two-forest.jpg')
    if not found:
        return html
    st, en, s = found
    g = re.search(r'<div\b[^>]*\bgrid-cols-2\b[^>]*\bmd:grid-cols-3\b[^>]*>', s, re.I)
    if not g:
        return html
    figure = f'''<!-- guest-gallery-family-photo (idempotent marker) -->
<figure class='guest-featured-photo' id='guest-family-photo'>
  <img src='{FAMILY_SRC}' alt='{html_lib.escape(alt)}' width='1600' height='1200' loading='lazy' decoding='async'>
</figure>
'''
    s = s[:g.start()] + figure + s[g.start():]
    s = add_section_id_if_missing(s)
    return html[:st] + s + html[en:]

def update_tours(html, alt):
    if 'id=\'guest-van-angkor-photo\'' in html:
        return html
    found = find_by_id(html, 'tours')
    if not found:
        return html
    st, en, s = found
    g = re.search(r'<div\b[^>]*\bgrid-cols-1\b[^>]*\bmd:grid-cols-3\b[^>]*>', s, re.I)
    if not g:
        return html
    end_grid = matching_end(s, g.start(), 'div')
    h3s = re.findall(r'<h3\b[^>]*>(.*?)</h3>', s, re.I|re.S)
    caption = ''
    if len(h3s) >= 2:
        caption = re.sub(r'<[^>]+>', '', h3s[1]).strip()
    caption = html_lib.escape(html_lib.unescape(caption) or 'Airport Transfers')
    figure = f'''<!-- guest-van-angkor-photo (idempotent marker) -->
<figure class='guest-van-photo' id='guest-van-angkor-photo'>
  <img src='{VAN_SRC}' alt='{html_lib.escape(alt)}' width='960' height='1280' loading='lazy' decoding='async'>
  <figcaption>{caption}</figcaption>
</figure>
'''
    s = s[:end_grid] + figure + s[end_grid:]
    return html[:st] + s + html[en:]

def update_about(html):
    if PROFILE_SRC in html:
        return html
    found = find_by_id(html, 'about')
    if not found:
        return html
    st, en, s = found
    old = re.search(r'<img\b(?=[^>]*\bsrc=[\x22\x27]' + re.escape(OLD_PROFILE_SRC) + r'[\x22\x27])[^>]*>', s, re.I)
    if not old:
        return html
    old_tag = old.group(0)
    alt_m = re.search(r'alt=[\x22\x27]([^\x22\x27]*)[\x22\x27]', old_tag, re.I)
    alt_raw = alt_m.group(1).strip() if alt_m and alt_m.group(1).strip() else 'Leng Chea Heng with his Hyundai H1 minivan'
    alt = html_lib.escape(html_lib.unescape(alt_raw))
    new_img = f'''<img alt='{alt}' class='profile-photo-original w-full h-auto' src='{PROFILE_SRC}' width='1195' height='896' loading='lazy' decoding='async'>'''
    s = s[:old.start()] + new_img + s[old.end():]
    s = s.replace('<!-- Real photo: Leng Chea Heng with his Hyundai H1 minivan on the Angkor road -->',
                  '<!-- Original photo: Leng Chea Heng with his Hyundai H1 minivan -->')
    return html[:st] + s + html[en:]

def process_page(path, alts):
    html = Path(path).read_text(encoding='utf-8')
    html = add_css(html)
    html = update_gallery(html, alts[0])
    html = update_tours(html, alts[1])
    html = update_about(html)
    Path(path).write_text(html, encoding='utf-8')

if __name__ == '__main__':
    for page, alts in PAGES.items():
        p = Path(page)
        if p.exists():
            process_page(page, alts)
            print('updated', page)
        else:
            print('missing', page)
