"""Genera v2/servicios.html, v2/precios.html y v2/nosotros.html.

Reutiliza el nav y el footer de v2/index.html, así que cualquier cambio ahí se copia a las demás páginas.
Uso:  python3 docs/build_pages.py   (desde la raíz del repo)
"""
import os
import re
from urllib.parse import quote

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'v2') + os.sep
src = open(ROOT + 'index.html', encoding='utf-8').read()
NAV = re.search(r'<header class="nav" id="nav">.*?</header>', src, re.S).group(0)
FOOT = re.search(r'<footer class="footer">.*?</footer>', src, re.S).group(0)


def wa(msg):
    return 'https://wa.me/593959420676?text=' + quote(msg, safe='')


def btn(cls, label, href, ext=True):
    t = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a class="{cls}" href="{href}"{t}>{label}</a>'


def cta(word, title, button):
    long = ' cta__word--long' if len(word) > 6 else ''
    return f'''  <section class="wrap" id="cta-final">
    <div class="cta" data-progress>
      <p class="cta__word{long}" aria-hidden="true">{word}</p>
      <div class="cta__copy">
        <h2>{title}</h2>
        {button}
      </div>
    </div>
  </section>'''


def page(name, title, desc, body, current, solid=False):
    n = NAV
    if solid:
        n = n.replace('<header class="nav" id="nav">', '<header class="nav" id="nav" data-solid>')
    n = n.replace('<a class="nav__logo" href="#top"', '<a class="nav__logo" href="index.html"')
    if current == 'servicios':
        n = n.replace('<div class="nav__drop">', '<div class="nav__drop" data-current>', 1)
    else:
        n = n.replace(f'<a class="nav__link" href="{current}.html">', f'<a class="nav__link" href="{current}.html" aria-current="page">')
    f = FOOT.replace('href="#calculadora"', 'href="index.html#calculadora"').replace('href="#faq"', 'href="index.html#faq"')
    html = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#FAFAF8">
<link rel="icon" href="../favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&family=Anton&display=swap">
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="css/inicio.css">
<link rel="stylesheet" href="css/motion.css">
<link rel="stylesheet" href="css/pages.css">
</head>
<body class="ig-root page-{name[:-5]}">

{n}

<main id="top">

{body}
</main>

{f}

