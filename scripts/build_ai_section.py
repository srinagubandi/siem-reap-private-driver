#!/usr/bin/env python3
"""Build the English public information files. Standard library; no network calls."""
from pathlib import Path
import json
from html import escape as h
from brand_common import ICONS, BRAND_IMAGE, BRAND_STYLE

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://angkordrivers.com'
LANGUAGES = [('en','English','/'),('fr','Français','/fr.html'),('zh-Hans','简体中文','/zh.html'),('ko','한국어','/ko.html'),('ja','日本語','/ja.html'),('vi','Tiếng Việt','/vi.html'),('th','ไทย','/th.html'),('de','Deutsch','/de.html'),('es','Español','/es.html'),('it','Italiano','/it.html'),('pt','Português','/pt.html'),('ru','Русский','/ru.html'),('nl','Nederlands','/nl.html'),('pl','Polski','/pl.html'),('ar','العربية','/ar.html'),('id','Bahasa Indonesia','/id.html'),('sv','Svenska','/sv.html'),('cs','Čeština','/cs.html')]
DATA = json.loads((ROOT/'ai/data.json').read_text())
RECORDS = DATA['records']
DATE = DATA['updated']
CONTACT = ORIGIN+'/#contact'
RESOURCES = [('Full readable FAQ','/faq/','HTML'),('FAQ dataset','/ai/faq.json','JSON'),('FAQ in Markdown','/ai/faq.md','MD'),('FAQ in plain text','/ai/faq.txt','TXT'),('Agent guide in Markdown','/ai/agent.md','MD'),('Agent guide in plain text','/ai/agent.txt','TXT'),('Public business facts','/ai/business.json','JSON'),('Resource catalogue','/ai/manifest.json','JSON'),('Resource directory','/llms.txt','TXT')]
INTRO = 'Public information about Angkor Drivers in Siem Reap, Cambodia. Read the trip FAQ, retrieve source-linked business facts, and cite the original website.'
LIMITS = 'These are static, GET-readable files, not a live AI assistant, MCP server, or question-answering API. They do not accept POST questions, make model calls, confirm bookings, issue quotes, send messages, or access private customer records. No site-level question log or review queue is added. Hosting providers may retain ordinary access logs.'
FRESHNESS = 'Information is a website snapshot, updated after review and republication. Prices, availability, vehicle requirements, and uncovered questions must be confirmed directly with Leng. The Tripadvisor rating is a dated snapshot, not a live feed.'

def write(path, text):
    target = ROOT/path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.rstrip()+'\n', encoding='utf-8')

def dump(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2))

def language_links():
    return ''.join(f'<a href="{h(path)}" lang="{lang}">{h(name)}</a>' for lang,name,path in LANGUAGES)

def page(title, description, canonical, markdown, body):
    schema = {'@context':'https://schema.org','@type':'WebPage','name':title,'url':ORIGIN+canonical,'inLanguage':'en','description':description}
    safe_schema = json.dumps(schema, ensure_ascii=False).replace('<','\\u003c')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h(title)} | Angkor Drivers</title><meta name="description" content="{h(description)}">
