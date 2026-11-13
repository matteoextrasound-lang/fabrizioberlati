import re, json, os
os.chdir(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
tpl = open('su-misura.html').read()
head_common = tpl[:tpl.index('<title>')]
fonts = re.search(r'(<link rel="icon".*?<link rel="stylesheet" href="craft.css\?v=\d+">)', tpl, re.S).group(1)
header = re.search(r'(<header class="solid">.*?</header>)', tpl, re.S).group(1)
header = header.replace(' aria-current="page"', '')
foot_bottom = re.search(r'(<div class="wrap foot">.*?</footer>)', tpl, re.S).group(1)
wa_svg = re.search(r'(<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true">.*?</svg>)', tpl, re.S).group(1)

def page(fn, title, desc, ld, body, css_extra='', js=''):
    hdr = header.replace('<a href="guide.html">Guide</a>', '<a href="guide.html" aria-current="page">Guide</a>')
    s = head_common + f'<title>{title}</title>\n<meta name="description" content="{desc}">\n' + fonts + \
        f'\n<link rel="stylesheet" href="guide.css?v=3">\n' + ('<link rel="stylesheet" href="anim.css?v=1">\n' if 'class="anim"' in body else '') + f'<link rel="canonical" href="https://fabrizioberlati.com/{fn}">\n' + \
        '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>\n<body>\n' + hdr + \
        '\n\n<main>\n' + body + '\n</main>\n\n<footer>' + fcta(title) + '\n' + foot_bottom + '\n\n<script src="site.js?v=5"></script>\n' + js + ('<script src="anim.js?v=1"></script>\n' if 'class="anim"' in body else '') + '</body>\n</html>\n'
    open(fn, 'w').write(s)

def fcta(t):
    return ('<div class="wrap fcta"><p>Hai una domanda? Scrivimi o mandami un messaggio su WhatsApp.</p><div class="ctas">'
            '<a class="btn" href="mailto:info@fabrizioberlati.com?subject=Domanda%20dalle%20guide">Chiedi informazioni</a>'
            '<a class="link tel" href="https://wa.me/393334188754?text=Ciao%20Fabrizio%2C%20ho%20una%20domanda." target="_blank" rel="noopener" aria-label="Scrivi a Fabrizio su WhatsApp al 333 418 8754">'
            + wa_svg + '333 418 8754</a></div></div>')


# riquadro "compra su Extrasound" in fondo a ogni guida (testi in guide_negozio.json)
SHOP = json.load(open('_strumenti/guide_negozio.json'))
def shop_box(key):
    t, txt, links = SHOP[key]
    bt = ''.join(f'<a class="{"btn" if i == 0 else "link"}" href="{u}" target="_blank" rel="noopener">{l}</a>' for i, (l, u) in enumerate(links))
    return f'\n  <div class="shopbox"><p><b>{t}</b>{txt}</p><div class="ctas">{bt}</div></div>\n'

STANDS = [
 dict(name='Extrasound Clessidra', url='stand-clessidra.html', img='images/clessidra-card.jpg?v=2', h=39, note='Faggio massello · 200 € la coppia'),
 dict(name='Extrasound Zeta', url='stand-zeta.html', img='images/zeta-card.jpg', h=61, note='Rovere e faggio · prezzo su richiesta'),
 dict(name='Extrasound Line', url='stand-line.html', img='images/line-card.jpg', h=54, note='Multistrato e metallo · prezzo su richiesta'),
 dict(name='Extrasound Rigatini', url='stand-rigatini.html', img='images/rigatini-card.jpg', h=50.3, note='Faggio massello · 250 € la coppia'),
 dict(name='Stand Stile Pannello', url='stand-stile-pannello.html', img='images/pannello-card.jpg?v=2', h=54.6, note='Faggio massello · 300 € la coppia'),
 dict(name='Wood Brick', url='stand-wood-brick.html', img='images/woodbrick-card.jpg', h=55, note='Legno massello · 300 € la coppia'),
 dict(name='Art Triangle', url='stand-art-triangle.html', img='images/art-triangle-card.jpg?v=4', h=60.3, note='Faggio massello · 300 € la coppia'),
 dict(name='Extrasound Stylus', url='stand-stylus.html', img='images/stylus-card.jpg', h=61, note='Doussiè massello · da 280 € la coppia'),
 dict(name='ESSE2', url='stand-esse2.html', img='images/esse2-card.jpg', h=64, note='Faggio, per KEF LS50 · su richiesta'),
 dict(name='Modern Art Grey Buttons', url='stand-modern-art.html', img='images/modern-art-card.jpg?v=3', h=65.6, note='Faggio massello · 300 € la coppia'),
 dict(name='Extrasound Tree', url='stand-tree.html', img='images/tree-card.jpg?v=2', h=71.5, note='Faggio massello · 350 € la coppia'),
 dict(name='Listelli Rado', url='stand-listelli-rado.html', img='images/listelli-rado-card.jpg?v=2', h=75, note='Faggio massello · 200 € la coppia'),
 dict(name='Extrasound Ground', url='stand-ground.html', img='images/ground-card.jpg?v=6', h=24, note='Stand bassi in multistrato · da 250 €', low=True),
]
def it(v): return (f'{v:.1f}'.rstrip('0').rstrip('.')).replace('.', ',')

FAQ = [
 ("Quanto devono essere alti gli stand per le casse?",
  "Per i diffusori da scaffale più comuni, ascoltati da un divano, di solito tra 60 e 75 cm. Il calcolo esatto è semplice: altezza delle orecchie da seduto meno l'altezza del tweeter dalla base del diffusore. Con orecchie a 100 cm e tweeter a 25 cm, lo stand giusto è alto circa 75 cm."),
 ("Il tweeter deve essere all'altezza delle orecchie?",
  "È la regola più affidabile: il tweeter è l'altoparlante più direzionale e, se punta verso le orecchie, la voce e gli strumenti restano a fuoco. Alcuni costruttori indicano invece un punto tra tweeter e woofer: se il manuale del tuo diffusore lo dice, segui quello."),
 ("Meglio uno stand più alto o più basso del necessario?",
  "Se proprio non trovi l'altezza esatta, meglio qualche centimetro in meno: il tweeter resta appena sotto le orecchie, che è la situazione più naturale. Uno stand troppo alto fa arrivare il suono dall'alto e si nota di più."),
 ("Posso mettere le casse su un mobile invece che sugli stand?",
  "Sì, ma di solito il mobile è più basso delle orecchie e fa vibrare il ripiano. In quel caso aiutano un supporto inclinato, che punta il tweeter verso l'alto, e un appoggio che stacchi il diffusore dal piano."),
 ("Che altezza devono avere gli stand per una scrivania o per le casse da pavimento?",
  "Sulla scrivania si usano supporti bassi o inclinati, perché le orecchie sono vicine e già alte rispetto al piano. Per i diffusori da pavimento non servono stand alti: bastano basi da 10-25 cm che li alzino da terra e li rendano più stabili."),
]

calc = f'''
<section class="calc" id="calc" aria-labelledby="calc-t">
  <div>
    <h2 id="calc-t">Calcola l'altezza del tuo stand</h2>
    <p class="c-sub">Tre misure, e ti dico quanto deve essere alto lo stand e quali dei miei modelli vanno bene.</p>
    <fieldset>
      <legend>1. Dove ti siedi per ascoltare?</legend>
      <div class="chips" role="group" aria-label="Seduta tipica">
        <button type="button" data-v="95" aria-pressed="false">Divano basso</button>
        <button type="button" data-v="100" aria-pressed="true">Divano</button>
        <button type="button" data-v="108" aria-pressed="false">Poltrona</button>
        <button type="button" data-v="115" aria-pressed="false">Sedia</button>
      </div>
      <label class="lb" for="ear">Altezza delle orecchie da seduto</label>
      <div class="num"><input id="ear" type="number" inputmode="decimal" min="60" max="160" step="1" value="100"><span>cm da terra</span></div>
      <span class="hint">Meglio misurarla: siediti dove ascolti e fatti misurare da terra al foro dell'orecchio.</span>
    </fieldset>
    <fieldset>
      <label class="lb" for="tw">2. Altezza del tweeter</label>
      <div class="num"><input id="tw" type="number" inputmode="decimal" min="3" max="80" step="0.5" value="22"><span>cm dalla base del diffusore</span></div>
      <span class="hint">Dal piano su cui appoggia il diffusore al centro del tweeter, l'altoparlante piccolo in alto.</span>
    </fieldset>
    <fieldset>
      <label class="lb" for="ft">3. Piedini o punte sotto il diffusore</label>
      <div class="num"><input id="ft" type="number" inputmode="decimal" min="0" max="15" step="0.5" value="0"><span>cm</span></div>
      <span class="hint">Se non ne usi, lascia 0.</span>
    </fieldset>
  </div>
  <div aria-live="polite">
    <svg class="scene" viewBox="0 -30 430 290" role="img" aria-label="Schema: diffusore sullo stand e ascoltatore seduto, con il tweeter all'altezza delle orecchie"></svg>
    <div class="c-out">
      <p>Lo stand ideale è alto circa</p>
      <p class="big" id="out-h">78 <small>cm</small></p>
      <p id="out-txt"></p>
    </div>
    <ul class="picks" id="picks"></ul>
    <div class="c-cta"><a class="btn" id="out-mail" href="mailto:info@fabrizioberlati.com">Chiedimi uno stand su misura</a><a class="link" href="stand-per-diffusori.html">Tutti gli stand</a></div>
  </div>
  <script type="application/json" id="stands-data">{json.dumps([{k: v for k, v in s.items()} for s in STANDS], ensure_ascii=False)}</script>
</section>'''

rows = ''.join(f'<tr><td><a href="{s["url"]}">{s["name"]}</a></td><td>{s["note"].split(" · ")[0]}</td><td>{it(s["h"])} cm</td></tr>' for s in sorted(STANDS, key=lambda s: s['h']))

art = f'''
<div class="art">
  <h2>La regola: il tweeter all'altezza delle orecchie.</h2>
  <p>Un diffusore da scaffale ha di solito due altoparlanti: il woofer, più grande, per i bassi e le voci, e il tweeter, piccolo, per le frequenze alte. Il tweeter è molto direzionale: se punta alle tue orecchie senti i dettagli, la voce sta al centro e gli strumenti hanno un posto preciso. Se punta al petto o sopra la testa, il suono diventa più spento e meno a fuoco.</p>
  <p>Per questo l'altezza giusta di uno stand non è un numero fisso: dipende da dove ti siedi e da come è fatto il tuo diffusore. La formula è una sola:</p>
  <p class="note"><b>Altezza dello stand</b> = altezza delle orecchie da seduto − altezza del tweeter dalla base del diffusore − eventuali piedini o punte.</p>
  <p>Alcuni costruttori progettano le casse per essere ascoltate con le orecchie tra il tweeter e il woofer, non esattamente sul tweeter. Se il manuale del tuo diffusore indica un'altezza o un asse d'ascolto, segui quello: basta mettere quella misura al posto dell'altezza del tweeter nel calcolatore.</p>

  <h2>Come prendere le misure.</h2>
  <ol>
    <li><b>Le orecchie.</b> Siediti dove ascolti di solito, nella posizione in cui stai davvero, e fatti misurare da terra al foro dell'orecchio. Su un divano si sta in genere tra 95 e 105 cm, su una poltrona un po' più in alto, su una sedia tra 110 e 120 cm.</li>
    <li><b>Il tweeter.</b> Misura dal piano su cui appoggia il diffusore al centro del tweeter. Nei diffusori da scaffale è quasi sempre tra 18 e 30 cm.</li>
    <li><b>I piedini.</b> Se sotto il diffusore metti punte, coni o piedini, aggiungi la loro altezza: alzano il tweeter anche loro.</li>
  </ol>
  <p>Con un divano e un diffusore da scaffale di media grandezza il risultato cade quasi sempre tra 60 e 75 cm. Ecco perché molti stand in commercio sono alti intorno ai 60-70 cm.</p>

  <h2>Qualche centimetro conta poco, la simmetria molto.</h2>
  <p>Non serve la precisione al millimetro. Da tre metri, una differenza di 5 cm sposta l'asse di un grado appena: non lo sentiresti. Se non trovi l'altezza esatta, scegli uno stand qualche centimetro più basso, non più alto: il tweeter appena sotto le orecchie è la situazione più naturale.</p>
  <p>Conta molto di più che i due diffusori siano <b>alla stessa altezza</b>, alla stessa distanza da te e girati allo stesso modo. Un buon punto di partenza è un triangolo equilatero: i due diffusori e la tua testa ai tre vertici, con le casse leggermente girate verso di te.</p>

  <h2>Se lo stand è troppo basso, inclina il diffusore.</h2>
  <p>Quando le casse stanno su un mobile basso, una mensola o una scrivania, il tweeter finisce sotto le orecchie. In quel caso un <a href="supporti-inclinati-diffusori.html">supporto inclinato</a> punta il diffusore verso l'alto e recupera l'asse d'ascolto senza cambiare mobile. Vale anche al contrario, se le casse sono più in alto di te: il supporto le inclina verso il basso. Se ti serve, lo <a href="su-misura.html">costruisco su misura</a> per la tua cassa.</p>

  <h2>Non solo l'altezza: com'è fatto uno stand buono.</h2>
  <h3>Rigido e stabile</h3>
  <p>Lo stand deve tenere fermo il diffusore. Se il supporto oscilla o vibra insieme alla cassa, i bassi diventano confusi. Per questo costruisco gli stand in legno massello o in multistrato spesso, con basi larghe e incastri, non con tubi leggeri.</p>
  <h3>Un piano della misura giusta</h3>
  <p>Il piano superiore dovrebbe essere grande più o meno quanto la base del diffusore. Non deve combaciare al millimetro: un diffusore che sporge di 2-3 cm, o un piano un po' più grande, vanno benissimo. Se invece il piano è molto più piccolo la cassa è instabile, e se sporge molto davanti crea una superficie che riflette il suono. Quando costruisco uno stand su misura parto proprio dalle misure della base del tuo diffusore.</p>
  <h3>Punte o piedini</h3>
  <p>Sotto lo stand, su moquette o tappeto, le punte attraversano il pelo e appoggiano sul pavimento. Su parquet o piastrelle meglio sottopunte o feltri, per non rovinare il pavimento. Tra stand e diffusore vanno bene piedini in gomma o sughero: tengono ferma la cassa e la staccano dal legno. I miei stand di serie appoggiano direttamente sul legno; piedini, gommini o punte li aggiungo su richiesta, anche a uno stand già pronto.</p>
  <h3>Lontano dalla parete</h3>
  <p>Più il diffusore è vicino alla parete dietro, più i bassi si gonfiano. Se il tuo diffusore ha il foro del reflex sul retro, lascia almeno 30-50 cm dalla parete e poi prova ad avvicinarlo o allontanarlo di qualche centimetro, ascoltando.</p>

  <h2>L'altezza dei miei stand.</h2>
  <p>Questi sono gli stand che costruisco nel laboratorio di Cesena, in ordine di altezza. Se nessuno è quello giusto per te, lo costruisco su misura: altezza, piano e essenza sui tuoi diffusori.</p>
  <table class="htable"><thead><tr><th>Modello</th><th>Legno</th><th>Altezza</th></tr></thead><tbody>{rows}</tbody></table>

''' + shop_box('altezza') + f'''  <h2>Domande frequenti.</h2>
  <div class="faq" style="margin-top:1rem">
    {''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)}
  </div>
</div>'''

hero = '''
<section class="g-hero"><div class="wrap">
  <nav class="crumb" aria-label="Percorso"><a href="./">Home</a><span>›</span><a href="guide.html">Guide</a></nav>
  <h1>A che altezza mettere le casse? <span class="h1s">Come scegliere l'altezza degli stand per diffusori, con il calcolatore</span></h1>
  <p class="lead">La regola è una sola: il tweeter all'altezza delle orecchie. Qui sotto la calcoli in un attimo per il tuo divano e i tuoi diffusori; più giù trovi il perché e gli altri dettagli che fanno suonare bene uno stand.</p>
  <p class="g-meta">Di Fabrizio Berlati · Laboratorio artigiano a Cesena</p>
</div></section>'''

URL = 'https://fabrizioberlati.com/guida-altezza-stand-diffusori.html'
TITLE = "Altezza stand per diffusori: calcolatore e guida"
DESC = "A che altezza mettere le casse? Calcola l'altezza giusta degli stand per i tuoi diffusori e il tuo divano, e scopri come scegliere uno stand che suona bene."
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "Article", "headline": "A che altezza mettere le casse? Come scegliere l'altezza degli stand per diffusori", "description": DESC, "url": URL,
   "inLanguage": "it", "datePublished": "2026-10-29", "dateModified": "2026-10-29", "image": "https://fabrizioberlati.com/images/guida-altezza-3.jpg",
   "author": {"@type": "Person", "name": "Fabrizio Berlati", "url": "https://fabrizioberlati.com/laboratorio.html"},
   "publisher": {"@id": "https://fabrizioberlati.com/#laboratorio"}, "mainEntityOfPage": URL},
  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
  {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://fabrizioberlati.com/"},
    {"@type": "ListItem", "position": 2, "name": "Guide", "item": "https://fabrizioberlati.com/guide.html"},
    {"@type": "ListItem", "position": 3, "name": "Altezza degli stand per diffusori", "item": URL}]},
  {"@type": "FurnitureStore", "@id": "https://fabrizioberlati.com/#laboratorio", "name": "Fabrizio Berlati · Mobili per l'ascolto", "alternateName": "Fabrizio Berlati", "url": "https://fabrizioberlati.com/",
   "telephone": "+39 333 418 8754", "parentOrganization": {"@type": "Organization", "name": "Extrasound Srl", "url": "https://www.extrasound.it/", "vatID": "IT04436860409"}, "address": {"@type": "PostalAddress", "streetAddress": "Via Archimede 605", "postalCode": "47521", "addressLocality": "Cesena", "addressRegion": "FC", "addressCountry": "IT"}}]}