<script src="js/icons.js"></script>
<script src="js/inicio.js"></script>
<script src="js/scroll.js"></script>
</body>
</html>
'''
    open(ROOT + name, 'w', encoding='utf-8').write(html)


def ul(items, cls='checks'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


# ================================================================== SERVICIOS
SERV = [
    dict(id='agentes-ia', name='Agentes IA', img='agentes.webp',
         h='Un asistente que atiende por ti, a cualquier hora',
         p='Responde en WhatsApp e Instagram con tu tono, agenda citas, recuerda pagos pendientes y te avisa cuando un cliente necesita a una persona.',
         inc=['Un número de WhatsApp para tu negocio', 'Respuestas con el tono que tú apruebas', 'Agenda automática en tus horarios libres', 'Recordatorios de citas y de pagos', 'Traspaso a una persona cuando hace falta'],
         ex='Una barbería recibe un mensaje a las once de la noche. El asistente confirma el corte del sábado y deja la cita en la agenda.'),
    dict(id='automatizacion', name='Automatización', img='automatizacion.webp',
         h='Lo repetitivo, fuera de tu día',
         p='Conectamos tus herramientas con n8n y Make para que las cotizaciones, los pedidos, los reportes y los seguimientos se hagan solos.',
         inc=['Cotizaciones y confirmaciones de pedido automáticas', 'Reportes semanales a tu correo o a tu WhatsApp', 'Seguimiento a los clientes que no respondieron', 'Datos que pasan de una app a otra sin copiar y pegar', 'Avisos cuando algo se sale de lo normal'],
         ex='Un taller recibe un pedido por formulario. Se crea la orden, se avisa al cliente y se descuenta del inventario sin que nadie toque el teclado.'),
    dict(id='consultoria', name='Consultoría', img='consultoria.webp',
         h='Por dónde empezar con IA, sin gastar de más',
         p='Revisamos cómo trabaja tu negocio, medimos dónde se te va el tiempo y te entregamos una hoja de ruta con prioridades, costos y plazos.',
         inc=['Diagnóstico de 15 minutos, gratis', 'Mapa de tus tareas repetitivas y el tiempo que ahorras', 'Hoja de ruta ordenada por impacto', 'Recomendación de herramientas y proveedores', 'Acompañamiento para ponerla en marcha'],
         ex='Una clínica descubre que la mayor parte de su trabajo administrativo son recordatorios de cita. Empieza por ahí y lo demás puede esperar.'),
    dict(id='a-medida', name='A medida', img='tienda.webp',
         h='Si tu negocio es distinto, la solución también',
         p='Varias sedes, sistemas propios, flujos que nadie más tiene. Diseñamos e integramos lo que necesitas, incluidas páginas web que llevan al cliente directo a tu WhatsApp.',
         inc=['Varios números o sucursales', 'Integración con tu calendario, tus pagos o tu sistema actual', 'Flujos diseñados para tu operación', 'Páginas web conectadas a WhatsApp', 'Acompañamiento dedicado'],
         ex='Una cadena de tres locales junta citas, pagos y mensajes en un solo panel, sin cambiar el sistema que ya usa cada sede.'),
]


def active(i):
    return ' class="is-active"' if i == 0 else ''


media = ''.join(f'<img data-media{active(i)} src="img/fotos/{s["img"]}" alt="" loading="{"eager" if i == 0 else "lazy"}">' for i, s in enumerate(SERV))
nums = ''.join(f'<span data-num{active(i)}>{i + 1:02d}</span>' for i in range(len(SERV)))
dots = ''.join(f'<li data-dot{active(i)}></li>' for i in range(len(SERV)))
steps = ''.join(f'''
      <article class="chap__step" data-step id="{s["id"]}" aria-labelledby="{s["id"]}-t">
        <div class="chap__card">
          <p class="chap__kicker">{i + 1:02d} · {s["name"]}</p>
          <h2 id="{s["id"]}-t">{s["h"]}</h2>
          <p class="chap__lead">{s["p"]}</p>
          {ul(s["inc"])}
          <p class="chap__example"><small>Ejemplo ilustrativo</small>{s["ex"]}</p>
          {btn("btn-cta", "Cuéntanos tu caso", wa("Hola Iguana, me interesa " + s["name"]))}
        </div>
      </article>''' for i, s in enumerate(SERV))
body = f'''  <section class="shero" id="hero" data-progress="exit" aria-labelledby="h1">
    <div class="shero__media" style="background-image:url('img/fotos/servicios.webp')"></div>
    <div class="shero__copy">
      <p class="shero__kicker">Servicios</p>
      <h1 id="h1">Cuatro formas de recuperar tu tiempo</h1>
      <p>Agentes, automatizaciones, consultoría y soluciones a medida. Elige una o combínalas: todas parten de cómo trabaja tu negocio hoy.</p>
    </div>
    <p class="scroll-cue" aria-hidden="true">Desliza</p>
  </section>

  <section class="chap" data-chapters aria-label="Nuestros servicios">
    <div class="chap__stage" aria-hidden="true">
      <div class="chap__media">{media}</div>
      <p class="chap__num">{nums}</p>
      <ol class="chap__dots">{dots}</ol>
    </div>
    <div class="chap__steps">{steps}
    </div>
  </section>

