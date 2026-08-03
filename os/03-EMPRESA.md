# Memoria de la Empresa — qué se mide y qué se registra

`EMPRESA-v1` · 03/08/2026

**Este archivo no describe los negocios** — eso vive en `~/.claude/CLAUDE.md` y no se
duplica (regla 12: una sola fuente de verdad). Acá va lo que ese archivo no tiene:
**qué número mira cada negocio, de dónde se saca, y dónde se escribe cada cosa.**

---

## Objetivos — próximos 3 a 6 meses

1. **Más plata, mes a mes.** Todo lo que genere ingresos este mes va primero.
2. **Menos horas de Facu en tareas de bajo valor**, para usar el tiempo pensando cómo
   hacer más plata.
3. Todo lo demás es interesante y va al backlog, no a la agenda.

## KPIs — el tablero

Regla: **un KPI sin fuente escrita no es un KPI, es una impresión.** La columna "dónde
se saca" es lo que hace que el número se pueda volver a calcular igual el mes que viene.
Los valores de abajo son la última lectura conocida, con su fecha: **si el valor y la
fuente no coinciden, manda la fuente.**

### Astronomy Academy

| KPI | Dónde se saca | Última lectura |
|---|---|---|
| Margen operativo | `sales` (Supabase) menos egresos de la planilla *Finanzas - Astronomy Academy*, hoja Base | **−3,0%** acumulado 10 meses (31/07/2026) |
| Ingresos del mes | tabla `sales` → `/admin/libro` | — |
| Egresos del mes | planilla de finanzas, hoja Base — **no están en Supabase** | julio incompleto: 3 filas y una era un test |
| Costo por lead | API de Meta Ads, cuenta `CP - Astronomy Academy` | **US$1,94/lead** (31/07/2026) |
| Gasto de pauta | API de Meta, 1 al 1 del mes — **no** el extracto del BofA, que cierra 15-al-15 y desfasa el margen hasta 49% | techo definido: **US$500/mes sólo Meta** |
| Alumnos activos | `profiles` con `es_interno = false` | **49 reales** + 9 cuentas internas (01/08/2026) |
| Precios de catálogo | web / Supabase | Silver $143.520 (250 cr) · Gold $195.600 (360) · Platinum $272.000 (480) |

Detalle y trampas de cada uno: memorias `astronomy-margen-real`, `meta-ads-astronomy`,
`pauta-como-se-carga-el-egreso`, `cuentas-internas-astronomy`, `astronomy-catalog-data`.

### Paseo Nordelta

| KPI | Dónde se saca | Nota |
|---|---|---|
| ¿El operativo cierra o no cierra? | skill `cierre-mes-nordelta` — extracto Macro vs. Master Plan | **La pregunta de fondo del negocio.** |
| Cobrado vs. facturado del mes | Master Plan + Ctas Ctes | quién no pagó, cuánto falta |
| Rampa de alquileres | `radar_rampa.py` | próxima alta: La Jaula, **$2M/mes desde agosto 2026** |
| Caja: efectivo, transferencia, banco | seguimiento diario, pesos y dólares | incluye compra/venta de USD |
| Recupero de la inversión | plan de financiación | el número que miran los inversores |

### Astronomy Eventos

| KPI | Dónde se saca | Nota |
|---|---|---|
| Conversión invitado → asistente | export de Passline: quién **entró**, no quién compró | el dolor declarado #1 |
| Resultado por evento | libro compartido estilo Splitwise, no porcentajes fijos | ver `eventos-libro-compartido` |

### Campos (Chaco)

| KPI | Dónde se saca | Nota |
|---|---|---|
| Precio de la carne del día | mercado | define cuándo vender y a cuánto el kilo |
| % de desbaste | negociación | entra en el precio efectivo |
| Punto de venta de una jaula (32 cabezas) | conteo + precio + desbaste | lo que hay que sistematizar |

**Restricción no negociable de Chaco:** conectividad mala, poca tecnología, gente que no
va a usar una app complicada. WhatsApp, papel y planillas simples por sobre cualquier
sistema que requiera entrenamiento.

---

## Estándares

**Branding.** Astronomy Academy tiene manual oficial: `active/astronomy/BRANDING_ACADEMY.md`
(Aktiv Grotesk + Roboto Mono; blanco, negro y azul marino `#180040`, tres colores y nada
más). **No aplica a eventos**, que tienen su propia estética y a veces marcas de terceros.

**Diseño de producto.** Minimalista y consistente: sin emojis en la web (rótulos mono en
mayúsculas), tamaños y colores parejos y medidos en el navegador, toda lista larga con su
propio scroll a 20 filas, nada de diálogos nativos. Detalle en las memorias
`app-aesthetic-rules`, `estetica-simetrica-siempre`, `estetica-sin-emojis`, `regla-20-filas`.

**Datos centralizados — con una trampa.** Hay **dos bases de Supabase distintas**, una
por negocio (Astronomy y Paseo Nordelta). Antes de un query o una migración, confirmar
contra cuál se está pegando: un `ref` equivocado escribe en el negocio equivocado y no
avisa.

**Versionado.** Los documentos de `os/` llevan tag de versión arriba (`CONSTITUCION-v1`).
Cambio de fondo → sube la versión y se anota qué cambió. El código va en git.

---

## Dónde se escribe cada cosa — las tres capas

Si se mezclan, los documentos se llenan de data vieja y empiezan a mentir.

| Capa | Dónde | Qué va | Ejemplo |
|---|---|---|---|
| **Reglas** | `~/facu-os/os/` | Lo que vale en toda sesión, todo negocio | "nada sale al mundo sin OK" |
| **Ejecución** | `~/facu-os/` | Código, skills, estado operativo por frente | `cierre-mes-nordelta`, `active/*/ESTADO.md` |
| **Estado** | memoria de Claude Code | En qué quedó cada cosa, con fecha | "el podio de julio corrió el 1/8" |

> `~/.claude/` es un repo git desde el 03/08/2026 (local, sin remoto). Versiona
> `CLAUDE.md`, `settings.json`, `scripts/` y las memorias; el `.gitignore` es lista
> blanca, así que **lo que se agregue ahí adentro no entra hasta que alguien lo habilite**.

| **Conocimiento** | `~/Obsidian/facu-vault/` | Lo que va a seguir siendo cierto en un año | patrones, aprendizajes destilados |
| **Data cruda** | `~/Desktop/` | Extractos, exports, PDFs, planillas | por path absoluto, no se mueve |

## Qué se registra siempre

- **Procesos**: cuando algo se hizo 3 veces igual, se escribe.
- **Decisiones**: qué se decidió, cuándo, y **por qué** — el porqué es lo que se olvida.
- **KPIs**: valor, fecha y fuente. Los tres o no cuenta.
- **Automatizaciones**: qué corre solo, cada cuánto, y cómo se sabe si falló.
- **Errores y soluciones**: `LAB_NOTES.md`, con causa raíz.
- **Pendientes de dato**: lo que falta para que un número cierre, escrito donde se va a
  volver a necesitar, no en la cabeza de nadie.
