(function(){
  const sc=document.getElementById('scene'),w=document.getElementById('world'),ph=document.getElementById('phase'),btn=document.getElementById('play'),rg=document.getElementById('scrub');
  const el={f:document.getElementById('pf'),b:document.getElementById('pb'),r:document.getElementById('pr'),l:document.getElementById('pl')};
  const e=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2,rng=(t,a,b)=>Math.min(1,Math.max(0,(t-a)/(b-a)));
  const T=['Cinque pannelli in multistrato da 18 mm: una base e quattro lati.','Il primo lato si alza verso la base.','Il secondo si alza e gli incastri si agganciano.','Il terzo lato chiude la parte posteriore.','L\'ultimo lato completa il Cube.','Extrasound Cube montato, pronto per i tuoi vinili.'];
  let t=0,raf=0,playing=false,last=0;const DUR=10000;
  function fit(){sc.style.setProperty('--k',sc.clientWidth/760);render(t)}
  function render(t){
    const g=(1-e(rng(t,0,.14)))*50,a={f:90*e(rng(t,.18,.36)),r:90*e(rng(t,.38,.56)),b:90*e(rng(t,.58,.76)),l:90*e(rng(t,.78,.94))};
    el.f.style.transform='translateY('+g+'px) rotateX('+a.f+'deg)';
    el.b.style.transform='translateY('+(-g)+'px) rotateX('+(-a.b)+'deg)';
    el.r.style.transform='translateX('+g+'px) rotateY('+(-a.r)+'deg)';
    el.l.style.transform='translateX('+(-g)+'px) rotateY('+a.l+'deg)';
    for(const k in el)el[k].classList.toggle('done',a[k]>=89.9);
    const k=sc.clientWidth/760*(1+.45*e(rng(t,.45,1)));
    w.style.transform='scale('+k+') rotateX('+(60-6*e(t))+'deg) rotateZ('+(-20-22*e(t))+'deg)';
    ph.textContent=T[t<.18?0:t<.38?1:t<.58?2:t<.78?3:t<.95?4:5];
    rg.value=Math.round(t*1000);
  }
  function tick(n){if(!playing)return;t=Math.min(1,t+(n-last)/DUR);last=n;render(t);if(t>=1){playing=false;btn.textContent='Riavvia'}else raf=requestAnimationFrame(tick)}
  function play(){if(t>=1)t=0;playing=true;btn.textContent='Pausa';last=performance.now();cancelAnimationFrame(raf);raf=requestAnimationFrame(tick)}
  function pause(){playing=false;cancelAnimationFrame(raf);btn.textContent=t>=1?'Riavvia':'Riprendi'}
  btn.onclick=()=>playing?pause():play();
  rg.oninput=()=>{pause();t=rg.value/1000;render(t);btn.textContent=t>=1?'Riavvia':'Riprendi'};
  new ResizeObserver(fit).observe(sc);
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce){t=1;fit();btn.textContent='Riavvia'}else{
    fit();new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){o.disconnect();play()}},{threshold:.5}).observe(sc)}
})();
(function(){
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  const st=document.querySelector('.story'),A=st.querySelector('.l-a'),B=st.querySelector('.l-b'),C=st.querySelector('.l-c'),D=st.querySelector('.l-d'),bar=st.querySelector('.bar'),steps=st.querySelectorAll('.step');
  const e=x=>x*x*(3-2*x),seg=(p,a,b)=>e(Math.min(1,Math.max(0,(p-a)/(b-a))));
  function upd(){
    const r=st.getBoundingClientRect(),p=Math.min(1,Math.max(0,-r.top/(st.offsetHeight-innerHeight)));
    const ab=seg(p,.1,.27),bc=seg(p,.36,.55),cd=seg(p,.64,.84);
    B.style.opacity=1;B.style.transform='scale('+(1+ab*.08)+')';
    A.style.opacity=ab;A.style.transform='scale('+(.9+ab*.1)+') rotate('+((1-ab)*-2)+'deg)';
    C.style.clipPath='circle('+(bc*75)+'% at 50% 50%)';
    D.style.clipPath='inset('+((1-cd)*100)+'% 0 0 0)';
    bar.style.width=(p*100)+'%';
    const i=p<.2?0:p<.45?1:p<.72?2:3;steps.forEach((s,k)=>s.classList.toggle('on',k===i));
  }
  addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);upd();
})();
(function(){
  const grid=document.getElementById('grid'),P={
    single:[0,0,0,0,0,0,0,0,1,0,0,0],
    low:[0,0,0,0,0,0,0,0,1,2,1,2],
    col:[2,0,0,0,1,0,0,0,2,0,0,0],
    wall:[1,2,1,2,2,1,2,1,1,2,1,2]};
  let s=P.low.slice();const names=['vuoto','Pioppo','Doussiè'];
  const cells=s.map((_,i)=>{const b=document.createElement('button');b.className='cell';
    b.onclick=()=>{s[i]=(s[i]+1)%3;draw()};grid.appendChild(b);return b});
  function draw(){
    cells.forEach((c,i)=>{c.dataset.s=s[i];c.setAttribute('aria-label','Posizione '+(i+1)+': '+names[s[i]])});
    const a=s.filter(x=>x==1).length,d=s.filter(x=>x==2).length,n=a+d;
    document.getElementById('count').textContent=n?n+(n==1?' modulo':' moduli')+': '+a+' in Pioppo, '+d+' in Doussiè.':'Nessun modulo: tocca una cella per iniziare.';
    const body='Vorrei informazioni su una composizione di '+n+' moduli Extrasound Cube: '+a+' in Pioppo e '+d+' in Doussiè.';
    document.getElementById('req').href='mailto:info@fabrizioberlati.com?subject='+encodeURIComponent('Composizione Extrasound Cube')+'&body='+encodeURIComponent(body);
  }
  document.querySelectorAll('#presets .chip').forEach(b=>b.onclick=()=>{s=P[b.dataset.p].slice();draw()});
  draw();
})();
(function(){
  const z=document.getElementById('zoom'),p=document.getElementById('ess-p'),tabs=document.querySelectorAll('#tabs .chip');
  const M={all:['images/cube-frontale.jpg','Puoi combinare le due essenze nella stessa composizione, come nella foto. Il legno resta protagonista, con struttura e spessori a vista.'],
    pioppo:['images/cube-pioppo.jpg','Il Pioppo ha una superficie chiara e naturale, adatta ad ambienti contemporanei, minimalisti o nordici.'],
    doussie:['images/cube-doussie.jpg','Il Doussiè ha tonalità più calde e una presenza visiva marcata, per chi preferisce il carattere delle essenze scure.']};
  Object.values(M).forEach(m=>{const i=new Image();i.src=m[0]});
  z.style.transition='opacity .3s ease';
  tabs.forEach(b=>b.onclick=()=>{const m=M[b.dataset.e];tabs.forEach(t=>t.setAttribute('aria-pressed',t===b));p.textContent=m[1];
    if(z.getAttribute('src')===m[0])return;
    z.style.opacity=0;setTimeout(()=>{z.src=m[0];z.style.opacity=1},300)});
})();
(function(){
  const dots=document.querySelectorAll('#hot .dot'),cap=document.getElementById('hot-cap');
  dots.forEach(d=>d.onclick=()=>{dots.forEach(x=>x.setAttribute('aria-pressed',x===d));cap.textContent=d.dataset.t});
})();