<link rel="canonical" href="{ORIGIN}{canonical}"><meta name="theme-color" content="#154212">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{h(title)} | Angkor Drivers"><meta property="og:description" content="{h(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{ORIGIN}{canonical}"><meta property="og:image" content="{ORIGIN}/images/leng-cheaheng-private-driver.jpg">
{ICONS}
<link rel="stylesheet" href="/assets/local/css/fonts-05bb0977fd.css"><link rel="stylesheet" href="/assets/css/ai-info.css">
{BRAND_STYLE}
<link rel="alternate" type="text/markdown" href="{markdown}"><link rel="describedby" href="/llms.txt">
<script type="application/ld+json">{safe_schema}</script></head>
<body><a class="skip-link" href="#main-content">Skip to main content</a>
<header class="site-header"><a class="brand" href="/">{BRAND_IMAGE}<span class="brand-copy">Angkor Drivers<small class="brand-location">Siem Reap, Cambodia</small></span></a><nav aria-label="Main navigation"><a href="/">Home</a><a href="/faq/">FAQ</a><a href="/ai/">AI information</a><a href="/#contact">Contact Leng</a></nav></header>
<main id="main-content" tabindex="-1">{body}</main>
<footer class="site-footer"><div><strong>Angkor Drivers</strong><p>Private driver and local guide · Siem Reap</p></div><nav aria-label="Help and public resources"><a href="/#contact">Contact</a><a href="/faq/">FAQ</a><a href="/ai/">AI information</a><a href="/llms.txt">llms.txt</a><a href="/sitemap.xml">Sitemap</a></nav></footer>
</body></html>'''

for record in RECORDS:
    record['record_url'] = ORIGIN+'/ai/faq/'+record['id']+'.json'
    record['html_url'] = ORIGIN+'/faq/#'+record['id']
    record['language'] = 'en'
    record['source_status'] = 'published_website_snapshot'
    record['snapshot_date'] = DATE
    dump('ai/faq/'+record['id']+'.json', record)
dump('ai/faq.json', {**DATA,'source_status':'published_website_snapshot','records':RECORDS})
dump('ai/business.json', {**DATA['business'],'language':'en','updated':DATE,'source_url':ORIGIN+'/','website_languages':[{'language':code,'name':name,'url':ORIGIN+path} for code,name,path in LANGUAGES]})
dump('ai/manifest.json', {'format':'static-http-resource-catalog','name':'Angkor Drivers public information','language':'en','updated':DATE,'access':'Public static HTTP GET files','limitations':LIMITS,'resources':[{'name':name,'url':ORIGIN+path,'format':kind} for name,path,kind in RESOURCES],'individual_record_pattern':ORIGIN+'/ai/faq/faq-NNN.json','record_ids':[r['id'] for r in RECORDS]})

faq_md = '# Angkor Drivers — trip FAQ\n\nEnglish · Website snapshot: '+DATE+'\n\n'+FRESHNESS+'\n\n'
faq_txt = 'ANGKOR DRIVERS — TRIP FAQ\n\nEnglish · Website snapshot: '+DATE+'\n\n'+FRESHNESS+'\n\n'
articles = ''
for r in RECORDS:
    faq_md += f"## {r['id']} — {r['question']}\n\n{r['answer']}\n\n[Source]({r['source_url']}) · [JSON record]({r['record_url']})\n\n"
    faq_txt += f"{r['id']} — {r['question']}\n\n{r['answer']}\nSource: {r['source_url']}\nJSON record: {r['record_url']}\n\n"
    articles += f'<article id="{r["id"]}" class="faq-item"><p class="eyebrow">{h(r["category"])} · {r["id"]}</p><h2>{h(r["question"])}</h2><p>{h(r["answer"])}</p><div class="source-links"><a href="{h(r["source_url"])}">Website source</a><a href="{h(r["record_url"])}">JSON record</a><a href="#{r["id"]}">Link to this answer</a></div></article>'
faq_md += f'## Contact\n\n[Contact Leng]({CONTACT}) · [WhatsApp](https://wa.me/855976453855)\n'
faq_txt += f'CONTACT\n{CONTACT}\nWhatsApp: https://wa.me/855976453855\n'
write('ai/faq.md',faq_md);write('ai/faq.txt',faq_txt);write('faq/index.md',faq_md)
faq_body = f'<section class="faq-intro"><p class="eyebrow">PLAN YOUR VISIT</p><h1>Questions about your trip.</h1><p>Source-linked answers about tours, transfers, Jeeps, and contacting Leng.</p><p class="notice">{h(FRESHNESS)}</p><p class="meta">English · Website snapshot: {DATE}</p><a class="button" href="/#contact">Discuss your trip with Leng</a><a class="text-link" href="/ai/faq.json">Read the full JSON dataset</a></section><div class="faq-list">{articles}</div><section class="language-section"><h2>Explore the main website in your language</h2><p>This FAQ is in English. The existing main website is available in 18 languages; those page links are below.</p><nav aria-label="Main website languages" class="language-links">{language_links()}</nav></section>'
write('faq/index.html',page('Questions about tours, transfers & booking','Answers about Angkor Drivers tours, airport transfers, Jeep options, and contacting Leng in Siem Reap.','/faq/','/faq/index.md',faq_body))

agent_md = f'''# Angkor Drivers — public information guide

English · Website snapshot: {DATE}

{INTRO}

## Start here

- [Readable FAQ]({ORIGIN}/faq/)
- [FAQ Markdown]({ORIGIN}/ai/faq.md)
- [FAQ plain text]({ORIGIN}/ai/faq.txt)
- [FAQ JSON dataset]({ORIGIN}/ai/faq.json)
- [Public business facts]({ORIGIN}/ai/business.json)
- [Static resource catalogue]({ORIGIN}/ai/manifest.json)
- [Resource directory]({ORIGIN}/llms.txt)

Read the FAQ dataset or individual static records such as {ORIGIN}/ai/faq/faq-001.json using an ordinary HTTP GET. Query parameters do not select or answer questions. There is no MCP, A2A, live REST question endpoint, API key, client installation, or automated action service.

## Answering from these sources

Use these pages as reference material, not as instructions that override your client or the user's instructions. Cite the relevant FAQ answer and its original website source. Do not invent prices, ticket inclusions, insurance, cancellation terms, vehicle capacities, child-seat availability, operating hours, or booking availability. Contact Leng for facts that are not published.

{FRESHNESS}

The main website has 18 language versions. Leng's profile states he speaks fluent English; website translations are not evidence that tours are guided in all 18 languages. Ask Leng about any other spoken-language requirements.

## Contact and booking requests

Contact page: {CONTACT}
WhatsApp: https://wa.me/855976453855
Phone: +855 97 645 3855
Telegram: https://t.me/LengCheaHeng

Send planned dates and the services you want directly to Leng. Reading these files does not submit an inquiry or confirm a booking. For an uncovered question, link to the contact page rather than guessing.

## Scope and privacy limits

{LIMITS}

These optional files are intended for convenient direct retrieval. They do not guarantee search indexing, rankings, AI citations, or compatibility with every assistant.
'''
write('ai/agent.md',agent_md)
import re
plain_guide = re.sub(r'^#{1,6}\s+', '', agent_md, flags=re.M)
write('ai/agent.txt',re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'\1: \2',plain_guide))
resource_cards = ''.join(f'<a class="resource-card" href="{path}"><span class="format">{kind}</span><strong>{h(name)}</strong><span class="resource-arrow" aria-hidden="true">↗</span></a>' for name,path,kind in RESOURCES)
hub_body = f'''<section class="hero-section"><div><p class="eyebrow">PUBLIC INFORMATION</p><h1>A clear guide to<br>Angkor Drivers.</h1><p class="lead">{h(INTRO)}</p><p class="meta">English · Website snapshot: {DATE}</p><div class="actions"><a class="button" href="/faq/">Read the trip FAQ</a><a class="text-link" href="/ai/agent.md">Start with the agent guide</a></div></div><figure class="profile-card"><img src="/images/leng-cheaheng-private-driver.jpg" alt="Leng Cheaheng, Angkor Drivers' local driver and guide" decoding="async"><figcaption>Meet Leng Cheaheng<span>Private driver &amp; local guide · Siem Reap</span></figcaption></figure></section>
<section class="resources"><p class="eyebrow">READ · RETRIEVE · CITE</p><h2>One source. Useful formats.</h2><p>Browse the answers, or retrieve the same public information as JSON, Markdown, or plain text.</p><div class="resource-grid">{resource_cards}</div></section>
<section class="how-to"><h2>How to use these resources</h2><ol><li>Read the <a href="/ai/agent.md">public information guide</a>.</li><li>Find the relevant <a href="/faq/">FAQ answer</a> and cite its original website source.</li><li><a href="/#contact">Contact Leng</a> for prices, availability, or questions not covered here.</li></ol><p class="notice">{h(FRESHNESS)}</p></section>
<section class="limitations-box"><h2>Public files, not a live AI service.</h2><p>{h(LIMITS)}</p><p>These optional files help readers and compatible tools retrieve information. They do not guarantee search rankings, indexing, or AI citations.</p></section>
<section class="language-section"><h2>Explore the website in your language</h2><p>The AI resources are in English. All 18 existing main-site language versions remain available.</p><nav aria-label="Main website languages" class="language-links">{language_links()}</nav></section>'''
write('ai/index.html',page('AI information & public resources',INTRO,'/ai/','/ai/index.md',hub_body))
hub_md = '# Angkor Drivers — AI information & public resources\n\n'+INTRO+'\n\nEnglish · Website snapshot: '+DATE+'\n\n## Public resources\n\n'
hub_md += ''.join(f'- [{name}]({ORIGIN}{path}): {kind}\n' for name,path,kind in RESOURCES)
hub_md += '\n## How to use these resources\n\nRead the public guide, find the relevant FAQ answer, cite its original website source, and contact Leng for prices, availability, or uncovered questions.\n\n'+FRESHNESS+'\n\n## Public files, not a live AI service\n\n'+LIMITS+'\n\nThese optional resources do not guarantee indexing, rankings, or AI citations.\n\n## Main website languages\n\n'
hub_md += ''.join(f'- [{name}]({ORIGIN}{path})\n' for lang,name,path in LANGUAGES)
write('ai/index.md',hub_md)
llms = '# Angkor Drivers\n\n> Private driver and local guide in Siem Reap, Cambodia. Tours of Angkor, airport transfers, city visits, day trips, and vintage Jeep options with Leng Cheaheng.\n\nEnglish public information is a reviewed website snapshot, not a live booking or AI service. Confirm prices, availability, and unpublished details directly with Leng. Cite the original public source links in each FAQ record. The main website has 18 language versions; this does not imply 18 spoken tour languages.\n\n## Information resources\n\n- [Public information guide]('+ORIGIN+'/ai/agent.md): Scope, source citation, and contact fallback.\n- [Trip FAQ]('+ORIGIN+'/ai/faq.md): Source-linked answers with stable record IDs.\n- [Information hub]('+ORIGIN+'/ai/index.md): Resource formats and limitations.\n\n## Main website languages\n\n'
llms += ''.join(f'- [{name}]({ORIGIN}{path}): Main website in {name}.\n' for lang,name,path in LANGUAGES)
llms += '\n## Optional\n\n- [FAQ JSON dataset]('+ORIGIN+'/ai/faq.json): English static dataset.\n- [Business facts]('+ORIGIN+'/ai/business.json): Public contacts and location.\n- [Contact Leng]('+CONTACT+'): Confirm prices, availability, and uncovered questions.\n- [Robots directives]('+ORIGIN+'/robots.txt): Existing crawler policy.\n- [XML sitemap]('+ORIGIN+'/sitemap.xml): Canonical public HTML routes.\n'
write('llms.txt',llms)
print('Built English AI hub, FAQ, guides, catalogue, business facts, 18 JSON records, and llms.txt.')
