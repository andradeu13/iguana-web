/* ============================================================
   perk-home.js — interacciones del home con estructura tipo Perk
============================================================ */
(function(){
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- cursor: bola que sigue al mouse con suavizado ---------- */
  (function(){
    if(!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
    const ball = document.createElement('div');
    ball.className = 'p-cursor';
    ball.setAttribute('aria-hidden', 'true');
    document.body.appendChild(ball);
    document.body.classList.add('p-has-cursor');

    let x = -100, y = -100, cx = x, cy = y;
    const ease = reduce ? 1 : 0.2;

    window.addEventListener('mousemove', e=>{
      x = e.clientX; y = e.clientY;
      ball.classList.add('is-visible');
    }, { passive:true });
    document.addEventListener('mouseleave', ()=> ball.classList.remove('is-visible'));
    window.addEventListener('mousedown', ()=> ball.classList.add('is-down'));
    window.addEventListener('mouseup', ()=> ball.classList.remove('is-down'));

    const interactive = 'a, button, [role="tab"], input, select, textarea, label';
    document.addEventListener('mouseover', e=>{
      if(e.target.closest(interactive)) ball.classList.add('is-hover');
    });
    document.addEventListener('mouseout', e=>{
      if(e.target.closest(interactive) && !(e.relatedTarget && e.relatedTarget.closest && e.relatedTarget.closest(interactive))){
        ball.classList.remove('is-hover');
      }
    });

    (function loop(){
      cx += (x - cx) * ease;
      cy += (y - cy) * ease;
      ball.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
      requestAnimationFrame(loop);
    })();
  })();

  /* ---------- hero: palabras del título entran una por una ---------- */
  document.querySelectorAll('.p-hero h1 .word').forEach((w, i)=>{
    w.style.animationDelay = (0.1 + i * 0.07) + 's';
  });

  /* ---------- hero: la imagen crece un poco al hacer scroll ---------- */
  (function(){
    const media = document.querySelector('.p-hero-media');
    if(!media || reduce) return;
    let ticking = false;
    function update(){
      const r = media.getBoundingClientRect();
      const vh = window.innerHeight;
      const p = Math.min(Math.max((vh - r.top) / vh, 0), 1);
      media.style.transform = `scale(${0.9 + p * 0.1})`;
      ticking = false;
    }
    window.addEventListener('scroll', ()=>{ if(!ticking){ requestAnimationFrame(update); ticking = true; } }, { passive:true });
    update();
  })();

  /* ---------- contadores: suben hasta la cifra al entrar en pantalla ---------- */
  (function(){
    const fmt = new Intl.NumberFormat('es-EC');
    const els = document.querySelectorAll('.p-count[data-to]');
    if(!els.length) return;
    function run(el){
      const from = parseFloat(el.dataset.from || 0);
      const to = parseFloat(el.dataset.to);
      if(reduce){ el.textContent = fmt.format(to); return; }
      const dur = 1800, t0 = performance.now();
      (function tick(now){
        const p = Math.min((now - t0) / dur, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = fmt.format(Math.round(from + (to - from) * eased));
        if(p < 1) requestAnimationFrame(tick);
      })(t0);
    }
    const io = new IntersectionObserver(entries=>{
      entries.forEach(e=>{ if(e.isIntersecting){ run(e.target); io.unobserve(e.target); } });
    }, { threshold: 0.6 });
    els.forEach(el=> io.observe(el));
  })();

  /* ---------- tabs: indicador que se desliza + contenido que entra ---------- */
  document.querySelectorAll('[data-tabs]').forEach(root=>{
    const tabs = Array.from(root.querySelectorAll('[role="tab"]'));
    const ind = root.querySelector('.p-tab-ind');
    function moveInd(tab){
      if(!ind) return;
      ind.style.width = tab.offsetWidth + 'px';
      ind.style.transform = `translateX(${tab.offsetLeft}px)`;
    }
    function select(tab, focus){
      tabs.forEach(t=>{
        const on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        const panel = document.getElementById(t.getAttribute('aria-controls'));
        if(!panel) return;
        panel.hidden = !on;
        if(on){ panel.classList.remove('is-entering'); void panel.offsetWidth; panel.classList.add('is-entering'); }
      });
      moveInd(tab);
      if(focus) tab.focus();
    }
    tabs.forEach((t, i)=>{
      t.addEventListener('click', ()=> select(t));
      t.addEventListener('keydown', e=>{
        if(e.key === 'ArrowRight' || e.key === 'ArrowLeft'){
          e.preventDefault();
          const n = (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
          select(tabs[n], true);
        }
      });
    });
    const first = tabs.find(t=> t.getAttribute('aria-selected') === 'true') || tabs[0];
    requestAnimationFrame(()=> moveInd(first));
    window.addEventListener('resize', ()=> moveInd(tabs.find(t=> t.getAttribute('aria-selected') === 'true')));
  });

  /* ---------- carrusel de casos: flechas mueven una tarjeta ---------- */
  document.querySelectorAll('[data-carousel]').forEach(root=>{
    const track = root.querySelector('.p-track');
    const prev = root.querySelector('[data-prev]');
    const next = root.querySelector('[data-next]');
    if(!track) return;
    function step(dir){
      const card = track.querySelector('.p-case');
      const gap = parseFloat(getComputedStyle(track).columnGap) || 22;
      track.scrollBy({ left: dir * ((card ? card.offsetWidth : 300) + gap), behavior: reduce ? 'auto' : 'smooth' });
    }
    if(prev) prev.addEventListener('click', ()=> step(-1));
    if(next) next.addEventListener('click', ()=> step(1));
  });
})();
