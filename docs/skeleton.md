# Esqueleto: iguana.ec (rediseño 2026)

> Qué bloques lleva cada página y en qué orden. **Todavía sin diseño ni copy final**: los textos entre comillas son solo intención.
> Cada sección es un **bloque con ID**. Cuando lleguen los diseños, se adapta bloque por bloque (un diseño de "hero" sirve para todos los `hero`) sin rehacer la estructura.
> Wireframes de cada página: [`maps/wireframes/`](maps/wireframes/).

## Catálogo de bloques

| ID | Bloque | Contenido | Se usa en |
|---|---|---|---|
| `nav` | Header | Logo, menú, CTA fijo | Todas |
| `hero` | Hero | Titular, subtítulo, 2 CTAs, visual | Todas (variante corta en internas) |
| `stats` | Datos de mercado | 3 cifras citadas con fuente | Home, Consultoría |
| `problema` | El problema | 3 dolores: tiempo perdido, procesos a mano, quedarse atrás | Home, servicios |
| `pilares` | Qué resolvemos | Tiempo · Procesos · Adaptación | Home |
| `servicios-grid` | Grilla de servicios | 4 tarjetas: nombre, para quién, resultado, enlace | Home, Servicios |
| `proceso` | Cómo trabajamos | 4 pasos con plazo: diagnóstico → propuesta → implementación → acompañamiento | Home (corto), Cómo trabajamos, servicios |
| `incluye` | Qué incluye | Lista de entregables / capacidades | Servicios individuales |
| `casos-uso` | Ejemplos de uso | 3-6 ejemplos ilustrativos (rotulados "ejemplo") | Servicios, Soluciones |
| `verticales` | Por tipo de negocio | Selector o pestañas: salud, belleza, talleres, retail, servicios profesionales, educación | Home (resumen), Soluciones |
| `a-medida` | Banner a medida | "Cada negocio es distinto": lleva a A medida | Home, Servicios, Precios |
| `planes` | Tarjetas de planes | Básico $15 · Estándar $35 (recomendado) · Pro $60 · A medida | Home (resumen), Precios, servicios |
| `comparativa` | Tabla comparativa | Filas de características × 4 planes | Precios |
| `condiciones` | Sin letras chicas | IVA incluido, configuración incluida, sin permanencia, listo en ~11 días | Precios, Cómo trabajamos |
| `quiz` | Quiz | Preguntas → recomendación de servicio + plan → WhatsApp | Es para ti |
| `concepto` | Por qué la iguana | La iguana que se adaptó (versión corta) | Home, Nosotros (versión larga) |
| `mision` | Misión | Qué hacemos y para quién | Nosotros |
| `equipo` | Equipo | 3 fundadores: nombre, rol, foto | Nosotros |
| `valores` | Valores | 3-5 ideas (heredan "Por qué Galápagos", recortado) | Nosotros |
| `faq` | FAQ | Acordeón; corto (4-5) o completo por grupos | Todas (corto), FAQ (completo) |
| `canales` | Canales de contacto | WhatsApp, redes, qué pasa en el diagnóstico de 15 min | Contacto |
| `cta-final` | CTA final | Frase de cierre + botón diagnóstico | Todas |
| `footer` | Footer | Columnas del sitemap, redes, legal | Todas |

## Páginas

### `/`: Home
**Objetivo:** que en 10 s se entienda "agencia de IA que te ahorra tiempo y te ayuda a adaptarte, a medida".

1. `nav`
2. `hero`: agencia de IA + adaptarse. CTA: diagnóstico gratis · secundario: ¿Es para ti?
3. `stats`: el mercado cambia rápido (21 % de negocios ecuatorianos usa IA · 54 % de pymes de las Américas · 83,7 % de ecuatorianos en internet; con fuentes)
4. `pilares`: tiempo · procesos · adaptación
5. `servicios-grid`: los 4 servicios
6. `proceso` (corto): 4 pasos, enlace a Cómo trabajamos
7. `verticales` (resumen): enlace a Soluciones
8. `a-medida`
9. `planes` (resumen): enlace a Precios
10. `concepto`: la iguana se adaptó
11. `faq` (corto)
12. `cta-final`: "La iguana se adaptó. ¿Y tú?" (se conserva como idea)
13. `footer`

### `/servicios`: Hub
1. `nav` · 2. `hero` (corto) · 3. `servicios-grid` (tarjetas ampliadas) · 4. `a-medida` · 5. bloque "¿No sabes cuál?" que lleva al quiz · 6. `proceso` (corto) · 7. `faq` (corto) · 8. `cta-final` · 9. `footer`

### `/servicios/*`: Plantilla de servicio (4 páginas)
Misma plantilla para `automatizacion`, `agentes-ia`, `consultoria` y `a-medida`:

1. `nav`
2. `hero`: nombre del servicio + resultado. CTA: WhatsApp prellenado con el servicio
3. `problema`: 3 dolores específicos
4. `incluye`
5. `proceso`: aplicado a este servicio
6. `casos-uso`
7. `planes` (si aplica) **o** `a-medida`. Agentes IA usa planes; consultoría y a medida usan cotización
8. `faq` (del servicio)
9. `cta-final` · 10. `footer`

