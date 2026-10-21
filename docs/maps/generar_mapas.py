#!/usr/bin/env python3
"""Genera los mapas SVG (sitemap, redistribución, wireframes) para docs/maps/."""
import os
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
FONT = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

INK = "#1a1a1a"
MID = "#6b6b6b"
LINE = "#b8b8b8"
FILL = "#efefef"
FILL2 = "#dcdcdc"
DARK = "#3a3a3a"
BG = "#ffffff"


def t(x, y, s, size=13, weight=400, fill=INK, anchor="start", mono=False, extra=""):
    fam = MONO if mono else FONT
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{escape(s)}</text>')


def r(x, y, w, h, fill=FILL, stroke="none", rx=4, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>')


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(title)}">\n<title>{escape(title)}</title>\n'
            f'{r(0, 0, w, h, BG, rx=0)}\n' + "\n".join(body) + "\n</svg>\n")


def write(name, content):
    path = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------- sitemap.svg
def sitemap():
    W, H = 1480, 640
    b = [t(40, 46, "iguana.ec: sitemap (rediseño 2026)", 22, 700),
         t(40, 70, "Iguana como agencia de IA · 14 rutas · las 4 URLs actuales se conservan", 13, 400, MID)]
    NW, NH = 112, 58
    root_x, root_y = W / 2 - 80, 100
    b.append(r(root_x, root_y, 160, 64, INK, rx=8))
    b.append(t(W / 2, root_y + 28, "Home", 16, 700, "#fff", "middle"))
    b.append(t(W / 2, root_y + 48, "/", 12, 400, "#ddd", "middle", mono=True))

    groups = [
        ("Menú principal", [("Servicios", "/servicios", "nav", False, True),
                            ("Cómo trabajamos", "/como-trabajamos", "nav", True, False),
                            ("Soluciones", "/soluciones", "nav", True, False),
                            ("Precios", "/precios", "nav", False, False),
                            ("Nosotros", "/nosotros", "nav", False, False)]),
        ("Entradas por CTA y pie", [("¿Es para ti?", "/es-para-ti", "cta", False, False),
                                    ("FAQ", "/faq", "cta", True, False),
                                    ("Contacto", "/contacto", "cta", True, False)]),
        ("Legal y sistema", [("Privacidad", "/privacidad", "legal", True, False),
                             ("Términos", "/terminos", "legal", True, False),
                             ("404", "/404", "legal", False, False)]),
    ]
    gap, ggap = 10, 40
    total = sum(len(g[1]) for g in groups) * (NW + gap) - gap + ggap * (len(groups) - 1)
    x = (W - total) / 2
    y = 270
    bus_y = 215
    xs = []
    servicios_x = None
    for gname, nodes in groups:
        gx0 = x
        for (name, url, kind, new, has_children) in nodes:
            cx = x + NW / 2
            xs.append(cx)
            if kind == "nav":
                b.append(r(x, y, NW, NH, "#fff", INK, rx=6, sw=2))
            elif kind == "cta":
                b.append(r(x, y, NW, NH, FILL, DARK, rx=6, sw=1.2))
            else:
                b.append(r(x, y, NW, NH, "#fff", MID, rx=6, sw=1, dash="4 3"))
            b.append(t(cx, y + 25, name, 13 if len(name) < 13 else 11.5, 600, INK, "middle"))
            b.append(t(cx, y + 43, url, 10.5, 400, MID, "middle", mono=True))
            if new:
                b.append(r(x + NW - 46, y - 9, 50, 18, INK, rx=9))
                b.append(t(x + NW - 21, y + 4, "NUEVA", 9.5, 700, "#fff", "middle"))
            b.append(f'<line x1="{cx}" y1="{bus_y}" x2="{cx}" y2="{y}" stroke="{LINE}" stroke-width="1.5"/>')
            if has_children:
                servicios_x = x
            x += NW + gap
        gx1 = x - gap
        b.append(t((gx0 + gx1) / 2, y + NH + 34, gname.upper(), 10.5, 700, MID, "middle",
                   extra=' letter-spacing="1.2"'))
        b.append(f'<line x1="{gx0}" y1="{y + NH + 18}" x2="{gx1}" y2="{y + NH + 18}" stroke="{LINE}" stroke-width="1"/>')
        x += ggap - gap
    b.insert(3, f'<line x1="{W / 2}" y1="{root_y + 64}" x2="{W / 2}" y2="{bus_y}" stroke="{LINE}" stroke-width="1.5"/>')
    b.insert(3, f'<line x1="{xs[0]}" y1="{bus_y}" x2="{xs[-1]}" y2="{bus_y}" stroke="{LINE}" stroke-width="1.5"/>')

    # hijos de servicios
    kids = [("Automatización", "/servicios/automatizacion"), ("Agentes IA", "/servicios/agentes-ia"),
            ("Consultoría", "/servicios/consultoria"), ("A medida", "/servicios/a-medida")]
    sx = servicios_x + 26
    cy = y + NH + 70
    b.append(f'<line x1="{sx - 12}" y1="{y + NH}" x2="{sx - 12}" y2="{cy + 3 * 52 + 22}" stroke="{LINE}" stroke-width="1.5"/>')
    for i, (name, url) in enumerate(kids):
        yy = cy + i * 52
        b.append(f'<line x1="{sx - 12}" y1="{yy + 22}" x2="{sx}" y2="{yy + 22}" stroke="{LINE}" stroke-width="1.5"/>')
        b.append(r(sx, yy, 190, 44, "#fff", INK, rx=6, sw=1.5))
        b.append(t(sx + 12, yy + 19, name, 12.5, 600))
        b.append(t(sx + 12, yy + 35, url, 10, 400, MID, mono=True))
        b.append(r(sx + 190 - 44, yy - 7, 46, 16, INK, rx=8))
        b.append(t(sx + 190 - 21, yy + 4, "NUEVA", 9, 700, "#fff", "middle"))

    # leyenda
    lx, ly = 900, 470
    b.append(t(lx, ly, "LEYENDA", 10.5, 700, MID, extra=' letter-spacing="1.2"'))
    items = [(r(lx, ly + 14, 34, 22, "#fff", INK, rx=4, sw=2), "En el menú del header"),
             (r(lx, ly + 46, 34, 22, FILL, DARK, rx=4, sw=1.2), "Sin menú: entra por CTA secundario y footer"),
             (r(lx, ly + 78, 34, 22, "#fff", MID, rx=4, sw=1, dash="4 3"), "Solo en el footer / sistema")]
    for i, (shape, label) in enumerate(items):
        b.append(shape)
        b.append(t(lx + 46, ly + 30 + i * 32, label, 12.5))
    b.append(r(lx, ly + 112, 50, 18, INK, rx=9))
    b.append(t(lx + 25, ly + 125, "NUEVA", 9.5, 700, "#fff", "middle"))
    b.append(t(lx + 62, ly + 126, "Página que no existe en el sitio actual", 12.5))
    b.append(t(40, H - 24, "Fase 2 (fuera del MVP): /blog · /casos/<cliente> · integración con CRM iguanaec/iguana.ec", 12, 400, MID))
    write("sitemap.svg", svg(W, H, b, "Sitemap de iguana.ec"))


