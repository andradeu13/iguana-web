#!/usr/bin/env python3
"""Genera los mapas SVG del rediseño de iguana.ec (4 páginas, estructura de la referencia).

Uso: python3 docs/maps/generar_mapas.py docs/maps
Salida: sitemap.svg, redistribucion.svg y wireframes/*.svg
"""
import os
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
FONT = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

INK = "#1a1a1a"
MID = "#6b6b6b"
LINE = "#c4c4c4"
FILL = "#efefef"
FILL2 = "#dcdcdc"
DARK = "#2b2b2b"
BG = "#ffffff"
GREEN = "#0c7a3e"      # verde de marca: solo CTAs y forma orgánica
TINT = "#dcefe2"       # verde claro de fondo
TINT2 = "#c3e3cd"


# ------------------------------------------------------------------ helpers
def t(x, y, s, size=13, weight=400, fill=INK, anchor="start", mono=False, extra=""):
    fam = MONO if mono else FONT
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{escape(s)}</text>')


def r(x, y, w, h, fill=FILL, stroke="none", rx=4, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>')


def line(x1, y1, x2, y2, stroke=LINE, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'role="img" aria-label="{escape(title)}">\n<title>{escape(title)}</title>\n'
            f'{r(0, 0, w, h, BG, rx=0)}\n' + "\n".join(body) + "\n</svg>\n")


def write(name, content):
    path = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def bars(x, y, widths, h=8, gap=8, fill=FILL2):
    return [r(x, y + i * (h + gap), w, h, fill, rx=h / 2) for i, w in enumerate(widths)]


def img(x, y, w, h, rx=18, fill=FILL):
    return [r(x, y, w, h, fill, LINE, rx=rx),
            f'<path d="M{x + rx * 0.3:.1f},{y + rx * 0.3:.1f} L{x + w - rx * 0.3:.1f},{y + h - rx * 0.3:.1f} '
            f'M{x + w - rx * 0.3:.1f},{y + rx * 0.3:.1f} L{x + rx * 0.3:.1f},{y + h - rx * 0.3:.1f}" stroke="{LINE}" fill="none"/>']


def pill(x, y, w=120, h=32, fill=DARK, label=None, fg="#fff", stroke=None, arrow=True):
    out = [r(x, y, w, h, fill, stroke or fill, rx=h / 2, sw=1.2)]
    if label:
        out.append(t(x + 16, y + h / 2 + 4.5, label, 12, 600, fg))
    if arrow:
        out.append(f'<circle cx="{x + w - h / 2:.1f}" cy="{y + h / 2:.1f}" r="{h / 2 - 6:.1f}" fill="{fg}"/>')
    return out


def tag(x, y, s, fill=DARK, fg="#fff", size=10.5):
    w = 18 + len(s) * size * 0.58
    return [r(x, y, w, size + 10, fill, rx=(size + 10) / 2), t(x + w / 2, y + size + 4, s, size, 700, fg, "middle")], w


def blob(x, y, w, h):
    """Forma orgánica verde de fondo (en la referencia, una 'M' gigante)."""
    return (f'<path d="M{x},{y + h * 0.85} C{x + w * 0.05},{y + h * 0.15} {x + w * 0.22},{y - h * 0.05} {x + w * 0.32},{y + h * 0.3} '
            f'C{x + w * 0.4},{y + h * 0.62} {x + w * 0.47},{y + h * 0.7} {x + w * 0.55},{y + h * 0.35} '
            f'C{x + w * 0.65},{y - h * 0.05} {x + w * 0.9},{y + h * 0.05} {x + w},{y + h * 0.55} '
            f'L{x + w},{y + h} L{x},{y + h} Z" fill="{TINT2}"/>')


def cols(x, w, n, gap, pad):
    cw = (w - 2 * pad - (n - 1) * gap) / n
    return [(x + pad + i * (cw + gap), cw) for i in range(n)]


# ------------------------------------------------------------------ bloques desktop
def b_nav(x, y, w, o):
    h = 84
    s = [r(x, y, w, h, TINT, rx=0),
         r(x + 40, y + 16, w - 80, 52, "#fff", LINE, rx=16, sw=1),
         r(x + 60, y + 32, 26, 20, DARK, rx=5), r(x + 92, y + 34, 70, 7, FILL2, rx=3), r(x + 92, y + 45, 50, 7, FILL2, rx=3)]
    lx = x + w / 2 - 130
    for i, (lab, caret) in enumerate([("Servicios", True), ("Precios", False), ("Nosotros", False)]):
        s.append(t(lx + i * 96, y + 46, lab + (" ▾" if caret else ""), 12.5, 500, INK))
    s += pill(x + w - 246, y + 26, 186, 32, GREEN, "Diagnóstico gratis")
    return s, h


def b_hero(x, y, w, o):
    h = 430
    s = [r(x, y, w, h, TINT, rx=0), blob(x, y + 40, w, h - 40)]
    s += [r(x + 60, y + 90, 380, 40, DARK, rx=8), r(x + 60, y + 140, 330, 40, DARK, rx=8), r(x + 60, y + 190, 250, 40, DARK, rx=8)]
    s += bars(x + 60, y + 254, [360, 330, 240], 9, 9, "#9fb8a7")
    s += pill(x + 60, y + 316, 176, 36, DARK, "Diagnóstico gratis")
    s += pill(x + 248, y + 316, 120, 36, "#fff", "Calcular", INK, DARK, False)
    cx, cw = x + w - 380, 300
    s += img(cx, y + 40, cw, 340, 22, "#e9e9e9")
    # chip flotante con dato
    s += [r(cx - 70, y + 90, 170, 74, "#fff", LINE, rx=12),
          t(cx - 56, y + 112, "Horas recuperadas", 10.5, 500, MID),
          t(cx - 56, y + 146, "38 h / mes", 22, 800, INK),
          r(cx + 46, y + 100, 44, 18, TINT2, rx=6), t(cx + 68, y + 113, "+12", 10, 700, GREEN, "middle")]
    lab, lw = tag(cx + 20, y + 346, "Ejemplo ilustrativo", "#fff", INK)
    s += [r(cx + 20, y + 346, lw, 20.5, "#fff", LINE, rx=10)] + lab[1:]
    return s, h


def b_cifras(x, y, w, o):
    h = 190
    s = [r(x, y, w, h, TINT, rx=0)]
    nums = o.get("nums", ["21 %", "54 %", "83,7 %"])
    for i, (cx, cw) in enumerate(cols(x, w, 3, 40, 110)):
        s.append(t(cx + cw / 2, y + 86, nums[i], 56, 800, INK, "middle"))
        s += [r(cx + cw / 2 - 90, y + 112, 180, 8, "#9fb8a7", rx=4), r(cx + cw / 2 - 60, y + 128, 120, 8, "#9fb8a7", rx=4)]
    s.append(t(x + w / 2, y + 170, "cifra + leyenda + fuente", 10.5, 400, MID, "middle"))
    return s, h


def b_servicios_foto(x, y, w, o):
    h = 520
    s = [r(x, y, w, h, TINT, rx=0)]
    s += img(x + 16, y + 10, w - 32, h - 20, 28, "#d9d9d9")
    s += [r(x + w / 2 - 230, y + 70, 460, 34, "#fff", rx=8),
          r(x + w / 2 - 200, y + 118, 400, 9, "#f6f6f6", rx=4), r(x + w / 2 - 130, y + 134, 260, 9, "#f6f6f6", rx=4)]
    names = [("Agentes IA", "WhatsApp, agenda, atención"), ("Automatización", "tareas repetitivas fuera"),
             ("Consultoría", "por dónde empezar con IA")]
    heights = [190, 210, 230]
    for i, (cx, cw) in enumerate(cols(x, w, 3, 18, 120)):
        ch = heights[i]
        cy = y + 430 - ch
        s.append(r(cx, cy, cw, ch, "#fff", rx=16))
        s.append(t(cx + 18, cy + 40, names[i][0], 22 + i * 2, 800, INK))
        s.append(t(cx + 18, cy + 62, names[i][1], 11.5, 400, MID))
        s += pill(cx + 18, cy + ch - 50, 112, 30, DARK, "Descubrir")
    s.append(t(x + w / 2, y + 470, "¿Algo distinto para tu negocio? A medida →", 13, 700, "#fff", "middle"))
    return s, h


def b_proceso(x, y, w, o):
    h = 250
    lw = tag(0, 0, "Cómo trabajamos")[1]
    s = tag(x + w / 2 - lw / 2, y + 30, "Cómo trabajamos")[0]
    s += [r(x + w / 2 - 210, y + 66, 420, 22, DARK, rx=6)]
    steps = ["Diagnóstico", "Propuesta", "Implementación", "Acompañamiento"]
    for i, (cx, cw) in enumerate(cols(x, w, 4, 14, 60)):
        s.append(r(cx, y + 112, cw, 108, "#fff", LINE, rx=14))
        s.append(f'<circle cx="{cx + 28:.1f}" cy="{y + 140:.1f}" r="14" fill="{TINT}"/>')
        s.append(t(cx + 28, y + 145, str(i + 1), 13, 800, GREEN, "middle"))
        s.append(t(cx + 16, y + 180, steps[i], 13, 700, INK))
        s += bars(cx + 16, y + 192, [cw * 0.7], 7)
    return s, h


def b_calculadora(x, y, w, o):
    h = 450
    lw = tag(0, 0, "Calculadora")[1]
    s = tag(x + w / 2 - lw / 2, y + 30, "Calculadora")[0]
    s += [r(x + w / 2 - 260, y + 66, 520, 24, DARK, rx=6), r(x + w / 2 - 190, y + 98, 380, 24, DARK, rx=6)]
    # selector
    s += [r(x + w / 2 - 200, y + 142, 400, 40, TINT, rx=12),
          t(x + w / 2 - 184, y + 167, "Tu negocio", 12.5, 600, INK),
          r(x + w / 2 - 90, y + 148, 280, 28, "#9fd3ae", rx=8),
          t(x + w / 2 - 78, y + 167, "Consultorio / clínica", 12, 600, INK), t(x + w / 2 + 176, y + 167, "▾", 12, 700, INK, "end")]
    # inputs
    lx = x + 90
    for i, (lab, val) in enumerate([("Mensajes o tareas al día", "40"), ("Minutos que te toma cada uno", "3")]):
        yy = y + 220 + i * 84
        s.append(t(lx, yy, lab, 12, 600, INK))
        s.append(r(lx, yy + 14, 300, 44, "#fff", LINE, rx=10))
        s.append(t(lx + 284, yy + 42, val, 18, 800, INK, "end"))
        s.append(r(lx, yy + 66, 300, 4, FILL2, rx=2))
        s.append(r(lx, yy + 66, 120 + i * 40, 4, GREEN, rx=2))
        s.append(f'<circle cx="{lx + 120 + i * 40:.1f}" cy="{yy + 68:.1f}" r="7" fill="#fff" stroke="{GREEN}" stroke-width="2"/>')
    # resultado
    rx_ = x + w - 90 - 330
    s += [r(rx_, y + 206, 330, 210, TINT, rx=18),
          t(rx_ + 24, y + 238, "Horas al mes que recuperas", 12, 600, INK),
          t(rx_ + 24, y + 290, "≈ 40 h", 44, 800, INK),
          t(rx_ + 24, y + 322, "Plan recomendado: Estándar ($35)", 12.5, 600, INK)]
    s += pill(rx_ + 24, y + 352, 214, 36, GREEN, "Hablar por WhatsApp")
    s.append(t(x + w / 2, y + 438, "valores de ejemplo · el cálculo se define en la fase de copy", 10.5, 400, MID, "middle"))
    return s, h


def b_planes(x, y, w, o):
    full = o.get("full")
    ch = 300 if full else 230
    h = ch + 70
    s = []
    names = ["Básico", "Estándar", "Pro", "A medida"]
    prices = ["$15", "$35", "$60", "Hablemos"]
    for i, (cx, cw) in enumerate(cols(x, w, 4, 14, 60)):
        hi = i == 1
        cy = y + 34
        s.append(r(cx, cy, cw, ch, TINT if hi else "#fff", GREEN if hi else LINE, rx=18, sw=2 if hi else 1))
        if hi:
            tw_ = tag(0, 0, "RECOMENDADO")[1]
            s += tag(cx + cw / 2 - tw_ / 2, cy - 11, "RECOMENDADO", GREEN)[0]
        s += [t(cx + 18, cy + 40, names[i], 14, 700), t(cx + 18, cy + 78, prices[i], 28, 800)]
        if i < 3:
            s.append(t(cx + 22 + len(prices[i]) * 19, cy + 78, "/mes", 11, 400, MID))
        s += bars(cx + 18, cy + 100, [cw * 0.7, cw * 0.6, cw * 0.75] + ([cw * 0.5, cw * 0.65, cw * 0.55] if full else []), 7, 10)
        s += pill(cx + 18, cy + ch - 52, cw - 36, 32, GREEN if hi else "#fff", None, INK, DARK, False)
    if not full:
        s.append(t(x + w / 2, y + h - 10, "Ver comparativa completa → /precios", 12, 600, MID, "middle"))
    return s, h


def b_comparativa(x, y, w, o):
    s = []
    rows, ncol = 8, 5
    cw = (w - 120) / ncol
    for i in range(rows):
        yy = y + 30 + i * 30
        s.append(r(x + 60, yy, w - 120, 28, FILL if i % 2 == 0 else "#fff", rx=4))
        s.append(r(x + 74, yy + 10, cw * 0.6, 8, FILL2, rx=4))
        for c in range(1, ncol):
            cx = x + 60 + c * cw + cw / 2
            if i == 0:
                s.append(t(cx, yy + 19, ["Básico", "Estándar", "Pro", "A medida"][c - 1], 11.5, 700, INK, "middle"))
            else:
                ok = (i + c) % 3 != 0 or c > 2
                s.append(f'<circle cx="{cx:.1f}" cy="{yy + 14:.1f}" r="5" fill="{GREEN if ok else LINE}"/>')
    return s, 30 + rows * 30 + 30


def b_condiciones(x, y, w, o):
    s = []
    labels = ["IVA incluido", "Configuración incluida", "Sin permanencia", "Listo en ~11 días"]
    for i, (cx, cw) in enumerate(cols(x, w, 4, 14, 60)):
        s += [r(cx, y + 20, cw, 56, TINT, rx=14),
              f'<circle cx="{cx + 26:.1f}" cy="{y + 48:.1f}" r="9" fill="{GREEN}"/>',
              t(cx + 44, y + 52, labels[i], 12.5, 600, INK)]
    return s, 100


def b_concepto(x, y, w, o):
    long = o.get("long")
    h = 300 if long else 250
    s = img(x + 60, y + 30, 360, h - 60, 22)
    s += [r(x + 460, y + 60, 300, 26, DARK, rx=6), r(x + 460, y + 94, 220, 26, DARK, rx=6)]
    s += bars(x + 460, y + 140, [340, 320, 300, 250] + ([330, 280] if long else []), 8, 10)
    return s, h


def b_faq(x, y, w, o):
    n = o.get("n", 5)
    s = [r(x + 60, y + 30, 260, 26, DARK, rx=6)]
    for i in range(n):
        yy = y + 76 + i * 50
        s.append(r(x + 60, yy, w - 120, 42, "#fff", LINE, rx=12))
        s.append(r(x + 80, yy + 17, 280 + (i % 3) * 60, 8, FILL2, rx=4))
        s.append(t(x + w - 84, yy + 27, "+", 18, 400, MID, "middle"))
    return s, 76 + n * 50 + 20


def b_cta(x, y, w, o):
    h = 220
    s = [r(x + 16, y + 10, w - 32, h - 20, GREEN, rx=28),
         r(x + w / 2 - 230, y + 64, 460, 30, "#f2f8f4", rx=8),
         r(x + w / 2 - 150, y + 106, 300, 9, "#7fbf97", rx=4)]
    s += pill(x + w / 2 - 100, y + 136, 200, 38, "#fff", "Diagnóstico gratis", INK, None, True)
    return s, h


def b_footer(x, y, w, o):
    h = 190
    s = [r(x, y, w, h, DARK, rx=0), r(x + 60, y + 34, 26, 20, "#fff", rx=5)]
    heads = ["Servicios", "Iguana", "Legal", "Redes"]
    for i, (cx, cw) in enumerate(cols(x, w, 4, 30, 180)):
        s.append(t(cx, y + 48, heads[i], 12, 700, "#fff"))
        s += bars(cx, y + 66, [cw * 0.8, cw * 0.6, cw * 0.7, cw * 0.5][: 4 if i == 0 else 3], 7, 10, "#555")
    s.append(t(x + 60, y + h - 22, "WhatsApp +593 95 942 0676 · privacidad · términos", 11, 400, "#aaa"))
    return s, h


def b_hero_corto(x, y, w, o):
    h = 230 if o.get("anchors") else 190
    s = [r(x, y, w, h, TINT, rx=0), blob(x, y + 60, w, h - 60)]
    s += [r(x + w / 2 - 240, y + 40, 480, 38, DARK, rx=8), r(x + w / 2 - 170, y + 90, 340, 9, "#9fb8a7", rx=4),
          r(x + w / 2 - 120, y + 106, 240, 9, "#9fb8a7", rx=4)]
    if o.get("anchors"):
        labs = o["anchors"]
        tw = sum(28 + len(lb) * 7 for lb in labs) + 10 * (len(labs) - 1)
        px = x + w / 2 - tw / 2
        for lb in labs:
            pw = 28 + len(lb) * 7
            s += [r(px, y + 150, pw, 32, "#fff", LINE, rx=16), t(px + pw / 2, y + 170, lb, 12, 600, INK, "middle")]
            px += pw + 10
    return s, h


def b_servicio(x, y, w, o):
    h = 360
    flip = o.get("flip")
    ix = x + w - 60 - 380 if flip else x + 60
    tx = x + 60 if flip else x + 60 + 380 + 50
    s = img(ix, y + 30, 380, h - 60, 24)
    s += [t(tx, y + 66, o["name"], 26, 800, INK)]
    s += bars(tx, y + 86, [330, 280], 8, 10)
    for i in range(4):
        yy = y + 136 + i * 26
        s += [f'<circle cx="{tx + 8:.1f}" cy="{yy:.1f}" r="7" fill="{TINT2}"/>',
              t(tx + 8, yy + 4, "✓", 9, 700, GREEN, "middle"), r(tx + 24, yy - 4, 220 - (i % 2) * 40, 8, FILL2, rx=4)]
    s += [r(tx, y + 246, 300, 40, FILL, rx=14), r(tx + 14, y + 262, 170, 8, FILL2, rx=4),
          t(tx + 290, y + 270, "ejemplo", 10, 400, MID, "end")]
    s += pill(tx, y + 300, 60 + len("Quiero " + o["short"]) * 7.4, 34, GREEN, "Quiero " + o["short"])
    return s, h


def b_mision(x, y, w, o):
    s = [r(x + w / 2 - 300, y + 40, 600, 30, DARK, rx=6), r(x + w / 2 - 220, y + 80, 440, 30, DARK, rx=6),
         r(x + w / 2 - 180, y + 128, 360, 9, FILL2, rx=4)]
    return s, 170


def b_equipo(x, y, w, o):
    s = []
    names = [("Gustavo Campana", "CEO"), ("Doménica Escobar", "CTO"), ("Esteban Andrade", "CPO")]
    for i, (cx, cw) in enumerate(cols(x, w, 3, 20, 120)):
        s += img(cx, y + 30, cw, 200, 20)
        s += [t(cx, y + 258, names[i][0], 14, 700), t(cx, y + 276, names[i][1], 12, 400, MID)]
    return s, 300


BLOCKS = {"nav-flotante": b_nav, "hero": b_hero, "cifras": b_cifras, "servicios-foto": b_servicios_foto,
          "proceso": b_proceso, "calculadora": b_calculadora, "planes": b_planes, "comparativa": b_comparativa,
          "condiciones": b_condiciones, "concepto": b_concepto, "faq": b_faq, "cta-final": b_cta,
          "footer": b_footer, "hero-corto": b_hero_corto, "servicio": b_servicio, "mision": b_mision,
          "equipo": b_equipo}

WX, WW = 40, 980
AX = WX + WW + 30


def page(fname, title, url, objective, items):
    b = [t(WX, 46, title, 24, 800), t(WX, 72, f"{url}  ·  {objective}", 13, 400, MID),
         t(AX, 92, "NOTAS", 10.5, 700, MID, extra=' letter-spacing="1.2"')]
    y = 100
    for item in items:
        kind, note = item[0], item[1]
        o = item[2] if len(item) > 2 else {}
        label = o.get("label", kind)
        shapes, h = BLOCKS[kind](WX, y, WW, o)
        b.append(f'<g id="blk-{label}">')
        b += shapes
        b.append(line(WX, y, WX + WW, y, "#e3e3e3", 1, "2 4"))
        tw = 14 + len(label) * 7.2
        b.append(r(WX + WW - tw - 8, y + 6, tw, 19, "#fff", DARK, rx=4, sw=1))
        b.append(t(WX + WW - 8 - tw / 2, y + 19.5, "#" + label, 11, 600, INK, "middle", mono=True))
        b.append("</g>")
        if note:
            b.append(line(WX + WW + 6, y + 16, AX - 6, y + 16, LINE, 1))
            for i, ln in enumerate(note.split("\n")):
                b.append(t(AX, y + 20 + i * 17, ln, 12.5, 700 if i == 0 else 400, INK if i == 0 else MID))
        y += h
    H = y + 50
    b.insert(0, r(WX - 1, 99, WW + 2, y - 98, "none", LINE, rx=0))
    b.append(t(WX, H - 18, "Wireframe de fidelidad media (desktop 1440 escalado). Estructura basada en la referencia; sin copy final.", 11, 400, MID))
    write(f"wireframes/{fname}.svg", svg(AX + 290, H, b, f"Wireframe {title}"))


SERV = [("Agentes IA", "agentes IA", "agentes-ia"), ("Automatización", "automatizar", "automatizacion"),
        ("Consultoría", "consultoría", "consultoria"), ("A medida", "algo a medida", "a-medida")]

PAGES = [
    ("inicio", "Inicio", "/", "agencia de IA: tiempo, procesos, adaptación", [
        ("nav-flotante", "Nav en píldora flotante\nServicios ▾ · Precios · Nosotros\nCTA verde: diagnóstico gratis"),
        ("hero", "Titular grande: agencia de IA + adaptarse\nTarjeta-foto con chip de dato flotante\nEtiqueta «Ejemplo ilustrativo» (sin clientes aún)\nCTA: diagnóstico · 2º: ir a la calculadora"),
        ("cifras", "3 cifras gigantes\nmercado (21 % · 54 % · 83,7 %) o propias\n(15 min · ~11 días · desde $15)"),
        ("servicios-foto", "Foto a sangre + 3 tarjetas de servicio\nDescubrir → /servicios#ancla\nLínea a medida → /servicios#a-medida"),
        ("proceso", "ÚNICA VEZ en todo el sitio\n4 pasos; absorbe «Tu parte»,\n«Listo en 11 días» y «Tu primer año»"),
        ("calculadora", "Reemplaza al quiz (/es-para-ti redirige aquí)\nnegocio · tareas/día · minutos\n→ horas/mes + plan + WhatsApp prellenado"),
        ("planes", "Planes en resumen\n→ /precios para la comparativa"),
        ("concepto", "La iguana que se adaptó (corto)\n→ /nosotros"),
        ("faq", "FAQ general (5 preguntas)", {"n": 5}),
        ("cta-final", "Banda verde: «La iguana se adaptó. ¿Y tú?»"),
        ("footer", "Servicios · Iguana · Legal · Redes\nprivacidad y términos: texto simple")]),
    ("servicios", "Servicios", "/servicios", "una página, un ancla por servicio", [
        ("nav-flotante", ""),
        ("hero-corto", "Intro + 4 píldoras de ancla", {"anchors": [s[0] for s in SERV]}),
    ] + [("servicio", f"#{s[2]}\nqué resuelve · qué incluye · ejemplo\nCTA WhatsApp prellenado: «{s[0]}»\nsin pasos de proceso (están en el Inicio)",
          {"name": s[0], "short": s[1], "label": s[2], "flip": i % 2 == 1}) for i, s in enumerate(SERV)] + [
        ("cta-final", "«¿No sabes cuál?» → /#calculadora"),
        ("footer", "")]),
    ("precios", "Precios", "/precios", "precio claro, sin letras chicas", [
        ("nav-flotante", ""),
        ("hero-corto", "«Precios claros»"),
        ("planes", "Básico $15 · Estándar $35 · Pro $60 · A medida\nEstándar destacado · sin islas", {"full": True}),
        ("comparativa", "Tabla comparativa"),
        ("condiciones", "Sin letras chicas"),
        ("faq", "FAQ de precios y pagos", {"n": 4}),
        ("cta-final", ""),
        ("footer", "")]),
    ("nosotros", "Nosotros", "/nosotros", "confianza: quiénes somos", [
        ("nav-flotante", ""),
        ("hero-corto", "«Aprendimos de la iguana»"),
        ("concepto", "La iguana que se adaptó (largo)\nhereda «Por qué la iguana»", {"long": True}),
        ("mision", "Misión: qué hacemos y para quién"),
        ("equipo", "3 fundadores · fotos reales pendientes"),
        ("cta-final", ""),
        ("footer", "")]),
]


# ------------------------------------------------------------------ móvil
def mobile():
    W0, MW = 40, 390
    x = W0
    b = [t(W0, 46, "Inicio · móvil", 24, 800), t(W0, 72, "/  ·  390 px, mismo orden que desktop", 13, 400, MID)]
    y = 100
    notes = []

    def label(lbl, yy):
        tw = 14 + len(lbl) * 7.2
        b.extend([r(x + MW - tw - 6, yy + 6, tw, 19, "#fff", DARK, rx=4, sw=1),
                  t(x + MW - 6 - tw / 2, yy + 19.5, "#" + lbl, 11, 600, INK, "middle", mono=True)])

    # nav
    b += [r(x, y, MW, 70, TINT, rx=0), r(x + 14, y + 12, MW - 28, 46, "#fff", LINE, rx=14),
          r(x + 28, y + 25, 22, 18, DARK, rx=4), r(x + 56, y + 30, 60, 7, FILL2, rx=3)]
    b += pill(x + MW - 160, y + 20, 92, 30, GREEN, "Diagnóstico", arrow=False)
    b += [t(x + MW - 44, y + 41, "☰", 18, 700, INK, "middle")]
    label("nav-flotante", y)
    y += 70
    # hero
    h = 600
    b += [r(x, y, MW, h, TINT, rx=0), blob(x, y + 200, MW, h - 200)]
    b += [r(x + 20, y + 30, 330, 32, DARK, rx=6), r(x + 20, y + 70, 290, 32, DARK, rx=6), r(x + 20, y + 110, 220, 32, DARK, rx=6)]
    b += bars(x + 20, y + 162, [330, 280], 8, 9, "#9fb8a7")
    b += pill(x + 20, y + 206, 186, 38, DARK, "Diagnóstico gratis")
    b += img(x + 20, y + 270, MW - 40, 300, 20, "#e9e9e9")
    b += [r(x + 32, y + 290, 160, 64, "#fff", LINE, rx=12), t(x + 44, y + 310, "Horas recuperadas", 10, 500, MID),
          t(x + 44, y + 340, "38 h / mes", 19, 800)]
    label("hero", y)
    y += h
    # cifras en columna
    h = 330
    b.append(r(x, y, MW, h, TINT, rx=0))
    for i, n in enumerate(["21 %", "54 %", "83,7 %"]):
        b += [t(x + MW / 2, y + 66 + i * 100, n, 44, 800, INK, "middle"), r(x + MW / 2 - 80, y + 82 + i * 100, 160, 7, "#9fb8a7", rx=3)]
    label("cifras", y)
    y += h
    # servicios: carrusel
    h = 470
    b += img(x + 10, y + 10, MW - 20, h - 20, 24, "#d9d9d9")
    b += [r(x + 40, y + 50, MW - 80, 30, "#fff", rx=6)]
    for i, (nm, cx) in enumerate([("Agentes IA", x + 30), ("Automatiz…", x + 30 + 270)]):
        cw = 250
        b.append(r(cx, y + 150, cw if i == 0 else MW - 40 - 270 + 10, 260, "#fff", rx=16))
        b.append(t(cx + 16, y + 190, nm, 22, 800, INK))
        if i == 0:
            b += pill(cx + 16, y + 360, 110, 30, DARK, "Descubrir")
    b += [f'<circle cx="{x + MW / 2 - 12 + i * 12:.1f}" cy="{y + 432:.1f}" r="4" fill="{"#fff" if i == 0 else "#aaa"}"/>' for i in range(3)]
    b.append(t(x + MW / 2, y + h - 14, "carrusel horizontal: se desliza", 10.5, 600, "#fff", "middle"))
    label("servicios-foto", y)
    y += h
    # proceso vertical
    h = 360
    b += tag(x + 20, y + 24, "Cómo trabajamos")[0]
    for i, st in enumerate(["Diagnóstico", "Propuesta", "Implementación", "Acompañamiento"]):
        yy = y + 66 + i * 70
        b += [r(x + 20, yy, MW - 40, 58, "#fff", LINE, rx=12), f'<circle cx="{x + 46:.1f}" cy="{yy + 29:.1f}" r="13" fill="{TINT}"/>',
              t(x + 46, yy + 34, str(i + 1), 12, 800, GREEN, "middle"), t(x + 70, yy + 34, st, 13, 700)]
    label("proceso", y)
    y += h
    # calculadora
    h = 470
    b += tag(x + 20, y + 24, "Calculadora")[0]
    b += [r(x + 20, y + 60, 320, 24, DARK, rx=6), r(x + 20, y + 106, MW - 40, 40, TINT, rx=12),
          t(x + 34, y + 131, "Tu negocio: Consultorio ▾", 12.5, 600)]
    for i in range(2):
        yy = y + 168 + i * 74
        b += [r(x + 20, yy, MW - 40, 44, "#fff", LINE, rx=10), r(x + 20, yy + 54, MW - 40, 4, FILL2, rx=2), r(x + 20, yy + 54, 140, 4, GREEN, rx=2)]
    b += [r(x + 20, y + 330, MW - 40, 124, TINT, rx=16), t(x + 36, y + 376, "≈ 40 h / mes", 30, 800)]
    b += pill(x + 36, y + 398, 200, 34, GREEN, "Hablar por WhatsApp")
    label("calculadora", y)
    y += h
    # resto resumido
    for lbl, hh, fn in [("planes", 330, "planes"), ("faq", 300, "faq"), ("cta-final", 220, "cta"), ("footer", 260, "footer")]:
        if fn == "planes":
            b += [r(x + 20, y + 30, 260, 250, TINT, GREEN, rx=18, sw=2), t(x + 38, y + 70, "Estándar", 14, 700), t(x + 38, y + 106, "$35", 28, 800),
                  r(x + 292, y + 30, 120, 250, "#fff", LINE, rx=18)]
            b.append(t(x + MW / 2, y + hh - 14, "planes en carrusel", 10.5, 400, MID, "middle"))
        elif fn == "faq":
            for i in range(5):
                b += [r(x + 20, y + 30 + i * 50, MW - 40, 42, "#fff", LINE, rx=12), t(x + MW - 40, y + 57 + i * 50, "+", 16, 400, MID, "middle")]
        elif fn == "cta":
            b += [r(x + 10, y + 10, MW - 20, hh - 20, GREEN, rx=24), r(x + 50, y + 70, MW - 100, 26, "#f2f8f4", rx=6)]
            b += pill(x + MW / 2 - 98, y + 130, 196, 36, "#fff", "Diagnóstico gratis", INK)
        else:
            b.append(r(x, y, MW, hh, DARK, rx=0))
            b += bars(x + 24, y + 40, [120, 160, 140, 100, 150, 90], 7, 18, "#555")
        label(lbl, y)
        y += hh
    head, body = b[:2], b[2:]
    b = head + [f'<clipPath id="mclip"><rect x="{x}" y="100" width="{MW}" height="{y - 100}"/></clipPath>',
                '<g clip-path="url(#mclip)">'] + body + ["</g>", r(x - 1, 99, MW + 2, y - 98, "none", LINE, rx=0)]
    write("wireframes/inicio-movil.svg", svg(W0 + MW + 40, y + 40, b, "Wireframe Inicio móvil"))


# ------------------------------------------------------------------ sitemap
TREE = [
    ("Inicio", "/", ["hero", "cifras", "servicios-foto", "proceso", "calculadora", "planes", "concepto", "faq", "cta-final"]),
    ("Servicios", "/servicios", ["agentes-ia", "automatizacion", "consultoria", "a-medida"]),
    ("Precios", "/precios", ["planes", "comparativa", "condiciones", "faq"]),
    ("Nosotros", "/nosotros", ["concepto", "mision", "equipo"]),
]


def sitemap():
    W, H = 1240, 640
    b = [t(40, 46, "iguana.ec: sitemap", 24, 800),
         t(40, 72, "4 páginas · cada bloque vive en una sola página · el proceso solo en el Inicio", 13, 400, MID)]
    # header
    b += [r(40, 100, W - 80, 52, TINT, rx=16), r(60, 116, 24, 20, DARK, rx=4),
          t(100, 131, "Header:  Servicios ▾  ·  Precios  ·  Nosotros", 13, 600)]
    b += pill(W - 246, 110, 186, 32, GREEN, "Diagnóstico gratis")
    NW = (W - 80 - 3 * 24) / 4
    for i, (name, url, anchors) in enumerate(TREE):
        x = 40 + i * (NW + 24)
        b.append(line(x + NW / 2, 152, x + NW / 2, 184, LINE))
        hh = 74 + len(anchors) * 30 + 14
        b.append(r(x, 184, NW, hh, "#fff", INK, rx=16, sw=2))
        b.append(t(x + 20, 216, name, 18, 800))
        b.append(t(x + 20, 238, url, 12, 400, MID, mono=True))
        for j, a in enumerate(anchors):
            yy = 256 + j * 30
            uniq = a == "proceso"
            b.append(r(x + 14, yy, NW - 28, 24, TINT if uniq else FILL, GREEN if uniq else "none", rx=8, sw=1.5))
            b.append(t(x + 26, yy + 16, "#" + a, 11.5, 600 if uniq else 400, INK, mono=True))
            if uniq:
                b.append(t(x + NW - 24, yy + 16, "única vez", 10, 700, GREEN, "end"))
    # footer y redirecciones
    b += [r(40, 560, (W - 80) / 2 - 12, 50, DARK, rx=14),
          t(60, 590, "Footer: privacidad · términos · redes · WhatsApp", 12.5, 600, "#fff")]
    rx_ = 40 + (W - 80) / 2 + 12
    b += [r(rx_, 560, (W - 80) / 2 - 12, 50, "#fff", MID, rx=14, dash="4 3"),
          t(rx_ + 20, 582, "Redirige:  /es-para-ti → /#calculadora", 12, 600, INK),
          t(rx_ + 20, 600, "no se crean: /faq · /contacto · /soluciones · /como-trabajamos", 11, 400, MID)]
    write("sitemap.svg", svg(W, H, b, "Sitemap de iguana.ec en 4 páginas"))


# ------------------------------------------------------------------ redistribución
OLD = [
    ("index.html (home en main)", [
        ("Hero «Tu negocio no necesita más manos…»", "/#hero", "move"),
        ("«No es falta de talento» (dolores)", "/#hero", "merge"),
        ("«Solo 2 de cada 10 negocios… usa IA»", "/#cifras", "move"),
        ("«Lo que hacemos» (6 servicios)", "/#servicios-foto", "merge"),
        ("«Así se ve» (conversaciones de ejemplo)", "/servicios#agentes-ia", "move"),
        ("«Todas las iguanas saben nadar…»", "/#concepto", "merge"),
        ("CTA «La iguana se adaptó. ¿Y tú?»", "/#cta-final", "move"),
    ]),
    ("precios.html", [
        ("Hero «Planes desde $15 al mes»", "/precios#planes", "merge"),
        ("Franja de condiciones", "/precios#condiciones", "move"),
        ("«Elige tu plan» (Esencial, Crecimiento…)", "/precios#planes", "rename"),
        ("«Mientras más grande…» (mapa de islas 3D)", None, "drop"),
        ("«Tu parte»", "/#proceso", "merge"),
        ("«Listo en 11 días»", "/#proceso", "merge"),
        ("«Tu primer año»", "/#proceso", "merge"),
        ("«Lo que viene» (automatización, memoria…)", "/servicios#automatizacion", "merge"),
    ]),
    ("nosotros.html", [
        ("Hero «Aprendimos de la iguana»", "/nosotros#concepto", "merge"),
        ("«Por qué la iguana» (carrusel)", "/nosotros#concepto", "merge"),
        ("«El equipo»", "/nosotros#equipo", "move"),
        ("«Tu día, antes y después»", "/servicios#automatizacion", "move"),
    ]),
    ("es-para-ti.html", [
        ("Quiz de 4 preguntas", "/#calculadora", "merge"),
        ("«Donde más ayudamos»", "/#calculadora", "merge"),
        ("«¿Te reconoces en alguno?»", "/servicios#agentes-ia", "merge"),
        ("CTA «Probar no te cuesta»", "/#cta-final", "merge"),
    ]),
    ("Todo el sitio", [
        ("Imágenes de Unsplash (14)", None, "drop"),
        ("Enlaces internos «.html»", None, "drop"),
    ]),
]


def redistribucion():
    W = 1400
    ROW, HEAD = 30, 40
    lx, lw = 40, 430
    tag_x = lx + lw + 14
    start_x = tag_x + 120
    rx_, rw = 1070, 290
    b = [t(40, 46, "Redistribución: main → 4 páginas", 24, 800),
         t(40, 72, "Cada sección del sitio actual (rama main) y a qué página y bloque pasa.", 13, 400, MID)]
    y = 110
    rows = []
    for pg, secs in OLD:
        b.append(t(lx, y + 24, pg, 15, 700))
        y += HEAD
        for (lab, dest, kind) in secs:
            if kind == "drop":
                b += [r(lx, y, lw, ROW - 6, "#fff", MID, rx=6, dash="4 3"),
                      t(lx + 12, y + 16, lab, 12.5, 400, MID, extra=' text-decoration="line-through"'),
                      t(tag_x, y + 16, "✕ se elimina", 12, 700, INK)]
            else:
                b += [r(lx, y, lw, ROW - 6, FILL, rx=6), t(lx + 12, y + 16, lab, 12.5)]
                verb = {"move": "→ mueve", "merge": "⇢ fusiona", "rename": "→ renombra"}[kind]
                b.append(t(tag_x, y + 16, verb, 11, 400, MID, mono=True))
                rows.append((y + (ROW - 6) / 2, dest, kind))
            y += ROW
        y += 10
    left_bottom = y
    # columna derecha: páginas con anclas
    anchors = {}
    ry = 110
    b.append(t(rx_, ry + 24, "Sitio nuevo", 15, 700))
    ry += HEAD
    for name, url, ancs in TREE:
        hh = 46 + len(ancs) * 26 + 8
        b.append(r(rx_, ry, rw, hh, "#fff", INK, rx=14, sw=1.8))
        b.append(t(rx_ + 16, ry + 26, name, 15, 800))
        b.append(t(rx_ + rw - 16, ry + 26, url, 11.5, 400, MID, "end", mono=True))
        for j, a in enumerate(ancs):
            yy = ry + 40 + j * 26
            key = ("/#" + a) if url == "/" else (url + "#" + a)
            uniq = a == "proceso"
            b.append(r(rx_ + 12, yy, rw - 24, 22, TINT if uniq else FILL, rx=6))
            b.append(t(rx_ + 24, yy + 15, "#" + a, 11, 600 if uniq else 400, INK, mono=True))
            anchors[key] = (rx_ + 12, yy + 11)
        ry += hh + 14
    paths = []
    for (yy, dest, kind) in rows:
        ax, ay = anchors[dest]
        c1 = start_x + (ax - start_x) * 0.45
        c2 = start_x + (ax - start_x) * 0.55
        dash = ' stroke-dasharray="5 4"' if kind == "merge" else ""
        paths += [f'<path d="M{start_x:.1f},{yy:.1f} C{c1:.1f},{yy:.1f} {c2:.1f},{ay:.1f} {ax - 6:.1f},{ay:.1f}" fill="none" '
                  f'stroke="{DARK}" stroke-opacity="0.45" stroke-width="1.4"{dash} marker-end="url(#arr)"/>',
                  f'<circle cx="{start_x:.1f}" cy="{yy:.1f}" r="2.5" fill="{DARK}"/>']
    H = max(left_bottom, ry) + 130
    ly = H - 100
    leg = [t(40, ly, "LEYENDA", 10.5, 700, MID, extra=' letter-spacing="1.2"'),
           line(40, ly + 22, 90, ly + 22, DARK, 1.6), t(100, ly + 26, "se mueve (el copy se reescribe en la fase de copy)", 12.5),
           line(40, ly + 48, 90, ly + 48, DARK, 1.6, "5 4"), t(100, ly + 52, "se fusiona dentro de otro bloque", 12.5),
           r(40, ly + 62, 50, 18, "#fff", MID, rx=4, dash="4 3"), t(100, ly + 76, "se elimina", 12.5),
           t(520, ly + 26, "Planes: Esencial → Básico $15 · Crecimiento → Estándar $35 · Pro $60 · A medida", 12.5),
           t(520, ly + 52, "/es-para-ti deja de ser página: redirige a /#calculadora", 12.5)]
    head = ['<defs><marker id="arr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0,0 L8,4 L0,8 z" fill="{DARK}"/></marker></defs>']
    write("redistribucion.svg", svg(W, H, head + paths + b + leg, "Redistribución del sitio actual a 4 páginas"))


if __name__ == "__main__":
    sitemap()
    redistribucion()
    for p in PAGES:
        page(*p)
    mobile()
    print("ok")
