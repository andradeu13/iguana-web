/* ============================================================
   home.js — animaciones exclusivas del home
============================================================ */

(function(){
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function onceVisible(el, cb, threshold){
    if(!el) return;
    if(typeof IntersectionObserver === 'undefined'){ cb(); return; }
    const io = new IntersectionObserver(entries=>{
      if(entries[0].isIntersecting){ cb(); io.disconnect(); }
    }, { threshold: threshold || 0.2 });
    io.observe(el);
  }

  // arco de negocios: las fotos se abren en abanico
  const photos = document.getElementById('arcPhotos');
  onceVisible(document.getElementById('sobre'), ()=> photos && photos.classList.add('in'), 0.15);

  // las 9 de la noche: los mensajes aparecen uno tras otro
  const log = document.getElementById('nightLog');
  onceVisible(log, ()=> log.classList.add('in'), 0.35);

  // la iguana cruza nadando la sección "el giro" según el scroll
  const swimmer = document.getElementById('swimmer');
  if(swimmer && !reduce){
    const section = swimmer.parentElement;
    let ticking = false;
    function update(){
      const r = section.getBoundingClientRect();
      const vh = window.innerHeight;
      const p = Math.min(Math.max((vh - r.top) / (vh + r.height), 0), 1);
      const x = -40 + p * (section.clientWidth / swimmer.offsetWidth * 100 + 40);
      const wave = Math.sin(p * Math.PI * 6) * 6;
      swimmer.style.transform = `translate(${x}%, calc(-50% + ${wave}px)) rotate(-90deg)`;
      ticking = false;
    }
    window.addEventListener('scroll', ()=>{ if(!ticking){ requestAnimationFrame(update); ticking = true; } }, { passive:true });
    window.addEventListener('resize', update);
    update();
  }

  // cierre: la pregunta se ilumina palabra por palabra
  const statement = document.getElementById('darkStatement');
  if(statement){
    const words = Array.from(statement.querySelectorAll('.statement-word'));
    if(reduce){ words.forEach(w=> w.classList.add('is-lit')); return; }
    let ticking = false;
    function light(){
      const r = statement.getBoundingClientRect();
      const vh = window.innerHeight;
      const p = Math.min(Math.max((vh * 0.85 - r.top) / (vh * 0.6), 0), 1);
      const n = Math.round(p * words.length);
      words.forEach((w, i)=> w.classList.toggle('is-lit', i < n));
      ticking = false;
    }
    window.addEventListener('scroll', ()=>{ if(!ticking){ requestAnimationFrame(light); ticking = true; } }, { passive:true });
    light();
  }
})();
