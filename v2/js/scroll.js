/* iguana.ec v2 · Animaciones con scroll, compartidas por las 4 páginas.
   [data-reveal]    aparece al entrar en pantalla (retraso escalonado con style="--d:n")
   [data-progress]  recibe --p de 0 a 1:  "view" (por defecto) mientras cruza la ventana,
                    "exit" mientras sale por arriba, "pin" mientras recorre su contenedor sticky,
                    "stack" cuánto lo tapa la siguiente tarjeta de un mazo sticky
   [data-words]     parte el texto en palabras que se encienden con --p
   [data-chapters]  el [data-step] que cruza el centro activa su [data-media] y su punto [data-dot]
   [data-swim]      recibe .is-up mientras el scroll sube (la iguana nadadora se da vuelta) */
(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce) root.classList.add('motion');
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  // Palabras: se envuelven antes de medir nada
  $$('[data-words]').forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.style.setProperty('--n', words.length);
    el.innerHTML = words.map(function (w, i) { return '<span class="w" style="--i:' + i + '">' + w + '</span>'; }).join(' ');
    el.setAttribute('aria-label', words.join(' '));
  });

  // 1. Aparición
  var reveals = $$('[data-reveal]');
  if (reduce || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.1 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  // 2. Progreso y 3. capítulos, en un solo cuadro de animación por scroll
  var progress = reduce ? [] : $$('[data-progress]');
  var chapters = $$('[data-chapters]').map(function (c) {
    return { steps: $$('[data-step]', c), media: $$('[data-media]', c), dots: $$('[data-dot]', c), nums: $$('[data-num]', c), current: -1 };
  });
  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var swimmers = reduce ? [] : $$('[data-swim]');
  var lastY = window.scrollY;

  function update() {
    var vh = window.innerHeight, y = window.scrollY;
    if (y !== lastY) {
      swimmers.forEach(function (el) { el.classList.toggle('is-up', y < lastY); });
      lastY = y;
    }
    progress.forEach(function (el) {
      var r = el.getBoundingClientRect(), mode = el.getAttribute('data-progress'), p;
      if (r.bottom < -vh || r.top > vh * 2) return; // lejos de la pantalla
      if (mode === 'exit') p = -r.top / r.height;
      else if (mode === 'stack') { var nx = el.nextElementSibling; p = nx ? (r.bottom - nx.getBoundingClientRect().top) / r.height : 0; }
      else if (mode === 'pin') p = -r.top / Math.max(1, r.height - vh);
      else p = (vh - r.top) / (vh + r.height);
      el.style.setProperty('--p', clamp(p).toFixed(4));
    });
    chapters.forEach(function (c) {
      var idx = 0;
      c.steps.forEach(function (s, i) { if (s.getBoundingClientRect().top < vh * 0.55) idx = i; });
      if (idx === c.current) return;
      c.current = idx;
      [c.media, c.dots, c.nums].forEach(function (list) {
        list.forEach(function (el, i) { el.classList.toggle('is-active', i === idx); });
      });
      c.steps.forEach(function (s, i) { s.classList.toggle('is-active', i === idx); });
    });
  }
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { ticking = false; update(); });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
})();
