"""Apply the approved brand without rewriting page copy or inquiry controls."""
from pathlib import Path
import re
from brand_common import ICONS, BRAND_IMAGE, BRAND_STYLE

ROOT=Path(__file__).resolve().parents[1]
ICON_RELS={'icon','shortcut icon','apple-touch-icon','apple-touch-icon-precomposed','mask-icon','manifest'}


def update(text, path):
    # Only icon/config declarations are removed, preserving canonicals,
    # localized metadata, fonts, links, schema, and crawler policy verbatim.
    def links(match):
        tag=match.group();rel=re.search(r'\brel\s*=\s*[\"\']([^\"\']+)',tag,re.I)
        if rel and rel.group(1).lower() in ICON_RELS:return ''
        if 'assets/css/branding.css' in tag:return ''
        return tag
    text=re.sub(r'<link\b[^>]*>',links,text,flags=re.I)
    text=re.sub(r'<meta\b(?=[^>]*name=[\"\']msapplication-(?:config|TileColor|TileImage)[\"\'])[^>]*>','',text,flags=re.I)
    text=re.sub(r'<!-- Approved Option A: local, versioned browser and device icons\. -->\s*','',text)
    text=re.sub(r'<!--\s*=+\s*FAVICONS.*?=+\s*-->','',text,flags=re.S)
    if 'class="nav-logo"' in text:
        logo='<a href="/" class="nav-logo" dir="ltr">'+BRAND_IMAGE+'<span class="nav-wordmark"><span>Angkor</span> <span>Drivers</span></span></a>'
        text=re.sub(r'<a\b[^>]*class="nav-logo"[^>]*>.*?</a>',logo,text,flags=re.S)
    if path.as_posix() in {'ai/index.html','faq/index.html'}:
        brand='<a class="brand" href="/">'+BRAND_IMAGE+'<span class="brand-copy">Angkor Drivers<small class="brand-location">Siem Reap, Cambodia</small></span></a>'
        text=re.sub(r'<a\b[^>]*class="brand"[^>]*>.*?</a>',brand,text,flags=re.S)
    if path.name=='thank-you.html':
        text=re.sub(r'<a href="/" class="(?:flex items-center gap-3|brand-link)">.*?</a>',
                    '<a href="/" class="brand-link">'+BRAND_IMAGE+'<span class="font-serif text-lg font-bold text-primary">Angkor Drivers</span></a>',text,count=1,flags=re.S)
    if path.name=='404.html':
        text=re.sub(r'<a href="/" class="logo(?: brand-link)?">.*?</a>',
                    '<a href="/" class="logo brand-link">'+BRAND_IMAGE+'<span class="error-wordmark">Angkor Drivers</span></a>',text,count=1,flags=re.S)
    # This block is normalized at the end of head to keep stronger brand CSS
    # after old responsive layers; blank-line runs are kept stable on reruns.
    text=re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+','\n\n',text)
    text=re.sub(r'\s*</head>',lambda _: '\n'+ICONS+BRAND_STYLE+'\n</head>',text,count=1)
    return text


def main():
    pages=sorted(ROOT.glob('*.html'))+[ROOT/'ai/index.html',ROOT/'faq/index.html']
    for page in pages:
        rel=page.relative_to(ROOT);old=page.read_text();new=update(old,rel)
        if new!=old:page.write_text(new)
        print('Updated brand/icons:',rel)

if __name__=='__main__':main()
