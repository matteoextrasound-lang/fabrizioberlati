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
