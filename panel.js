// Pannello in listarelle: parte di tre quarti, diviso in tre moduli con le listarelle staccate,
// e si ricompone ruotando fino alla vista frontale.
(function(){
  const stage=document.querySelector('.panel3d');
  if(!stage)return;
  const world=stage.querySelector('.pw');
  const W=960,H=270,COLS=96,CW=W/COLS,SEC=COLS/3,MID=H*.52;

  // generatore pseudo-casuale fisso: il pannello è sempre lo stesso
  let seed=7;const rnd=()=>(seed=(seed*16807)%2147483647)/2147483647;
  const woods=['#c99a63','#b07a4a','#d9b688','#8f5a36','#e4c79e','#a8683f','#c48a55','#7a4b2c','#dcb98c','#b98b5e','#9c6b43','#e9d3b0'];
  const blacks=['#1f1c1a','#2a2624','#24211f'];

  // onda sonora: inviluppo fatto di picchi, come nel pannello vero
  const peaks=[[10,.75,3],[18,.5,2.5],[27,.62,2.5],[39,1,3.2],[50,.45,3],[59,.8,2.6],[69,.4,2.4],[76,.32,1.6],[81,.2,1.2]];
  const amp=i=>{if(i<7||i>84)return 0;let a=.07;for(const[c,h,w]of peaks)a=Math.max(a,h*Math.exp(-((i-c)**2)/(2*w*w)));return a*(.62+.38*Math.abs(Math.sin(i*2.3)))};

  const sections=[0,1,2].map(s=>{const g=document.createElement('div');g.className='psec';world.appendChild(g);return g});
  const pieces=[];
  function add(sec,x,y,w,h,z,color,black){
    const d=document.createElement('i');
    d.className=black?'sl blk':'sl';
    d.style.cssText=`left:${x}px;top:${y}px;width:${w}px;height:${h}px;background-color:${color};--d:${black?9:5}px`;
    sections[sec].appendChild(d);
    pieces.push({el:d,z,
      dz:50+rnd()*150, dy:(rnd()-.5)*26, dx:(rnd()-.5)*6, rz:(rnd()-.5)*3,
      delay:rnd()*.22});
  }
  for(let i=0;i<COLS;i++){
    const s=Math.floor(i/SEC),x=i*CW;
    // ogni colonna è fatta di 2-3 listarelle di lunghezza diversa
    let y=0;const n=2+(rnd()<.45?1:0);
    for(let k=0;k<n;k++){
      const h=k===n-1?H-y:Math.round(H*(.22+rnd()*.42));
      if(h<=0)break;
      add(s,x,y,CW-.6,Math.min(h,H-y),rnd()*4,woods[Math.floor(rnd()*woods.length)],false);
      y+=h;if(y>=H)break;
    }
    const a=amp(i);
    if(a>0){
      const h=Math.round(14+a*200),top=Math.round(MID-h/2+(rnd()-.5)*6);
      add(s,x,top,CW-.6,h,8+a*10,blacks[i%3],true);
    }
  }

  const ease=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
  const cl=x=>Math.min(1,Math.max(0,x));
  const END=.86; // listarelle e moduli si chiudono insieme

  function render(t){
    const k=stage.clientWidth/W;
    const r=ease(cl(t));
    world.style.transform=`scale3d(${k},${k},${k}) translate3d(${-40*(1-r)}px,${-10*(1-r)}px,${-260*(1-r)}px) translate(480px,135px) rotateX(${8*(1-r)}deg) rotateY(${-36*(1-r)}deg) translate(-480px,-135px)`;
    const sp=1-ease(cl(t/END));
    sections.forEach((g,s)=>{const o=s-1;g.style.transform=`translate3d(${o*120*sp}px,0,${(s===1?30:-10*o)*sp}px)`});
    for(const p of pieces){
      const q=1-ease(cl((t-p.delay)/(END-p.delay)));
      p.el.style.transform=`translate3d(${p.dx*q}px,${p.dy*q}px,${p.z+p.dz*q}px) rotateZ(${p.rz*q}deg)`;
      
    }
  }

  const DUR=4200;let t0=0,t=0;
  function tick(n){if(!t0)t0=n;t=cl((n-t0)/DUR);render(t);if(t<1)requestAnimationFrame(tick)}
  new ResizeObserver(()=>render(t)).observe(stage);
  if(matchMedia('(prefers-reduced-motion: reduce)').matches){t=1;render(1)}
  else{render(0);setTimeout(()=>requestAnimationFrame(tick),350)}
  stage.addEventListener('click',()=>{if(t>=1){t0=0;t=0;requestAnimationFrame(tick)}});
})();
