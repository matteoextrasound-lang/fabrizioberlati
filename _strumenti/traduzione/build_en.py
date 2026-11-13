# Genera la versione inglese del sito in /en/ a partire dalle pagine italiane.
# Uso: python3 build_en.py  (rigenera tutte le pagine EN e aggiorna hreflang/selettore lingua sulle IT)
import re, os, json, html, glob, urllib.parse as up

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
BASE = 'https://fabrizioberlati.com/'

SLUG = {
 'index.html': 'index.html', 'su-misura.html': 'made-to-measure.html', 'laboratorio.html': 'workshop.html',
 'guide.html': 'guides.html', 'guida-altezza-stand-diffusori.html': 'speaker-stand-height.html',
 'mobili-hi-fi.html': 'hifi-furniture.html', 'porta-vinili.html': 'vinyl-record-storage.html',
 'stand-per-diffusori.html': 'speaker-stands.html', 'pannelli-acustici.html': 'acoustic-panels.html',
 'accessori.html': 'accessories.html',
 'extrasound-vinyl.html': 'extrasound-vinyl.html', 'extrasound-cube.html': 'extrasound-cube.html', 'extrasound-wave.html': 'extrasound-wave.html',
 'pannelli-pyramid.html': 'acoustic-panels-pyramid.html', 'pannelli-skyline.html': 'acoustic-panels-skyline.html',
 'pannello-soundwave.html': 'acoustic-panel-soundwave.html', 'sollevatori-cavi-bridge.html': 'cable-lifters-bridge.html',
 'supporti-inclinati-diffusori.html': 'tilting-speaker-supports.html', 'supporto-dap.html': 'dap-stand.html',
 'guida-conservare-vinili.html': 'how-to-store-vinyl-records.html', 'guida-giradischi-vibrazioni.html': 'turntable-vibration-isolation.html',
 'guida-pannelli-acustici.html': 'acoustic-panels-absorb-or-diffuse.html', 'guida-posizionare-diffusori.html': 'how-to-position-speakers.html',
 'guida-diffusori-scrivania.html': 'desktop-speaker-placement.html',
}
for f in glob.glob('mobile-hifi-*.html'): SLUG[f] = 'hifi-rack-' + f[len('mobile-hifi-'):]
for f in glob.glob('stand-*.html'):
    if f != 'stand-per-diffusori.html': SLUG[f] = 'speaker-stand-' + f[len('stand-'):]
# le pagine di rimando dei vecchi indirizzi (meta refresh) non si traducono
PAGES = sorted(f for f in glob.glob('*.html') if not f.startswith('google') and 'http-equiv="refresh"' not in open(f).read())
missing_slug = [f for f in PAGES if f not in SLUG]
assert not missing_slug, missing_slug

seg = json.load(open(f'{HERE}/segments.json'))['segments']
tr = {}
for g in 'ABC': tr.update(json.load(open(f'{HERE}/tr_{g}.json')))
T = {seg[k]: v for k, v in tr.items()}
T.update(json.load(open(f'{HERE}/extra.json')))       # testi aggiunti a mano (attributi data-t, JSON, correzioni)
FIX = json.load(open(f'{HERE}/fix.json'))              # correzioni puntuali alle traduzioni
T.update(FIX)
MISSING = set()

def t(s):
    k = s.strip()
    if not re.search('[A-Za-zÀ-ú]', k):
        m = re.fullmatch(r'([\d.,]+)\s*€', k)
        return '€' + m.group(1) if m else k
    if k in T: return T[k]
    MISSING.add(k); return k

def tr_text(raw):
    u = html.unescape(raw)
    if not u.strip(): return raw
    lead = u[:len(u) - len(u.lstrip())]; trail = u[len(u.rstrip()):]
    return lead + html.escape(t(u), quote=False) + trail

MAIL = json.load(open(f'{HERE}/mail.json'))
def tr_query(v):
    if v in MAIL: return MAIL[v]
    m = re.fullmatch(r'Informazioni su (.+)', v)
    if m: return 'Information about ' + m.group(1)
    m = re.fullmatch(r'Ciao Fabrizio, vorrei informazioni su (.+)\.', v)
    if m: return f"Hi Fabrizio, I'd like some information about {m.group(1)}."
    MISSING.add('QUERY:' + v); return v

