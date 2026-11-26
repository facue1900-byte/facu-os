# Webs para negocios de EE.UU. sin página — ESTADO

Arrancado 26/11/2026 a pedido de Facu. **Base: ¿personal de Facu (como cripto) o de la empresa? — sin definir, preguntar antes de repartir nada.**

## La apuesta (en una línea)
Negocios locales hispanos de EE.UU. con buenas reseñas en Google y **sin web** → les mandamos **su web ya hecha** (demo con su nombre, fotos y reseñas reales) → cobro de setup + mensualidad por Stripe.

**Por qué hispanos:** la mayoría de las agencias que salieron de los reels hacen esto en inglés. Atender en español es una ventaja real y el equipo ya la tiene.

## Oferta a probar (hipótesis, no medida)
- Setup: US$299–499 una vez. Mensualidad: US$49/mes (hosting, cambios chicos, ficha de Google).
- Costo nuestro por cliente: dominio ~US$10–15/año (a confirmar al comprar) + hosting gratis (Netlify/Cloudflare Pages).
- Meta de prueba: **3 clientes pagando en 30 días**. Si con 100 contactos no sale ni 1, se para y se revisa el canal, no se construye más.

## Cobro
Facu es ciudadano de EE.UU. → Stripe como persona (SSN, sin LLC) con payout a la BofA. 🔴 Confirmar con Facu y su contador de EE.UU. que lo declara ahí.

## Canal y reglas (regla 10: nada sale sin OK)
- Los negocios sin web casi nunca tienen mail: el canal es **llamada o WhatsApp 1 a 1, humano**. Nada de SMS masivos ni marcador automático (TCPA en EE.UU.: multas por mensaje).
- Si se usa mail: dirección física + baja en cada mail (CAN-SPAM) y un dominio aparte, nunca el de Astronomy.

## Embudo
1. `leads.py "<rubro>" "<ciudad>"` → CSV de sin-web con teléfono, ordenado por reseñas.
2. Demo: copiar `demo/index.html`, reemplazar lo marcado `data-fill` (nombre, tel, fotos y reseñas reales de su ficha). Publicar en Netlify con URL de preview.
3. Mensaje (abajo) con el link → Facu lo manda.
4. Si dice que sí: link de pago de Stripe → dominio → se publica.

**Mensaje base (WhatsApp, ES):**
> Hola [nombre], vi [negocio] en Google Maps, tienen [X] reseñas muy buenas pero no tienen página web. Les armé una de muestra, sin compromiso: [link]. Si les gusta, la dejamos andando con su dominio esta semana. ¿Le doy una mirada con usted?

## Contador (regla 24)
| Fecha | Leads sacados | Demos hechas | Contactados | Respondieron | Pagaron |
|---|---|---|---|---|---|
| 26/11 | 0 | 1 plantilla | 0 | 0 | 0 |

## Pendientes de dato
- 🔴 `APIFY_API_TOKEN` está vacío en `.env` → sin esto no hay lista. (Plan gratis: US$5/mes de crédito ≈ 1.000 lugares.)
- 🔴 Primer rubro + ciudad (propuesta: landscaping en Houston, después cleaning en Miami).
- 🔴 Base: personal o empresa.
- `leads.py` **no se corrió todavía** (falta la key): primera corrida = verificación.
