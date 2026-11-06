"""Build Option A's production brand/icon files; no runtime image service.

The approved Nano Banana artwork and native-alpha preparation are retained as
sources. Resizing never crops the symbol. Potrace is a development-only vector
tracer; its generated paths preserve the existing silhouette rather than drawing
another logo. Browser SVG adapts its color for dark tabs. Apple/Windows/Android
icons use ivory backgrounds; maskable icons have extra safe-area padding.
"""
from pathlib import Path
from PIL import Image, ImageOps
import json, subprocess, tempfile, shutil, hashlib, re

ROOT=Path(__file__).resolve().parents[1]
BRAND=ROOT/'assets/brand'
SOURCE=BRAND/'source/option-a-transparent-master.png'
VERSION='option-a-20261106'
GREEN='#154212'
IVORY='#FCF9F2'
BROWSER_SIZES=[16,24,32,48,64,96,128,256]
APPLE_SIZES=[57,60,72,76,114,120,144,152,167,180]
ICO_SIZES=[16,24,32,48,64]
RECORDS=[]


def record(path, purpose):
    row={'path':str(path.relative_to(ROOT)), 'purpose':purpose,
         'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    if path.suffix.lower() in {'.png','.ico'}:
        with Image.open(path) as im: row['width'],row['height']=im.size
    RECORDS.append(row)


def fit(symbol, size, coverage=.88, opaque=False):
    fitted=ImageOps.contain(symbol,(round(size*coverage),round(size*coverage)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(size,size),IVORY if opaque else (0,0,0,0))
    canvas.alpha_composite(fitted,((size-fitted.width)//2,(size-fitted.height)//2))
    return canvas


def save_icon(symbol, path, size, purpose, coverage=.88, opaque=False):
    fit(symbol,size,coverage,opaque).save(path,optimize=True)
    record(path,purpose)


def main():
    BRAND.mkdir(parents=True,exist_ok=True)
    master=Image.open(SOURCE).convert('RGBA')
    alpha=master.getchannel('A')
    lowest,highest=alpha.getextrema()
    assert lowest==0 and highest>=250,'Source must contain genuine native transparency'
    # This native-alpha export tops out at254 rather than255. Normalize only
    # its opacity scale; the zero-alpha background and silhouette are intact.
    if highest<255:
        master.putalpha(alpha.point(lambda a:round(a*255/highest)))
    # Ignore only near-invisible1/255 export specks when measuring padding.
    # Keep two extra pixels so visible anti-aliased silhouette edges remain.
    bounds=master.getchannel('A').point(lambda a:255 if a>8 else 0).getbbox()
    left,top,right,bottom=bounds
    symbol=master.crop((max(0,left-2),max(0,top-2),min(master.width,right+2),min(master.height,bottom+2)))
    for size in BROWSER_SIZES:
        save_icon(symbol,ROOT/f'favicon-{size}x{size}.png',size,'browser PNG')
    # Opaque legacy ICO is visible in both light and dark browser chrome.
    fit(symbol,256,.88,True).save(ROOT/'favicon.ico',format='ICO',sizes=[(s,s) for s in ICO_SIZES])
    record(ROOT/'favicon.ico','legacy browser ICO:16/24/32/48/64')
    for size in APPLE_SIZES:
        save_icon(symbol,ROOT/f'apple-touch-icon-{size}x{size}.png',size,'Apple touch icon',.84,True)
    shutil.copyfile(ROOT/'apple-touch-icon-180x180.png',ROOT/'apple-touch-icon.png')
    record(ROOT/'apple-touch-icon.png','default Apple touch icon180x180')
    for size in [192,512]:
        save_icon(symbol,ROOT/f'android-chrome-{size}x{size}.png',size,'Android/PWA any icon',.84,True)
        save_icon(symbol,ROOT/f'maskable-icon-{size}x{size}.png',size,'PWA maskable safe-area icon',.54,True)
    for size in [70,144,150,310]:
        save_icon(symbol,ROOT/f'mstile-{size}x{size}.png',size,'Windows tile',.70,True)
    wide=Image.new('RGBA',(310,150),IVORY)
    tile=fit(symbol,150,.70,True);wide.alpha_composite(tile,(80,0))
    wide.save(ROOT/'mstile-310x150.png',optimize=True);record(ROOT/'mstile-310x150.png','Windows wide tile')
    for size in [96,192,512]:
        save_icon(symbol,BRAND/f'angkor-drivers-logo-{size}.png',size,'transparent website logo',.92,False)
    # Trace the actual native alpha silhouette. Interior transparent regions
    # become vector cutouts, including the temple doors and steering spokes.
    trace_image=fit(symbol,1024,.88,False)
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp);trace_image.getchannel('A').point(lambda a:0 if a>=128 else 255,mode='1').save(tmp/'symbol.pbm')
        subprocess.run(['potrace',str(tmp/'symbol.pbm'),'-s','-o',str(tmp/'symbol.svg'),'--turdsize','3','--opttolerance','0.2'],check=True)
        traced=(tmp/'symbol.svg').read_text()
    traced=re.sub(r'<\?xml.*?\?>','',traced,flags=re.S)
    traced=re.sub(r'<!DOCTYPE.*?\]>|<!DOCTYPE[^>]*>','',traced,flags=re.S)
    traced=re.sub(r'<metadata>.*?</metadata>','',traced,flags=re.S)
    traced=re.sub(r'width="[^"]+"','width="1024"',traced,count=1)
    traced=re.sub(r'height="[^"]+"','height="1024"',traced,count=1)
    traced=traced.replace('fill="#000000"',f'fill="{GREEN}"')
    assert '<path' in traced and '<image' not in traced
    (BRAND/'angkor-drivers-logo.svg').write_text(traced.strip()+'\n');record(BRAND/'angkor-drivers-logo.svg','true vector logo traced from approved silhouette')
    (ROOT/'safari-pinned-tab.svg').write_text(traced.replace(GREEN,'#000000').strip()+'\n')
    record(ROOT/'safari-pinned-tab.svg','Safari monochrome pinned-tab mask')
    favicon=traced.replace('<g ', '<g class="brand-shape" ',1)
    favicon=re.sub(r'(<svg\b[^>]*>)',r'\1\n<style>.brand-shape{fill:'+GREEN+'}@media(prefers-color-scheme:dark){.brand-shape{fill:'+IVORY+'}}</style>',favicon,count=1,flags=re.S)
    (ROOT/'favicon.svg').write_text(favicon.strip()+'\n');record(ROOT/'favicon.svg','color-adaptive vector browser favicon')
    manifest=json.loads((ROOT/'site.webmanifest').read_text())
    manifest.update({'id':'/','background_color':IVORY.lower(),'theme_color':GREEN})
    manifest['icons']=[{'src':f'/{kind}-{s}x{s}.png?v={VERSION}','sizes':f'{s}x{s}','type':'image/png','purpose':purpose}
                       for kind,purpose in [('android-chrome','any'),('maskable-icon','maskable')] for s in [192,512]]
    (ROOT/'site.webmanifest').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');record(ROOT/'site.webmanifest','static app icon manifest; does not promise offline functionality')
    (ROOT/'browserconfig.xml').write_text('<?xml version="1.0" encoding="utf-8"?>\n<browserconfig><msapplication><tile><square70x70logo src="/mstile-70x70.png"/><square150x150logo src="/mstile-150x150.png"/><square310x310logo src="/mstile-310x310.png"/><wide310x150logo src="/mstile-310x150.png"/><TileColor>'+GREEN+'</TileColor></tile></msapplication></browserconfig>\n');record(ROOT/'browserconfig.xml','Windows browser tile config')
    (BRAND/'asset-manifest.json').write_text(json.dumps({'version':VERSION,'approved_option':'A','native_alpha_source':str(SOURCE.relative_to(ROOT)),'browser_png_sizes':BROWSER_SIZES,'apple_touch_sizes':APPLE_SIZES,'ico_sizes':ICO_SIZES,'files':RECORDS},indent=2)+'\n')
    print('Generated',len(RECORDS),'production files from approved Option A.')

if __name__=='__main__':main()