| Servicio | Contenido base que se reaprovecha del sitio actual |
|---|---|
| Automatización | "Agentes de IA a medida: cotizaciones, pedidos, seguimientos" (home actual) |
| Agentes IA | Todo el asistente de WhatsApp: responde, agenda, recuerda; conversaciones de ejemplo por negocio |
| Consultoría | "Consultoría de procesos con IA" (home actual) + datos de mercado |
| A medida | Plan A medida (varias sedes, integraciones, flujos propios) + "Páginas web que llevan al WhatsApp" |

### `/como-trabajamos`
1. `nav` · 2. `hero` (corto) · 3. `proceso` (completo, con plazos: ~11 días) · 4. bloque "Tu parte" (qué necesitamos de ti; viene de precios actual) · 5. bloque "Después de lanzar" (acompañamiento, ajustes; viene de "Tu primer año") · 6. `condiciones` · 7. `faq` · 8. `cta-final` · 9. `footer`

### `/soluciones`
1. `nav` · 2. `hero` (corto) · 3. `verticales` (selector) → por vertical: problema típico · qué hacemos · `casos-uso` (ilustrativo) · servicio relacionado · 4. `a-medida` · 5. `cta-final` · 6. `footer`

### `/precios`
1. `nav` · 2. `hero` (corto: "Precios claros, sin letras chicas") · 3. `planes` · 4. `comparativa` · 5. `condiciones` · 6. `a-medida` · 7. `faq` (de precios) · 8. `cta-final` · 9. `footer`

| Plan | Precio (USD/mes, IVA incl.) | Antes |
|---|---|---|
| Básico | $15 | Esencial / San Cristóbal |
| Estándar *(recomendado)* | $35 | Crecimiento / Santiago |
| Pro | $60 | Pro / Santa Cruz |
| A medida | Hablemos | A medida / Isabela |

### `/es-para-ti`: Quiz
1. `nav` · 2. `quiz` (con progreso) · 3. resultado: servicio + plan + WhatsApp · 4. `casos-uso` ("¿Te reconoces?") · 5. `cta-final` ("Probar no te cuesta") · 6. `footer`

Lógica base actual en `js/main.js` (`computeResult`). Se amplía con una pregunta de **qué quieres resolver** que mapea a servicio:

| Respuesta | Servicio recomendado |
|---|---|
| Responder mensajes / agendar | Agentes IA |
| Tareas repetitivas / reportes | Automatización |
| No sé por dónde empezar | Consultoría |
| Algo propio de mi negocio / varias sedes | A medida |

### `/nosotros`
1. `nav` · 2. `hero` ("Aprendimos de la iguana") · 3. `mision` · 4. `concepto` (versión larga) · 5. `valores` · 6. `equipo` · 7. `cta-final` · 8. `footer`

### `/faq`
1. `nav` · 2. `hero` (corto) · 3. `faq` completo por grupos: Qué hacemos · Precios y pagos · Implementación · Datos y privacidad · Cancelación · 4. `cta-final` · 5. `footer`

### `/contacto`
1. `nav` · 2. `hero` (corto) · 3. `canales` · 4. `faq` (corto) · 5. `footer`

### `/404`, `/privacidad`, `/terminos`
`nav` · bloque de texto simple · `footer`. 404 con enlaces a Inicio y Servicios.

## Qué se elimina o cambia del sitio actual

| Elemento actual | Destino |
|---|---|
| Nombres de isla en planes ("Elige tu isla") | **Eliminado**: Básico / Estándar / Pro / A medida |
| Hero "Tu negocio, atendiendo solo." | Pasa a `/servicios/agentes-ia`; la home habla de la agencia |
| "Lo que viene" (Pinzón, Cormorán, Tortuga Gigante) | **Eliminado** (los nombres de complementos ya no aplican) |
| "Tu día, antes y después" (nosotros) | Pasa a `casos-uso` en servicios |
| "Por qué Galápagos" (5 ideas) | `valores` en Nosotros, recortado |
| Carrusel "Así trabaja en cada negocio" | `verticales` en `/soluciones` |
| Rails de tipos de negocio | `verticales` |
| Imágenes Unsplash | **Eliminadas**: solo fotos propias o ilustración |
| Marcadores "Imagen de ejemplo" | Se resuelven en fase de diseño |

## Inventario de assets

| Asset | Estado | Uso propuesto |
|---|---|---|
| `images/logo-iguana.webp`, favicons, `og-image.jpg` | Existe | `nav`, `footer`, OG (rehacer OG con el nuevo mensaje) |
| `images/iguana-hero.webp`, `images/iguana nado/1.webp`, `images/hero-rocas.webp` | Existe | `hero` / `concepto` |
| `images/isla-*.webp` (5) | Existe | `valores` o fondos; ya no se ligan a planes |
| Fotos del equipo | **Falta** (hoy hay iniciales) | `equipo` |
| Mockups de producto (WhatsApp, panel) | **Falta** | Agentes IA, `casos-uso` |
| Íconos de servicios y pilares | **Falta** | `servicios-grid`, `pilares` |
| Diseños del usuario | **Pendiente** | Se mapean sobre los bloques de este catálogo |

## Huecos de contenido

- Qué incluye cada plan ahora que no es solo el asistente. En el asistente actual, Estándar y Pro dicen "más mensajes" sin cifra.
- ¿Los planes aplican a todos los servicios o solo a Agentes IA? Propuesta: planes = Agentes IA y automatizaciones simples; consultoría y a medida, por cotización.
- Clientes reales o testimonios: no hay. Los ejemplos se rotulan como ilustrativos.
- Fuentes exactas de `stats` (se heredan del sitio actual y se revalidan en fase de copy).