# ---------------------------------------------------------- redistribucion.svg
OLD = [
    ("index.html (home en main)", [
        ("Hero «Tu negocio no necesita más manos…»", "/", "hero", "move"),
        ("«No es falta de talento» (dolores)", "/", "problema", "move"),
        ("«Solo 2 de cada 10 negocios… usa IA»", "/", "stats", "move"),
        ("«Lo que hacemos» (6 servicios)", "/servicios", "servicios-grid", "merge"),
        ("«Así se ve» (conversaciones de ejemplo)", "/servicios/agentes-ia", "casos-uso", "move"),
        ("«Todas las iguanas saben nadar…»", "/", "concepto", "merge"),
        ("CTA «La iguana se adaptó. ¿Y tú?»", "/", "cta-final", "move"),
    ]),
    ("precios.html", [
        ("Hero «Planes desde $15 al mes»", "/precios", "hero", "move"),
        ("Franja de condiciones", "/precios", "condiciones", "move"),
        ("«Elige tu plan» (Esencial, Crecimiento…)", "/precios", "planes", "rename"),
        ("«Mientras más grande…» (mapa de islas 3D)", None, None, "drop"),
        ("«Tu parte»", "/como-trabajamos", "tu-parte", "move"),
        ("«Listo en 11 días»", "/como-trabajamos", "proceso", "merge"),
        ("«Tu primer año»", "/como-trabajamos", "despues", "move"),
        ("«Lo que viene» (automatización, memoria…)", "/servicios/automatizacion", "incluye", "merge"),
    ]),
    ("nosotros.html", [
        ("Hero «Aprendimos de la iguana»", "/nosotros", "hero", "move"),
        ("«Por qué la iguana» (carrusel)", "/nosotros", "concepto", "merge"),
        ("«El equipo»", "/nosotros", "equipo", "move"),
        ("«Tu día, antes y después»", "/soluciones", "casos-uso", "move"),
    ]),
    ("es-para-ti.html", [
        ("Quiz de 4 preguntas", "/es-para-ti", "quiz", "merge"),
        ("«Donde más ayudamos»", "/soluciones", "verticales", "merge"),
        ("«¿Te reconoces en alguno?»", "/es-para-ti", "casos-uso", "move"),
        ("CTA «Probar no te cuesta»", "/es-para-ti", "cta-final", "move"),
    ]),
    ("Todo el sitio", [
        ("Imágenes de Unsplash (14)", None, None, "drop"),
        ("Enlaces internos «.html»", None, None, "drop"),
    ]),
]
NEW = [("/", "Home", False), ("/servicios", "Servicios", True),
       ("/servicios/automatizacion", "Automatización", True), ("/servicios/agentes-ia", "Agentes IA", True),
       ("/servicios/consultoria", "Consultoría", True), ("/servicios/a-medida", "A medida", True),
       ("/como-trabajamos", "Cómo trabajamos", True), ("/soluciones", "Soluciones", True),
       ("/precios", "Precios", False), ("/es-para-ti", "¿Es para ti?", False),
       ("/nosotros", "Nosotros", False), ("/faq", "FAQ", True), ("/contacto", "Contacto", True),
       ("/privacidad · /terminos · /404", "Legal y sistema", True)]


