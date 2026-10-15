document.documentElement.classList.add('js');
document.querySelectorAll('.yr').forEach(s=>s.textContent=new Date().getFullYear());
// l'immagine ha il clip-path: si osserva il contenitore, non l'immagine stessa
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.querySelectorAll('.pic').forEach(p=>p.classList.add('in'));io.unobserve(e.target)}}),{threshold:.2});
document.querySelectorAll('.pic').forEach(p=>io.observe(p.parentElement));
const dk=document.querySelector('.deck');
if(dk){const sc=dk.querySelector('.scaler'),fit=()=>sc.style.setProperty('--k',dk.clientWidth/480);new ResizeObserver(fit).observe(dk);fit()}
