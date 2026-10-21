# Esqueleto: iguana.ec (rediseño 2026)

> Bloques de cada página y su orden, tomando la estructura de la referencia ([`maps/referencia.jpg`](maps/referencia.jpg)). Todavía **sin copy final**.
> Cada bloque tiene un `#id`. Diseño y copy se trabajan bloque por bloque.
> Wireframes: [`maps/wireframes/`](maps/wireframes/): `inicio.svg`, `inicio-movil.svg`, `servicios.svg`, `precios.svg`, `nosotros.svg`.

## De la referencia a Iguana

| Referencia | Iguana | Bloque |
|---|---|---|
| Nav en píldora flotante, links con dropdown, CTA verde | Servicios ▾ · Precios · Nosotros · [Diagnóstico gratis] | `#nav-flotante` |
| Forma orgánica verde gigante de fondo | Forma verde de marca (silueta o trazo de iguana) | fondo de `#hero` |
| Titular grande + párrafo + botón píldora; tarjeta-foto con chip de dato flotante y etiqueta de persona | Titular de agencia de IA; foto con chip "Horas recuperadas"; etiqueta "Ejemplo ilustrativo" mientras no haya clientes | `#hero` |
| 3 cifras gigantes (200K · 200M€ · 4.5/5) | 3 cifras: mercado o propias | `#cifras` |
| Foto a sangre con titular y 3 tarjetas de producto ("Découvrir") | 3 tarjetas de servicio: Agentes IA, Automatización y Consultoría + línea "A medida" | `#servicios-foto` |
| Simulador (selector + inputs + resultado) | Calculadora de tiempo ahorrado → plan recomendado → WhatsApp | `#calculadora` |

## Catálogo de bloques

| ID | Contenido | Página |
|---|---|---|
| `nav-flotante` | Logo, menú, CTA verde | Todas |
| `hero` | Titular, párrafo, 2 CTAs, tarjeta-foto con chip | Inicio |
| `hero-corto` | Titular centrado + párrafo (+ píldoras de ancla en Servicios) | Servicios, Precios, Nosotros |
| `cifras` | 3 cifras gigantes con leyenda y fuente | Inicio |
| `servicios-foto` | Foto a sangre, titular, 3 tarjetas con "Descubrir" → `/servicios#…` | Inicio |
| `proceso` | 4 pasos: diagnóstico → propuesta → implementación (~11 días) → acompañamiento. Absorbe "Tu parte" y "Tu primer año" | **Solo Inicio** |
| `calculadora` | Tipo de negocio · tareas al día · minutos por tarea → horas/mes, plan recomendado, WhatsApp | Inicio |
| `planes` | Básico $15 · Estándar $35 (recomendado) · Pro $60 · A medida. En el Inicio, resumen; completo en Precios | Inicio (resumen), Precios |
| `comparativa` | Tabla de características × 4 planes | Precios |
| `condiciones` | IVA incluido · configuración incluida · sin permanencia · listo en ~11 días | Precios |
| `servicio` | Foto + qué resuelve + qué incluye + un ejemplo + CTA WhatsApp; alterna lados | Servicios (×4) |
| `concepto` | La iguana que se adaptó (corto en Inicio, largo en Nosotros) | Inicio, Nosotros |
| `mision` | Qué hacemos y para quién | Nosotros |
| `equipo` | Gustavo Campana (CEO), Doménica Escobar (CTO), Esteban Andrade (CPO) | Nosotros |
| `faq` | Acordeón: general en Inicio, pagos en Precios | Inicio, Precios |
| `cta-final` | Banda verde redondeada + botón | Todas |
| `footer` | Columnas, legal, redes, WhatsApp | Todas |

## Páginas

### `/` Inicio
1. `nav-flotante`
2. `hero`
3. `cifras`
4. `servicios-foto`
5. `proceso`
6. `calculadora`
7. `planes` (resumen)
8. `concepto` (corto)
9. `faq`
10. `cta-final`
11. `footer`

**Móvil:**

- se apila en el mismo orden;
- la tarjeta-foto va debajo del titular;
- cifras en columna;
- servicios y planes en carrusel horizontal;
- proceso en lista vertical.

### `/servicios`
1. `nav-flotante`
2. `hero-corto` con 4 píldoras de ancla
3. `servicio` × 4 (`#agentes-ia`, `#automatizacion`, `#consultoria`, `#a-medida`)
4. `cta-final` ("¿No sabes cuál?" → `/#calculadora`)
5. `footer`

| Servicio | Contenido que se reaprovecha de `main` |
|---|---|
| Agentes IA | Asistente de WhatsApp: responde, agenda, recuerda. "Así se ve" y "¿Te reconoces?" como ejemplos |
| Automatización | "Lo que viene" (más automatización, memoria de clientes) y "Tu día, antes y después" |
| Consultoría | Diagnóstico y hoja de ruta con IA |
| A medida | Plan A medida (varias sedes, integraciones, flujos propios), webs que llevan al WhatsApp |

### `/precios`
1. `nav-flotante`
2. `hero-corto`
3. `planes` (completo)
4. `comparativa`
5. `condiciones`
6. `faq` (pagos)
7. `cta-final`
8. `footer`

### `/nosotros`
1. `nav-flotante`
2. `hero-corto` ("Aprendimos de la iguana")
3. `concepto` (largo)
4. `mision`
5. `equipo`
6. `cta-final`
7. `footer`

## Qué sale del sitio actual

El detalle sección por sección está en [`maps/redistribucion.svg`](maps/redistribucion.svg).

- Mapa de islas 3D en precios: **eliminado**.
- Planes Esencial / Crecimiento pasan a llamarse Básico / Estándar.
- Quiz de `/es-para-ti`: reemplazado por `#calculadora`; la URL redirige.
- "Tu parte", "Listo en 11 días" y "Tu primer año" se fusionan en un único `#proceso`.
- Imágenes de Unsplash: **eliminadas**. Solo fotos propias.
- Enlaces internos `.html` pasan a rutas limpias.

## Assets

| Asset | Estado | Uso |
|---|---|---|
| Logo, favicons | Existe | `nav-flotante`, `footer` |
| `iguana-hero.webp`, `iguana nado/1.webp` | Existe | `hero` (tarjeta-foto), `concepto` |
| Foto grande para `servicios-foto` | **Falta** | Foto propia a sangre (personas usando el celular o trabajando) |
| Fotos por servicio (×4) | **Falta** | `servicio` |
| Fotos del equipo | **Falta** | `equipo` |
| Forma orgánica de marca | **Falta** | Fondo del hero; se define en diseño |
| OG image | Rehacer | Con el nuevo mensaje |
