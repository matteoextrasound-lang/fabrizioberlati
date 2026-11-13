# Sei copertine coerenti per le guide: stesso stile piatto, stessa palette,
# stesso modo di disegnare il suono (tre archi color ottone che sfumano).
import math, random
DARK='#3b2a1e'; WOOD='#d9bb8c'; WOOD2='#c9a774'; BRASS='#a87a2f'; ORANGE='#ff9a2e'; REC='#1f1915'; LABEL='#c98a3a'; PALE='#e8d6b4'
SH='<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="12" fill="#2a1d14" opacity=".08"/>'
def arcs(cx,cy,r0,step,a0,a1,w=6,col=BRASS):
    out=''
    for k,op in enumerate((.9,.55,.28)):
        r=r0+k*step; s=math.radians(a0); e=math.radians(a1)
        x1,y1=cx+r*math.cos(s),cy+r*math.sin(s); x2,y2=cx+r*math.cos(e),cy+r*math.sin(e)
        out+=f'<path d="M{x1:.1f} {y1:.1f} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'
    return out
def speaker(x,y,w,h):  # cassa vista di fronte
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w*.06:.1f}" fill="{DARK}"/>'
            f'<circle cx="{x+w/2}" cy="{y+h*.24}" r="{w*.13:.1f}" fill="{PALE}"/>'
            f'<circle cx="{x+w/2}" cy="{y+h*.64}" r="{w*.3:.1f}" fill="#5b4636"/><circle cx="{x+w/2}" cy="{y+h*.64}" r="{w*.11:.1f}" fill="{DARK}"/>')
def record(cx,cy,r,lab=True):
    g=''.join(f'<circle cx="{cx}" cy="{cy}" r="{rr:.1f}" fill="none" stroke="#3a302a" stroke-width="1.1" opacity=".8"/>' for rr in [r*f for f in (.42,.5,.58,.66,.74,.82,.9)])
    s=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#rec)"/>{g}'
    if lab: s+=f'<circle cx="{cx}" cy="{cy}" r="{r*.33:.1f}" fill="{LABEL}"/><circle cx="{cx}" cy="{cy}" r="{r*.27:.1f}" fill="none" stroke="#e7b86e" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="{max(5,r*.03):.1f}" fill="#f6efe2"/>'
    return s
DEFS=('<defs><radialGradient id="rec" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#4d423a"/><stop offset=".5" stop-color="#1f1915"/><stop offset="1" stop-color="#110d0b"/></radialGradient>'
      '<linearGradient id="shine" x1="0" y1="0" x2="1" y2="1"><stop offset=".3" stop-color="#fff" stop-opacity="0"/><stop offset=".44" stop-color="#fff" stop-opacity=".15"/><stop offset=".52" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>')
def svg(body): return f'<svg viewBox="0 0 960 700" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'
C={}
# 1. altezza: cassa sullo stand, quota verticale, linea del tweeter fino alla testa
b=SH.format(cx=420,cy=622,rx=150)
b+=f'<rect x="350" y="604" width="140" height="14" rx="3" fill="{WOOD2}"/><rect x="404" y="330" width="32" height="276" fill="{WOOD}"/><rect x="346" y="318" width="148" height="14" rx="3" fill="{WOOD2}"/>'
b+=speaker(352,118,136,200)
b+=f'<g stroke="{BRASS}" stroke-width="4" fill="none"><line x1="300" y1="166" x2="300" y2="612"/><line x1="286" y1="166" x2="314" y2="166"/><line x1="286" y1="612" x2="314" y2="612"/></g>'
b+=f'<line x1="438" y1="166" x2="640" y2="166" stroke="{BRASS}" stroke-width="4" stroke-dasharray="12 10"/>'
b+=f'<circle cx="680" cy="166" r="40" fill="#6f6254"/><circle cx="660" cy="170" r="7" fill="{PALE}"/>'
b='<g transform="translate(60 40)">'+b+'</g>'
C['altezza']=svg(b)
# 2. vinili: il disco, con il riflesso
b=SH.format(cx=480,cy=650,rx=230)+record(480,345,285)+'<circle cx="480" cy="345" r="285" fill="url(#shine)"/>'
C['vinili']=svg(b)
# 3. giradischi: dall'alto, più piccolo, con le vibrazioni intorno
b=SH.format(cx=480,cy=600,rx=250)
b+=f'<rect x="250" y="170" width="460" height="340" rx="18" fill="#c99a63"/><rect x="250" y="170" width="460" height="340" rx="18" fill="none" stroke="#a87a4a" stroke-width="3"/>'
b+='<g stroke="#b9895a" stroke-width="2" opacity=".5">'+''.join(f'<line x1="262" y1="{y}" x2="698" y2="{y}"/>' for y in range(190,500,22))+'</g>'
b+=f'<circle cx="410" cy="340" r="155" fill="#2b2420"/>'+record(410,340,145)
b+=f'<circle cx="625" cy="235" r="30" fill="#8b7a66"/><circle cx="625" cy="235" r="17" fill="#cfc3b2"/><path d="M625 235 L608 420 L548 462" fill="none" stroke="#e3dccf" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
b+='<rect x="526" y="450" width="36" height="24" rx="4" transform="rotate(-33 544 462)" fill="#d9d2c6"/><circle cx="660" cy="470" r="13" fill="#2b2420"/>'
for (cx,cy,a0,a1) in ((250,510,95,175),(710,510,5,85),(250,170,185,265),(710,170,275,355)):
    b+=arcs(cx,cy,40,30,a0,a1,w=5,col=ORANGE)
