"""Shared static Option A brand metadata; imported by build/migration tools.

Only local GitHub Pages resources are referenced. Versioned URLs avoid retaining
older icons in ordinary browser caches after the artwork changes.
"""
VERSION='option-a-20261106'
LOGO_URL=f'/assets/brand/angkor-drivers-logo.svg?v={VERSION}'
BRAND_STYLE=f'<link rel="stylesheet" href="/assets/css/branding.css?v={VERSION}">'
BRAND_IMAGE=f'<img class="brand-mark" src="{LOGO_URL}" width="40" height="40" alt="" aria-hidden="true" decoding="async" fetchpriority="high">'
ICONS='\n<!-- Approved Option A: local, versioned browser and device icons. -->\n'
ICONS+=f'<link rel="icon" type="image/x-icon" sizes="16x16 24x24 32x32 48x48 64x64" href="/favicon.ico?v={VERSION}">\n'
ICONS+=f'<link rel="icon" type="image/svg+xml" sizes="any" href="/favicon.svg?v={VERSION}">\n'
for size in [16,32,48,96]:
    ICONS+=f'<link rel="icon" type="image/png" sizes="{size}x{size}" href="/favicon-{size}x{size}.png?v={VERSION}">\n'
for size in [152,167,180]:
    ICONS+=f'<link rel="apple-touch-icon" sizes="{size}x{size}" href="/apple-touch-icon-{size}x{size}.png?v={VERSION}">\n'
ICONS+=f'<link rel="mask-icon" href="/safari-pinned-tab.svg?v={VERSION}" color="#154212">\n'
ICONS+=f'<link rel="manifest" href="/site.webmanifest?v={VERSION}">\n'
ICONS+=f'<meta name="msapplication-config" content="/browserconfig.xml?v={VERSION}">\n'
ICONS+='<meta name="msapplication-TileColor" content="#154212">\n'
ICONS+=f'<meta name="msapplication-TileImage" content="/mstile-144x144.png?v={VERSION}">\n'