''' + cta('elige', '¿No sabes cuál? Calcula cuánto tiempo recuperas.', btn('btn-dark', 'Abrir la calculadora', 'index.html#calculadora', ext=False))
page('servicios.html', 'Servicios · Iguana', 'Agentes IA, automatización, consultoría y soluciones a medida para negocios del Ecuador.', body, 'servicios')

# ================================================================== PRECIOS
PLANS = [
    dict(name='Básico', isla='sancristobal', price='$15', who='Para empezar a responder a tiempo.', msg='Hola Iguana, me interesa el plan Básico',
         items=['Número de WhatsApp nuevo, solo para tu negocio', '50 mensajes al mes', 'Recordatorios de citas', 'Agenda automática en tus horarios libres', 'Respuestas con el tono que tú apruebas']),
    dict(name='Estándar', isla='santiago', price='$35', who='Para negocios que viven de las citas.', msg='Hola Iguana, me interesa el plan Estándar', cls=' deck__card--hi', badge=True,
         items=['Todo lo del plan Básico', 'Más mensajes al mes', 'Panel para ver citas y conversaciones', 'Soporte por WhatsApp']),
    dict(name='Pro', isla='santacruz', price='$60', who='Para negocios con mucho movimiento.', msg='Hola Iguana, me interesa el plan Pro',
         items=['Todo lo del plan Estándar', 'Aún más mensajes al mes', 'Seguimiento de pagos y cuotas pendientes', 'Ajuste mensual de respuestas']),
    dict(name='A medida', isla='isabela', price='Hablemos', who='Para varias sedes o procesos propios.', msg='Hola Iguana, quiero algo a medida', cls=' deck__card--dark', label='Cotizar',
         items=['Todo lo del plan Pro', 'Varios números o sucursales', 'Integración con tu calendario, tus pagos o tu sistema', 'Flujos diseñados para tu operación', 'Acompañamiento dedicado']),
]
deck = ''
for i, pl in enumerate(PLANS):
    price = f'<p class="deck__price"><b>{pl["price"]}</b><span>al mes · IVA incl.</span></p>' if pl['price'].startswith('$') else f'<p class="deck__price"><b>{pl["price"]}</b><span>cotización a tu medida</span></p>'
    badge = '<p class="deck__badge">Recomendado</p>' if pl.get('badge') else ''
    bcls = 'btn-dark' if pl.get('cls') != ' deck__card--hi' else 'btn-cta'
    if pl.get('cls') == ' deck__card--dark':
        bcls = 'btn-cta'
    deck += f'''
      <article class="deck__card{pl.get("cls", "")}" style="--i:{i}" data-progress="stack">
        <div class="deck__head">
          <img class="deck__isla" src="img/grabados/isla-{pl["isla"]}.webp" alt="" loading="lazy">
          <p class="deck__n">{i + 1:02d} / 04</p>
          {badge}
          <h3>{pl["name"]}</h3>
          <p class="deck__who">{pl["who"]}</p>
          {price}
        </div>
        <div class="deck__body">
          {ul(pl["items"])}
          {btn(bcls, pl.get("label", "Elegir " + pl["name"]), wa(pl["msg"]))}
        </div>
      </article>'''
Y = '<svg class="ig-icon" role="img" aria-label="Incluido"><use href="#i-check"/></svg>'
N = '<span class="cmp__no" role="img" aria-label="No incluido">—</span>'
rows = [
    ('Número de WhatsApp propio', [Y, Y, Y, Y]),
    ('Mensajes al mes', ['50', 'Más', 'Aún más', 'A tu volumen']),
    ('Recordatorios y agenda automática', [Y, Y, Y, Y]),
    ('Respuestas con tu tono', [Y, Y, Y, Y]),
    ('Panel de citas y conversaciones', [N, Y, Y, Y]),
    ('Soporte por WhatsApp', [N, Y, Y, Y]),
    ('Seguimiento de pagos y cuotas', [N, N, Y, Y]),
    ('Ajuste mensual de respuestas', [N, N, Y, Y]),
    ('Varios números o sucursales', [N, N, N, Y]),
    ('Integración con tu sistema', [N, N, N, Y]),
    ('Flujos diseñados para tu operación', [N, N, N, Y]),
    ('Acompañamiento dedicado', [N, N, N, Y]),
]
trs = ''.join('<tr><th scope="row">' + r + '</th>' + ''.join(('<td class="is-hi">' if j == 1 else '<td>') + c + '</td>' for j, c in enumerate(cs)) + '</tr>' for r, cs in rows)
RULES = [('IVA incluido.', 'Los precios son finales y en dólares. Sin cargos escondidos.'),
         ('Configuración incluida.', 'Dejamos todo listo y probado. No pagas por instalarlo.'),
         ('Sin permanencia.', 'Pagas mes a mes y cancelas cuando quieras.'),
         ('Listo en unos 11 días.', 'Cuentan desde que apruebas la propuesta.')]
rules = ''.join(f'''
      <li class="rule" data-progress><p class="rule__big" data-words>{t}</p><p class="rule__note">{d}</p></li>''' for t, d in RULES)
FAQ = [('¿Cómo pago el plan?', 'Mes a mes, en dólares y con el IVA incluido. Te explicamos la forma de pago cuando apruebes la propuesta.'),
       ('¿Cobran algo por la configuración?', 'No. La configuración y las pruebas están incluidas en todos los planes.'),
       ('¿Puedo cambiar de plan?', 'Sí. Si tu negocio crece o necesitas menos, nos escribes por WhatsApp y lo ajustamos.'),
       ('¿Cómo sé cuál plan me conviene?', 'Usa la calculadora del Inicio: con tus tareas de cada día te decimos cuántas horas recuperas y qué plan encaja. En el diagnóstico gratis lo confirmamos contigo.')]
faq = ''.join(f'<details class="qa" data-reveal style="--d:{i}"><summary>{q}<svg class="ig-icon" aria-hidden="true"><use href="#i-plus"/></svg></summary><p>{a}</p></details>' for i, (q, a) in enumerate(FAQ))
body = f'''  <section class="wrap phero" data-progress="exit" aria-labelledby="h1">
    <p class="kicker">Precios</p>
    <h1 id="h1" class="phero__title"><span>Planes desde</span> <b class="phero__big">$15</b> <span>al mes</span></h1>
    <p class="phero__lead">Configuración e IVA incluidos. Sin contrato de permanencia y sin letras chicas.</p>
    <p class="scroll-cue scroll-cue--dark" aria-hidden="true">Desliza para ver los planes</p>
  </section>

  <section class="wrap deck" id="planes" aria-label="Planes">{deck}
  </section>

  <section class="wrap" id="comparativa" aria-labelledby="cmp-t">
    <div class="sec-head sec-head--split" data-reveal>
      <h2 id="cmp-t">Compara lo que incluye cada plan</h2>
      <p>Mientras más grande el plan, más hace Iguana por ti. <a class="ig-link" href="index.html#calculadora">Calcula cuál te conviene</a></p>
    </div>
    <div class="cmp-wrap" data-reveal>
      <div class="cmp" tabindex="0" role="region" aria-label="Comparativa de planes">
        <table>
          <thead><tr><td></td><th scope="col">Básico<small>$15/mes</small></th><th scope="col" class="is-hi">Estándar<small>$35/mes</small></th><th scope="col">Pro<small>$60/mes</small></th><th scope="col">A medida<small>Hablemos</small></th></tr></thead>
          <tbody>{trs}</tbody>
        </table>
      </div>
    </div>
    <p class="cmp-hint">Desliza la tabla para ver todos los planes</p>
  </section>

  <section class="wrap rules" id="condiciones" aria-labelledby="cond-t">
    <h2 class="kicker" id="cond-t">Lo que no cambia en ningún plan</h2>
    <ul class="rules__list">{rules}
    </ul>
  </section>

  <section class="wrap faq" id="faq" aria-labelledby="faq-t">
    <div class="sec-head" data-reveal><h2 id="faq-t">Dudas sobre pagos</h2></div>
    <div class="faq__list">{faq}</div>
  </section>