body = hero + '\n<div class="wrap">' + calc + art + '\n</div>'
page('guida-altezza-stand-diffusori.html', TITLE, DESC, ld, body, js='<script src="guide.js?v=1"></script>\n')

# guide aggiuntive (testi in guide_nuove.json)
NUOVE = json.load(open('_strumenti/guide_nuove.json'))
for g in NUOVE:
    url = 'https://fabrizioberlati.com/' + g['fn']
    faq_html = '<div class="faq" style="margin-top:1rem">\n    ' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in g['faq']) + '\n  </div>\n</div>'
    hero_g = f"""
<section class="g-hero"><div class="wrap">
  <nav class="crumb" aria-label="Percorso"><a href="./">Home</a><span>›</span><a href="guide.html">Guide</a></nav>
  <h1>{g['h1']} <span class="h1s">{g['h1s']}</span></h1>
  <p class="lead">{g['lead']}</p>
  <p class="g-meta">Di Fabrizio Berlati · Laboratorio artigiano a Cesena</p>
</div></section>"""
    ldg = {"@context": "https://schema.org", "@graph": [
      {"@type": "Article", "headline": g['h1'], "description": g['desc'], "url": url, "inLanguage": "it",
       "datePublished": g.get('date', '2026-11-03'), "dateModified": g.get('mod', g.get('date', '2026-11-03')), "image": "https://fabrizioberlati.com/" + g['img'],
       "author": {"@type": "Person", "name": "Fabrizio Berlati", "url": "https://fabrizioberlati.com/laboratorio.html"},
       "publisher": {"@id": "https://fabrizioberlati.com/#laboratorio"}, "mainEntityOfPage": url},
      {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g['faq']]},
      {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://fabrizioberlati.com/"},
        {"@type": "ListItem", "position": 2, "name": "Guide", "item": "https://fabrizioberlati.com/guide.html"},
        {"@type": "ListItem", "position": 3, "name": g['crumb'], "item": url}]}]}
    # animazioni: _strumenti/anim/<nome>.html, in alto (hero_anim) o nel testo con <!--ANIM:nome-->
    anim = lambda n: open(f'_strumenti/anim/{n}.html').read().strip()
    fig = anim(g['hero_anim']) if g.get('hero_anim') else f'<figure class="g-fig"><img src="{g["img"]}" alt="{g["img_alt"]}" loading="lazy"></figure>'
    art = re.sub(r'<!--ANIM:([a-z-]+)-->', lambda m: anim(m.group(1)), g['art'])
    art = art.replace('  <h2>Domande frequenti.</h2>', shop_box(g['fn']) + '  <h2>Domande frequenti.</h2>')
    page(g['fn'], g['title'], g['desc'], ldg, hero_g + '\n<div class="wrap">' + fig + art + faq_html + '\n</div>')

