# Mensaje para Luqui — PREPARADO Y FRENADO

**No se manda hasta que Facu dé el OK** (regla 10). Escrito el 04/08/2026.

**Por qué existe:** el 26/07 se cambió en el código la fecha desde la cual el reporte de
finanzas deja de leer la planilla y pasa a leer la app. **Nadie se lo dijo a Luqui.** No
dejó de cargar por desidia: el lugar donde hay que cargar cambió y no se enteró.

**[HECHO] Y hoy pasó el caso que lo prueba — con una corrección importante.** El pago de
*Juan Manuel Inchausty · Silver · $143.520 · transferencia* **Luqui lo cargó bien y en la
web**: `audit_log` lo registra a las 15:17 UTC del 04/08 desde `/admin/carga-manual`, con
+240 créditos y fecha de pago 31/07. Media hora después, a las 15:46, el cron trajo la copia
del Form con fecha **04/08**.

**El pago estaba en las dos fuentes con dos fechas distintas — y con el corte en el 01/08 no
lo contaba ninguna:**

| | Dónde | Fecha | ¿Lo leía el reporte con el corte en 01/08? |
|---|---|---|---|
| La web | `sales` (`manual:7cb33a79…`) | 31/07 | **No** — el sistema recién empieza el 01/08 |
| El Form | `payment_links` | 04/08 | **No** — la planilla sólo se lee antes del 01/08 |

**Mover el corte al 25/07 lo arregló:** ahora se cuenta una vez, por la venta del 31/07.
**[HECHO] Verificado contra la base el 04/08.**

> **La trampa que deja la doble carga, y que hay que mirar mientras dure:** el mismo pago
> cargado con **fechas distintas** en los dos lados puede caer de los dos lados del corte.
> Hoy salió gratis; si la fecha del Form hubiera sido anterior al 25/07 y la de la web
> posterior, el pago se contaba **dos veces**.

---

## El mensaje

> Hola Luqui, te aviso un cambio importante que es culpa nuestra por no habértelo dicho antes.
>
> **Desde fines de julio, el reporte de finanzas dejó de leer la planilla y pasó a leer la
> web.** Nadie te lo dijo, así que esto no es un reclamo: es información que te faltaba.
>
> Arrancá por lo bueno: **la carga de Inchausty de hoy la hiciste perfecto.** Quedó el pago
> registrado y los 240 créditos acreditados en un solo acto — eso el Form no lo hace, y es
> justo lo que hacía que algunos alumnos pagaran y se quedaran sin créditos.
>
> **Lo que hay que cargar ahora en la web, no en el Form:**
>
> - **Los ingresos que no pasan por Mercado Pago**: efectivo, transferencias y clases de
>   prueba. Van en `astronomyofficial.com/admin/carga-manual`. Eso además le acredita los
>   créditos al alumno en el mismo acto — cosa que el Form **no hace**, y es la razón por la
>   que a veces alguien paga y se queda sin créditos.
> - **Todos los egresos**: alquiler, sueldos, Splice, pauta, insumos. Van en
>   `astronomyofficial.com/admin/libro` → pestaña "Salió".
>
> Los cobros de Mercado Pago **no los cargues**: ésos entran solos.
>
> **Y hay una semana que quedó sin cargar en ningún lado: del 25 al 31 de julio.** Los cobros
> de Mercado Pago de esos días ya están, pero lo que fue efectivo, transferencia o gasto no
> está en ninguna parte. ¿Podés cargarlos en la web cuando puedas? Si no te acordás de todo,
> decime qué sí y qué no y lo vemos.
>
> Si algo no te cierra o te falta un acceso, escribime y lo resolvemos en el momento.

---

## Lo que hay que verificar antes de mandarlo

1. **[HECHO] Luqui tiene los dos permisos**: `add_credits` (para la carga manual) y
   `view_salaries` (para los egresos). No hace falta darle nada.
2. **Decidir qué pasa con el Form.** Si sigue existiendo "por las dudas", va a seguir
   recibiendo cargas que nadie lee. **[OPINIÓN] O se apaga, o se le pone un aviso arriba
   que diga que desde agosto no se usa.**
3. **El pago de Inchausty YA ESTÁ BIEN CARGADO** — se corrigió el corte y ahora se cuenta.
   No hay nada que rehacer, y conviene decírselo así: hizo bien el trabajo.
4. **[OPINIÓN] Mientras dure la doble carga, que la FECHA sea la misma en los dos lados.**
   Es lo único que puede hacer que un pago se cuente dos veces.
