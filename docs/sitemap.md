# Sitemap: iguana.ec (rediseño 2026)

> Fase 1 del rediseño: **sitemap → esqueleto → diseño → copy**.
> "Sitio actual" = rama `main`. Estructura visual basada en la referencia [`maps/referencia.jpg`](maps/referencia.jpg).
> Orden de bloques por página: [`skeleton.md`](skeleton.md). Mapas: [`maps/`](maps/).

## Posicionamiento

Iguana es una **agencia de IA**: ayuda a los negocios a ahorrar tiempo, ordenar sus procesos y adaptarse a un mercado que cambia muy rápido, con soluciones a medida. El asistente de WhatsApp es uno de sus servicios, no el centro del sitio.

Se mantienen:

- el concepto de marca (la iguana que se adaptó);
- el tono: tuteo, directo, sin letras chicas, sin permanencia;
- el diagnóstico gratis de 15 min;
- la implementación en unos 11 días.

## 4 páginas

```
iguana.ec
├── /            Inicio      hero · herramientas · cifras · servicios sobre foto · galería · beneficios · proceso · calculadora · planes · FAQ · CTA
├── /servicios   Servicios   #agentes-ia · #automatizacion · #consultoria · #a-medida
├── /precios     Precios     planes · comparativa · condiciones · FAQ de precios
└── /nosotros    Nosotros    concepto · misión · equipo
Footer: privacidad · términos (texto simple) · redes · WhatsApp
```

| URL | Objetivo | CTA primario |
|---|---|---|
| `/` | Entender en 10 s qué hace Iguana, calcular cuánto tiempo recupera y pedir el diagnóstico | Diagnóstico gratis (WhatsApp) |
| `/servicios` | Elegir servicio; cada uno con su ancla para enlazar desde anuncios y desde el Inicio | WhatsApp prellenado con el servicio |
| `/precios` | Precio claro: Básico $15 · Estándar $35 (recomendado) · Pro $60 · A medida | WhatsApp prellenado con el plan |
| `/nosotros` | Confianza: quiénes somos y por qué la iguana | Diagnóstico gratis |

## Regla anti-repetición

- **Cada bloque vive completo en una sola página.** En las demás aparece, como mucho, un enlace.
- **El proceso de 4 pasos (`#proceso`) solo está en el Inicio.** Servicios, Precios y Nosotros no repiten etapas; cada servicio muestra qué incluye y un ejemplo.
- **Los tipos de negocio** (lo que antes era "Soluciones") aparecen como ejemplos dentro de cada servicio. No tienen página propia.
- **La FAQ general va en el Inicio** y la de pagos va en Precios. Las preguntas no se duplican.

## Navegación

- **Header (nav flotante en píldora):** Logo · Servicios ▾ (4 anclas) · Precios · Nosotros · **[Diagnóstico gratis]** en verde.
- **Móvil:** Logo · [Diagnóstico] · ☰.
- **Footer:** Servicios · Iguana (Nosotros, Precios, Calculadora) · Legal (privacidad, términos) · Redes (Instagram `@iguana.ec`, Facebook, LinkedIn `iguanaec`) · WhatsApp.

## CTAs

Todos terminan en `wa.me/593959420676` con un mensaje prellenado según de dónde viene el clic:

| Origen | Mensaje (borrador) |
|---|---|
| Header / Inicio / Nosotros | "Hola Iguana, quiero mi diagnóstico gratis" |
| Servicio | "Hola Iguana, me interesa {servicio}" |
| Plan | "Hola Iguana, me interesa el plan {Básico/Estándar/Pro}" |
| Calculadora | "Hola Iguana, calculé {N} h al mes ({tareas} al día de {tiempo}). Me recomendaron el plan {plan}" |

## Redirecciones

| Ruta | Destino |
|---|---|
| `/es-para-ti` | `/#calculadora` (la calculadora reemplaza al quiz) |
| `/index.html`, `/precios.html`, `/nosotros.html`, `/es-para-ti.html` | Rutas sin `.html` |

No se crean `/faq`, `/contacto`, `/soluciones`, `/como-trabajamos` ni las subpáginas `/servicios/*`.

## Fase 2 (fuera del MVP)

- `/blog`, alimentado por `iguanaec/content-strategy`.
- Casos reales, cuando haya clientes con permiso.
- Integración con el CRM `iguanaec/iguana.ec`.

## Decisiones abiertas

- ¿Qué incluye cada plan ahora que no es solo el asistente? Propuesta: los planes cubren Agentes IA y automatizaciones simples; Consultoría y A medida van por cotización.
- Umbrales finales de la calculadora para recomendar cada plan (propuesta en `skeleton.md`).
