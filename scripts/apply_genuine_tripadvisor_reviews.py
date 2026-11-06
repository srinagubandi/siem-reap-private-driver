"""Build permission-cleared, source-attributed Tripadvisor cards as static HTML.

No production APIs, scraping jobs, third-party scripts, or automatic refresh.
Quoted reviews remain in their original English. Public handles are not expanded
into invented legal names. Source metadata and owner-confirmed permission are
versioned in data/tripadvisor-reviews.json and images/tripadvisor/SOURCES.json.
"""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/tripadvisor-reviews.json').read_text())
LABELS = json.loads((ROOT / 'data/tripadvisor-ui-labels.json').read_text())
LOCALES = ['en','fr','zh','ko','ja','vi','th','de','es','it','pt','ru','nl','pl','ar','id','sv','cs']


def section_span(text, section_id):
    """Find the complete section; current templates have no nested sections."""
    pattern = rf'<section\b[^>]*\bid=[\"\']{re.escape(section_id)}[\"\'][^>]*>.*?</section>'
    match = re.search(pattern, text, re.S)
    if not match:
        raise ValueError(f'Missing required section {section_id}')
    return match


def move_van(text, labels):
    """Move the existing figure once, not a copy, into the original photo column."""
    if 'id="profile-vehicle-media"' in text:
        return text
    van = re.search(r'<figure\b[^>]*\bid=[\"\']guest-van-angkor-photo[\"\'][^>]*>.*?</figure>', text, re.S)
    if not van:
        raise ValueError('Missing original van figure')
    figure = re.sub(r'<figcaption>.*?</figcaption>', lambda _: '<figcaption>'+escape(labels['van_caption'])+'</figcaption>', van.group(), flags=re.S)
    text = text[:van.start()] + text[van.end():]
    text = re.sub(r'<!--\s*guest-van-angkor-photo\s*\(idempotent marker\)\s*-->','',text)
    about = section_span(text, 'about')
    original = about.group()
    photo = re.search(r'<div class="rounded-2xl overflow-hidden shadow-2xl">\s*(?:<!--.*?-->\s*)?<img\b[^>]*\bprofile-photo-original\b[^>]*>\s*</div>', original, re.S)
    if not photo:
        raise ValueError('Missing original profile-photo wrapper')
    replacement = '<div class="profile-vehicle-media" id="profile-vehicle-media">\n'+photo.group()+'\n'+figure+'\n</div>'
    updated = original[:photo.start()]+replacement+original[photo.end():]
    return text[:about.start()]+updated+text[about.end():]


def review_card(review, labels):
    """Every displayed rating, name, date, quote and permalink has a source."""
    url=escape(review['url'],quote=True)
    name=escape(review['display_name'])
    # Avatar is the exact source profile image, including default landscape
    # avatars chosen by Tripadvisor; it is not claimed to be a portrait.
    avatar='<img class="ta-review-avatar" src="'+escape(review['avatar_path'],quote=True)+'" width="100" height="100" alt="" loading="lazy" decoding="async">'
    location='<p class="ta-review-meta" lang="en" dir="ltr">'+escape(review['location'])+'</p>' if review['location'] else ''
    return f'''<article class="ta-review-card" data-review-id="{review['review_id']}">
<p class="ta-review-rating"><span aria-hidden="true">★★★★★</span> <span dir="ltr">5/5</span></p>
<blockquote lang="en" dir="ltr" cite="{url}"><p>“{escape(review['excerpt'])}”</p></blockquote>
<div class="ta-review-person">{avatar}<div class="ta-review-person-body">
<p class="ta-review-meta">{escape(labels['source'])}</p>
<p class="ta-review-name"><bdi>{name}</bdi></p>{location}
<p class="ta-review-meta">{escape(labels['written'])} <time datetime="{review['review_date']}" dir="ltr">{review['review_date']}</time></p>
</div></div>
<a class="ta-review-link" href="{url}" target="_blank" rel="noopener noreferrer">{escape(labels['read_review'])}<span class="sr-only"> — <bdi>{name}</bdi></span></a>
</article>'''


