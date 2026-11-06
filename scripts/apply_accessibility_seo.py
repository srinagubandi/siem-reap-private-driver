#!/usr/bin/env python3
"""Apply scoped accessibility and locale SEO fixes; no network or dependencies."""
from pathlib import Path
from html import escape, unescape
import re
import json

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://angkordrivers.com'
LANGS = ['en','fr','zh','ko','ja','vi','th','de','es','it','pt','ru','nl','pl','ar','id','sv','cs']
LABELS = json.loads((ROOT/'ai/ui-labels.json').read_text())
CODES = {lang:('zh-Hans' if lang=='zh' else lang) for lang in LANGS}
LOCALES = dict(zip(LANGS,['en_GB','fr_FR','zh_CN','ko_KR','ja_JP','vi_VN','th_TH','de_DE','es_ES','it_IT','pt_PT','ru_RU','nl_NL','pl_PL','ar_SA','id_ID','sv_SE','cs_CZ']))
URLS = {lang:ORIGIN+('/' if lang=='en' else '/'+lang+'.html') for lang in LANGS}

def attrs(tag):
    return {k.lower():unescape(v) for k,_,v in re.findall(r'([\w:-]+)\s*=\s*([\"\'])(.*?)\2',tag,re.S)}

def add_attrs(tag, additions):
    current = attrs(tag)
    for key,value in additions.items():
        if key not in current:
            tag = tag[:-1]+' '+key+'="'+escape(value,quote=True)+'">'
    return tag

def meta(head, key, value, attribute='name'):
    found = False
    def replace(m):
        nonlocal found
        if attrs(m.group()).get(attribute)==key:
            if found: return ''
            found=True
            return f'<meta {attribute}="{key}" content="{escape(value,quote=True)}">'
        return m.group()
    head = re.sub(r'<meta\b[^>]*>',replace,head,flags=re.I)
    if not found: head += f'\n<meta {attribute}="{key}" content="{escape(value,quote=True)}">\n'
    return head

