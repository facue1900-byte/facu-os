# Agente de inquilinos — Paseo Nordelta

Lo corre una rutina diaria en la nube de Claude (con la Mac de Facu apagada). Creado el
20/11/2026 a pedido de Facu. **Este archivo es la única fuente de las instrucciones**: si
cambian los locales o el criterio, se cambia acá, no en el prompt de la rutina.

## Qué es el Paseo

Paseo Nordelta: paseo comercial en Nordelta (Tigre, zona norte del GBA), de MAHNI
MANAGEMENT S.A. Público de alto poder adquisitivo, familias. Hoy tiene o tiene comprometidos:
heladería (Shock), gimnasio (BIGG), wellness, parrilla, hamburguesería, cafetería (en
negociación), academia de DJ, y un lavadero de autos en el futuro. **No buscar esos rubros.**

## Qué hay que llenar (Facu, 20/11/2026)

| Local | Superficie | Entrega |
|---|---|---|
| **8 locales de servicios** | 29,7 m² c/u (3,30 m de frente × 9 de fondo), sobre el paseo, junto al Market | obra en gris · julio 2027 aprox. |
| **Market** | ~119 m² en planta libre (~13 m de frente × 9), junto al acceso principal | obra en gris · julio 2027 aprox. |

Rubros que encajan en los de servicios: estética, peluquería, barbería, uñas, depilación,
farmacia o perfumería, óptica, veterinaria o pet shop, tintorería/lavandería, consultorios,
laboratorio de análisis, kinesiología, celulares y reparación, regalería, librería,
inmobiliaria, agencia de viajes, cerrajería, punto de retiro de paquetería, cajero/sucursal.
Para el Market: supermercado de cercanía premium, almacén gourmet, dietética o tienda
natural de cadena, carnicería o verdulería premium con varias sucursales.

## A quién buscar

**Marcas o comercios que ya tienen 2 o más sucursales y se están expandiendo**, idealmente en
zona norte (Tigre, Nordelta, Benavídez, Escobar, Pilar, San Isidro, Vicente López) o en
barrios de perfil parecido de CABA. Un comercio de una sola sucursal sólo si es muy fuerte.

Dónde mirar (variar las fuentes día a día):
- Noticias de aperturas y expansión (iProfesional, Infobae, La Nación, Clarín, diarios de zona
  norte, Revista Mercado, Brandlab).
- Portales de franquicias argentinas (AAMF, franquiciasonline, mundofranquicia, etc.) y la
  sección «Franquicias» o «Expansión» de cada marca.
- Posteos públicos de marcas que anuncian «próxima apertura» o «buscamos locales».
- Competencia directa: qué marcas abrieron en otros paseos de la zona (Nordelta Centro
  Comercial, Paseo Puerto Escondido, Tortugas Open Mall, Unicenter, Paseo Champagnat, Las
  Palmas del Pilar) en el último año.

Para cada candidato hace falta un **contacto comercial público**: mail de expansión,
franquicias o comercial que figure en su web o en una nota. **Entrar a la web de la marca
(páginas «Franquicias», «Expansión», «Contacto») antes de marcarlo «sin contacto».** Si un
sitio no abre por la red de la sesión, decir cuál en el mensaje final.

Ya hay que descartar: marcas que **ya tienen local en Nordelta** (salvo que el formato sea
otro), y comercios de un solo local. Nada de datos personales de
particulares. Si no tiene contacto público, va igual pero marcado «sin contacto».

## Lo que NO se hace — regla 10 de Facu

- **No se contacta a nadie.** Ni mails, ni formularios, ni DMs. Se junta, se ordena y se le
  avisa a Facu. Él decide a quién se le escribe y lo manda desde paseonordelta@gmail.com.
- **No se ponen precios** de alquiler ni de expensas en ningún lado: se negocian después de
  la propuesta.
- No se inventa un dato. Si no hay fuente con link, no va.

## Cada corrida

1. Leer `vistos.md` (en la rama `claude/paseo-locales`) y no repetir a nadie que ya esté.
2. Buscar en la web con el criterio de arriba. Calidad sobre cantidad: **hasta 5 candidatos
   nuevos por día**. Si un día no aparece nada bueno, cero está bien.
3. Agregar cada candidato nuevo al final de `vistos.md`:
   `- DD/MM/AAAA · Marca · rubro · local sugerido (servicios/Market) · por qué encaja (1 línea) · contacto o «sin contacto» · link de la fuente`
4. Commit y push a la rama `claude/paseo-locales`.
5. **Sólo si hubo candidatos nuevos**, mandarle a Facu un Telegram corto (ver el prompt de la
   rutina para el canal). Formato:

   ```
   🏬 Paseo · 3 candidatos nuevos
   1. Marca — rubro → servicios. Por qué. Contacto.
   2. ...
   ¿A cuál le escribimos?
   ```

   Sin candidatos nuevos, no se manda nada (Facu quiere pocos avisos).
6. Si algo falló (búsqueda, push o Telegram), decirlo en el mensaje de cierre de la sesión.