def replace_reviews(text, labels):
    if 'id="guest-reviews"' in text:
        return text
    marker = text.find('<!-- Testimonials -->')
    if marker < 0:
        raise ValueError('Missing original testimonial section marker')
    section = re.search(r'<section\b.*?</section>', text[marker:], re.S)
    if not section:
        raise ValueError('Missing testimonial section')
    a,b=marker+section.start(),marker+section.end()
    old=text[a:b]
    heading=re.search(r'<h2\b[^>]*>.*?</h2>',old,re.S).group()
    cards='\n'.join(review_card(r,labels) for r in DATA['reviews'] if r.get('featured'))
    listing=escape(DATA['listing_url'],quote=True)
    new=f'''<section class="py-24 bg-surface-container-low" id="guest-reviews">
<div class="max-w-7xl mx-auto px-6">
<div class="mb-16">{heading}<p class="text-on-surface-variant">{escape(labels['subtitle'])}</p></div>
<div class="ta-review-grid">{cards}</div>
<p class="ta-review-source-note"><a class="ta-review-link" href="{listing}" target="_blank" rel="noopener noreferrer">{escape(labels['all_reviews'])}</a></p>
<p class="ta-review-source-note">{escape(labels['tip_label'])}: <q lang="en" dir="ltr">Contact direct via WhatsApp</q> — <bdi>BigMac666</bdi></p>
</div></section>'''
    return text[:a]+new+text[b:]


def add_gallery(text, labels):
    if 'id="tripadvisor-traveler-photos"' in text:
        return text
    gallery=section_span(text,'guest-gallery')
    photos=[]
    for image in DATA['featured_photos']:
        photos.append(f'''<figure class="ta-traveler-photo">
<a href="{escape(image['source_page'],quote=True)}" target="_blank" rel="noopener noreferrer">
<img src="{escape(image['web_path'],quote=True)}" width="{image['web_dimensions'][0]}" height="{image['web_dimensions'][1]}" alt="{escape(image['alt'],quote=True)}" lang="en" loading="lazy" decoding="async"></a>
<figcaption>{escape(labels['photo_credit'])} <bdi>{escape(image['creator_display_name'])}</bdi> · <a class="ta-review-link" href="{escape(image['source_page'],quote=True)}" target="_blank" rel="noopener noreferrer">Tripadvisor</a></figcaption>
</figure>''')
    block='<div id="tripadvisor-traveler-photos" class="mt-12"><h3 class="text-2xl font-serif text-primary mb-6">'+escape(labels['photos_heading'])+'</h3><div class="ta-traveler-photo-grid">'+''.join(photos)+'</div></div>'
    original=gallery.group()
    last=original.rfind('</div>')
    updated=original[:last]+block+'\n'+original[last:]
    return text[:gallery.start()]+updated+text[gallery.end():]


def remove_decorative_contact_image(text):
    """This pointer-styled photo is not a working map or useful contact action.

    Remove only its two wrappers. Keep every real contact link, input, label,
    submit action and booking endpoint unchanged.
    """
    contact = section_span(text, 'contact')
    original = contact.group()
    pattern = r'<div class="pt-12">\s*<div class="w-full h-48 rounded-xl overflow-hidden opacity-50 grayscale hover:grayscale-0 transition-all cursor-pointer">\s*<img\b[^>]*>\s*</div>\s*</div>'
    updated = re.sub(pattern, '', original, count=1)
    return text[:contact.start()]+updated+text[contact.end():]


def main():
    assert DATA['permission']['confirmed_by_owner'] is True
    for locale in LOCALES:
        path=ROOT/('index.html' if locale=='en' else locale+'.html')
        original=path.read_text()
        text=move_van(original,LABELS[locale])
        text=replace_reviews(text,LABELS[locale])
        text=add_gallery(text,LABELS[locale])
        text=remove_decorative_contact_image(text)
        for href in ['/assets/css/profile-vehicle.css','/assets/css/tripadvisor-reviews.css']:
            if href not in text:
                text=text.replace('</head>','<link rel="stylesheet" href="'+href+'">\n</head>',1)
        assert text.count('id="guest-van-angkor-photo"')+text.count("id='guest-van-angkor-photo'")==1
        assert all(name not in text for name in ['Sarah &amp; James','David Chen','Elena Rodriguez'])
        if text!=original:path.write_text(text)
        print('Updated',path.name)

    # The ancillary design document is noindex but still publicly served.
    # Remove its unsupported testimonials too, without changing its legacy
    # photos, route policy, or unrelated layout.
    legacy = ROOT / 'code.html'
    if legacy.exists():
        original = legacy.read_text()
        text = replace_reviews(original, LABELS['en'])
        text = remove_decorative_contact_image(text)
        href = '/assets/css/tripadvisor-reviews.css'
        if href not in text:
            text = text.replace('</head>', '<link rel="stylesheet" href="'+href+'">\n</head>', 1)
        if text != original:
            legacy.write_text(text)

if __name__=='__main__':
    main()