alternates = '\n'.join(f'<link rel="alternate" hreflang="{CODES[lang]}" href="{URLS[lang]}">' for lang in LANGS)+'\n'+f'<link rel="alternate" hreflang="x-default" href="{URLS["en"]}">'
for lang in LANGS:
    path = ROOT/('index.html' if lang=='en' else lang+'.html')
    text = path.read_text()
    labels = LABELS[lang]
    text = re.sub(r'<main\b[^>]*>',lambda m:add_attrs(m.group(),{'id':'main-content','tabindex':'-1'}),text,count=1)
    if not re.search(r'<a\b[^>]*class=[\"\'][^\"\']*skip-link',text):
        text = re.sub(r'<body\b[^>]*>',lambda m:m.group()+'\n<a class="skip-link" href="#main-content">'+escape(labels['skip'])+'</a>',text,count=1)
    text = re.sub(r'<div\b[^>]*\bid=[\"\']langBar[\"\'][^>]*>',lambda m:add_attrs(m.group(),{'role':'navigation','aria-label':labels['language_nav']}),text)
    text = re.sub(r'<div\b[^>]*\bid=[\"\']mobile-book-bar[\"\'][^>]*>',lambda m:add_attrs(m.group(),{'role':'region','aria-label':labels['booking']}),text)
    if 'quick-contact-landmark' not in text:
        text = re.sub(r'<a\b(?=[^>]*\bclass=[\"\'][^\"\']*floating-whatsapp)[^>]*>.*?</a>',lambda m:'<aside class="quick-contact-landmark" aria-label="'+escape(labels['quick_contact'],quote=True)+'">'+m.group()+'</aside>',text,flags=re.S)
    text = re.sub(r'<span\b(?=[^>]*\bclass=[\"\'][^\"\']*material-symbols-outlined)[^>]*>',lambda m:add_attrs(m.group(),{'aria-hidden':'true'}),text)
    text = re.sub(r'<svg\b[^>]*>',lambda m:add_attrs(m.group(),{'aria-hidden':'true','focusable':'false'}),text)
    text = re.sub(r'<(/?)h4\b',r'<\1h3',text)
    footer = re.search(r'<footer\b.*?</footer>',text,re.S)
    if footer and 'href="/ai/"' not in footer.group():
        old=footer.group();new=re.sub(r'(<div class="flex gap-8">)',lambda m:m.group()+'\n<a class="text-stone-500 hover:text-emerald-700 transition-colors duration-300" href="/ai/" lang="'+CODES[lang]+'">'+escape(labels['ai_link'])+'</a>',old,count=1)
        assert new!=old, 'Footer insertion target missing: '+lang
        text=text.replace(old,new,1)
    match = re.search(r'(<head\b[^>]*>)(.*?)(</head>)',text,re.S|re.I)
    assert match
    head=match.group(2)
    title=unescape(re.search(r'<title>(.*?)</title>',head,re.S).group(1)).strip()
    descriptions=[attrs(m.group()).get('content','') for m in re.finditer(r'<meta\b[^>]*>',head) if attrs(m.group()).get('name')=='description']
    assert len(descriptions)>=1 and descriptions[0], 'Missing localized description: '+lang
    description=descriptions[0]
    h1=re.search(r'<h1\b[^>]*>(.*?)</h1>',text,re.S)
    service_type=' '.join(unescape(re.sub(r'<[^>]+>',' ',h1.group(1))).split())
    head=re.sub(r'<link\b[^>]*>',lambda m:'' if 'hreflang' in attrs(m.group()) or attrs(m.group()).get('rel')=='canonical' else m.group(),head)
    seen=set()
    def dedup_css(m):
        a=attrs(m.group())
        if a.get('rel')=='stylesheet':
            if a.get('href') in seen:return ''
            seen.add(a.get('href'))
        return m.group()
    head=re.sub(r'<link\b[^>]*>',dedup_css,head)
    if '/assets/css/accessibility-seo-fixes.css' not in head:head+='\n<link rel="stylesheet" href="/assets/css/accessibility-seo-fixes.css">\n'
    if 'rel="describedby"' not in head:head+='\n<link rel="describedby" href="/llms.txt">\n'
    head=meta(head,'description',description)
    for key,value in [('og:title',title),('og:description',description),('og:url',URLS[lang]),('og:locale',LOCALES[lang])]:head=meta(head,key,value,'property')
    for key,value in [('twitter:title',title),('twitter:description',description),('twitter:url',URLS[lang])]:head=meta(head,key,value)
    def schema_fix(m):
        obj=json.loads(m.group(2))
        if obj.get('@type')=='Service':
            obj.pop('offers',None)
            obj.update(name=title,description=description,serviceType=service_type,url=URLS[lang])
        elif obj.get('@type')=='WebPage':
            obj.update(name=title,description=description,url=URLS[lang],inLanguage=CODES[lang])
        return m.group(1)+json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+m.group(3)
    head=re.sub(r'(<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>)(.*?)(</script>)',schema_fix,head,flags=re.S)
    marker='id="locale-webpage-schema"'
    if marker not in head:
        webpage={'@context':'https://schema.org','@type':'WebPage','name':title,'description':description,'url':URLS[lang],'inLanguage':CODES[lang]}
        head+='\n<script type="application/ld+json" '+marker+'>'+json.dumps(webpage,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>\n'
    head=head.rstrip()+'\n<link rel="canonical" href="'+URLS[lang]+'">\n'+alternates+'\n'
    head=re.sub(r'\n[ \t]*\n+', '\n', head)
    text=text[:match.start(2)]+head+text[match.end(2):]
    path.write_text(text)

for name in ['code.html','thank-you.html','404.html']:
    p=ROOT/name
    if not p.exists():continue
    text=p.read_text();m=re.search(r'(<head\b[^>]*>)(.*?)(</head>)',text,re.S|re.I)
    if m:text=text[:m.start(2)]+meta(m.group(2),'robots','noindex, follow')+text[m.end(2):]
    p.write_text(text)
urls=list(URLS.values())+[ORIGIN+'/ai/',ORIGIN+'/faq/']
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
xml+=''.join('  <url><loc>'+u+'</loc><lastmod>2026-11-06</lastmod></url>\n' for u in urls)
xml+='</urlset>\n'
(ROOT/'sitemap.xml').write_text(xml)
print('Applied localized accessibility labels and SEO metadata on 18 pages; wrote a 20-route sitemap.')
