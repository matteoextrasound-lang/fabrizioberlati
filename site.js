document.documentElement.classList.add('js');
document.querySelectorAll('.yr').forEach(s=>s.textContent=new Date().getFullYear());
// l'immagine ha il clip-path: si osserva il contenitore, non l'immagine stessa
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.querySelectorAll('.pic').forEach(p=>p.classList.add('in'));io.unobserve(e.target)}}),{threshold:.2});
document.querySelectorAll('.pic').forEach(p=>io.observe(p.parentElement));
const dk=document.querySelector('.deck');
if(dk){const sc=dk.querySelector('.scaler'),fit=()=>sc.style.setProperty('--k',dk.clientWidth/480);new ResizeObserver(fit).observe(dk);fit()}
// menu Prodotti: sui touch il primo tocco apre la tendina, il secondo segue il link
document.querySelectorAll('.dd-t').forEach(t=>t.addEventListener('click',e=>{
  if(matchMedia('(hover:none)').matches){const d=t.parentElement;if(!d.classList.contains('open')){e.preventDefault();d.classList.add('open')}}}));
document.addEventListener('click',e=>{if(!e.target.closest('.dd'))document.querySelectorAll('.dd.open').forEach(d=>d.classList.remove('open'))});
// home: mostra i prodotti a gruppi di 6, gli altri restano nella pagina (e per Google) ma nascosti
const hc=document.getElementById('home-cards'),hb=document.getElementById('more-cards');
if(hc&&hb){const cs=[...hc.children],step=6;let n=step;
  const upd=()=>{cs.forEach((c,i)=>c.hidden=i>=n);hb.hidden=n>=cs.length};
  hb.addEventListener('click',()=>{const first=n;n+=step;upd();cs[first]&&cs[first].focus({preventScroll:true})});upd()}
// telefono: barra "Acquista" fissa in basso quando il pulsante principale è uscito dallo schermo
const bb=document.querySelector('.buybar'),buy=document.querySelector('.ctas .btn-buy');
if(bb&&buy){document.body.classList.add('has-buybar');
  new IntersectionObserver(es=>{const e=es[0];bb.classList.toggle('on',!e.isIntersecting&&e.boundingClientRect.top<0)}).observe(buy)}
// categorie: la riga dei filtri scorre fino al filtro attivo
const ac=document.querySelector('.catchips a[aria-current=page]');if(ac)ac.parentElement.scrollLeft=ac.offsetLeft-24;
// GoatCounter: conta i clic che portano fuori dal sito (Extrasound, WhatsApp, email) come eventi.
// Nome evento = destinazione, provenienza = pagina da cui è partito il clic.
const gcOut=a=>{try{const h=a.href;let p;
  if(/^https?:\/\/(www\.)?extrasound\.it/i.test(h)){const u=new URL(h);p='extrasound'+(u.pathname==='/'&&u.search?'/?'+u.searchParams.get('s'):u.pathname.replace(/\/$/,'')||'/')}
  else if(/^https:\/\/wa\.me\//.test(h))p='contatto/whatsapp';
  else if(/^mailto:/i.test(h))p='contatto/email';
  else if(/^tel:/i.test(h))p='contatto/telefono';
  if(!p||!window.goatcounter||!goatcounter.count)return;
  goatcounter.count({path:p,title:(a.textContent||'').trim().slice(0,80),referrer:location.pathname,event:true})}catch(_){}};
['click','auxclick'].forEach(t=>document.addEventListener(t,e=>{const a=e.target.closest&&e.target.closest('a[href]');if(a)gcOut(a)},true));
// Galleria a schermo intero nelle schede prodotto: clic su una foto, poi frecce, tastiera o scorrimento col dito.
(()=>{const hero=document.querySelector('.pp-hero');if(!hero)return;
const imgs=[...document.querySelectorAll('.pp-hero .ph img, .gallery .ph img')];if(!imgs.length)return;
const en=document.documentElement.lang==='en';const T=en?{c:'Close',p:'Previous photo',n:'Next photo',o:'Open photo'}:{c:'Chiudi',p:'Foto precedente',n:'Foto successiva',o:'Apri la foto'};
const lb=document.createElement('div');lb.className='lb';lb.hidden=true;lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');
lb.innerHTML=`<button class="lb-x" type="button" aria-label="${T.c}">×</button><button class="lb-p" type="button" aria-label="${T.p}">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-n" type="button" aria-label="${T.n}">›</button>`;
document.body.appendChild(lb);const big=lb.querySelector('img'),cap=lb.querySelector('figcaption');let i=0,last=null;
const show=k=>{i=(k+imgs.length)%imgs.length;big.src=imgs[i].currentSrc||imgs[i].src;big.alt=imgs[i].alt;cap.textContent=(imgs.length>1?(i+1)+' / '+imgs.length+(imgs[i].alt?' · ':''):'')+imgs[i].alt};
const open=k=>{last=document.activeElement;show(k);lb.hidden=false;document.documentElement.classList.add('lb-on');lb.querySelector('.lb-x').focus()};
const close=()=>{lb.hidden=true;document.documentElement.classList.remove('lb-on');last&&last.focus()};
if(imgs.length<2)lb.classList.add('one');
imgs.forEach((im,k)=>{const ph=im.closest('.ph');ph.classList.add('zoom');ph.tabIndex=0;ph.setAttribute('role','button');ph.setAttribute('aria-label',T.o+(im.alt?': '+im.alt:''));
ph.addEventListener('click',()=>open(k));ph.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open(k)}})});
lb.querySelector('.lb-x').onclick=close;lb.querySelector('.lb-p').onclick=()=>show(i-1);lb.querySelector('.lb-n').onclick=()=>show(i+1);
lb.addEventListener('click',e=>{if(e.target===lb||e.target.tagName==='FIGURE')close()});
document.addEventListener('keydown',e=>{if(lb.hidden)return;if(e.key==='Escape')close();else if(e.key==='ArrowLeft')show(i-1);else if(e.key==='ArrowRight')show(i+1);
else if(e.key==='Tab'){const b=[...lb.querySelectorAll('button')].filter(x=>x.offsetParent);const a=b.indexOf(document.activeElement);e.preventDefault();b[(a+(e.shiftKey?-1:1)+b.length)%b.length].focus()}});
let x0=null,y0=0;lb.addEventListener('touchstart',e=>{x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
lb.addEventListener('touchend',e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy))show(i+(dx<0?1:-1));else if(dy>90&&Math.abs(dy)>Math.abs(dx))close();x0=null},{passive:true});
})();
