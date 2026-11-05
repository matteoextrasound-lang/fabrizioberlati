# Manutenzione di fabrizioberlati.com

Questa cartella non viene pubblicata (GitHub Pages ignora le cartelle che iniziano con "_").

## Regola fissa: il sito è in due lingue

- Le pagine italiane sono nella radice del sito, quelle inglesi in `/en/`.
- Le pagine inglesi **non si modificano a mano**: si generano da quelle italiane con `python3 _strumenti/traduzione/build_en.py`.
- Ogni modifica a una pagina italiana va seguita, nello stesso lavoro, dalla rigenerazione dell'inglese.
- Il comando segnala i "testi non tradotti": vanno aggiunti in `_strumenti/traduzione/extra.json` (testo italiano esatto → inglese) e si rilancia finché il numero è 0.
- Le correzioni a una traduzione esistente vanno in `_strumenti/traduzione/fix.json`.
- Glossario e tono dell'inglese: `_strumenti/traduzione/GLOSSARY.md`.
- Testi dentro i file JavaScript (calcolatore, Vinyl, Cube): coppie italiano/inglese in `js_guide.json`, `js_prod.json`, `js_cube.json`; generano `guide-en.js`, `prod-en.js`, `cube-en.js`.
- Una pagina italiana nuova va aggiunta alla tabella `SLUG` in `build_en.py` con il suo indirizzo inglese.
- Il comando aggiorna anche `sitemap.xml` (con le alternative di lingua), i tag hreflang e il selettore IT/EN nel menu.

## Ordine dei comandi

1. Se cambiano le guide: `python3 _strumenti/build_guida.py` (la guida all'altezza è nello script; le altre guide sono in `_strumenti/guide_nuove.json`)
2. Sempre, alla fine: `python3 _strumenti/traduzione/build_en.py`

## Altre regole del sito

- Pubblicazione: si lavora sul ramo `bozza-artigiano`; su `main` (sito pubblico) solo quando il proprietario dice "pubblica".
- Non cancellare `googleb1674c031429042a.html` (verifica di Search Console).
- Niente anteprime social (Open Graph).
- Nome dell'attività: "Fabrizio Berlati · Mobili per l'ascolto" (in inglese "Furniture for listening").
- Stand: di serie appoggiano sul legno; piedini o punte su richiesta. Vanno bene anche diffusori che sporgono di 2-3 cm dal piano.
- I supporti inclinati non vanno presentati come "per Argon": sono per qualsiasi diffusore da scaffale.
- Piano SEO e stato degli obiettivi: documento "Piano SEO fabrizioberlati.com" (Claude Docs).
- Pagine categoria: in fondo hanno la sezione «Come scegliere…» con domande frequenti (classe `catguide`), anche nei dati strutturati.
- Ogni prodotto nuovo va su fabrizioberlati.com (prima persona, accento sull'artigiano e sul su misura, scontorno solo per la scheda in categoria) e su extrasound.it in bozza (terza persona, foto originali senza scontorno, nessuna foto nel testo, link alla pagina di Fabrizio). I due testi devono essere scritti da zero: frasi in comune sotto il 5%.
