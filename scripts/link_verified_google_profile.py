"""Expose only the verified Google Maps profile, not invented Google reviews.

Business identity was checked against its website, phone and address. This
static migration needs no Maps API, iframe, Elfsight, server or runtime key.
"""
from pathlib import Path
from html import escape
import re
import json

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/google-business-profile.json').read_text())
LABELS=json.loads((ROOT/'data/google-profile-ui-labels.json').read_text())


def process(text,labels):
    url=escape(DATA['profile_url'],quote=True)
    # Stable replacement marker makes rebuilding a no-op once integrated.
    if 'id="google-business-profile"' not in text:
        old=re.search(r'<!-- Google Reviews — powered by Elfsight -->.*?(?=<!-- TripAdvisor Reviews -->)',text,re.S)
        if old:
            logo=re.search(r'<svg\b.*?</svg>',old.group(),re.S)
            icon=logo.group() if logo else ''
            new=f'''<!-- Verified Google business profile: static external link, no review feed -->
<div id="google-business-profile" class="mb-16">
<div class="flex items-center gap-3 mb-6">{icon}<h3 class="font-serif text-xl text-primary">{escape(labels['google_heading'])}</h3></div>
<div class="bg-white rounded-2xl shadow-sm border border-outline-variant p-10">
<p class="text-lg font-bold text-primary" lang="en">Angkor Driver</p>
<p class="text-on-surface-variant mt-2">{escape(labels['google_note'])}</p>
<a class="ta-review-link" href="{url}" target="_blank" rel="noopener noreferrer">{escape(labels['google_link'])}</a>
</div></div>
'''
            text=text[:old.start()]+new+text[old.end():]
    # A profile link is not a direct write-review form. Relabel the previous
    # broken call to action truthfully; users can choose Write a review there.
    pattern=r'<a\b[^>]*href="https://g\.page/r/REPLACE_WITH_GOOGLE_REVIEW_LINK/review"[^>]*>.*?</a>'
    def cta(match):
        source=match.group();opening=source[:source.index('>')+1]
        opening=opening.replace('https://g.page/r/REPLACE_WITH_GOOGLE_REVIEW_LINK/review',url)
        logo=re.search(r'<svg\b.*?</svg>',source,re.S)
        return opening+(logo.group() if logo else '')+escape(labels['google_link'])+'</a>'
    return re.sub(pattern,cta,text,flags=re.S)


def main():
    for locale,labels in LABELS.items():
        path=ROOT/('index.html' if locale=='en' else locale+'.html')
        original=path.read_text();text=process(original,labels)
        assert 'REPLACE_WITH_GOOGLE_REVIEW_LINK' not in text
        assert 'elfsight.com/google-reviews-widget' not in text
        if text!=original:path.write_text(text)
        print('Linked verified Google profile:',path.name)
    legacy=ROOT/'code.html'
    if legacy.exists():
        original=legacy.read_text();text=process(original,LABELS['en'])
        if text!=original:legacy.write_text(text)

if __name__=='__main__':main()