# indice delle guide
gl = '''
<section class="g-hero"><div class="wrap">
  <nav class="crumb" aria-label="Percorso"><a href="./">Home</a></nav>
  <h1>Guide <span class="h1s">Consigli pratici per sistemare l'impianto hi-fi e la stanza d'ascolto</span></h1>
  <p class="lead">Quello che ho imparato costruendo mobili, stand e pannelli per gli impianti dei miei clienti: misure, legni, posizionamento. Con qualche strumento per fare i conti in fretta.</p>
</div></section>
<div class="wrap"><div class="glist">
  <a href="guida-altezza-stand-diffusori.html"><div class="ph"><img src="images/guida-altezza-3.jpg" alt="Illustrazione: diffusore sullo stand con il tweeter all'altezza delle orecchie" loading="lazy"></div>
    <h2>A che altezza mettere le casse?</h2><p>La regola del tweeter, come prendere le misure e un calcolatore che ti dice quanto deve essere alto lo stand.</p></a>
''' + ''.join(f'''  <a href="{g['fn']}"><div class="ph"><img src="{g['img']}" alt="{g['img_alt']}" loading="lazy"></div>\n    <h2>{g['h1']}</h2><p>{g['card']}</p></a>\n''' for g in NUOVE) + '''</div></div>'''
ld2 = {"@context": "https://schema.org", "@graph": [
  {"@type": "CollectionPage", "name": "Guide all'impianto hi-fi e alla stanza d'ascolto", "url": "https://fabrizioberlati.com/guide.html",
   "hasPart": [{"@type": "Article", "headline": "A che altezza mettere le casse?", "url": URL}] + [{"@type": "Article", "headline": g["h1"], "url": "https://fabrizioberlati.com/" + g["fn"]} for g in NUOVE]},
  {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://fabrizioberlati.com/"},
    {"@type": "ListItem", "position": 2, "name": "Guide", "item": "https://fabrizioberlati.com/guide.html"}]}]}
page('guide.html', "Guide all'impianto e alla sala d'ascolto · Fabrizio Berlati",
     "Consigli pratici per l'impianto hi-fi e la stanza d'ascolto: altezza degli stand, mobili, legni e acustica, dal laboratorio artigiano di Fabrizio Berlati a Cesena.", ld2, gl)
print('ok')
