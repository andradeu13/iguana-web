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
    const label = document.createElement('span');
    label.className = 'p-cursor-label';
    ball.appendChild(label);
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
      const zone = e.target.closest('[data-cursor]');
      if(zone){ label.textContent = zone.dataset.cursor; ball.classList.add('has-label'); ball.classList.remove('is-hover'); return; }
      ball.classList.remove('has-label');
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

  /* ---------- carrusel de casos: arrastrar, auto-avance, puntos ---------- */
  document.querySelectorAll('[data-carousel]').forEach(root=>{
    const track = root.querySelector('.p-track');
    const prev = root.querySelector('[data-prev]');
    const next = root.querySelector('[data-next]');
    const dotsWrap = root.querySelector('.p-dots');
    if(!track) return;
    const cards = Array.from(track.querySelectorAll('.p-case'));
    const stepW = ()=> (cards[0] ? cards[0].offsetWidth : 300) + (parseFloat(getComputedStyle(track).columnGap) || 22);
    const maxIdx = ()=> Math.max(0, Math.round((track.scrollWidth - track.clientWidth) / stepW()));
    const current = ()=> Math.round(track.scrollLeft / stepW());

    function goTo(i){
      const n = maxIdx();
      if(i > n) i = 0;
      if(i < 0) i = n;
      track.scrollTo({ left: i * stepW(), behavior: reduce ? 'auto' : 'smooth' });
    }

    // puntos indicadores
    let dots = [];
    function buildDots(){
      if(!dotsWrap) return;
      dotsWrap.innerHTML = '';
      dots = [];
      for(let i = 0; i <= maxIdx(); i++){
        const d = document.createElement('button');
        d.type = 'button'; d.className = 'p-dot';
        d.setAttribute('aria-label', 'Ir a la tarjeta ' + (i + 1));
        d.addEventListener('click', ()=>{ goTo(i); restart(); });
        dotsWrap.appendChild(d); dots.push(d);
      }
      syncDots();
    }
    function syncDots(){
      const c = current();
      dots.forEach((d, i)=> d.classList.toggle('is-active', i === c));
    }
    track.addEventListener('scroll', ()=> requestAnimationFrame(syncDots), { passive:true });

    // arrastrar con el mouse (en touch el scroll nativo ya funciona)
    let down = false, startX = 0, startLeft = 0, moved = 0;
    track.addEventListener('pointerdown', e=>{
      if(e.pointerType !== 'mouse') return;
      down = true; moved = 0; startX = e.clientX; startLeft = track.scrollLeft;
      track.style.scrollBehavior = 'auto';
    });
    window.addEventListener('pointermove', e=>{
      if(!down) return;
      const dx = e.clientX - startX;
      moved = Math.max(moved, Math.abs(dx));
      if(moved > 4) track.classList.add('is-dragging');
      track.scrollLeft = startLeft - dx;
    });
    window.addEventListener('pointerup', ()=>{
      if(!down) return;
      down = false;
      track.style.scrollBehavior = '';
      track.classList.remove('is-dragging');
      if(moved > 4){
        const dir = track.scrollLeft > startLeft ? 0.3 : -0.3;   // se acomoda a la tarjeta más cercana en la dirección del gesto
        goTo(Math.round(track.scrollLeft / stepW() + dir));
      }
      restart();
    });
    track.addEventListener('dragstart', e=> e.preventDefault());

    // auto-avance que se pausa al pasar el mouse o fuera de pantalla
    let timer = null, hovering = false, visible = false;
    function tick(){ if(!hovering && visible && !down) goTo(current() + 1); }
    function restart(){ clearInterval(timer); if(!reduce) timer = setInterval(tick, 4500); }
    root.addEventListener('mouseenter', ()=> hovering = true);
    root.addEventListener('mouseleave', ()=> hovering = false);
    new IntersectionObserver(es=> es.forEach(e=> visible = e.isIntersecting), { threshold: .4 }).observe(track);

    if(prev) prev.addEventListener('click', ()=>{ goTo(current() - 1); restart(); });
    if(next) next.addEventListener('click', ()=>{ goTo(current() + 1); restart(); });
    buildDots(); restart();
    window.addEventListener('resize', buildDots);
  });

  /* ---------- preloader: se retira al cargar ---------- */
  (function(){
    const done = ()=> document.documentElement.classList.add('is-loaded');
    if(reduce) return done();
    const t0 = performance.now();
    const finish = ()=> setTimeout(done, Math.max(0, 650 - (performance.now() - t0)));
    if(document.readyState === 'complete') finish(); else window.addEventListener('load', finish);
    setTimeout(done, 2500);   // por si alguna fuente externa tarda
  })();

  /* ---------- títulos: cada palabra sube desde una máscara ---------- */
  function splitWords(el){
    let n = 0;
    (function walk(node){
      Array.from(node.childNodes).forEach(ch=>{
        if(ch.nodeType === 3){
          const frag = document.createDocumentFragment();
          ch.textContent.split(/(\s+)/).forEach(part=>{
            if(!part) return;
            if(/^\s+$/.test(part)){ frag.appendChild(document.createTextNode(part)); return; }
            const w = document.createElement('span'); w.className = 'p-w';
            const inner = document.createElement('span'); inner.textContent = part;
            inner.style.setProperty('--d', n++);
            w.appendChild(inner); frag.appendChild(w);
          });
          ch.replaceWith(frag);
        } else if(ch.nodeType === 1 && !ch.classList.contains('p-count') && !ch.classList.contains('p-star')){
          walk(ch);
        }
      });
    })(el);
    el.classList.add('p-split');
  }
  const inView = (els, cls, opts)=>{
    const io = new IntersectionObserver(es=> es.forEach(e=>{
      if(e.isIntersecting){ e.target.classList.add(cls || 'is-in'); io.unobserve(e.target); }
    }), opts || { threshold: .2, rootMargin: '0px 0px -8% 0px' });
    els.forEach(el=> io.observe(el));
  };
  const titles = document.querySelectorAll('.p-stat h2, .p-head h2, .p-cases-top h2, .p-wave-title, .final-cta h2');
  if(!reduce) titles.forEach(splitWords);
  inView(titles);

  /* ---------- imágenes que se destapan, tiles que crecen ---------- */
  const medias = document.querySelectorAll('.p-panel-item .p-media, .p-persona .p-media, .p-resource .p-media');
  medias.forEach(m=> m.classList.add('p-unveil'));
  inView(medias);
  inView(document.querySelectorAll('.p-grow'));

  /* ---------- números apilados: cada tarjeta entra rotada y se endereza ---------- */
  (function(){
    const cards = document.querySelectorAll('.p-num-card');
    if(!cards.length || reduce) return;
    const items = Array.from(cards).map((c, i)=> ({ c, item: c.parentElement, rot: i % 2 ? 9 : -9 }));
    let ticking = false;
    function update(){
      const vh = window.innerHeight;
      items.forEach(({ c, item, rot }, i)=>{
        const r = item.getBoundingClientRect();
        // progreso 0→1 mientras la tarjeta sube desde el fondo de la pantalla hasta su punto fijo
        const p = Math.min(Math.max((vh - r.top) / (vh * .75), 0), 1);
        const e = 1 - Math.pow(1 - p, 3);
        // la tarjeta de abajo se hunde un poco cuando llega la siguiente
        const nx = items[i + 1];
        let s = 1;
        if(nx){
          const nr = nx.item.getBoundingClientRect();
          const np = Math.min(Math.max((vh - nr.top) / (vh * .75), 0), 1);
          s = 1 - np * .06;
        }
        c.style.transform = `translateY(${(1 - e) * 22}%) rotate(${(1 - e) * rot}deg) scale(${s})`;
      });
      ticking = false;
    }
    window.addEventListener('scroll', ()=>{ if(!ticking){ requestAnimationFrame(update); ticking = true; } }, { passive:true });
    window.addEventListener('resize', update);
    update();
  })();

  /* ---------- parallax suave del hero y de las tarjetas de casos ---------- */
  if(!reduce && window.gsap && window.ScrollTrigger){
    gsap.registerPlugin(ScrollTrigger);
    gsap.utils.toArray('.p-case').forEach((el, i)=>{
      gsap.from(el, { y: 60 + i * 20, opacity: 0, duration: .9, ease: 'power3.out', delay: i * .08,
        scrollTrigger: { trigger: el.parentElement, start: 'top 85%' } });
    });
    gsap.to('.p-hero h1', { yPercent: -20, opacity: .3, ease: 'none',
      scrollTrigger: { trigger: '.p-hero', start: 'top top', end: 'bottom top', scrub: true } });
    gsap.utils.toArray('.p-rail').forEach((r, i)=>{
      gsap.fromTo(r, { x: i % 2 ? -80 : 80 }, { x: i % 2 ? 80 : -80, ease: 'none',
        scrollTrigger: { trigger: '.p-rails', start: 'top bottom', end: 'bottom top', scrub: true } });
    });
  }
})();
