# Astronomy — estado

Última actualización: 2026-07-28

Participaciones, ramas, equipo y objetivos: en el CLAUDE.md global. Acá va solo lo
operativo y lo que cambió.

## Dónde está todo

`~/Desktop/Productoras/Astronomy/` y `~/Desktop/Productoras/Puzzle/`

**La academia se gestiona con app propia**: `astronomy-members` (Next.js + Supabase +
Mercado Pago), **en producción en astronomyofficial.com**. Código en
`~/Desktop/Productoras/Astronomy/astronomy-members/`. El detalle vive en la memoria
(`membership-system-project`, `reconciliacion-pagos-sistema`, `egresos-sistema`).

## Datos que ya no son hueco (migrados a la memoria el 27/07/2026)

Fuente: la web y la app en producción (verificado 09-24/07/2026).

- **Membresías** (mensuales, ARS): Silver $143.520 / 250 créditos · Gold $195.600 / 360 ·
  Platinum $272.000 / 480 · Bronze $1 (secreta, para amigos, a mano).
- **Costos en créditos**: clase individual (DJ o producción) 60 · alquiler cabina/estudio 50 ·
  clase grupal 50 por alumno.
- **Regla central de créditos**: las membresías **acumulan** mes a mes; el Curso de DJ
  **renueva** (cada pago resetea a 240 = 4 clases). Los créditos vencen a los 3 meses.
- **Clases**: cancelación con menos de 24 hs no devuelve créditos y el profe cobra igual;
  con más de 24 hs devuelve y el profe no cobra. Anticipación mínima para agendar: 12 hs.
  Los dos umbrales son editables desde la app (`studio_config`).
- **Cobros**: suscripción por Mercado Pago + cargas manuales. `sales` es la fuente única
  de verdad de la plata; la comisión de José (closer) sale de ahí.

## Frentes abiertos

- **Eventos** — lo que más duele: invitaciones. 1) conversión invitado → asistente,
  2) FOMO real, 3) influencers a bajo costo.

  **Puzzle: dos fechas analizadas end-to-end (27/07/2026).** Datos en
  `data/eventos/puzzle/` (gitignoreado: ~1.500 personas con mail, teléfono y DNI).
  Todo verificado contra el panel de Passline y contra los totales de la planilla.

  | | Abril (490638) | Junio (514816) |
  |---|---|---|
  | Entradas | 823 pers · $19.030.000 | 727 pers · $14.460.000 |
  | Mesas | 470 pers · $20.662.500 | 436 pers · $21.580.000 |
  | **Total** | **1.293 pers · $39.692.500** | **1.163 pers · $36.040.000** |
  | Ocupación (aforo 2.000) | 64,6% | 58,1% |

  Hallazgos accionables:
  - **La mesa vale 1,9x–2,5x la entrada** por persona ($43.963 y $49.495 vs $23.123 y
    $19.890). Las mesas son el 52% y el 60% del ingreso con ~37% de la gente.
  - **Cortesías curadas convierten 7,6x mejor**: en junio, las 391 que estaban en las
    planillas del Desktop entraron al 55,8%; las 262 sueltas, al 7,3%.
  - **Techo de precio de entrada: $25.000–$30.000.** Todo tier de $25k para abajo se
    agotó; de $30k para arriba quedó stock con días por delante. Idéntico en las dos fechas.
  - **El 74% entra entre las 2 y las 3 AM**, en una sola hora.
  - **Retención 22%**: de 633 que entraron en abril, 140 volvieron en junio. Esa lista de
    140 vale más que cualquier lista de RRPP y hoy no existe como activo.
  - **Vladimir Nadinic: 90 cortesías en las dos fechas, 0 validadas.** Cero es demasiado
    limpio para ser "convierte mal" — algo está roto (no se enviaron, link caído, o
    cargadas a un nombre que no las repartió). **Preguntarle antes de concluir.**
  - Junio colocó 37 de 46 mesas (80%) vs abril 43 de 45 (96%). Las 9 sin colocar no son
    plata por cobrar (Facu confirmó: no se vendieron o se regalaron), pero ahí hay más
    plata que en optimizar las cortesías.

  **Dónde vive el dato de mesas**: Drive de la cuenta `facu` (no `studio`), planillas
  `RompeCabezas - Master Plan` y `RompeCabezas 2.0 - Master Plan`, pestaña
  **`Ingresos/Mesas`, la tabla de abajo** (fila ~29 en adelante). El resumen de arriba y la
  pestaña del plano de mesas **no cierran** con el ingreso — no usar esas.

  Pendiente: escribir `wiki/eventos/`, que sigue vacía.
- **Academia** — la app está productiva. Queda: pase de estética final (contra el demo
  aprobado), sitio público etapa 3, y decidir si se reemplaza Calendly por el booking
  nativo (ya está completo y listo).
- **Música** — Sin City: trío de Facu (@thefacu__), Vlado (@vladinicc) y Lucas
  Lanfranconi. Ver memoria `sin-city-proyecto-musical`.

## Pendiente de dato

- Nombre del equipo de pauta.

(Resuelto 27/07/2026: "Mateo Iní" y "Mateo Guini" eran la misma persona — confirmado
por Facu. El nombre correcto es **Mateo Guini**; ya está unificado en todos lados.)
