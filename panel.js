// Pannello in listarelle disegnato su un'unica tela (canvas): leggero, si muove solo durante
// l'animazione e poi resta un'immagine ferma. Parte di tre quarti, con i tre moduli separati e
// le listarelle staccate, e si ricompone ruotando fino alla vista frontale.
(function(){
  const stage=document.querySelector('.panel3d');
  if(!stage)return;
  const cv=document.createElement('canvas');stage.appendChild(cv);
  const ctx=cv.getContext('2d');
  const W=960,H=270,VX=-36,VY=-80,VW=1032,VH=372,COLS=72,CW=W/COLS,SEC=COLS/3,MID=H*.52,F=2000;

  let seed=7;const rnd=()=>(seed=(seed*16807)%2147483647)/2147483647;
  const woods=['#c99a63','#b07a4a','#d9b688','#8f5a36','#e4c79e','#a8683f','#c48a55','#7a4b2c','#dcb98c','#9c6b43','#e9d3b0'];
  const peaks=[[7,.75,2.4],[13,.5,2],[20,.62,2],[29,1,2.4],[37,.45,2.2],[44,.8,2],[51,.4,1.8],[57,.32,1.3],[61,.2,1]];
  const amp=i=>{if(i<5||i>63)return 0;let a=.07;for(const[c,h,w]of peaks)a=Math.max(a,h*Math.exp(-((i-c)**2)/(2*w*w)));return a*(.62+.38*Math.abs(Math.sin(i*2.3)))};

  const P=[];
  const add=(s,x,y,w,h,z,col,blk)=>P.push({s,x,y,w,h,z,col,blk,dz:50+rnd()*150,dy:(rnd()-.5)*26,dx:(rnd()-.5)*6,d:rnd()*.14});
  for(let i=0;i<COLS;i++){
    const s=Math.floor(i/SEC),x=i*CW;
    let y=0;const n=2+(rnd()<.35?1:0);
    for(let k=0;k<n&&y<H;k++){const h=k===n-1?H-y:Math.round(H*(.25+rnd()*.4));add(s,x,y,CW-.5,Math.min(h,H-y),rnd()*4,woods[Math.floor(rnd()*woods.length)],0);y+=h}
    const a=amp(i);
    if(a>0){const h=Math.round(14+a*200);add(s,x,Math.round(MID-h/2+(rnd()-.5)*6),CW-.5,h,8+a*10,'#221f1d',1)}
  }

  const ease=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
  const out=x=>1-Math.pow(1-x,4);
  const cl=x=>Math.min(1,Math.max(0,x));
  let k=1,dpr=1;
  function fit(){
    dpr=Math.min(2,devicePixelRatio||1);k=stage.clientWidth/VW;
    cv.width=Math.round(stage.clientWidth*dpr);cv.height=Math.round(stage.clientWidth*VH/VW*dpr);
    draw(t);
  }

  let t=0;
  function draw(t){
    const r=1-ease(cl(t)),sp=1-ease(cl(t/.86));
    const a=-36*r*Math.PI/180,b=3*r*Math.PI/180,ca=Math.cos(a),sa=Math.sin(a),cb=Math.cos(b),sb=Math.sin(b);
    const tx=-40*r,ty=-10*r,tz=-260*r;
    // punto del pannello -> schermo (stessa prospettiva del CSS 3D)
    const pr=(x,y,z)=>{
      let X=x-480,Y=y-135,Z=z;
      const X1=X*ca+Z*sa,Z1=-X*sa+Z*ca;
      const Y2=Y*cb-Z1*sb,Z2=Y*sb+Z1*cb;
      X=X1+tx;Y=Y2+ty;Z=Z2+tz;
      const s=F/(F-Z);
      return [(480+X*s-VX)*k*dpr,(135+Y*s-VY)*k*dpr,Z];
    };
    const quad=(p,col)=>{ctx.fillStyle=col;ctx.beginPath();ctx.moveTo(p[0][0],p[0][1]);for(let i=1;i<4;i++)ctx.lineTo(p[i][0],p[i][1]);ctx.closePath();ctx.fill()};
    ctx.clearRect(0,0,cv.width,cv.height);
    const secOff=s=>[(s-1)*120*sp,(s===1?30:-10*(s-1))*sp];

    // i tre telai di supporto
    for(let s=0;s<3;s++){
      const[ox,oz]=secOff(s),x0=s*320+ox,z=oz-6;
      quad([pr(x0,0,z),pr(x0+320,0,z),pr(x0+320,H,z),pr(x0,H,z)],'#ddcfb8');
      const f=10;ctx.globalAlpha=.9;
      quad([pr(x0,0,z),pr(x0+320,0,z),pr(x0+320,f,z),pr(x0,f,z)],'#c7ac88');
      quad([pr(x0,H-f,z),pr(x0+320,H-f,z),pr(x0+320,H,z),pr(x0,H,z)],'#c7ac88');
      quad([pr(x0,0,z),pr(x0+f,0,z),pr(x0+f,H,z),pr(x0,H,z)],'#c7ac88');
      quad([pr(x0+320-f,0,z),pr(x0+320,0,z),pr(x0+320,H,z),pr(x0+320-f,H,z)],'#c7ac88');
      ctx.globalAlpha=1;
    }
    // listarelle: le più lontane per prime
    const L=P.map(p=>{
      const q=1-out(cl((t-p.d)/(.86-p.d))),[ox,oz]=secOff(p.s);
      return {p,x:p.x+ox+p.dx*q,y:p.y+p.dy*q,z:p.z+oz+p.dz*q};
    }).sort((u,v)=>u.z-v.z);
    for(const o of L){
      const{p,x,y,z}=o;
      if(p.blk){ // fianco visibile delle listarelle nere in rilievo
        quad([pr(x+p.w,y,z),pr(x+p.w,y,z-9),pr(x+p.w,y+p.h,z-9),pr(x+p.w,y+p.h,z)],'#100f0e');
        quad([pr(x,y,z),pr(x+p.w,y,z),pr(x+p.w,y,z-9),pr(x,y,z-9)],'#3a3532');
      }
      quad([pr(x,y,z),pr(x+p.w,y,z),pr(x+p.w,y+p.h,z),pr(x,y+p.h,z)],p.col);
    }
  }

  const DUR=4200;let t0=0,raf=0;
  function tick(n){if(!t0)t0=n;t=cl((n-t0)/DUR);draw(t);if(t<1)raf=requestAnimationFrame(tick)}
  function play(){cancelAnimationFrame(raf);t0=0;t=0;raf=requestAnimationFrame(tick)}
  new ResizeObserver(fit).observe(stage);fit();
  if(matchMedia('(prefers-reduced-motion: reduce)').matches){t=1;draw(1)}
  else new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){o.disconnect();setTimeout(play,250)}},{threshold:.3}).observe(stage);
  stage.addEventListener('click',play);
})();
