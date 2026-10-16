// pagine prodotto: interazioni leggere, solo eventi (nessun ciclo di animazione)
document.querySelectorAll('.gallery').forEach(g=>{
  const chk=()=>{if(!g.querySelector('img'))g.classList.add('none')};
  g.querySelectorAll('img').forEach(i=>i.addEventListener('error',()=>{i.closest('.ph').remove();chk()}));
});
// Wave: dove posizionarlo
(function(){
  const box=document.getElementById('room');if(!box)return;
  const bs=document.querySelectorAll('button[data-r]'),note=document.getElementById('room-note');
  bs.forEach(b=>b.onclick=()=>{
    bs.forEach(x=>x.setAttribute('aria-pressed',x===b));
    box.querySelectorAll('.pan').forEach(p=>p.classList.toggle('on',p.dataset.r===b.dataset.r));
    note.textContent=b.dataset.t;
  });
  bs[0].click();
})();
// Vinyl: senza foto, in cima mostra il disegno del mobile
(function(){const h=document.getElementById('vhero');if(!h)return;const i=h.querySelector('img');
  const fb=()=>{const s=document.querySelector('#cab svg');if(!s)return;const c=s.cloneNode(true);c.querySelectorAll('.lvl').forEach(g=>g.remove());c.style.cssText='display:block;width:100%;height:100%';h.replaceChildren(c);h.style.background='none'};
  if(i.complete&&!i.naturalWidth)fb();else i.addEventListener('error',fb)})();
// Vinyl: essenza e ripiani
(function(){
  const cab=document.getElementById('cab');if(!cab)return;
  const E={
    faggio:{c:['#d9b07c','#c69a64','#b5875a'],dim:'57,6 × 82,5 × 39,6 cm',sh:'53,6 × 39,6 cm (superiore 50,1 × 39,6 cm)',h:['28,4 cm','39 cm'],w:'23 kg'},
    noce:{c:['#7a5236','#6a4630','#593a27'],dim:'58,2 × 85 × 39,5 cm',sh:'53 × 39,5 cm (superiore 49,5 × 39,5 cm)',h:['27,5 cm','41,3 cm'],w:'22 kg'}};
  const set=k=>{const e=E[k];
    document.querySelectorAll('.wd').forEach(p=>p.style.fill=e.c[+p.dataset.t||0]);
    document.querySelectorAll('[data-v]').forEach(s=>{const v=s.dataset.v;s.textContent=v==='h0'?e.h[0]:v==='h1'?e.h[1]:e[v]});
    document.querySelectorAll('[data-e]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.e===k));
    const hi=document.querySelector('#vhero img');if(hi)hi.src=k==='noce'?'images/vinyl-noce-hifi.jpg':'images/vinyl-faggio-pro.jpg';
  };
  document.querySelectorAll('[data-e]').forEach(b=>b.onclick=()=>set(b.dataset.e));
  set('faggio');
  const lb=document.querySelectorAll('[data-l]');
  const pick=i=>{lb.forEach(b=>b.setAttribute('aria-pressed',b.dataset.l===i));cab.querySelectorAll('.lvl').forEach(g=>g.classList.toggle('on',g.dataset.l===i))};
  lb.forEach(b=>b.onclick=()=>pick(b.dataset.l));
  cab.querySelectorAll('.lvl').forEach(g=>g.onclick=()=>pick(g.dataset.l));
  pick('0');
})();
