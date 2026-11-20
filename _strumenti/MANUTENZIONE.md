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
2. Sempre: `python3 _strumenti/img_dims.py` (misure delle foto e prima foto caricata subito)
3. Sempre, alla fine: `python3 _strumenti/traduzione/build_en.py`

- I vecchi indirizzi si tengono come pagine di rimando (vedi `supporti-inclinati-argon.html`: meta refresh + canonical + noindex); `build_en.py` le salta. Non vanno nella sitemap.
- Link alla home: sempre `./` (o `./#prodotti`), mai `index.html`.
- Title fino a ~60 caratteri, meta description fino a 160.

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

## Schede prodotto da telefono (13/11)
- Il pulsante principale è «Acquista su Extrasound» (`class="btn btn-buy"`, nuova scheda); «Chiedi informazioni» è un link.
- Ogni scheda con prezzo ha prima di `</main>` la barra `<div class="buybar">` (prezzo + «Acquista»), che compare sul telefono quando il pulsante principale esce dallo schermo (site.js).
- Versioni attuali: craft.css?v=25, site.js?v=6, guide.css?v=4, anim.css?v=1.

## Conteggio dei clic in uscita (GoatCounter)
`site.js` registra come evento GoatCounter ogni clic verso extrasound.it (nome `extrasound/<percorso>`, oppure `extrasound/?<ricerca>`), WhatsApp (`contatto/whatsapp`), email (`contatto/email`) e telefono (`contatto/telefono`). Come provenienza registra la pagina da cui parte il clic. Vale anche per i link aggiunti in futuro, senza fare niente. I clic dal browser escluso (skipgc) non vengono contati.

## IndexNow (Bing)
Il file `297ad8a6ffd21d440f2e547aeae304d5.txt` nella root è la chiave IndexNow: non va tolto né rinominato. Dopo ogni pubblicazione su `main`, il workflow `.github/workflows/indexnow.yml` parte da solo, aspetta 2 minuti che GitHub Pages pubblichi e invia a IndexNow le pagine .html cambiate in quel commit (escluse le pagine di rimando). Il risultato si vede nella scheda Actions del repository. Su Google la richiesta di indicizzazione resta manuale dalla Search Console.

## Inviti al lavoro su misura
- Schede prodotto: sotto i pulsanti c'è `<p class="sumisura">` con il link a su-misura.html. Va messo anche nelle schede nuove.
- Guide: la frase su misura sta nel riquadro negozio, dal dizionario `SUMISURA` in `build_guida.py` (chiave = nome file della guida, o 'altezza'). Le guide che non c'entrano con i mobili non la hanno.

## Link da Extrasound (20/11/2026)
In fondo alla descrizione di 27 schede Extrasound dei prodotti di Fabrizio c'è un paragrafo marcato `<!-- link-fabrizioberlati -->` con il link alla scheda corrispondente su questo sito (nuova scheda). Il testo originale di ogni scheda è salvato nel campo personalizzato `_backup_descrizione_20261120` del prodotto. Se una pagina di questo sito cambia nome, va aggiornato anche il link su Extrasound. Zeta e Line (bozze 57734 e 57735) non hanno il link.