def tr_href(h, it_file):
    if h.startswith(('mailto:', 'https://wa.me/')):
        base, _, q = h.partition('?')
        if not q: return h
        parts = []
        for kv in html.unescape(q).split('&'):
            k, _, v = kv.partition('=')
            parts.append(k + '=' + up.quote(tr_query(up.unquote(v)), safe=''))
        return base + '?' + '&amp;'.join(parts)
    if re.match(r'(https?:|//|#|data:|tel:)', h): return h
    path, hashp = (h.split('#', 1) + [''])[:2]
    path_only, q = (path.split('?', 1) + [''])[:2]
    if path_only == './':
        out = './'
    elif path_only.endswith('.html') and path_only in SLUG:
        out = SLUG[path_only] if SLUG[path_only] != 'index.html' else './'
    elif path_only == '' and hashp:
        return h
    else:
        out = '../' + path_only
    if q: out += '?' + q
    if hashp: out += '#' + hashp
    return out

def en_url(it): return BASE + 'en/' + (SLUG[it] if SLUG[it] != 'index.html' else '')
def it_url(it): return BASE + (it if it != 'index.html' else '')
def map_url(u):
    if u.startswith(BASE) and not u.startswith(BASE + 'images/'):
        rest = u[len(BASE):]; p, _, frag = rest.partition('#')
        p = p or 'index.html'
        if p in SLUG: return en_url(p) + ('#' + frag if frag else '')
    return u

def tr_json(o, key=None):
    if isinstance(o, dict): return {k: tr_json(v, k) for k, v in o.items()}
    if isinstance(o, list): return [tr_json(v, key) for v in o]
    if isinstance(o, str):
        if key in ('url', 'item', 'mainEntityOfPage'): return map_url(o)
        if key in ('@id', '@type', '@context', 'image', 'priceCurrency', 'availability', 'email', 'telephone',
                   'streetAddress', 'postalCode', 'addressLocality', 'addressRegion', 'addressCountry', 'datePublished',
                   'dateModified', 'price', 'lowPrice', 'highPrice'): return o
        if key == 'inLanguage': return 'en'
        if o.startswith('http'): return o
        if re.search('[A-Za-zÀ-ú]', o): return t(o)
    return o

STANDS_NOTE = json.load(open(f'{HERE}/stands_notes.json'))
def tr_stands(o):
    for s in o:
        s['url'] = SLUG.get(s['url'], s['url']); s['img'] = '../' + s['img']
        if s['note'] in STANDS_NOTE: s['note'] = STANDS_NOTE[s['note']]
        else: MISSING.add('NOTE:' + s['note'])
    return o

ATTR = ('alt', 'title', 'aria-label', 'placeholder', 'data-t')
def tr_tag(tag, it_file):
    def attr(m):
        name, q, val = m.group(1), m.group(2), m.group(3)
        if name in ATTR and re.search('[A-Za-zÀ-ú]', val):
            return f'{name}={q}{html.escape(t(html.unescape(val)))}{q}'
        if name in ('href', 'src'):
            if tag.startswith('<link') and 'rel="canonical"' in tag: return f'{name}={q}{en_url(it_file)}{q}'
            if tag.startswith('<link') and 'hreflang' in tag: return m.group(0)
            return f'{name}={q}{tr_href(val, it_file)}{q}'
        return m.group(0)
    if tag.startswith('<meta') and 'name="description"' in tag:
        return re.sub(r'content="([^"]*)"', lambda m: 'content="' + html.escape(t(html.unescape(m.group(1)))) + '"', tag)
    if tag.startswith('<html'): return tag.replace('lang="it"', 'lang="en"')
    return re.sub(r'([a-zA-Z-]+)=(")([^"]*)"', attr, tag)

JS_EN = {'guide.js': 'guide-en.js', 'prod.js': 'prod-en.js', 'cube.js': 'cube-en.js'}

def lang_links(it_file):
    return (f'<link rel="alternate" hreflang="it" href="{it_url(it_file)}">\n'
            f'<link rel="alternate" hreflang="en" href="{en_url(it_file)}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{it_url(it_file)}">')