C['giradischi']=svg(b)
# 4. pannelli: pannello di blocchetti, onde che arrivano, riflessioni sparpagliate
random.seed(7)
woods=['#c99a63','#b07a4a','#d9b688','#a8683f','#e4c79e','#c48a55','#dcb98c','#9c6b43','#d0a46f']
N=7;S=54;ox,oy=500,155
b=SH.format(cx=690,cy=600,rx=210)+f'<clipPath id="pc"><rect x="{ox}" y="{oy}" width="{N*S}" height="{N*S}"/></clipPath><rect x="{ox-8}" y="{oy-8}" width="{N*S+16}" height="{N*S+16}" fill="#6b4126"/><rect x="{ox}" y="{oy}" width="{N*S}" height="{N*S}" fill="#4a2c19"/>'
b+='<g clip-path="url(#pc)">'
for j in range(N):
    for i in range(N):
        h=random.choice([1,2,3,4,5]);col=random.choice(woods);x=ox+i*S+3;y=oy+j*S+3;w=S-6;d=h*3.2
        b+=f'<rect x="{x+d:.1f}" y="{y+d:.1f}" width="{w}" height="{w}" fill="#2a1d14" opacity=".45"/><rect x="{x}" y="{y}" width="{w}" height="{w}" fill="{col}"/>'
b+='</g>'+arcs(-60,344,190,62,-38,38,w=6)
for y in (210,290,370,450):
    for a in (152,175,198):
        aa=math.radians(a+random.uniform(-6,6));L=random.uniform(55,85);x0=ox-14
        x1,y1=x0+math.cos(aa)*L,y-math.sin(aa)*L
        b+=f'<line x1="{x0}" y1="{y}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="{ORANGE}" stroke-width="4" stroke-linecap="round"/><circle cx="{x1:.0f}" cy="{y1:.0f}" r="4.5" fill="{ORANGE}"/>'
C['pannelli']=svg(b)
# 5. posizionamento: due casse su stand viste di fronte, triangolo d'ascolto a terra in prospettiva, suono che converge
b=SH.format(cx=480,cy=612,rx=330)
b+=f'<polygon points="250,560 710,560 480,660" fill="none" stroke="{BRASS}" stroke-width="4" stroke-dasharray="12 10"/>'
for x in (190,630):
    b+=f'<rect x="{x+20}" y="548" width="100" height="12" rx="3" fill="{WOOD2}"/><rect x="{x+58}" y="330" width="24" height="220" fill="{WOOD}"/><rect x="{x+16}" y="320" width="108" height="12" rx="3" fill="{WOOD2}"/>'
    b+=speaker(x+18,160,104,160)
b+=arcs(282,240,60,42,-20,40,w=6)+arcs(678,240,60,42,140,200,w=6)
b+=f'<circle cx="480" cy="630" r="22" fill="#6f6254"/>'
C['posizionamento']=svg(b)
# 6. scrivania: vista di fronte, monitor al centro, due casse inclinate su supporti, suono verso l'alto
b=SH.format(cx=480,cy=640,rx=360)
b+=f'<rect x="110" y="470" width="740" height="22" rx="3" fill="{WOOD}"/><rect x="140" y="492" width="22" height="140" fill="{WOOD2}"/><rect x="798" y="492" width="22" height="140" fill="{WOOD2}"/>'
b+=f'<rect x="330" y="230" width="300" height="190" rx="10" fill="#4a3a2e"/><rect x="344" y="244" width="272" height="162" rx="4" fill="#efe6d6"/><rect x="460" y="420" width="40" height="40" fill="#8b7a66"/><rect x="420" y="456" width="120" height="14" rx="4" fill="#8b7a66"/>'
for x,sg in ((170,1),(680,-1)):
    cx=x+55
    b+=f'<rect x="{x}" y="448" width="110" height="22" rx="3" fill="{WOOD2}"/>'
    b+=speaker(x+4,288,102,160)
b+=arcs(225,290,70,40,-120,-60,w=6)+arcs(735,290,70,40,-120,-60,w=6)
C['scrivania']=svg(b)
# 7. amplificatore: visto di fronte su un ripiano, con il calore che sale libero
b=SH.format(cx=480,cy=560,rx=300)
b+=f'<rect x="170" y="520" width="620" height="18" rx="3" fill="{WOOD}"/>'
b+=f'<rect x="250" y="400" width="460" height="120" rx="8" fill="#2d2621"/>'
b+=''.join(f'<line x1="{x}" y1="412" x2="{x}" y2="430" stroke="#6b5a4a" stroke-width="5"/>' for x in range(290,690,30))
b+=f'<circle cx="640" cy="470" r="26" fill="{BRASS}"/><circle cx="300" cy="470" r="11" fill="{BRASS}"/><rect x="350" y="460" width="110" height="18" rx="3" fill="#6b4f2a"/>'
for x in (400,560):
    b+=arcs(x,400,55,38,-115,-65,w=6,col=ORANGE)
C['amplificatore']=svg(b)
for k,v in C.items(): open(f'{k}.svg','w').write(v)
print(list(C))
