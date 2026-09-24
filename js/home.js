/* ============================================================
   home.js — animaciones exclusivas del home
   Requiere GSAP + ScrollTrigger cargados antes (defer en index.html).
============================================================ */

/* ---------- cifra grande de datos: cuenta de 0 a 21 al entrar en pantalla ---------- */
(function(){
  const el = document.getElementById('arcCount');
  if(!el || typeof IntersectionObserver === 'undefined') return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const to = parseInt(el.textContent, 10);
  el.textContent = '0';
  const io = new IntersectionObserver(entries=>{
    if(!entries[0].isIntersecting) return;
    io.disconnect();
    const t0 = performance.now(), dur = 1600;
    (function tick(now){
      const p = Math.min((now - t0) / dur, 1);
      el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3)));
      if(p < 1) requestAnimationFrame(tick);
    })(t0);
  }, { threshold: 0.5 });
  io.observe(el);
})();

window.addEventListener('DOMContentLoaded', ()=>{
  if(typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;
  gsap.registerPlugin(ScrollTrigger);

  /* ---------- pain-cards: carpeta apilada con pestañas, al hacer scroll ----------
     Todo el efecto es CSS (position:sticky con "top" escalonado por card —
     ver styles.css): cada card se detiene más abajo que la anterior, dejando
     ver la pestaña (.card-tab) de las de atrás, como una carpeta con
     separadores. El movimiento lo da el scroll mismo, sin pines ni JS —
     así se evitan los bugs de los intentos anteriores (saltos, desincronía,
     cards que se pasaban de sección). No hace falta nada más acá. */

  // recalcula posiciones una vez que todo (imágenes, fuentes) terminó de cargar,
  // para que los pines de arriba midan alturas finales correctas
  window.addEventListener('load', ()=> ScrollTrigger.refresh());

  /* ---------- parallax del hero: cada capa se mueve a distinta velocidad ---------- */
  const layers = document.querySelectorAll('[data-parallax]');
  if(layers.length){
    layers.forEach(el=>{
      const depth = parseFloat(el.dataset.parallax) || 0;
      gsap.to(el, {
        yPercent: -depth * 100,
        ease: 'none',
        scrollTrigger: {
          trigger: '#hero',
          start: 'top top',
          end: 'bottom top',
          scrub: 0.5
        }
      });
    });
  }

  /* ---------- palabra que cicla en el hero ("más manos." -> "más horas." -> ...) ---------- */
  (function(){
    const el = document.querySelector('h1 .word.cycle');
    if(!el) return;
    let options;
    try{ options = JSON.parse(el.dataset.cycle); }catch(e){ return; }
    if(!Array.isArray(options) || options.length < 2) return;

    let i = 0;
    function next(){
      i = (i + 1) % options.length;
      gsap.to(el, {
        opacity: 0, y: -8, filter: 'blur(6px)', duration: .3, ease: 'power2.in',
        onComplete: ()=>{
          el.textContent = options[i];
          gsap.fromTo(el,
            { opacity: 0, y: 12, filter: 'blur(6px)' },
            { opacity: 1, y: 0, filter: 'blur(0px)', duration: .5, ease: 'power2.out' }
          );
        }
      });
    }
    setInterval(next, 2400);
  })();

  /* ---------- statement negro: se ilumina palabra por palabra al hacer scroll ---------- */
  (function(){
    const wrap = document.getElementById('darkStatement');
    if(!wrap) return;
    const words = wrap.querySelectorAll('.statement-word');
    if(!words.length) return;

    gsap.to(words, {
      className: '+=is-lit',
      stagger: { each: 1 / words.length, from: 'start' },
      scrollTrigger: {
        trigger: wrap,
        start: 'top 75%',
        end: 'bottom 30%',
        scrub: true
      }
    });
  })();

  /* ---------- reveal genérico con stagger: cada .stat-card / .proj-card / .feat-card / .roadmap-card
              entra por separado con un pequeño delay entre sí al hacer scroll ---------- */
  const staggerSelectors = [
    { parent: '.stats-grid', child: '.stat-card' },
    { parent: '.proj-row',   child: '.proj-card' },
    { parent: '.feat-grid',  child: '.feat-card' },
    { parent: '.stepper',    child: '.t-item' },
    { parent: '.roadmap-grid', child: '.roadmap-card' }
  ];
  staggerSelectors.forEach(({ parent, child })=>{
    document.querySelectorAll(parent).forEach(container=>{
      const items = container.querySelectorAll(child);
      if(!items.length) return;
      gsap.from(items, {
        opacity: 0, y: 40,
        duration: .7, ease: 'power3.out',
        stagger: 0.09,
        scrollTrigger: { trigger: container, start: 'top 82%' }
      });
    });
  });

  /* ---------- contador de números en las stat cards ---------- */
  document.querySelectorAll('.stat-card .num').forEach(numEl=>{
    const raw = numEl.textContent.trim();
    // capturar el primer número entero al principio; conservar el resto (sup/símbolos)
    const match = raw.match(/^(\d+)/);
    if(!match) return;
    const target = parseInt(match[1], 10);
    const rest = raw.slice(match[1].length);
    const sup = numEl.querySelector('sup');
    const supHTML = sup ? sup.outerHTML : '';
    const restText = sup ? rest.slice(0, rest.length - sup.textContent.length) : rest;

    const counter = { val: 0 };
    ScrollTrigger.create({
      trigger: numEl,
      start: 'top 85%',
      once: true,
      onEnter: ()=>{
        gsap.to(counter, {
          val: target, duration: 1.4, ease: 'power2.out',
          onUpdate: ()=>{
            numEl.innerHTML = Math.round(counter.val) + restText + supHTML;
          }
        });
      }
    });
  });

  /* ---------- marquee negro: pausar en hover (opcional, elegante) ---------- */
  document.querySelectorAll('.marquee-track').forEach(track=>{
    track.addEventListener('mouseenter', ()=> track.style.animationPlayState = 'paused');
    track.addEventListener('mouseleave', ()=> track.style.animationPlayState = 'running');
  });

  /* ---------- section reveal de headers (pill + h2) por separado ---------- */
  document.querySelectorAll('.working-head, .compare-head, .timeline-head, .roadmap-head, .pain-head, .solutions-head, .islands-3d-copy').forEach(head=>{
    const pill = head.querySelector('.pill');
    const heading = head.querySelector('h2') || head.querySelector('h1');
    const lead = head.querySelector('.lead');
    const targets = [pill, heading, lead].filter(Boolean);
    if(!targets.length) return;
    gsap.from(targets, {
      opacity: 0, y: 24,
      duration: .8, ease: 'power3.out',
      stagger: 0.12,
      scrollTrigger: { trigger: head, start: 'top 82%' }
    });
  });
});
