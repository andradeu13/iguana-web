/* iguana.ec v2 · Todas las páginas: nav, carrusel de logos, cifras, carrusel de servicios, lista expandible y calculadora */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Nav: sólida al hacer scroll, menú de servicios y hoja móvil ---------- */
  var nav = document.getElementById('nav');
  var hero = document.getElementById('hero');
  var always = nav.hasAttribute('data-solid'); // páginas internas: sin foto debajo
  function onScroll() {
    if (always) { nav.classList.add('is-solid'); return; }
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
  var floatImg = float && float.querySelector('img');
  var section = document.getElementById('beneficios');
  var bens = list && float ? Array.prototype.slice.call(list.querySelectorAll('.ben')) : [];

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

  /* ---------- Servicios: carrusel en móvil (puntos, flechas y arrastre con mouse) ---------- */
  var track = document.querySelector('.serv-cards');
  if (track) {
    var cards = track.querySelectorAll('.serv-card');
    var dots = document.querySelectorAll('.serv-dots button');
    var arrows = document.querySelectorAll('.serv-nav__btn');
    var current = function () {
      var best = 0, min = Infinity, left = track.getBoundingClientRect().left;
      cards.forEach(function (c, i) { var d = Math.abs(c.getBoundingClientRect().left - left - 16); if (d < min) { min = d; best = i; } });
      return best;
    };
    var go = function (i) {
      i = Math.max(0, Math.min(cards.length - 1, i));
      var dx = cards[i].getBoundingClientRect().left - track.getBoundingClientRect().left - 16;
      track.scrollTo({ left: track.scrollLeft + dx, behavior: reduce ? 'auto' : 'smooth' });
    };
    var sync = function () {
      var i = current();
      dots.forEach(function (d, j) { d.setAttribute('aria-current', j === i ? 'true' : 'false'); });
      arrows[0].disabled = i === 0;
      arrows[1].disabled = i === cards.length - 1;
    };
    dots.forEach(function (d, j) { d.addEventListener('click', function () { go(j); }); });
    arrows.forEach(function (b) { b.addEventListener('click', function () { go(current() + +b.dataset.dir); }); });
    var raf;
    track.addEventListener('scroll', function () { cancelAnimationFrame(raf); raf = requestAnimationFrame(sync); }, { passive: true });
    sync();

    // Arrastre con mouse (en táctil el desplazamiento es nativo)
    var startX, startLeft, moved = false;
    track.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse' || track.scrollWidth <= track.clientWidth) return;
      startX = e.clientX; startLeft = track.scrollLeft; moved = false;
      var move = function (ev) {
        var dx = ev.clientX - startX;
        if (!moved && Math.abs(dx) > 5) { moved = true; track.classList.add('is-drag'); }
        if (moved) track.scrollLeft = startLeft - dx;
      };
      var up = function (ev) {
        window.removeEventListener('pointermove', move);
        window.removeEventListener('pointerup', up);
        if (!moved) return;
        var i = current(), dx = ev.clientX - startX;
        track.classList.remove('is-drag');
        go(Math.abs(dx) > 40 && i === current() ? i + (dx < 0 ? 1 : -1) : i);
      };
      window.addEventListener('pointermove', move);
      window.addEventListener('pointerup', up);
    });
    // Que soltar después de arrastrar no abra el enlace de la tarjeta
    track.addEventListener('click', function (e) { if (moved) { e.preventDefault(); moved = false; } }, true);
  }

  /* ---------- Calculadora: deslizadores de 1 a 5+ tareas al día y de 5 min a 2 h+ cada una ---------- */
  var form = document.getElementById('calc');
  if (form) {
    var $ = function (id) { return document.getElementById(id); };
    var MIN = [5, 15, 30, 60, 90, 120];
    var MIN_LABEL = ['5 min', '15 min', '30 min', '1 h', '1 h 30', '2 h+'];
    var plan = function (h, multi) {
      if (multi) return { name: 'A medida', label: 'A medida · hablemos' };
      if (h < 10) return { name: 'Básico', label: 'Básico · $15/mes' };
      if (h <= 40) return { name: 'Estándar', label: 'Estándar · $35/mes' };
      return { name: 'Pro', label: 'Pro · $60/mes' };
    };
    // Relleno de la pista, marca activa y texto que lee el lector de pantalla
    var paint = function (input, text) {
      var f = (input.value - input.min) / (input.max - input.min);
      input.style.setProperty('--f', f);
      input.setAttribute('aria-valuetext', text);
      input.parentNode.querySelectorAll('.rng__ticks span').forEach(function (s, i) { s.classList.toggle('is-on', i === input.value - input.min); });
    };
    var calc = function () {
      var t = +$('c-tareas').value, i = +$('c-tiempo').value;
      var tLabel = t === 5 ? '5+' : String(t);
      var tText = tLabel + (t === 1 ? ' tarea' : ' tareas');
      $('o-tareas').textContent = tText;
      $('o-tiempo').textContent = MIN_LABEL[i];
      paint($('c-tareas'), tText);
      paint($('c-tiempo'), MIN_LABEL[i] + ' por tarea');
      var h = Math.round(t * (MIN[i] / 60) * 22 * 0.7);
      var p = plan(h, $('c-sedes').checked);
      $('r-horas').textContent = h;
      $('r-dias').textContent = Math.max(1, Math.round(h / 8));
      $('r-plan').textContent = p.label;
      var msg = 'Hola Iguana, calculé ' + h + ' h al mes (' + tText + ' al día de ' + MIN_LABEL[i] +
        '). Me recomendaron el plan ' + p.name + '.';
      $('r-wa').href = 'https://wa.me/593959420676?text=' + encodeURIComponent(msg);
    };
    form.addEventListener('input', calc);
    form.addEventListener('change', calc);
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    calc();
  }
})();
