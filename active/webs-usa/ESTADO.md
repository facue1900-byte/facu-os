# Webs para negocios de EE.UU. sin página — ESTADO

> **26/11 tarde: Facu armó Clave Studio con Mateo Estevez** (agencia para belleza y bienestar en EE.UU.). Ver `active/clave-studio/ESTADO.md`. 🔴 Confirmar si esta línea queda absorbida ahí; hasta entonces no se avanza con Twilio, dominio ni publicación de estas demos.

Arrancado 26/11/2026 a pedido de Facu. **Base: PERSONAL de Facu (confirmado 26/11): negocio nuevo, sin socios. No se suma con Astronomy, Paseo ni campos.**

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
2. Demo: traer reseñas y fotos (`startUrls` en Apify, ver `leads/demo_3.json`), elegir portada/galería en `leads/curacion.json` (y servicios reales si los hay, p. ej. de su tarjeta) → `demo.py`. Cada rubro tiene su estética (SKINS). Publicar en Netlify con URL de preview.
3. Mensaje (abajo) con el link → Facu lo manda.
4. Si dice que sí: link de pago de Stripe → dominio → se publica.

**Mensaje base (WhatsApp, ES):**
> Hola [nombre], vi [negocio] en Google Maps, tienen [X] reseñas muy buenas pero no tienen página web. Les armé una de muestra, sin compromiso: [link]. Si les gusta, la dejamos andando con su dominio esta semana. ¿Le doy una mirada con usted?

## Contador (regla 24)
| Fecha | Leads sacados | Demos hechas | Contactados | Respondieron | Pagaron |
|---|---|---|---|---|---|
| 26/11 | 51 (jardinería Houston 15, limpieza Miami 5, remodelación Houston 15, detailing Dallas 16) | 3 (MedinaLawn, PGM, Chuy's) | 0 | 0 | 0 |

## Pendientes de dato
- ✅ Apify cargado 26/11. `leads.py` corrido: 240 lugares, 51 sin web con teléfono (CSV en `leads/`, gitignoreado).
- ✅ `demo.py leads/demo_3.json` arma la web con reseñas y fotos reales (ciudad por código de área; frena si queda texto de plantilla). 26/11 rediseño «mega profesional» a pedido de Facu: foto real a pantalla completa, tipografía y paleta por rubro, horarios reales, formulario que abre WhatsApp. Mirado en escritorio 1280 y celular 500 px.
- 🔴 Twilio está en TRIAL con US$0: Facu tiene que pasarla a paga y cargar saldo antes de comprar el número.
- 🔴 Publicar las 3 demos en Netlify (URL de preview, noindex) con OK de Facu.
- ✅ 26/11 Facu: los 4 rubros a la vez — jardinería Houston, limpieza Miami, remodelación Houston, detailing Dallas (~60 lugares c/u ≈ US$1 de Apify).
- ✅ Número: uno de EE.UU. nuevo en Twilio + WhatsApp Business. 🔴 Comprarlo sólo con el OK de Facu (gasto mensual).
- 🔴 Stripe: Facu la abre. **Ojo:** Shopify Payments exige vivir en EE.UU. y Stripe pide domicilio en EE.UU.; a confirmar si alcanza con ser ciudadano + SSN + BofA viviendo en Argentina. Plan B: domicilio de un familiar en EE.UU., o LLC (Stripe Atlas).
- Marca: .com libres verificados por RDAP el 26/11: holasitio.com (recomendado), sitiodelbarrio.com, webdelbarrio.com, placitaweb.com, latinolisto.com; 2ª tanda: sitiocompadre.com, andalesites.com, negocioarriba.com, webencasa.com, elsitiolisto.com, buenvecinoweb.com, webderaiz.com. 🔴 Facu elige; el dominio se compra con su OK.
