#!/usr/bin/env python3
"""Validate Angkor Drivers static site for production readiness."""
import os, re, json
from bs4 import BeautifulSoup
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [
    'index.html', 'fr.html', 'zh.html', 'ko.html', 'ja.html', 'vi.html',
    'th.html', 'de.html', 'es.html', 'it.html', 'pt.html', 'ru.html',
    'nl.html', 'pl.html', 'ar.html', 'id.html', 'sv.html', 'cs.html'
]
FORM_ACTION = 'https://formspree.io/f/xlganyvl'
DOMAIN = 'https://angkordrivers.com'


def file_exists_nonzero(path):
    return os.path.exists(path) and os.path.getsize(path) > 0


def check_secret_scan(content):
    secrets = ['sk-or-v1-', 'github_pat_', 'ghp_']
    for s in secrets:
        if s in content:
            return False, f"Secret found: {s}"
    return True, "No secrets"


def validate_page(page):
    path = os.path.join(ROOT, page)
    if not file_exists_nonzero(path):
        return False, [f"File missing: {page}"], []
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    errors = []
    warnings = []

    # Canonical
    canonical = soup.find('link', rel='canonical')
    if not canonical or f'{DOMAIN}/' not in canonical.get('href', ''):
        errors.append(f"Missing or incorrect canonical for {page}")

    # Hreflang set
    hreflangs = soup.find_all('link', rel='alternate', hreflang=True)
    hreflang_set = {l.get('hreflang') for l in hreflangs}
    expected_hreflangs = {'en', 'fr', 'zh-Hans', 'ko', 'ja', 'vi', 'th', 'de', 'es', 'it', 'pt', 'ru', 'nl', 'pl', 'ar', 'id', 'sv', 'cs', 'x-default'}
    if not expected_hreflangs.issubset(hreflang_set):
        missing = expected_hreflangs - hreflang_set
        errors.append(f"Missing hreflang tags: {missing}")

    # Service JSON-LD
    service_ld = None
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            if data.get('@type') == 'Service':
                service_ld = data
                break
        except:
            pass
    if service_ld is None:
        errors.append("Service JSON-LD not found")
    else:
        provider = service_ld.get('provider', {})
        if 'sameAs' not in provider:
            errors.append("Service JSON-LD provider missing 'sameAs'")
        if 'aggregateRating' in service_ld:
            errors.append("Service JSON-LD should not contain aggregateRating")

    # Form action and visible controls
    form = soup.find('form')
    if not form or form.get('action') != FORM_ACTION:
        errors.append(f"Form action should be {FORM_ACTION}")
    if form:
        visible_controls = []
        for ctrl in form.find_all(['input', 'select', 'textarea']):
            if ctrl.get('type') != 'hidden' and ctrl.get('style', '').find('display:none') == -1:
                visible_controls.append(ctrl)
        if len(visible_controls) != 6:
            errors.append(f"Expected 6 visible form controls, found {len(visible_controls)}")
        for ctrl in visible_controls:
            # Check label association
            linked_label = None
            if ctrl.get('id'):
                linked_label = form.find('label', attrs={'for': ctrl['id']})
            if linked_label is None:
                # Check if inside a label
                parent_label = ctrl.find_parent('label')
                if parent_label is None:
                    errors.append(f"Control {ctrl.get('name','?')} missing label association")

    # Local resource existence
    for tag, attr in [('img','src'), ('script','src'), ('link','href')]:
        for el in soup.find_all(tag):
            val = el.get(attr)
            if val and not val.startswith('http') and not val.startswith('data:'):
                # ignore anchor links
                if tag == 'link' and el.get('rel') and 'stylesheet' not in el.get('rel'):
                    continue
                if tag == 'a':
                    continue
                local_path = val.lstrip('/')
                abs_path = os.path.join(ROOT, local_path)
                if not file_exists_nonzero(abs_path):
                    errors.append(f"Missing local resource: {val}")

    # Favicon checks
    favicons = soup.find_all('link', rel=lambda x: x and ('icon' in x))
    for icon in favicons:
        href = icon.get('href')
        if href and not href.startswith('http'):
            abs_path = os.path.join(ROOT, href.lstrip('/'))
            if file_exists_nonzero(abs_path):
                try:
                    img = Image.open(abs_path)
                    sizes = icon.get('sizes')
                    if sizes:
                        w, h = map(int, sizes.lower().split('x'))
                        if img.width != w or img.height != h:
                            errors.append(f"Favicon size mismatch: {href}")
                except Exception:
                    pass
    manifest_link = soup.find('link', rel='manifest')
    if manifest_link and manifest_link.get('href', '').startswith('data:'):
        # parse data URI
        data_uri = manifest_link['href']
        if 'application/json' in data_uri:
            json_part = data_uri.split(',', 1)[1]
            try:
                manifest = json.loads(json_part)
                if 'icons' not in manifest:
                    errors.append("Manifest missing icons")
            except:
                errors.append("Invalid manifest JSON")

    # Tripadvisor summary
    trip_summary = soup.find(id='tripadvisor-summary')
    if trip_summary:
        text = trip_summary.get_text(' ', strip=True)
        if not re.search(r'5\.0|5', text) or '6' not in text or not re.search(r'\d{4}-\d{2}-\d{2}|\d{1,2}\s+[A-Za-z]+\s+\d{4}', text):
            errors.append("Tripadvisor summary missing rating/reviews/date")
        links = trip_summary.find_all('a')
        for l in links:
            href = l.get('href', '')
            if 'tripadvisor.com' in href and 'REPLACE_WITH' in href:
                errors.append("Tripadvisor link still placeholder")
    else:
        errors.append("Tripadvisor summary element not found (id=tripadvisor-summary)")

    # Google placeholder flag
    if soup.find(id='google-reviews-placeholder'):
        warnings.append("Google reviews placeholder present (flag, not fail)")

    # External resources check (no Manus/CloudFront/GoogleFont)
    external_urls = []
    for tag, attr in [('img','src'), ('script','src'), ('link','href')]:
        for el in soup.find_all(tag):
            val = el.get(attr)
            if val and val.startswith('http'):
                if any(d in val for d in ['manuscdn', 'cloudfront', 'fonts.googleapis']):
                    external_urls.append(val)
    if external_urls:
        errors.append(f"External resources remaining: {external_urls}")

    # Secret scan
    sec_ok, sec_msg = check_secret_scan(content)
    if not sec_ok:
        errors.append(sec_msg)

    return (not errors), errors, warnings


def main():
    all_errors = {}
    all_warnings = {}
    overall_pass = True
    for page in PAGES:
        ok, errors, warnings = validate_page(page)
        if not ok:
            overall_pass = False
            all_errors[page] = errors
        if warnings:
            all_warnings[page] = warnings
        print(f"{page}: {'PASS' if ok else 'FAIL'}")
        for e in errors:
            print(f"  ERROR: {e}")
        for w in warnings:
            print(f"  WARNING: {w}")
    if overall_pass:
        print("All main pages passed validation.")
    else:
        print("Validation failed.")
    return 0 if overall_pass else 1

if __name__ == '__main__':
    exit(main())