def redistribucion():
    W = 1480
    ROW, HEAD = 30, 40
    left_x, left_w = 40, 470
    tag_x = left_x + left_w + 14
    right_x, right_w = 1150, 290
    b = []
    y = 120
    rows = []
    for page, secs in OLD:
        b.append(t(left_x, y + 24, page, 15, 700))
        y += HEAD
        for (label, dest, block, kind) in secs:
            if kind == "drop":
                b.append(r(left_x, y, left_w, ROW - 6, "#fff", MID, rx=4, dash="4 3"))
                b.append(t(left_x + 12, y + 16, label, 12.5, 400, MID,
                           extra=' text-decoration="line-through"'))
                b.append(t(tag_x, y + 16, "✕ se elimina", 12, 700, INK))
            else:
                b.append(r(left_x, y, left_w, ROW - 6, FILL, rx=4))
                b.append(t(left_x + 12, y + 16, label, 12.5))
                verb = {"move": "→", "merge": "⇢ fusiona", "rename": "→ renombra"}[kind]
                b.append(t(tag_x, y + 16, f"{verb} #{block}", 11, 400, MID, mono=True))
                rows.append((y + (ROW - 6) / 2, dest, kind))
            y += ROW
        y += 10
    left_bottom = y

    # columna derecha
    n = len(NEW)
    rh = 56
    span = (left_bottom - 120)
    step = max(rh + 12, span / n)
    ry0 = 120 + HEAD
    anchors = {}
    for i, (url, name, new) in enumerate(NEW):
        yy = ry0 + i * step
        is_child = url.startswith("/servicios/")
        x0 = right_x + (24 if is_child else 0)
        w0 = right_w - (24 if is_child else 0)
        b.append(r(x0, yy, w0, rh, "#fff", INK if not new else DARK, rx=6, sw=1.8 if not new else 1.2))
        b.append(t(x0 + 14, yy + 24, name, 14, 700))
        b.append(t(x0 + 14, yy + 43, url, 11, 400, MID, mono=True))
        if new:
            b.append(r(x0 + w0 - 56, yy + 8, 48, 18, INK, rx=9))
            b.append(t(x0 + w0 - 32, yy + 21, "NUEVA", 9.5, 700, "#fff", "middle"))
        else:
            b.append(r(x0 + w0 - 92, yy + 8, 84, 18, FILL2, rx=9))
            b.append(t(x0 + w0 - 50, yy + 21, "URL se conserva", 9.5, 600, INK, "middle"))
        anchors[url] = (x0, yy + rh / 2)
    b.append(t(right_x, 120 + 24, "Sitio nuevo", 15, 700))

    # conectores
    start_x = tag_x + 185
    paths = []
    for (yy, dest, kind) in rows:
        ax, ay = anchors[dest]
        c1 = start_x + (ax - start_x) * 0.45
        c2 = start_x + (ax - start_x) * 0.55
        dash = ' stroke-dasharray="5 4"' if kind == "merge" else ""
        paths.append(f'<path d="M{start_x},{yy} C{c1},{yy} {c2},{ay} {ax - 6},{ay}" fill="none" '
                     f'stroke="{DARK}" stroke-opacity="0.45" stroke-width="1.4"{dash} marker-end="url(#arr)"/>')
        paths.append(f'<circle cx="{start_x}" cy="{yy}" r="2.5" fill="{DARK}"/>')
    H = int(max(left_bottom, ry0 + n * step) + 150)

    head = [
        '<defs><marker id="arr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0,0 L8,4 L0,8 z" fill="{DARK}"/></marker></defs>',
        t(40, 46, "Redistribución: sitio actual → sitio nuevo", 22, 700),
        t(40, 70, "Sitio actual = rama main. Cada sección, a qué página y bloque (#id del esqueleto) pasa.", 13, 400, MID),
    ]
    # leyenda
    ly = H - 110
    leg = [t(40, ly, "LEYENDA", 10.5, 700, MID, extra=' letter-spacing="1.2"'),
           f'<line x1="40" y1="{ly + 22}" x2="90" y2="{ly + 22}" stroke="{DARK}" stroke-width="1.6"/>',
           t(100, ly + 26, "se mueve tal cual (se reescribe el copy en fase 4)", 12.5),
           f'<line x1="40" y1="{ly + 48}" x2="90" y2="{ly + 48}" stroke="{DARK}" stroke-width="1.6" stroke-dasharray="5 4"/>',
           t(100, ly + 52, "se fusiona o recorta dentro de otro bloque", 12.5),
           r(40, ly + 64, 50, 18, "#fff", MID, rx=4, dash="4 3"),
           t(100, ly + 78, "se elimina", 12.5),
           t(520, ly + 26, "Planes: Esencial → Básico $15 · Crecimiento → Estándar $35", 12.5),
           t(520, ly + 52, "Pro → Pro $60 · A medida → A medida (sin islas ni mapa de islas)", 12.5)]
    write("redistribucion.svg", svg(W, H, head + paths + b + leg, "Mapa de redistribución del sitio actual al nuevo"))


