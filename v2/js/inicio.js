/* iguana.ec v2 · Inicio: nav, carrusel de logos, cifras y lista expandible */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Nav: sólida al hacer scroll, menú de servicios y hoja móvil ---------- */
  var nav = document.getElementById('nav');
  var hero = document.getElementById('hero');
  function onScroll() {
    var limit = hero ? hero.offsetTop + hero.offsetHeight - 120 : 200;
    nav.classList.toggle('is-solid', window.scrollY > limit);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  function toggler(btn, panel) {
    function set(open) {
      btn.setAttribute('aria-expanded', String(open));
      panel.hidden = !open;
    }
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      set(btn.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('click', function (e) { if (!panel.contains(e.target)) set(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
    panel.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
  }
  toggler(document.getElementById('btn-servicios'), document.getElementById('menu-servicios'));
  toggler(document.querySelector('.nav__burger'), document.getElementById('sheet'));

  /* ---------- Carrusel de logos: se duplica la lista para un bucle continuo ---------- */
  var track = document.querySelector('.marquee__track');
  if (track) {
    Array.prototype.slice.call(track.children).forEach(function (li) {
      var c = li.cloneNode(true);
      c.setAttribute('aria-hidden', 'true');
      track.appendChild(c);
    });
  }

  /* ---------- Cifras: cuentan al entrar en pantalla (el valor final ya es visible) ---------- */
  var fmt = function (n, d) { return n.toFixed(d).replace('.', ','); };
  if (!reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        var el = en.target, end = parseFloat(el.dataset.count), d = parseInt(el.dataset.decimals || '0', 10);
        var suf = el.dataset.suffix || '', t0 = null, dur = 1400;
        function step(ts) {
          if (!t0) t0 = ts;
          var p = Math.min((ts - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
          el.textContent = fmt(end * e, d) + suf;
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    document.querySelectorAll('[data-count]').forEach(function (el) { io.observe(el); });
  }

  /* ---------- Beneficios: hover muestra foto flotante, clic expande ---------- */
  var list = document.getElementById('ben-list');
  var float = document.getElementById('ben-float');
  var floatImg = float.querySelector('img');
  var section = document.getElementById('beneficios');
  var bens = Array.prototype.slice.call(list.querySelectorAll('.ben'));

  bens.forEach(function (li) {
    var btn = li.querySelector('.ben__row');
    btn.addEventListener('click', function () {
      var open = !li.classList.contains('is-open');
      bens.forEach(function (o) {
        o.classList.remove('is-open');
        o.querySelector('.ben__row').setAttribute('aria-expanded', 'false');
      });
      if (open) {
        li.classList.add('is-open');
        btn.setAttribute('aria-expanded', 'true');
        float.classList.remove('is-on');
      }
    });
    function place(e) {
      // La foto se ancla a la izquierda de las viñetas y sigue un poco al cursor, sin tapar el título.
      var s = section.getBoundingClientRect(), r = li.getBoundingClientRect();
      var pts = li.querySelector('.ben__points').getBoundingClientRect();
      var base = pts.left - s.left - 150 - 16;
      var drift = Math.max(-12, Math.min(12, (e.clientX - pts.left) / 16));
      float.style.setProperty('--fx', (base + drift) + 'px');
      float.style.setProperty('--fy', (r.top - s.top + r.height / 2 - 100) + 'px');
    }
    li.addEventListener('mouseenter', function (e) {
      if (li.classList.contains('is-open')) return;
      floatImg.src = li.dataset.img;
      place(e);
      float.classList.add('is-on');
    });
    li.addEventListener('mouseleave', function () { float.classList.remove('is-on'); });
    li.addEventListener('mousemove', function (e) {
      if (li.classList.contains('is-open')) { float.classList.remove('is-on'); return; }
      place(e);
    });
  });
})();
