# Paseo Nordelta — estado

Última actualización: 2026-07-27

## Qué es

Paseo comercial en Nordelta. 2.292 m². Algunos locales operativos, otros en obra.
La obra se financia casi 100% con capital de socios: **Richi ~$150–161M**,
**Facu ~$23M**, invertido en obra ~$166M (a julio 2026).

> **No confundir con [Nordelta Plaza](../nordelta-plaza/ESTADO.md)** — son dos negocios
> distintos, con sociedades, socios, bancos y carpetas separados. Paseo Nordelta opera
> por el **Banco Macro**; Nordelta Plaza (NDPL SAS) por el **BBVA**.

## Dónde está todo

| Qué | Path |
|---|---|
| Extractos Banco Macro | `~/Desktop/Paseo Nordelta/Principio de mes/Resumen de Banco Paseo Nordelta/<año>/` |
| Cierre de mes (facturas, impuestos, sueldos) | `~/Desktop/Paseo Nordelta/Principio de mes/` |
| Logos | `~/Desktop/Paseo Nordelta/Logotipos Nordelta Plaza/` |
| Web e informes a inversores | `~/Desktop/Paseo Nordelta/Paseo Nordelta - CLAUDE/` |

Sheets: **Master Plan** `1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs` ·
**Gastos Obra** `1wxaXia5lvoYk9lPZ_2Ie9imhxexUqmaU0wFqryNjIDY`

Skill: [`cierre-mes-nordelta`](../../.claude/skills/cierre-mes-nordelta/SKILL.md)

## Último cierre verificado

**Junio 2026** — conciliación banco impecable (neto y saldo al centavo).
Resultado del negocio **+$5,4M** (2º mejor mes). Saldos al cierre: Caja ~$4,37M ·
Banco $4.119.498 · USD 0.

## La rampa de alquileres (lo que más plata mueve)

A julio 2026 cobra alquiler de 5 locales. **$27,4M/mes están sin generar** sobre un
potencial de $51,4M/mes. Cada mes de atraso en un alta cuesta entre $2M y $15M.

| Mes | Alta | Alquiler |
|---|---|---|
| ago-2026 | La Jaula | $2M |
| nov-2026 | Cafetería | $3,5M |
| dic-2026 | Peak One | $4M |
| ene-2027 | Pizzería $2M + Salón Multiespacios $2,5M + Heladería nueva $5M | $9,5M |
| ~jul-2027 | Market | $4M |
| post-Market | Comercios 1 a 6 | $12M |

Run-rate neto comprometido a enero 2027: **$17,12M/mes**.
Peak One y Salón pagan solo expensas hasta nov y dic. La Cafetería paga dos meses de
expensas solas (sep y oct) antes del alquiler.

**Próxima alta a controlar: La Jaula, agosto 2026.**

## Frentes abiertos

- Parrilla para los 354 m² de Fabric: sin firmar. Mudar a Fabric al local de 88,3 m² no
  genera plata ($13,5M en los dos escenarios) — no moverlo sin la parrilla firmada.
- Comercios 1-6 y Market: no construidos. La fecha de los Comercios (2028-01) es un
  placeholder, no un compromiso.
- Se demuele solo la heladería vieja, cuando arranque la nueva.

## Pendientes operativos (de la memoria migrada, 27/07/2026)

- **Bigg debe la mitad en efectivo de julio** (~$1.910.387, "Diferencia Alquiler").
  Es el único que debe efectivo hoy. Ver memoria `paseo-ctas-ctes-import`.
- **La Jaula**: tenía saldo a favor; se le cobra recién desde agosto 2026. Los ~$12,6M
  cargados ene–jul en Ctas Ctes son un estimado inventado y hay que borrarlos.
- Ctas Ctes: `generarCargosDelMes` todavía lee CONTRATOS (valores viejos) en vez de
  Expensas Predio — no activar la generación automática hasta arreglarlo.
- **$0,69 de diferencia** entre el saldo de cierre del extracto de junio ($4.119.498,46)
  y la pestaña Saldo Actual ($4.119.497,77) — la detectó `conciliar.py` el 27/07.

## Pendiente de dato

- Bajo qué sociedad opera Paseo Nordelta (NDPL SAS es Nordelta Plaza, no esto).
- Qué relación societaria hay, si hay alguna, entre Paseo Nordelta y Nordelta Plaza.