# ---------------------------------------------------------------- wireframes
WX, WW = 40, 720
AX = WX + WW + 30


def bars(x, y, widths, h=8, gap=8, fill=FILL2):
    out = []
    for i, w in enumerate(widths):
        out.append(r(x, y + i * (h + gap), w, h, fill, rx=h / 2))
    return out


def img(x, y, w, h):
    return [r(x, y, w, h, FILL, LINE, rx=6),
            f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y + h}" stroke="{LINE}"/>',
            f'<line x1="{x + w}" y1="{y}" x2="{x}" y2="{y + h}" stroke="{LINE}"/>']


def pill(x, y, w=120, dark=True):
    return [r(x, y, w, 30, DARK if dark else "#fff", DARK, rx=15, sw=1.2)]


def blk_nav(x, y, w, o):
    h = 56
    s = [r(x + 20, y + 18, 70, 20, FILL2, rx=4)]
    for i in range(5):
        s.append(r(x + 210 + i * 72, y + 24, 56, 8, FILL2, rx=4))
    s += pill(x + w - 230, y + 13, 150)
    return s, h


def blk_hero(x, y, w, o):
    if o.get("short"):
        h = 150
        cx = x + w / 2
        return [r(cx - 220, y + 40, 440, 18, FILL2, rx=9), r(cx - 160, y + 70, 320, 18, FILL2, rx=9),
                r(cx - 190, y + 104, 380, 8, FILL, rx=4)], h
    h = 300
    s = [r(x + 30, y + 60, 300, 22, FILL2, rx=11), r(x + 30, y + 92, 260, 22, FILL2, rx=11),
         r(x + 30, y + 124, 200, 22, FILL2, rx=11)]
    s += bars(x + 30, y + 170, [290, 240])
    s += pill(x + 30, y + 220, 150) + pill(x + 194, y + 220, 110, False)
    s += img(x + w - 330, y + 30, 300, 240)
    return s, h


def cols(x, y, w, n, ch, inner, gap=16, pad=24):
    cw = (w - 2 * pad - (n - 1) * gap) / n
    out = []
    for i in range(n):
        cx = x + pad + i * (cw + gap)
        out += inner(cx, y, cw, ch, i)
    return out


def blk_stats(x, y, w, o):
    h = 150
    return cols(x, y + 30, w, 3, 100, lambda cx, cy, cw, ch, i:
                [r(cx, cy, cw * 0.5, 34, FILL2, rx=6)] + bars(cx, cy + 50, [cw * 0.8, cw * 0.6])), h


def card_icon(cx, cy, cw, ch, i):
    return ([r(cx, cy, cw, ch, "#fff", LINE, rx=8), f'<circle cx="{cx + 28}" cy="{cy + 30}" r="12" fill="{FILL2}"/>']
            + bars(cx + 16, cy + 56, [cw * 0.6, cw * 0.8, cw * 0.7]))


def blk_problema(x, y, w, o):
    return cols(x, y + 24, w, 3, 130, card_icon), 180