def add_switch(s, href, label, lang):
    # selettore lingua come ultima voce del menu principale
    s = re.sub(r'<a class="lang"[^>]*>[A-Z]{2}</a>', '', s)
    return re.sub(r'(<header[^>]*>.*?<nav>.*?)(</nav>)', lambda m: m.group(1) + f'<a class="lang" href="{href}" hreflang="{lang}" lang="{lang}">{label}</a>' + m.group(2), s, count=1, flags=re.S)

def add_hreflang(s, it_file):
    s = re.sub(r'\n<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', s)
    return re.sub(r'(<link rel="canonical" href="[^"]+">)', lambda m: m.group(1) + '\n' + lang_links(it_file), s, count=1)

def build(it_file):
    s = open(it_file).read()
    parts = re.split(r'(<!--.*?-->|<script\b[^>]*>.*?</script>|<style\b.*?</style>|<[^>]+>)', s, flags=re.S)
    out = []; in_title = False
    for p in parts:
        if not p: continue
        if p.startswith('<script'):
            m = re.match(r'(<script\b[^>]*>)(.*?)(</script>)', p, re.S)
            open_t, body, close_t = m.groups()
            if 'application/ld+json' in open_t:
                body = json.dumps(tr_json(json.loads(body)), ensure_ascii=False)
            elif 'id="stands-data"' in open_t:
                body = json.dumps(tr_stands(json.loads(body)), ensure_ascii=False)
            src = re.search(r'src="([^"?]+)(\?[^"]*)?"', open_t)
            if src and not re.match(r'(https?:)?//', src.group(1)):
                f = src.group(1); q = src.group(2) or ''
                open_t = open_t.replace(src.group(0), f'src="../{JS_EN.get(f, f)}{q}"')
            out.append(open_t + body + close_t)
        elif p.startswith('<!--') or p.startswith('<style'):
            out.append(p)
        elif p.startswith('<'):
            out.append(tr_tag(p, it_file))
        else:
            out.append(tr_text(p))
    s = ''.join(out)
    s = add_hreflang(s, it_file)
    s = add_switch(s, '../' + (it_file if it_file != 'index.html' else ''), 'IT', 'it')
    os.makedirs('en', exist_ok=True)
    open('en/' + SLUG[it_file], 'w').write(s)

GC = '<script data-goatcounter="https://matteoberlati.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'
for f in PAGES:
    # statistiche GoatCounter su ogni pagina (senza cookie)
    s = open(f).read()
    if GC not in s:
        s = s.replace('</body>', GC + '\n</body>', 1); open(f, 'w').write(s)
for f in PAGES:
    build(f)
    # pagina italiana: hreflang + selettore EN
    s = open(f).read()
    s2 = add_switch(add_hreflang(s, f), 'en/' + (SLUG[f] if SLUG[f] != 'index.html' else ''), 'EN', 'en')
    if s2 != s: open(f, 'w').write(s2)

# JS in inglese
for it_js, en_js in JS_EN.items():
    s = open(it_js).read()
    for a, b in json.load(open(f'{HERE}/js_{it_js.split(".")[0]}.json')):
        if a not in s: MISSING.add(f'JS {it_js}: {a[:60]}')
        s = s.replace(a, b)
    open(en_js, 'w').write(s)

# sitemap con le alternative di lingua
urls = []
for f in PAGES:
    for u in (it_url(f), en_url(f)):
        urls.append(f'  <url>\n    <loc>{u}</loc>\n    <lastmod>2026-11-03</lastmod>\n'
                    f'    <xhtml:link rel="alternate" hreflang="it" href="{it_url(f)}"/>\n'
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{en_url(f)}"/>\n'
                    f'    <xhtml:link rel="alternate" hreflang="x-default" href="{it_url(f)}"/>\n  </url>')
open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(urls) + '\n</urlset>\n')
json.dump(SLUG, open(os.path.join(HERE, 'pagine_abbinate.json'), 'w'), indent=1, ensure_ascii=False)
if os.environ.get('MISSING_DUMP'): json.dump(sorted(MISSING), open(os.environ['MISSING_DUMP'], 'w'), ensure_ascii=False, indent=1)
print('pagine', len(PAGES), '| testi non tradotti', len(MISSING))
for m in sorted(MISSING): print('  -', m[:140])
