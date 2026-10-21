# Sitemap: iguana.ec (rediseño 2026)

> "Sitio actual" = rama `main` (`90070b5`).

> Fase 1 del rediseño: **sitemap → esqueleto → diseño → copy**.
> Este documento define *qué páginas existen y para qué*. El orden de secciones de cada página está en [`skeleton.md`](skeleton.md) y los mapas visuales en [`maps/`](maps/).

## Posicionamiento (lo que cambia)

| Antes | Ahora |
|---|---|
| Producto único: asistente de WhatsApp con IA | **Agencia de IA**: varios servicios, el asistente es uno más |
| Promesa: "Tu negocio no necesita más manos. Necesita evolucionar." (home en `main`) | Se amplía a **ahorrar tiempo, ordenar procesos y adaptarse** a un mercado que cambia muy rápido |
| Planes Esencial / Crecimiento / Pro / A medida, con mapa de islas | Planes genéricos: **Básico · Estándar · Pro · A medida**, sin islas |
| Paquetes cerrados | **Soluciones a medida** de cada negocio como mensaje central |

Se mantienen el concepto de marca (la iguana que se adaptó), el tono (tuteo, directo, "sin letras chicas", sin permanencia), el diagnóstico gratis de 15 min y la implementación en unos 11 días.

## Árbol

```
iguana.ec
├── /                              Home
├── /servicios                     Hub de servicios
│   ├── /servicios/automatizacion    Automatización de procesos con IA
│   ├── /servicios/agentes-ia        Asistentes y agentes de IA (incluye WhatsApp)
│   ├── /servicios/consultoria       Consultoría, diagnóstico y capacitación en IA
│   └── /servicios/a-medida          Desarrollo a medida e integraciones (incluye webs)
├── /como-trabajamos               Proceso de trabajo
├── /soluciones                    Soluciones por tipo de negocio
├── /precios                       Planes y comparativa
├── /es-para-ti                    Quiz de recomendación
├── /nosotros                      Historia, misión y equipo
├── /faq                           Preguntas frecuentes
├── /contacto                      Agendar diagnóstico
├── /privacidad                    (pie) Política de privacidad, stub
├── /terminos                      (pie) Términos, stub
└── /404
```

**14 rutas.** Las 4 actuales (`/`, `/precios`, `/es-para-ti`, `/nosotros`) conservan su URL.

## Páginas

| URL | Objetivo | Público principal | CTA primario | CTA secundario |
|---|---|---|---|---|
| `/` | Explicar en 10 s qué es Iguana (agencia de IA) y llevar al diagnóstico | Dueños de pymes y profesionales que pierden tiempo en tareas repetitivas | Agenda tu diagnóstico gratis | ¿Es para ti? (quiz) |
| `/servicios` | Mostrar los 4 servicios y ayudar a elegir | Quien ya entendió la propuesta y compara | Ver servicio → | ¿No sabes cuál? (quiz) |
| `/servicios/automatizacion` | Vender automatización de procesos repetitivos | Negocios con tareas manuales (reportes, registros, seguimientos) | WhatsApp prellenado "Automatización" | Ver precios |
| `/servicios/agentes-ia` | Vender asistentes y agentes (WhatsApp, atención, agenda, cotizaciones, pedidos) | Negocios con alto volumen de mensajes o citas | WhatsApp prellenado "Agentes IA" | Ver precios |
| `/servicios/consultoria` | Vender diagnóstico, hoja de ruta y capacitación en IA | Equipos que no saben por dónde empezar | WhatsApp prellenado "Consultoría" | Cómo trabajamos |
| `/servicios/a-medida` | Vender desarrollo a medida, integraciones y webs que convierten | Negocios con procesos propios o varias sedes | WhatsApp prellenado "A medida" | Cómo trabajamos |
| `/como-trabajamos` | Bajar el riesgo percibido: pasos, plazos y qué pasa después | Indecisos | Agenda tu diagnóstico gratis | FAQ |
| `/soluciones` | Que cada tipo de negocio se reconozca | Llega desde anuncios o redes por vertical | Agenda tu diagnóstico gratis | Ver servicio relacionado |
| `/precios` | Mostrar precio claro y sin letras chicas | Listos para decidir | Elegir plan → WhatsApp con plan | A medida → Hablemos |
| `/es-para-ti` | Calificar y recomendar servicio + plan | Indecisos que no quieren hablar todavía | Resultado → WhatsApp prellenado | Ver servicio recomendado |
| `/nosotros` | Generar confianza: quiénes somos y por qué la iguana | Quien quiere saber con quién trabaja | Agenda tu diagnóstico gratis | — |
| `/faq` | Resolver objeciones sin hablar con nadie | Todos | Agenda tu diagnóstico gratis | Contacto |
| `/contacto` | Convertir: un solo paso al diagnóstico | Listos | WhatsApp | Redes |
| `/privacidad`, `/terminos` | Cumplimiento básico | — | — | — |
| `/404` | Recuperar la visita | — | Volver al inicio | Servicios |

## Navegación

**Header (desktop):** Logo · Servicios ▾ (los 4) · Cómo trabajamos · Soluciones · Precios · Nosotros · **[Agenda tu diagnóstico gratis]**
**Header (móvil):** Logo · [Diagnóstico] · ☰ (mismo orden, Servicios desplegado)
**Footer:** Servicios (4) · Empresa (Nosotros, Cómo trabajamos, FAQ, Contacto) · Herramientas (¿Es para ti?, Precios) · Legal (Privacidad, Términos) · Redes (Instagram `@iguana.ec`, Facebook, LinkedIn `iguanaec`) · WhatsApp
**Fuera del menú, pero con entrada:** `/es-para-ti` (CTA secundario en home, servicios y footer) y `/faq` (bloque FAQ corto al final de cada página + footer).

## Mapa de CTAs

Todo termina en **WhatsApp `wa.me/593959420676`** con mensaje prellenado según el origen, para que el equipo sepa de dónde viene cada lead:

| Origen | Mensaje prellenado (borrador, el copy final va en fase 4) |
|---|---|
| Header / home / contacto | "Hola Iguana, quiero mi diagnóstico gratis" |
| Página de servicio | "Hola Iguana, me interesa {servicio}" |
| Precios | "Hola Iguana, me interesa el plan {Básico/Estándar/Pro}" |
| A medida | "Hola Iguana, quiero algo a medida para mi negocio" |
| Quiz | "Hola Iguana, hice el quiz: {resumen de respuestas} → {recomendación}" |

## Redirecciones

| Ruta actual | Destino | Motivo |
|---|---|---|
| `/index.html` | `/` | URLs sin extensión (Cloudflare ya lo hace) |
| `/precios.html`, `/nosotros.html`, `/es-para-ti.html` | sin `.html` | Ídem; además los enlaces internos deben usar la ruta limpia |
| `/#soluciones` (ancla de "Lo que hacemos" en la home actual) | `/servicios` | La sección pasa a página propia |

## Fase 2 (fuera del MVP)

- `/blog`: alimentado por el pipeline de `iguanaec/content-strategy`.
- `/casos/<cliente>`: solo con clientes reales y permiso.
- Integración con el CRM de `iguanaec/iguana.ec`.

## Decisiones abiertas

- ¿Los 4 servicios (automatización, agentes IA, consultoría, a medida) son la lista correcta?
- ¿Qué incluye cada plan ahora que no es solo el asistente? Hoy los planes describen el asistente (50 mensajes en Básico; "más mensajes" en Estándar y Pro sin cifra).
- ¿El sitio migrará a la organización `iguanaec`?