def blk_pilares(x, y, w, o):
    return cols(x, y + 24, w, 3, 120, lambda cx, cy, cw, ch, i:
                [f'<circle cx="{cx + cw / 2}" cy="{cy + 26}" r="22" fill="{FILL2}"/>',
                 r(cx + cw * 0.25, cy + 62, cw * 0.5, 12, FILL2, rx=6)] + bars(cx + cw * 0.15, cy + 86, [cw * 0.7, cw * 0.55])), 170


def blk_servicios(x, y, w, o):
    def inner(cx, cy, cw, ch, i):
        return card_icon(cx, cy, cw, ch, i) + [t(cx + cw - 16, cy + ch - 16, "Ver →", 11, 600, MID, "end")]
    return cols(x, y + 24, w, 4, 170, inner, gap=12), 220


def blk_proceso(x, y, w, o):
    n = 4
    s = []
    pad = 60
    step = (w - 2 * pad) / (n - 1)
    s.append(f'<line x1="{x + pad}" y1="{y + 50}" x2="{x + w - pad}" y2="{y + 50}" stroke="{LINE}" stroke-width="2"/>')
    for i in range(n):
        cx = x + pad + i * step
        s.append(f'<circle cx="{cx}" cy="{y + 50}" r="20" fill="#fff" stroke="{DARK}" stroke-width="1.5"/>')
        s.append(t(cx, y + 55, str(i + 1), 14, 700, INK, "middle"))
        s += bars(cx - 50, y + 90, [100, 80], 8)
    return s, 150


def blk_incluye(x, y, w, o):
    s = []
    for c in range(2):
        for i in range(5):
            xx = x + 30 + c * (w / 2)
            yy = y + 30 + i * 28
            s.append(r(xx, yy, 14, 14, "#fff", DARK, rx=3))
            s.append(r(xx + 26, yy + 3, w / 2 - 110 - (i % 3) * 30, 8, FILL2, rx=4))
    return s, 180


def blk_casos(x, y, w, o):
    def inner(cx, cy, cw, ch, i):
        return ([r(cx, cy, cw, ch, "#fff", LINE, rx=8),
                 r(cx + 14, cy + 16, cw * 0.6, 26, FILL, rx=10),
                 r(cx + cw * 0.35, cy + 52, cw * 0.55, 26, FILL2, rx=10),
                 r(cx + 14, cy + 88, cw * 0.5, 26, FILL, rx=10),
                 t(cx + 14, cy + ch - 14, "ejemplo ilustrativo", 10, 400, MID)])
    return cols(x, y + 24, w, 3, 150, inner), 200


def blk_verticales(x, y, w, o):
    s = []
    for i in range(6):
        s += [r(x + 24 + i * 112, y + 24, 100, 28, DARK if i == 0 else "#fff", DARK, rx=14, sw=1)]
    s += bars(x + 24, y + 80, [260, 220, 240, 180], 10, 12)
    s += pill(x + 24, y + 176, 140)
    s += img(x + w - 330, y + 70, 306, 140)
    return s, 230


def blk_amedida(x, y, w, o):
    return [r(x + 16, y + 16, w - 32, 88, DARK, rx=10),
            r(x + 44, y + 40, 280, 14, "#777", rx=7), r(x + 44, y + 66, 220, 8, "#666", rx=4),
            r(x + w - 210, y + 44, 160, 30, "#fff", rx=15)], 120


def blk_planes(x, y, w, o):
    def inner(cx, cy, cw, ch, i):
        hi = i == 1
        out = [r(cx, cy, cw, ch, "#fff", DARK if hi else LINE, rx=8, sw=2.5 if hi else 1)]
        if hi:
            out += [r(cx + cw / 2 - 48, cy - 10, 96, 20, DARK, rx=10),
                    t(cx + cw / 2, cy + 4, "RECOMENDADO", 9, 700, "#fff", "middle")]
        names = ["Básico", "Estándar", "Pro", "A medida"]
        prices = ["$15", "$35", "$60", "Hablemos"]
        out += [t(cx + 16, cy + 34, names[i], 13, 700), t(cx + 16, cy + 64, prices[i], 20, 700)]
        out += bars(cx + 16, cy + 86, [cw * 0.7, cw * 0.6, cw * 0.75, cw * 0.5])
        out += [r(cx + 16, cy + ch - 46, cw - 32, 30, DARK if hi else "#fff", DARK, rx=15)]
        return out
    return cols(x, y + 30, w, 4, 210, inner, gap=12), 260