''' + cta('empieza', '¿Dudas con el plan? Escríbenos y lo vemos juntos.', btn('btn-dark', 'Hablar por WhatsApp', wa('Hola Iguana, tengo dudas sobre los planes')))
page('precios.html', 'Precios · Iguana', 'Planes de Iguana desde $15 al mes. IVA y configuración incluidos, sin permanencia.', body, 'precios', solid=True)

# ================================================================== NOSOTROS
STORY = [('mar-calma.webp', 'Todas nadan.', 'Cualquier iguana sabe nadar. Tener la habilidad no basta: lo que cuenta es usarla.'),
         ('mar-ola.webp', 'Solo una se lanzó.', 'La iguana marina fue a buscar comida donde las demás no se atrevían: bajo el agua, entre las olas.'),
         ('mar-fondo.webp', 'Se adaptó al entorno.', 'Aprendió a botar la sal del agua de mar para poder vivir de él. No cambió el mar: cambió ella.'),
         ('mar-roca.webp', 'Se ajusta cuando falta.', 'En años de escasez se hace más pequeña para gastar menos, y cuando vuelve la comida vuelve a crecer.'),
         ('servicios.webp', 'Tu negocio también puede.', 'La IA ya está al alcance de todos. La diferencia está en quién se lanza primero.')]
smedia = ''.join(f'<img data-media{active(i)} src="img/fotos/{f}" alt="" loading="{"eager" if i == 0 else "lazy"}">' for i, (f, _, _) in enumerate(STORY))
sdots = ''.join(f'<li data-dot{active(i)}></li>' for i in range(len(STORY)))
ssteps = ''.join(f'''
      <article class="story__step" data-step>
        <b class="story__n">{i + 1:02d}</b>
        <h2>{t}</h2>
        <p>{d}</p>
      </article>''' for i, (_, t, d) in enumerate(STORY))
TEAM = [('CEO · Fundador', 'Gustavo Campana', 'Estrategia y crecimiento. Lidera la visión de Iguana y la relación con cada negocio que se suma.'),
        ('CTO · Fundadora', 'Doménica Escobar', 'Tecnología e inteligencia artificial. Diseña cómo funciona todo por dentro para que responda bien y no falle.'),
        ('CPO · Fundador', 'Esteban Andrade', 'Producto y experiencia. Convierte lo que necesita cada negocio en algo simple de usar desde el primer día.')]
team = ''.join(f'''
      <li class="tm" data-reveal="{"left" if i % 2 == 0 else "right"}"><p class="tm__role">{r}</p><h3 class="tm__name">{n}</h3><p class="tm__bio">{d}</p></li>''' for i, (r, n, d) in enumerate(TEAM))
body = f'''  <section class="nhero" id="hero" data-progress="exit" aria-labelledby="h1">
    <img class="nhero__img" src="img/fotos/mar-hero.webp" alt="" fetchpriority="high">
    <div class="nhero__copy">
      <p class="shero__kicker">Nosotros</p>
      <h1 id="h1">Aprendimos de la iguana.</h1>
      <p>Todas las iguanas saben nadar, pero solo la marina se metió al mar a buscar comida. Eso hacemos con los negocios del Ecuador.</p>
    </div>
    <p class="scroll-cue" aria-hidden="true">Desliza</p>
  </section>

  <section class="story" data-chapters data-progress="pin" aria-label="La historia de la iguana">
    <div class="story__stage" aria-hidden="true">
      {smedia}
      <img class="story__swimmer" data-swim src="img/grabados/iguana-nado.webp" alt="">
      <ol class="story__dots">{sdots}</ol>
    </div>
    <div class="story__steps">{ssteps}
    </div>
  </section>

  <section class="grow" data-progress="pin" aria-labelledby="grow-t">
    <div class="grow__sticky">
      <h2 class="grow__word" id="grow-t">ADÁPTATE</h2>
      <img class="grow__obj" src="img/fotos/mani.webp" alt="Laptop con un chat de atención al cliente abierto" loading="lazy">
      <p class="grow__line">No cambió el mar. Cambió ella.</p>
    </div>
  </section>

  <section class="wrap manif" data-progress aria-labelledby="manif-t">
    <h2 class="kicker" id="manif-t">Qué hacemos</h2>
    <p class="manif__text" data-words>Somos una agencia de IA. Ayudamos a las personas y a los negocios a ahorrar tiempo, ordenar sus procesos y adaptarse a un mercado que cambia cada mes, con soluciones hechas a su medida.</p>
    <p class="manif__who" data-reveal>Trabajamos con consultorios, barberías, salones, restaurantes, tiendas y talleres de todo el Ecuador.</p>
  </section>

  <section class="wrap team" id="equipo" aria-labelledby="equipo-t">
    <h2 class="kicker" id="equipo-t">El equipo</h2>
    <ol class="team__list">{team}
    </ol>
  </section>

''' + cta('hola', 'Cuéntanos de tu negocio. Nosotros ponemos la IA.', btn('btn-dark', 'Agenda tu diagnóstico gratis', wa('Hola Iguana, quiero mi diagnóstico gratis')))
page('nosotros.html', 'Nosotros · Iguana', 'Somos una agencia de IA ecuatoriana. Aprendimos de la iguana marina: adaptarse es lo que cuenta.', body, 'nosotros')
print('ok')
