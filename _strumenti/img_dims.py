# Aggiunge width/height alle <img> locali (evita salti di impaginazione) e
# carica subito la prima foto se sta nella prima sezione della pagina.
# Uso: python3 _strumenti/img_dims.py   (poi rigenerare l'inglese con build_en.py)
import re, glob, os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
cache = {}
def dims(src):
    p = src.split('?')[0]
    if p not in cache:
        cache[p] = Image.open(p).size if os.path.exists(p) else None
    return cache[p]
def fix_img(tag):
    m = re.search(r'\bsrc="([^"]+)"', tag)
    if not m or m.group(1).startswith(('http', 'data:')) or ' width=' in tag: return tag
    d = dims(m.group(1))
    if not d: return tag
    return tag[:-1].rstrip('/').rstrip() + f' width="{d[0]}" height="{d[1]}">'
n = 0
for f in sorted(glob.glob('*.html')):
    if f.startswith('google'): continue
    s = open(f).read(); o = s
    s = re.sub(r'<img\b[^>]*>', lambda m: fix_img(m.group(0)), s)
    mm = re.search(r'<main>\s*<section.*?</section>', s, re.S)
    if mm:
        first = re.search(r'<img\b[^>]*>', mm.group(0))
        if first and 'loading="lazy"' in first.group(0):
            new = first.group(0).replace(' loading="lazy"', ' fetchpriority="high"')
            s = s[:mm.start()] + mm.group(0).replace(first.group(0), new, 1) + s[mm.end():]
    if s != o: open(f, 'w').write(s); n += 1
print('pagine aggiornate', n)