def blk_comparativa(x, y, w, o):
    s = []
    rows, colsn = 7, 5
    cw = (w - 48) / colsn
    for i in range(rows):
        yy = y + 24 + i * 28
        s.append(r(x + 24, yy, w - 48, 26, FILL if i % 2 == 0 else "#fff", rx=2))
        s.append(r(x + 34, yy + 9, cw * 0.6, 8, FILL2, rx=4))
        for c in range(1, colsn):
            cx = x + 24 + c * cw + cw / 2
            if i == 0:
                s.append(r(cx - 24, yy + 9, 48, 8, DARK, rx=4))
            else:
                s.append(f'<circle cx="{cx}" cy="{yy + 13}" r="4" fill="{DARK if (i + c) % 3 else LINE}"/>')
    return s, 230


def blk_condiciones(x, y, w, o):
    return cols(x, y + 24, w, 4, 40, lambda cx, cy, cw, ch, i:
                [f'<circle cx="{cx + 10}" cy="{cy + 14}" r="8" fill="#fff" stroke="{DARK}"/>',
                 r(cx + 26, cy + 10, cw * 0.65, 8, FILL2, rx=4)]), 80


def blk_quiz(x, y, w, o):
    cx = x + w / 2
    s = [r(cx - 240, y + 24, 480, 300, "#fff", DARK, rx=12, sw=1.2),
         r(cx - 210, y + 48, 420, 6, FILL, rx=3), r(cx - 210, y + 48, 160, 6, DARK, rx=3),
         r(cx - 160, y + 80, 320, 16, FILL2, rx=8)]
    for i in range(4):
        s.append(r(cx - 210, y + 120 + i * 46, 420, 36, "#fff", LINE, rx=18))
        s.append(r(cx - 190, y + 134 + i * 46, 160 - i * 20, 8, FILL2, rx=4))
    s.append(t(cx, y + 316, "→ resultado: servicio + plan + WhatsApp prellenado", 11, 400, MID, "middle"))
    return s, 350


def blk_concepto(x, y, w, o):
    s = img(x + 24, y + 24, 300, 170)
    s += [r(x + 360, y + 50, 260, 18, FILL2, rx=9)]
    s += bars(x + 360, y + 90, [300, 280, 260, 200])
    return s, 220


def blk_mision(x, y, w, o):
    cx = x + w / 2
    return [r(cx - 260, y + 36, 520, 18, FILL2, rx=9), r(cx - 220, y + 64, 440, 18, FILL2, rx=9),
            r(cx - 150, y + 98, 300, 8, FILL, rx=4)], 140


def blk_equipo(x, y, w, o):
    return cols(x, y + 24, w, 3, 150, lambda cx, cy, cw, ch, i:
                [f'<circle cx="{cx + cw / 2}" cy="{cy + 44}" r="42" fill="{FILL}" stroke="{LINE}"/>',
                 r(cx + cw / 2 - 60, cy + 100, 120, 10, FILL2, rx=5),
                 r(cx + cw / 2 - 40, cy + 120, 80, 8, FILL, rx=4)]), 190


def blk_valores(x, y, w, o):
    return cols(x, y + 24, w, 5, 110, lambda cx, cy, cw, ch, i:
                [r(cx, cy, cw, ch, "#fff", LINE, rx=8), r(cx + 12, cy + 16, 24, 24, FILL2, rx=4)]
                + bars(cx + 12, cy + 56, [cw * 0.7, cw * 0.55]), gap=10), 160


def blk_faq(x, y, w, o):
    n = 4 if o.get("short") else 7
    s = []
    for i in range(n):
        yy = y + 24 + i * 40
        s.append(r(x + 24, yy, w - 48, 32, "#fff", LINE, rx=6))
        s.append(r(x + 40, yy + 12, 260 + (i % 3) * 40, 8, FILL2, rx=4))
        s.append(t(x + w - 44, yy + 21, "+", 16, 400, MID, "middle"))
    return s, 24 + n * 40 + 16


def blk_canales(x, y, w, o):
    def inner(cx, cy, cw, ch, i):
        out = [r(cx, cy, cw, ch, "#fff", DARK if i == 0 else LINE, rx=10, sw=2 if i == 0 else 1),
               f'<circle cx="{cx + 30}" cy="{cy + 32}" r="14" fill="{FILL2}"/>']
        out += bars(cx + 16, cy + 62, [cw * 0.6, cw * 0.75])
        if i == 0:
            out += [r(cx + 16, cy + ch - 46, cw - 32, 30, DARK, rx=15)]
        return out
    return cols(x, y + 24, w, 3, 160, inner), 210


def blk_cta(x, y, w, o):
    cx = x + w / 2
    return [r(x + 16, y + 16, w - 32, 118, DARK, rx=12),
            r(cx - 180, y + 44, 360, 18, "#777", rx=9),
            r(cx - 90, y + 80, 180, 32, "#fff", rx=16)], 150


