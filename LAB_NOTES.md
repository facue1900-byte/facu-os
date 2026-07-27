# Lab Notes

Cada vez que algo falla, sale bien de forma no obvia, o revela una restricción escondida,
va una fila acá. **Nunca se borra una entrada** — es registro histórico. Cuando algo se
arregla, se marca `FAIL ✓` y se anota el fix.

Reglas: documentar la **causa raíz**, no el síntoma. Nombrar el script / la API / el skill.
El postmortem completo va acá; la lección corta (dos oraciones) va al `SKILL.md` del skill
afectado. Si es un patrón transferible, se destila como nota en el vault.

| Fecha | Tipo | Qué pasó | Qué hacer la próxima |
|---|---|---|---|
| 2026-07-27 | FAIL ✓ | El conector de Drive (`read_file_content`) devolvió la pestaña Movimientos del Master Plan cortada en 206 de 455 filas, **sin error ni aviso**. Los totales daban más chicos y plausibles. | Bajar siempre el export `.xlsx` completo. Un resultado uniformemente vacío o corto es un error hasta que se demuestre lo contrario: contar las filas antes de confiar en un total. |
| 2026-07-27 | FAIL ✓ | `radar_rampa.py` calculaba `piso = SOLO_EXPENSAS.get(local, 0) if desde > hoy else 0` dentro de la rama donde `desde <= hoy`: la condición estaba muerta y el piso daba **0 fijo**. Un local que pagaba solo expensas (Peak One, $1,71M) podía cruzar el umbral de medio alquiler y figurar "al día" sin haber pagado un peso de alquiler. | Fix: descontar las expensas siempre — el local las paga *además* del alquiler. Toda condición que compara con la variable que ya filtró el `continue` de arriba es sospechosa. |
| 2026-07-27 | LEARN | Los cargos bancarios chicos del Macro (SIRCREB, Ley 25.413, comisiones) cargados uno por uno hacían ruido en Movimientos. Agrupados en una línea mensual cada uno, junio 2026 concilió al centavo. | El criterio de agrupado está verificado contra un mes que cerró exacto. El neto se controla contra el extracto **crudo**, nunca contra el agrupado. |
| 2026-07-27 | LEARN | El extracto del Macro no separa débito de crédito por columna de forma confiable. | Deducir el signo de cómo se movió el saldo línea a línea, arrancando de "SALDO ULTIMO EXTRACTO". |
| 2026-07-27 | LEARN | El Dashboard Mensual matchea ingresos por **Local** y egresos por **Categoría**, con SUMIFS sensible a acentos y espacios. Un local mal escrito no tira error: suma cero y el mes queda desfasado en silencio. | Chequeo de categorías huérfanas en todo cierre. "Apex" → "Peak One" fue exactamente esto. |
| 2026-07-27 | LEARN | Las cuatro copias de `MEMORIA - Paseo Nordelta` en el Desktop divergieron entre sí; ninguna decía cuál era la buena. | Una sola fuente por tema. El estado vive en la memoria de Claude Code y en `active/`, no en copias sueltas con `copy` en el nombre. |
