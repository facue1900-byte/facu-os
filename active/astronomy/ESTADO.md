# Astronomy — estado

Última actualización: 2026-07-27

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
- **Academia** — la app está productiva. Queda: pase de estética final (contra el demo
  aprobado), sitio público etapa 3, y decidir si se reemplaza Calendly por el booking
  nativo (ya está completo y listo).
- **Música** — Sin City: trío de Facu (@thefacu__), Vlado (@vladinicc) y Lucas
  Lanfranconi. Ver memoria `sin-city-proyecto-musical`.

## Pendiente de dato

- Nombre del equipo de pauta.

(Resuelto 27/07/2026: "Mateo Iní" y "Mateo Guini" eran la misma persona — confirmado
por Facu. El nombre correcto es **Mateo Guini**; ya está unificado en todos lados.)