def blk_footer(x, y, w, o):
    s = [r(x, y, w, 170, FILL, rx=0)]
    s += cols(x, y + 24, w, 5, 120, lambda cx, cy, cw, ch, i:
              [r(cx, cy, cw * 0.6, 10, FILL2 if i else DARK, rx=5)] + bars(cx, cy + 26, [cw * 0.7, cw * 0.5, cw * 0.65, cw * 0.4], 7, 10, "#cfcfcf"))
    return s, 170


def blk_text(x, y, w, o):
    s = [r(x + 24, y + 24, 260, 16, FILL2, rx=8)]
    s += bars(x + 24, y + 56, [w * 0.8, w * 0.75, w * 0.6])
    if o.get("cta"):
        s += pill(x + 24, y + 104, 160)
        return s, 150
    return s, 120


BLOCKS = {"nav": blk_nav, "hero": blk_hero, "stats": blk_stats, "problema": blk_problema,
          "pilares": blk_pilares, "servicios-grid": blk_servicios, "proceso": blk_proceso,
          "incluye": blk_incluye, "casos-uso": blk_casos, "verticales": blk_verticales,
          "a-medida": blk_amedida, "planes": blk_planes, "comparativa": blk_comparativa,
          "condiciones": blk_condiciones, "quiz": blk_quiz, "concepto": blk_concepto,
          "mision": blk_mision, "equipo": blk_equipo, "valores": blk_valores, "faq": blk_faq,
          "canales": blk_canales, "cta-final": blk_cta, "footer": blk_footer, "texto": blk_text}


def page(fname, title, url, objective, items):
    b = [t(WX, 46, title, 22, 700), t(WX, 70, url, 13, 400, MID, mono=True),
         t(WX + 12 + len(url) * 8, 70, "· " + objective, 13, 400, MID),
         t(AX, 104, "NOTAS / CTA", 10.5, 700, MID, extra=' letter-spacing="1.2"')]
    y = 120
    for item in items:
        bid, note = item[0], item[1]
        opts = item[2] if len(item) > 2 else {}
        kind = opts.get("kind", bid)
        label = opts.get("label", bid)
        shapes, h = BLOCKS[kind](WX, y, WW, opts)
        b.append(f'<g id="blk-{label}">')
        b.append(r(WX, y, WW, h, "#fff", LINE, rx=0))
        b += shapes
        tw = 9 + len(label) * 7.2
        b.append(r(WX + WW - tw - 8, y + 6, tw, 18, "#fff", DARK, rx=3, sw=1))
        b.append(t(WX + WW - 8 - tw / 2, y + 19, "#" + label, 11, 600, INK, "middle", mono=True))
        b.append("</g>")
        if note:
            b.append(f'<line x1="{WX + WW + 6}" y1="{y + 15}" x2="{AX - 6}" y2="{y + 15}" stroke="{LINE}"/>')
            for i, line in enumerate(note.split("\n")):
                b.append(t(AX, y + 19 + i * 17, line, 12.5, 600 if i == 0 else 400, INK if i == 0 else MID))
        y += h
    H = y + 50
    b.append(t(WX, H - 18, "Wireframe de baja fidelidad (desktop). Sin diseño ni copy: los bloques se adaptarán a los diseños entregados.", 11, 400, MID))
    write(f"wireframes/{fname}.svg", svg(AX + 300, H, b, f"Wireframe {title}"))


