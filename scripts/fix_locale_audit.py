from pathlib import Path
import re
import html

def main():
    root = Path(__file__).resolve().parent.parent
    pages = [
        'index.html', 'fr.html', 'zh.html', 'ko.html', 'ja.html',
        'vi.html', 'th.html', 'de.html', 'es.html', 'it.html',
        'pt.html', 'ru.html', 'nl.html', 'pl.html', 'ar.html',
        'id.html', 'sv.html', 'cs.html'
    ]
    targets = [root / p for p in pages]
    translations = {
        'ja': '市内観光', 'vi': 'Khám Phá Thành Phố', 'th': 'การสำรวจเมือง',
        'de': 'Stadterkundung', 'es': 'Descubrimiento de la Ciudad', 'it': 'Scoperta della Città',
        'pt': 'Descoberta da Cidade', 'ru': 'Знакомство с городом', 'nl': 'Stadsverkenning',
        'pl': 'Odkrywanie Miasta', 'ar': 'اكتشاف المدينة', 'id': 'Penjelajahan Kota',
        'sv': 'Stadsutforskning', 'cs': 'Objevování Města'
    }
    pattern = r'(<h3\b[^>]*>)City Discovery(</h3>)'
    css_link = '<link rel="stylesheet" href="/assets/css/locale-layout-fixes.css">'
    
    if not (root / 'assets/css/locale-layout-fixes.css').exists():
        raise FileNotFoundError('Styles file missing')
    
    for path in targets:
        if not path.exists():
            raise FileNotFoundError(f'Missing {path}')
        content = path.read_text(encoding='utf-8')
        lang = path.stem
        
        if lang in translations:
            match_count = len(re.findall(pattern, content))
            translated_heading = re.compile(r'<h3\b[^>]*>' + re.escape(html.escape(translations[lang])) + r'</h3>')
            if translated_heading.search(content):
                pass  # already translated
            elif match_count == 1:
                content = re.sub(pattern, lambda m: m.group(1) + html.escape(translations[lang]) + m.group(2), content, count=1)
            else:
                raise AssertionError(f'Unexpected match count or translation state in {path}')
        
        if css_link not in content:
            head_end = '</head>'
            content = content.replace(head_end, f'{css_link}\n{head_end}', 1)
        
        if '\x01' in content or '\x02' in content:
            raise ValueError(f'SOH/STX characters found in {path}')
        
        content = content.rstrip('\n') + '\n'
        path.write_text(content, encoding='utf-8')

if __name__ == '__main__':
    main()
