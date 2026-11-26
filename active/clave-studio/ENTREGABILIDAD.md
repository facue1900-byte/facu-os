# Por qué los mails van a Spam y cómo se arregla — 26/11/2026

## Comprobado (con la fuente)
1. **Gmail lo dice textual** en el mail de Mateo (reenviado a facu1900, carpeta Spam): «Este mensaje se parece a otros mensajes que se han identificado como spam anteriormente». Causa = **parecido del contenido** con mails ya marcados como spam.
2. **No es configuración técnica del remitente:** SPF, DKIM y DMARC dan `pass` para clave.studio1@gmail.com (encabezados del mail).
3. **Hay mucho volumen del mismo molde:** ~934 previews publicados en github.com/clave-studio; cada uno se manda con la misma estructura, el mismo link `clave-studio.github.io/...` y una imagen con el mismo diseño. Cuántos mails salieron y cuántos se marcaron como spam: **no lo sé** (sólo Mateo lo ve).
4. **clavestudio.org no tiene mail:** sin MX, sin SPF, sin DKIM, DMARC `p=none` (dig 26/11).
5. **Al mail le falta dirección postal y baja** (CAN-SPAM). Es obligación legal; no está probado que sea causa del spam.

## Lo que NO se puede saber desde afuera
Qué parte exacta del mail tomó Gmail como «parecida» (Google no lo publica) y la reputación de la cuenta. Por eso cada cambio se **mide con un test de bandejas**, no se da por bueno.

## Plan, en orden
Ver la respuesta del 26/11 en la sesión; resumen:
0. Frenar el molde actual. 1. Test de bandejas. 2. Mail único por negocio. 3. Previews en dominio propio. 4. Imagen fuera del 1er mail (A/B). 5. Dirección + baja. 6. Rampa 10→50/día. 7. Verificar mails antes de mandar. 8. Dominio propio con Workspace + Postmaster Tools. 9. Corte automático por métricas.