PAGES = [
    ("home", "Home", "/", "agencia de IA: tiempo, procesos, adaptación", [
        ("nav", "Header\nCTA fijo: diagnóstico gratis"),
        ("hero", "Agencia de IA + adaptarse\nCTA: diagnóstico · 2º: ¿Es para ti?"),
        ("stats", "El mercado cambia rápido\n3 cifras con fuente"),
        ("pilares", "Qué resolvemos\nTiempo · Procesos · Adaptación"),
        ("servicios-grid", "Los 4 servicios\n→ /servicios/*"),
        ("proceso", "Cómo trabajamos (corto)\n→ /como-trabajamos"),
        ("verticales", "Por tipo de negocio\n→ /soluciones"),
        ("a-medida", "Soluciones a medida\n→ /servicios/a-medida"),
        ("planes", "Planes (resumen)\n→ /precios"),
        ("concepto", "Por qué la iguana\nla iguana se adaptó"),
        ("faq", "FAQ corta\n→ /faq", {"short": True}),
        ("cta-final", "«La iguana se adaptó. ¿Y tú?»\nCTA: diagnóstico gratis"),
        ("footer", "Footer\nservicios · empresa · legal · redes")]),
    ("servicios", "Servicios (hub)", "/servicios", "elegir servicio", [
        ("nav", ""), ("hero", "Intro corta", {"short": True}),
        ("servicios-grid", "4 tarjetas ampliadas\npara quién · qué resuelve · resultado"),
        ("a-medida", "Banner a medida"),
        ("texto", "¿No sabes cuál?\n→ /es-para-ti", {"kind": "texto", "label": "no-sabes", "cta": True}),
        ("proceso", "Proceso (corto)"), ("faq", "FAQ corta", {"short": True}),
        ("cta-final", ""), ("footer", "")]),
    ("servicio-plantilla", "Plantilla de servicio", "/servicios/*", "automatización · agentes IA · consultoría · a medida", [
        ("nav", ""), ("hero", "Servicio + resultado\nCTA: WhatsApp prellenado con el servicio"),
        ("problema", "3 dolores específicos"), ("incluye", "Qué incluye"),
        ("proceso", "Cómo funciona este servicio"), ("casos-uso", "Ejemplos de uso\nrotulados como ilustrativos"),
        ("planes", "Planes (Agentes IA, automatización)\no #a-medida (consultoría, a medida)"),
        ("faq", "FAQ del servicio", {"short": True}), ("cta-final", ""), ("footer", "")]),
    ("como-trabajamos", "Cómo trabajamos", "/como-trabajamos", "bajar el riesgo percibido", [
        ("nav", ""), ("hero", "", {"short": True}),
        ("proceso", "4 pasos con plazos\ndiagnóstico → propuesta → implementación (~11 días) → acompañamiento"),
        ("texto", "Tu parte\nqué necesitamos de ti", {"label": "tu-parte"}),
        ("texto", "Después de lanzar\nacompañamiento y ajustes", {"label": "despues"}),
        ("condiciones", "Sin letras chicas\nIVA incl. · config. incl. · sin permanencia"),
        ("faq", "", {"short": True}), ("cta-final", ""), ("footer", "")]),
    ("soluciones", "Soluciones", "/soluciones", "cada negocio se reconoce", [
        ("nav", ""), ("hero", "", {"short": True}),
        ("verticales", "Selector por tipo de negocio\nsalud · belleza · talleres · retail · profesionales · educación"),
        ("casos-uso", "Ejemplos por vertical\n+ servicio relacionado"),
        ("a-medida", ""), ("cta-final", ""), ("footer", "")]),
    ("precios", "Precios", "/precios", "precio claro, sin letras chicas", [
        ("nav", ""), ("hero", "Precios claros", {"short": True}),
        ("planes", "Básico $15 · Estándar $35 · Pro $60 · A medida\nsin nombres de islas"),
        ("comparativa", "Tabla comparativa"), ("condiciones", "IVA incl. · sin permanencia\nlisto en ~11 días"),
        ("a-medida", "¿Necesitas más? Hablemos"), ("faq", "FAQ de precios"),
        ("cta-final", ""), ("footer", "")]),
    ("es-para-ti", "¿Es para ti?", "/es-para-ti", "calificar y recomendar", [
        ("nav", ""), ("quiz", "Quiz con progreso\nrecomienda servicio + plan"),
        ("casos-uso", "¿Te reconoces en alguno?"),
        ("cta-final", "«Probar no te cuesta»"), ("footer", "")]),
    ("nosotros", "Nosotros", "/nosotros", "confianza", [
        ("nav", ""), ("hero", "«Aprendimos de la iguana»", {"short": True}),
        ("mision", "Misión"), ("concepto", "La iguana que se adaptó\n(hereda «Por qué la iguana»)"),
        ("valores", "Valores\ncómo trabajamos con el cliente"),
        ("equipo", "Gustavo Campana · Doménica Escobar\nEsteban Andrade"),
        ("cta-final", ""), ("footer", "")]),
    ("faq", "FAQ", "/faq", "resolver objeciones", [
        ("nav", ""), ("hero", "", {"short": True}),
        ("faq", "Por grupos\nqué hacemos · precios · implementación\ndatos y privacidad · cancelación"),
        ("cta-final", ""), ("footer", "")]),
    ("contacto", "Contacto", "/contacto", "un paso al diagnóstico", [
        ("nav", ""), ("hero", "", {"short": True}),
        ("canales", "WhatsApp (principal) · redes\nqué pasa en el diagnóstico de 15 min"),
        ("faq", "", {"short": True}), ("footer", "")]),
    ("simple", "Páginas simples", "/404 · /privacidad · /terminos", "texto simple", [
        ("nav", ""), ("texto", "404: enlaces a Inicio y Servicios\nLegal: texto", {"label": "texto", "cta": True}),
        ("footer", "")]),
]

if __name__ == "__main__":
    sitemap()
    redistribucion()
    for p in PAGES:
        page(*p)
    print("ok")
