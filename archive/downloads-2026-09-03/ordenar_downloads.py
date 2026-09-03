"""Ordena ~/Downloads en las carpetas del Escritorio.

Sin --apply sólo escribe el manifiesto (manifest.csv) y el resumen. Con --apply
mueve vía Finder (AppleScript), porque el proceso no tiene permiso TCC sobre
el Escritorio; los BORRAR van a la Papelera, no a rm.
"""
import os, re, sys, json, csv, hashlib, collections, subprocess, datetime, pathlib, unicodedata
NFC = lambda s: unicodedata.normalize('NFC', s)

DL = pathlib.Path.home() / "Downloads"
DESK = pathlib.Path.home() / "Desktop"
S = pathlib.Path(__file__).parent

# ── destinos ──────────────────────────────────────────────────────────────
PN = "Paseo Nordelta"; PM = f"{PN}/Principio de mes"; PD = f"{PN}/Documentación"
NP = "Nordelta Plaza"; NPM = f"{NP}/Principio de mes"; NE = "Noreventos"
AS = "Productoras/Astronomy"; AE = f"{AS}/Eventos"; AA = f"{AS}/Academia"; AM = f"{AS}/Marca Astronomy"
PZ = "Productoras/Puzzle"
FA = "Facu"; DJ = f"{FA}/DJ"; PR = f"{FA}/PRODUCCIÓN "   # ojo: la carpeta real termina en espacio
CH = "Chaco"

MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
def mes_de(fecha):  # "2026-01-20" -> "Enero 2026"
    y, m, _ = fecha.split("-"); return f"{MESES[int(m)-1]} {y}"

# ── inventario ────────────────────────────────────────────────────────────
items = []
for p in sorted(DL.iterdir()):
    st = p.stat()
    size = sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) if p.is_dir() else st.st_size
    items.append(dict(nombre=p.name, nfc=NFC(p.name), dir=p.is_dir(), size=size,
                      fecha=datetime.date.fromtimestamp(st.st_mtime).isoformat()))
byname = {i["nombre"]: i for i in items}

# ── duplicados exactos (md5) dentro de Downloads ──────────────────────────
def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""): h.update(ch)
    return h.hexdigest()
dup_de = {}
by_size = collections.defaultdict(list)
for i in items:
    if not i["dir"] and i["size"] > 1000: by_size[i["size"]].append(i["nombre"])
for s, fs in by_size.items():
    if len(fs) < 2: continue
    h = collections.defaultdict(list)
    for f in fs: h[md5(DL / f)].append(f)
    for g in h.values():
        if len(g) > 1:
            g.sort(key=lambda x: (len(x), x))
            for d in g[1:]: dup_de[d] = g[0]

# ── zips verificados (mismo conteo que su carpeta descomprimida) ──────────
ZIPS_OK = {
 "drive-download-20250320T124950Z-001.zip": "drive-download-20250320T124950Z-001",
 "Otra Cosa-20250321T203359Z-002.zip": "Otra Cosa",
 "Reggeaton-20250321T203357Z-002.zip": "Reggeaton",
 "This Is Sébastien Léger-20250323T230742Z-001.zip": "This Is Sébastien Léger",
 "Tech House-20250321T203356Z-001.zip": "Tech House",
 "Party-20250321T203358Z-003.zip": "Party 3",
 "CAMU SET-20240528T184549Z-001.zip": "CAMU SET",
 "wetransfer_ad-astra-ids_2024-01-23_2237.zip": "Ad Astra IDs",
 "wetransfer_3-png_2024-04-23_2256.zip": "wetransfer_3-png_2024-04-23_2256",
 "drive-download-20251113T215541Z-1-001.zip": "drive-download-20251113T215541Z-1-001",
 "drive-download-20251111T130250Z-1-001.zip": "drive-download-20251111T130250Z-1-001 (1)",
 "POSTEOS-20251111T130556Z-1-001.zip": "POSTEOS",
 "Municipal.zip": "Municipal", "Municipal.rar": "Municipal",
 "Before - Logos.zip": "Before - Logos", "files.zip": "files",
 "deemix-gui-main.zip": "deemix-gui-main",
 "drive-download-20251114T152142Z-1-007.zip": "C9942.MP4 y C9944.MP4 sueltos",
 "Reggeaton-20250323T230751Z-002.zip": "Reggeaton 3 (la carpeta tiene 1 archivo más que el zip)",
 "This Is Armen Miran-20250323T230742Z-001.zip": "This Is Armen Miran (sólo falta un .DS_Store)",
}
# zips que difieren un poco de su carpeta: NO se borran
# Reggeaton-20250323T230751Z-002.zip (103 vs 104), This Is Armen Miran (49 vs 48), Youtube.zip (10 vs 7)

# ── duplicados contra el destino (mismo nombre y tamaño ya en el Escritorio) ─
# se verificó por Finder: extractos del Macro ya archivados en Resumen de Banco
YA_EN_DESTINO = {
 "Resumen.pdf": "Resumen de Banco/2025/Agosto 2025.pdf", "Resumen (1).pdf": "Resumen de Banco/2025/Septiembre 2025.pdf",
 "Resumen (2).pdf": "Resumen de Banco/2025/Octubre 2025.pdf", "Resumen (3).pdf": "Resumen de Banco/2025/Noviembre 2025.pdf",
 "Resumen (4).pdf": "Resumen de Banco/2025/Diciembre 2025.pdf", "Resumen (5).pdf": "Resumen de Banco/2026/Enero 2026.pdf",
 "Resumen (6).pdf": "Resumen de Banco/2026/Febrero 2026.pdf", "Resumen (7).pdf": "Resumen de Banco/2026/Julio 2026.pdf",
 "ADENDA Nº1  CONTRATO DE CONCESIÓN RODOLFO SRL - BIGG - TG-ultimo.pdf": "Nordelta Plaza/Contratos Locatarios (mismo nombre y tamaño)",
 "ADENDA Nº1  Contrato de concesión - BIGG.pdf": "Nordelta Plaza/Contratos Locatarios/…RODOLFO SRL - BIGG - TG-ultimo.pdf (md5 igual)",
 "Gabriel Ananda - Doppelwhipper (Original Mix) [Truesoul].mp3": "Facu/DJ/Sin clasificar (mismo nombre y tamaño)",
 "Gorgon City - Voodoo (Extended Mix) [REALM Records].aiff": "Facu/DJ/Sin clasificar (mismo nombre y tamaño)",
 "Skream, FLETCH (GB) - Lost Without You (Extended Mix) [CircoLoco Records].mp3": "Facu/DJ/Sin clasificar (mismo nombre)",
 "Tiesto, Odd Mob, Goodboys - Won't Be Possible (Extended Mix) [Atlantic Records].mp3": "Facu/DJ/Sin clasificar (mismo nombre)",
}

# ── reglas por nombre: (regex, accion, destino, motivo) — la primera que matchea gana ─
R = []
def r(rx, accion, destino=None, motivo=""): R.append((re.compile(rx), accion, destino, motivo))

# basura / instaladores
r(r"^~\$", "BORRAR", None, "lock file de Office")
r(r"^\.DS_Store$|^\.Rapp\.history$|^winmail\.dat$", "BORRAR", None, "basura de sistema")
r(r"\.asd$", "BORRAR", None, "archivo de análisis de Ableton, se regenera solo")
r(r"^Sample Packs 202[5-8]$", "BORRAR", None, "carpeta vacía")
r(r"^(README|01-CONSTITUCION|02-PLAYBOOK|03-EMPRESA)\.md$", "BORRAR", None, "copia vieja de un archivo que vive en el repo facu-os")
r(r"^json\.txt$", "BORRAR", None, "respuesta de error de Google Sheets (ACCESS_DENIED)")
r(r"^review-iteration-1\.html$|^appsscriptsync\.gs$|^ARQUITECTURA_ADMIN\.md$", "BORRAR", None, "artefacto de desarrollo; lo que vale está en git")
r(r"^data \([2-9]\)\.csv$|^data \(10\)\.csv$", "BORRAR", None, "export viejo de Movimientos de la app del Paseo; se re-exporta cuando haga falta")
r(r"^Untitled design\.png$", "BORRAR", None, "placa vacía de Canva (13 KB)")
r(r"^RDE-Reglamento de Uso", "BORRAR", None, "reglamento de otro barrio (Residencias del Este), bajado de referencia")
r(r"^(Copas De Plástico|Enredadera Flores|Unidad Flash Sandisk)", "BORRAR", None, "comprobante de compra en MercadoLibre de 2024/2025")
r(r"^(FabFilter Total Bundle|Xfer_LFOTool|Splice\.dmg|VALHALLA BUNDLE)", "MOVER", f"{PR}/Instaladores", "instalador de plugin pago: cuesta volver a conseguirlo")
r(r"\.(dmg|pkg)$|^GitHubDesktop-arm64\.zip$|^macosx-10\.14-x86-deezloader|^deemix-gui-main", "BORRAR", None, "instalador: la app ya está instalada o se baja de nuevo")
r(r"^Amsterdam_Amsterdam_Four_Font", "BORRAR", None, "fuente bajada en 2022, sin uso conocido")

# Paseo Nordelta (MAHNI) ───────────────────────────────────────────────
r(r"^MAHNI - SUELDOS JULIO 2026", "MOVER", f"{PM}/Recibos de Sueldo/2026/Julio 2026", "recibos de sueldo MAHNI")
r(r"^MAHNI - SUELDOS AGOSTO 2026", "MOVER", f"{PM}/Recibos de Sueldo/2026/Agosto 2026", "recibos de sueldo MAHNI")
r(r"^MAHNI 2025-12 F\.2051|^MAHNI 202511 F\.2051", "MOVER", f"{PM}/Impuestos del mes/2025", "DDJJ IVA F.2051 de MAHNI, período 2025")
r(r"^MAHNI 2026\d\d F\.2051|^MAHNI IVA 2026", "MOVER", f"{PM}/Impuestos del mes/2026", "DDJJ IVA F.2051 de MAHNI, período 2026")
r(r"^MAHNI Cubo Comprobantes", "MOVER", f"{PD}/Balances/2026", "cubo de ventas y compras del contador, 1er semestre 2026")
r(r"^20081049980_001_00004_00000387 MAHNI", "MOVER", f"{PM}/Facturas de Compra/2026/Agosto 2026", "factura de Giaccio (contador) por el balance 2025")
r(r"^20251872628_001_00005_00001511", "MOVER", f"{PM}/Facturas de Compra/2026/Agosto 2026", "factura de Luis Costantini a MAHNI, 07/08/2026")
r(r"^MAHNI-FCA0000300023135\.pdf$", "MOVER", f"{PM}/Facturas de Compra/2026/Abril 2026", "Transportes Olivos (basura) a MAHNI, 30/04/2026")
r(r"^invoice-2000015961548450\.pdf$", "MOVER", f"{PM}/Facturas de Compra/2026/Abril 2026", "factura a MAHNI pagada 13/04/2026 ($249.765)")
r(r"^invoice-2000015882922938", "MOVER", f"{PM}/Facturas de Compra/2026/Abril 2026", "White Salud SRL, 10/04/2026")
r(r"^invoice-2000014673158286", "MOVER", f"{PM}/Facturas de Compra/2026/Enero 2026", "Magno Market a MAHNI, 12/01/2026")
r(r"^Comprobante FE - JGXLWKQAV", "MOVER", f"{PM}/Facturas de Compra/2026/Mayo 2026", "Soda Belén (agua), 02/05/2026")
r(r"^Comprobante FE - AXRSTFUNYZ", "MOVER", f"{PM}/Facturas de Compra/2026/Abril 2026", "Soda Belén (agua), 03/04/2026")
r(r"^0002 A 61730 _ 16-10-2025", "MOVER", f"{PM}/Facturas de Compra/2025/Octubre 2025", "Soda Belén (agua), 16/10/2025")
r(r"^Factura A-00002-00003524", "MOVER", f"{PM}/Facturas de Compra/2026/Enero 2026", "Redes y Servicios SA, 23/01/2026")
r(r"^factura A-00002-00003588", "MOVER", f"{PM}/Facturas de Compra/2026/Febrero 2026", "Redes y Servicios SA")
r(r"^factura A-00002-00003715", "MOVER", f"{PM}/Facturas de Compra/2026/Marzo 2026", "Redes y Servicios SA")
r(r"^factura A-00002-00003783", "MOVER", f"{PM}/Facturas de Compra/2026/Abril 2026", "Redes y Servicios SA, 24/04/2026")
r(r"^FC A0002-00000078", "MOVER", f"{PM}/Facturas de Compra/2026/Enero 2026", "Consultores Giaccio SRL, 05/01/2026")
r(r"^PDF document-4", "MOVER", f"{PM}/Comprobantes de pago/2026/Agosto 2026", "transferencias Macro de MAHNI a Redes y Servicios, 06/08/2026")
r(r"^1352ACA4-EAA2", "MOVER", f"{PM}/Comprobantes de pago/2026/Septiembre 2026", "transferencia Macro de MAHNI a Luis Costantini $600.000, 03/09/2026")
r(r"^Resultado_envio_comprobantes", "MOVER", f"{PM}/Facturas de Venta/2026/Agosto 2026", "resultado del envío de comprobantes (Bejerman)")
r(r"^Ultimos_Movimientos", "BORRAR", None, "listado parcial de movimientos Macro de abril 2026: el extracto entero ya está en Resumen de Banco/2026")
r(r"^\d{10}_factura_20_01_2026", "MOVER", f"{PM}/Facturas de Compra/Edenor/Enero 2026", "Edenor, bajadas el 20/01/2026")
r(r"^\d{10}_factura_23_02_2026", "MOVER", f"{PM}/Facturas de Compra/Edenor/Febrero 2026", "Edenor, bajadas el 23/02/2026")
r(r"^\d{10}_(\d\d[_-]2025|2025-\d\d)_factura|^Edenor .*2025", "MOVER", f"{PM}/Facturas de Compra/Edenor/2025", "Edenor 2025 (a nombre de Noreventos; mismos 14 medidores)")
r(r"^MAHNI MANAGEMENT CM CInsc", "MOVER", f"{PD}/Estatuto & Cuit", "constancia de inscripción MAHNI, 13/03/2026")
r(r"^Oferta Irrevocable de Contrato de Locación .*LA JAULA|^Oferta_Irrevocable_Locacion_MAHNI|^Contrato de Comodato Mahni|^modelo de cesion habi|^Paseo Nordelta - Anexo 1\.A|^ANEXO 1\.B|^Reglamento Paseo Nordelta|^Contrato Fabric 2 Firmado", "MOVER", f"{PD}/Contratos", "contrato / anexo / reglamento del Paseo (MAHNI)")
r(r"^Paseo Nordelta - Permiso Municipal - 2026\.3\.31|^Municipal$|^(F0139|F01407) CARTEL DE OBRA|^DOCUMENTACION A PRESENTAR INGRESO DE PLANOS|^Solicitud aprobacion Obra Nueva|^ENCOMIENDA PROFESIONAL|^Notas N05\. CHECK LIST|^06 PRUEBA DE ESTANQUEIDAD", "MOVER", f"{PD}/Municipales", "permiso municipal y formularios de obra")
r(r"\.dwg$|^2021-MENSURA 57-113-2021|^Parcela club de futbol_20240711\.pdf$|^Paseo Nordelta 14-01-26\.pdf$|^Fabric Nordelta2 - Arquitectura", "MOVER", f"{PD}/Obra /PLANOS", "plano / mensura")
r(r"^Paseo Nordelta - Presentación\.pdf$", "MOVER", f"{PD}/Obra ", "presentación (hay una casi igual ahí: difiere en 6 bytes, se guarda como copia)")
r(r"^Paseo Nordelta  Presentacion 2026|^Paseo Nordelta - Un nuevo punto|^Paseo_Nordelta(_1)?\.pptx|^Paseo_Nordelta\.pptx\.pdf|^E1 - PRESUPUESTO|^3 locales nuevos|^Metros de 3 locales|^APEX-2\.pdf", "MOVER", f"{PD}/Obra ", "presentación comercial / presupuesto de demolición / fotos de locales / propuesta APEX (wellness)")
r(r"^Liquidacion Casas del Golf|^N&D SOLUCIONES INDUSTRIALES", "MOVER", f"{PD}", "referencia: modelo de liquidación de expensas / chequeo ARCA de proveedor")
r(r"^Banner YTB|^FotoPerfil-YouTube|^foto yt grande|^WaterMark _ Paseo Nordelta|^(Argentina|Vuelve) - Final\.mp4", "MOVER", f"{PN}/Youtube", "material del canal de YouTube del Paseo (todo del 07/01/2026)")
r(r"^stock_LA_(MAGDALENA|VICTORINA)", "MOVER", f"{CH}/Stock", "foto de stock de hacienda por campo, 03/09/2026")
r(r"^Hoja de cálculo sin título\.xlsx$", "MOVER", f"{AE}/House n Bells", "hoja 'Gastos ARCHI', misma pestaña que la planilla de House & Bells")

r(r"^Factura C Facu BIGG", "MOVER", f"{FA}/Documentos/AFIP", "factura C emitida por Facu a Bigg, feb 2025")
r(r"^Nordelta Plaza - Contrato de Locación", "MOVER", f"{NP}/Contratos Locatarios", "modelo de contrato de locación NDPL, nov 2025")
r(r"^Europa_2026\.pptx$", "MOVER", f"{FA}/Documentos", "itinerario del viaje a Europa ago-sep 2026 (personal)")
r(r"^Reggeaton 3$", "FUSIONAR", f"{DJ}/Musica/Reggeaton", "98 de 104 tracks ya están en 'Reggeaton': se pasan los 6 que faltan y se tira la carpeta")
r(r"^clip_01KS0GRC", "PREGUNTAR", None, "video de 25 MB generado con IA (may 2026): ¿para qué era?")

# vistos a mano por el hilo principal (los subagentes no supieron)
r(r"^WhatsApp Image 2026-01-19 at 19\.31\.2[56]", "MOVER", f"{FA}/Documentos", "foto del DNI de Facu")
r(r"^WhatsApp Image 2026-01-28 at 15\.54\.58", "MOVER", f"{FA}/Documentos/Auto NFV983", "dorso del DNI de Polo, Eduardo José (titular anterior del auto)")
r(r"^WhatsApp Image 2026-03-26 at 21\.29\.08 \(1\)", "MOVER", f"{PD}/Obra ", "render del Paseo: Bigg, kiosco, heladería")
r(r"^WhatsApp Image 2025-1[01]-(30|03)", "MOVER", f"{PD}/Obra /PLANOS", "plano AutoCAD / implantación Arq. Max Elewaut")
r(r"^WhatsApp Image 2025-03-18", "MOVER", f"{NP}/Comprobantes de pago", "ticket Manso Restaurante a NDPL SAS, 16/03/2025 ($269.660)")
r(r"^WhatsApp Image 2025-12-02", "MOVER", f"{NPM}/Facturas & Rec de Gastos/2025", "factura Rhino (limpieza y fumigación) a NDPL SAS, 02/12/2025 ($1.694.000)")
r(r"^WhatsApp Image 2024-03-06", "MOVER", f"{FA}/Fotos", "retrato de una persona, sin contexto")
r(r"^WhatsApp Image 2025-10-20|^Photo \(\d+\)\.jpg$|^Screenshot_30\.png$|^PHOTO-2026-09-02", "MOVER", f"{AE}/_sin-evento-asignado", "fotos de fiesta (Sernova, may 2026) / pulsera Dominé / DJs en cabina")
r(r"^ig_bp2\.jpg$", "MOVER", f"{AE}/Private Boat Party", "flyer Private Boat Party 16.02")
r(r"^nd plaza 3-11\.psd$", "MOVER", f"{NP}/Logotipos Nordelta Plaza", "diseño PSD 'nd plaza', nov 2025")

r(r"^2025\.03\.28 Cami & Dante|^Rompecabezas\.pdf$|^ChatGPT Image Jan 14, 2026", "MOVER", f"{AE}/_sin-evento-asignado", "fotos de fiesta 28/03/2025 / logos 'Rompecabezas' (enero 2026)")
r(r"^ChatGPT Image Jan 29, 2026", "MOVER", f"{AM}/Logos/Prototipos : Ideas", "pruebas de logo Astronomy con calavera y sables (ChatGPT)")
r(r"^ChatGPT Image Jun 10, 2026|^IMG_786[04]\.MOV$", "MOVER", f"{AA}/Fotos del estudio", "renders de opciones para el estudio (mismo día que las fotos del estudio) / videos del estudio mar 2025")
r(r"^IMG_383[78]\.heic$", "MOVER", f"{FA}/Documentos", "foto del pasaporte de Facu")
r(r"^WhatsApp Audio 2026-0[89]-", "MOVER", f"{AA}/Capturas app", "notas de voz del 13/08 y 01/09, mismas horas que las capturas del panel del staff")
r(r"^WhatsApp Video 2026-08-13 at 17\.14\.56", "MOVER", f"{AE}/Obsession", "video del flyer de Obsession (misma hora que la imagen)")
r(r"^WhatsApp Video 2026-02-09", "MOVER", f"{FA}/Fotos", "videos personales (mismo momento que la foto del tiburón)")
r(r"^(Video_1___El_portal|Generate_an_ultra|Create_a_20_second)", "MOVER", f"{FA}/E-COMMERCE $$$", "videos verticales generados con IA el 30/06/2026 (creativos de e-commerce)")

# Nordelta Plaza (NDPL SAS) / Noreventos ──────────────────────────────
r(r"^Comprobante-(TransferenciasInmediatas|eCheq)|^Comprobante (Caro Z|Honorarios CZ|de pago RAW|RAW|Pei|Electricista)|^Trf Inmed Proveed|^Recibo de Pago Jeronimo|^BMA_MASTERCARD", "MOVER", f"{NP}/Comprobantes de pago", "comprobante BBVA / Macro de Nordelta Plaza SAS o Noreventos")
r(r"^\d\d-\d\d-\d{4}-eCheqs-emitidos|^Movimientos.*\.xls$|^transferenciasRealizadas\.xls$", "MOVER", f"{NP}/BBVA movimientos", "export de movimientos BBVA")
r(r"^30711024723_", "MOVER", f"{NE}", "factura emitida por Noreventos SRL (CUIT 30-71102472-3)")
r(r"^NE 20|^data\.csv$|^data \(1\)\.csv$", "MOVER", f"{NE}", "planilla / cashflow de Noreventos (NE)")
r(r"^LIQUIDACION-", "MOVER", f"{NE}/Liquidaciones Nordelta", "liquidación de Nordelta SA a Noreventos, EECC 12/2025")
r(r"^Statements\.pdf$", "MOVER", f"{NE}/Extracto bancario Noreventos", "resumen Pymes de Noreventos SRL, ene 2026")
r(r"(Contrato|CONTRATO|ADENDA|Addenda|RESCISION|Adenda).*(VOLTA|Volta|SUSHINOR|RIDERS|FABRICA DEL TACO|FDT|ATRUCKON|Atruckon|ENERGYPHARMA|HASHTAG|BARBERIA|ASTOR|STAND SUCRE|FABRIC|BIGG|NORDELTA PLAZA)|^NORDELTA PLAZA CONTRATOS|^Contratos-20240117|^CUIT SUNRA|^Recibo SUNRA|^CBU Nordelta Plaza|^comprobanteCBU|^Estatuto2\.zip", "MOVER", f"{NP}/Contratos Locatarios", "contrato / adenda / rescisión de locatario de Nordelta Plaza")
r(r"^(Cuentas? Corrientes?|CC |Cta Cte|Expensas 2022-2024|Calculos Medidores|Sector Gastronomico|Ds x Vtas|Pagos pendientes NPlaza|ESTIPULADO NDPL|FDT Cta Cte|Facturas Venta-SEPT)", "MOVER", f"{NPM}/Cuentas Corrientes ", "cuenta corriente / expensas / medidores de Nordelta Plaza")
r(r"AGO'|AGO´|^Alq SEPT'23|^Factura de venta A 0000|^\(NDPLSAS\)|^NDPLSAS|^FA-A-0008-00009858", "MOVER", f"{NPM}/Facturas & Rec de Gastos", "factura / recupero de gastos NDPL SAS")
r(r"^PROYECCION RTDOS NP|^Cashflow mensual '2023|^Ingresos vs Egresos NPlaza", "MOVER", f"{NP}/Informes ND Plaza", "proyección / cashflow / informe de Nordelta Plaza")
r(r"^Presupuesto CFI", "MOVER", f"{NP}/Eventos", "presupuesto de evento en el predio (cancha + catering), nov 2023")

# Astronomy — eventos ────────────────────────────────────────────────
r(r"House & Bells|HOUSE&BELLS", "MOVER", f"{AE}/House n Bells", "House & Bells 24/12/2025")
r(r"^OBSESSION", "MOVER", f"{AE}/Obsession", "fecha Obsession (ticketera)")
r(r"^THEATRE Precio Mesas", "MOVER", f"{AE}/Theatre", "precios de mesas Theatre")
r(r"^wetransfer_entrega-ad-mansion|^VISUALES\.mp4$|^TOM01\d{3}", "MOVER", f"{AE}/Mansion", "entrega del fotógrafo (TOM) y visuales de Mansion, nov 2023")
r(r"^events\.csv$", "MOVER", f"{AE}/Dark Mansion", "export de Passline del evento Dark Mansion")
r(r"^Lista Barcos", "MOVER", f"{AE}/Private Boat Party", "lista de la Private Boat Party (feb 2025)")
r(r"BIGFETT|Bigfett|Zamna|fernet c big fett|^Icono (Negro|Blanco)\.png|^Futura Tipografia", "MOVER", f"{AE}/Boiler Room (Futura:Big Fett) ", "material Big Fett / Futura, mar 2025")
r(r"^Propuesta Aybak|^Contrato - Aybak|^PDF estudio", "MOVER", f"{AM}/Contratos y propuestas", "Aybak Producciones / Music studio, 2023")
r(r"^Feedback Report - Natcheo", "MOVER", f"{AA}/Contenido/The Bunker", "feedback del video de The Bunker, ago 2023")
r(r"^NumerosMesas|^Mapa de mesas", "MOVER", f"{PZ}", "plano de mesas con 'puzzle STAGE' (evento con Puzzle, 2026)")
r(r"^Presupuesto Capri|^NachoReel_4\.mp4$|^bmbcolor|^Dálmata Gin|^Bombo-Logo|^Poolpa|^Banner-AD|^Cuadrado-AD|^1000x1000|^cuadrado\.png|^Passline( 2)?$|^Banner (correo|Superior)\.png|^Logo Foto de Perfil|^Lista frees|^_Rompk Personal|^division_por_genero|^base_unificada_contactos|^Before - Logos$|^BASE DE DATOS BEFORE|^SERNOVA|^NATIVE-logos|^TOM06\d{3}|^Copy of 345A|^Drop 4 - Scenarios|^Video 14-08-2025|^POSTEOS$|^IMG_0528\.MP4$|^IMG_0531\.MP4$|^C9[89]\d\d\.MP4$|^drive-download-20251113T215541Z-1-001$|^drive-download-20251111T130250Z-1-001 \(1\)$|^wetransfer_3-png_2024-04-23_2256$|^0504", "MOVER", f"{AE}/_sin-evento-asignado", "material de eventos sin evento identificado (Facu asigna)")

# Astronomy — academia / marca ───────────────────────────────────────
r(r"^Astronomy Closers|^Presupuesto anual - Set estudio", "MOVER", f"{AA}/Comercial", "job description closers / presupuesto set en vivo")
r(r"^Propuesta RAW", "MOVER", f"{AA}/Pauta", "propuesta de RAW para leads")
r(r"^Alumnos Activos|^Ventas_MercadoPago", "MOVER", f"{AA}/Reporte financiero", "export de alumnos / ventas MP")
r(r"^Horarios curso dj profesional|^Reel cursonuevo|^curso-astronomy$|^Grand Opening\.zip|^Early Bird\.png|^Sin apoyatura\.png|^FONDO ASTRO0|^1\.PNG$", "MOVER", f"{AA}/Contenido", "contenido / flyers de la academia")
r(r"^NuevoCurso_Astronomy( 2)?$", "BORRAR", None, "el zip con el mismo contenido ya está en Academia/Contenido/NuevoCurso_Astronomy.zip")
r(r"^Logos PNG\.zip|^unnamed\.png$|^logo blanco\.png$|^files$|^Youtube$|^Youtube\.zip$", "MOVER", f"{AM}/Logos", "logos Astronomy Academy / Vladinic / canal YouTube 2023")
r(r"^google5c6095a0ba26e6d7\.html$", "PREGUNTAR", None, "token de verificación de Google Search Console: ¿ya está subido al sitio?")

# Facu — DJ / producción ─────────────────────────────────────────────
r(r"^(Reggeaton|Reggeaton 2|Reggeaton 3|Party|Party 2|Party 3|Otra Cosa|Otra Cosa 2|Progressive House|Arabic Sunset|Tech House|This Is Sébastien Léger|This Is Armen Miran|CAMU SET|Ad Astra IDs)$", "MOVER", f"{DJ}/Musica", "playlist bajada de Drive")
r(r"^drive-download-20250320T124950Z-001$", "MOVER", f"{DJ}/Musica", "playlist bajada de Drive (100 tracks, mar 2025) → se renombra 'Playlist Drive 2025-03-20'")
r(r"^Kick Astronomy\.wav$", "MOVER", f"{PR}/SAMPLE PACKS", "sample")
r(r"^sin city 0[134]\.mp4$", "MOVER", f"{FA}/SIN CITY", "videos Sin City, may 2026")
r(r"^Sin_City_Demos_y_Sellos\.xlsx$", "MOVER", f"{FA}/SIN CITY", "versión más nueva (jul 2026) que la que está suelta en Facu/")
r(r"Super Virginia Cigare?tte Master", "PREGUNTAR", None, "3 masters .wav (mar 2026): ¿tracks tuyos? ¿van a PRODUCCIÓN o a Sin City?")
r(r"\.(mp3|aiff|wav|flac)$", "MOVER", f"{DJ}/Sin clasificar", "track suelto")

# Facu — personal ────────────────────────────────────────────────────
r(r"^(CEDULA 1 - NFV983|Registro Polo|Poliza_10895260|RTO NFV983|Comprobante_Pago_10895260|DNI 1 - POLO|Agrosalta_Carnet|Multa Alcoholemia)", "MOVER", f"{FA}/Documentos/Auto NFV983", "documentación del auto NFV983 (cédula, registro, póliza, RTO, DNI del titular anterior)")
r(r"^afip_presentacion_cuit_20947520580|^setiqueryw2w|^Credencial_20947520580|^20947520580_011|^2026_06_10_11_22_55_735_receipt|^W-9 Firmado", "MOVER", f"{FA}/Documentos/AFIP", "AFIP/ARCA personal (CUIT 20-94752058-0): F.1746 devoluciones, credencial, factura propia, pago, W-9")
r(r"^excel tesis|^Archivos\.zip$|^convenio de divulgacion|^Hospital General|^Dra Mallon|^Nuevo Formulario Alta Cliente", "MOVER", f"{FA}/Documentos", "tesis / universidad / salud / formulario de alta cliente")
r(r"^Visión de Mercado", "MOVER", f"{FA}/Inversiones", "resumen semanal de mercado")
r(r"^(GUIA-ARMAR-TU-OS|bootcamp\.pdf|evento-ia-20-junio|Claude Code Full Course)", "MOVER", f"{FA}/Formación", "cursos, guías, IA")
r(r"^facundo  Estevez\.m4a$|^IMG_5714\.MOV$|^IMG_786[04]\.MOV$", "PREGUNTAR", None, "audio/video grande sin contexto")
r(r"^CamScanner 10-17-2022", "PREGUNTAR", None, "escaneo de 10 páginas de 2022, sin texto")
r(r"^\.localized$", "IGNORAR", None, "marcador de sistema de macOS")

# ── resultados de los subagentes (imágenes miradas una por una) ──────────
def destino_por_bucket(b, que):
    q = que.lower()
    if b == "PASEO": return f"{PD}/Obra ", "foto/captura del Paseo"
    if b == "NDPL":
        if re.search(r"recibo|comprobante|transfer|dep[oó]sito", q): return f"{NP}/Comprobantes de pago", "comprobante"
        return f"{NP}/Informes ND Plaza", "foto/captura de Nordelta Plaza"
    if b == "CHACO": return f"{CH}/Otros", "foto/captura de Chaco"
    if b == "ASTRO_EVENTOS": return f"{AE}/_sin-evento-asignado", "foto/captura de eventos"
    if b == "ASTRO_ACADEMIA":
        if re.search(r"estudio|setup|cabina", q): return f"{AA}/Fotos del estudio", "foto del estudio"
        return f"{AA}/Capturas app", "captura de la academia"
    if b == "DJ_PRODUCCION":
        if re.search(r"estudio|setup|cabina", q): return f"{AA}/Fotos del estudio", "foto del estudio"
        return f"{DJ}/Sin clasificar", "material DJ"
    if b == "FACU":
        if re.search(r"pasaporte|dni|documento|ticket|factura|recibo|transferencia|estado", q): return f"{FA}/Documentos", "documento personal"
        return f"{FA}/Fotos", "foto personal"
    return None, None
BUCKET_DEST = {
 "PASEO": (f"{PD}/Obra /Fotos y capturas", "foto/captura del Paseo (subagente)"),
 "NDPL": (f"{NP}/Fotos y capturas", "foto/captura de Nordelta Plaza (subagente)"),
 "CHACO": (f"{CH}/Otros", "foto/captura de Chaco (subagente)"),
 "ASTRO_EVENTOS": (f"{AE}/_sin-evento-asignado", "foto/captura de eventos (subagente)"),
 "ASTRO_ACADEMIA": (f"{AA}/Capturas app", "captura de la academia (subagente)"),
 "DJ_PRODUCCION": (f"{DJ}/Sin clasificar", "material DJ (subagente)"),
 "FACU": (f"{FA}/Fotos y capturas", "foto/captura personal (subagente)"),
}
agente = {}
for f in S.glob("clasif_*.jsonl"):
    for line in f.read_text().splitlines():
        try: d = json.loads(line); agente[NFC(d["archivo"])] = d
        except Exception: pass

# ── clasificar ────────────────────────────────────────────────────────────
filas = []
for i in items:
    n = i["nfc"]; real = i["nombre"]
    if real in dup_de:
        filas.append((real, "BORRAR", "", f"duplicado exacto (md5) de: {dup_de[real]}", i)); continue
    if n in ZIPS_OK:
        filas.append((real, "BORRAR", "", f"zip ya descomprimido: mismo contenido que '{ZIPS_OK[n]}'", i)); continue
    if n in YA_EN_DESTINO:
        filas.append((real, "BORRAR", "", f"ya está archivado en {YA_EN_DESTINO[n]}", i)); continue
    hit = None
    for rx, acc, dest, mot in R:
        if rx.search(n): hit = (acc, dest, mot); break
    if hit:
        filas.append((real, hit[0], hit[1] or "", hit[2], i)); continue
    a = agente.get(n) or agente.get(real)
    if a:
        b = a["bucket"]
        if b == "BORRAR": filas.append((real, "BORRAR", "", f"subagente: {a['que_es']} ({a['confianza']})", i)); continue
        d, m = destino_por_bucket(b, a.get("que_es", ""))
        if d: filas.append((real, "MOVER", d, f"{m} (subagente): {a['que_es']} ({a['confianza']})", i)); continue
        filas.append((real, "PREGUNTAR", "", f"subagente no supo: {a.get('que_es','')}", i)); continue
    filas.append((real, "PREGUNTAR", "", "sin regla", i))

# renombres al mover
RENOMBRAR = {"drive-download-20250320T124950Z-001": "Playlist Drive 2025-03-20",
             "Municipal": "Permiso Municipal 2026-03-31",
             "Paseo Nordelta - Presentación.pdf": "Paseo Nordelta - Presentación (2).pdf",
             "Sin_City_Demos_y_Sellos.xlsx": "Sin_City_Demos_y_Sellos (jul 2026).xlsx",
             "files": "Vladinic logos", "Youtube": "Youtube 2023", "Youtube.zip": "Youtube 2023.zip",
             "Hoja de cálculo sin título.xlsx": "Gastos ARCHI (feb 2026).xlsx",
             "Statements.pdf": "enero 2026 (resumen pymes).pdf"}

with open(S / "manifest.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["archivo", "accion", "destino", "nuevo_nombre", "motivo", "bytes", "fecha"])
    for n, acc, dest, mot, i in filas:
        w.writerow([n, acc, dest, RENOMBRAR.get(n, ""), mot, i["size"], i["fecha"]])

# ── resumen ───────────────────────────────────────────────────────────────
def mb(b): return f"{b/1048576:,.0f} MB" if b < 1e9 else f"{b/1073741824:,.1f} GB"
tot = collections.defaultdict(lambda: [0, 0])
for n, acc, dest, mot, i in filas:
    tot[acc][0] += 1; tot[acc][1] += i["size"]
print("== RESUMEN ==")
for k, (c, b) in sorted(tot.items()): print(f"  {k:10s} {c:4d} items  {mb(b)}")
print("\n== MOVER por destino ==")
pd_ = collections.defaultdict(lambda: [0, 0])
for n, acc, dest, mot, i in filas:
    if acc == "MOVER": pd_[dest][0] += 1; pd_[dest][1] += i["size"]
for d, (c, b) in sorted(pd_.items()): print(f"  {c:4d}  {mb(b):>9s}  {d}")
print("\n== PREGUNTAR ==")
for n, acc, dest, mot, i in filas:
    if acc == "PREGUNTAR": print(f"  {mb(i['size']):>8s}  {n}  — {mot}")

# ── aplicar ───────────────────────────────────────────────────────────────
def osa(script):
    p = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if p.returncode: raise RuntimeError(p.stderr.strip())
    return p.stdout.strip()

def q(s): return s.replace("\\", "\\\\").replace('"', '\\"')

def finder_mkdirs(rel):
    """Crea la ruta bajo el Escritorio, nivel por nivel, vía Finder."""
    cur = DESK
    for part in rel.split("/"):
        nxt = cur / part
        existe = osa(f'tell application "Finder" to return exists (POSIX file "{q(str(nxt))}" as alias)') if False else None
        try:
            osa(f'tell application "Finder" to return (POSIX file "{q(str(nxt))}") as alias')
        except RuntimeError:
            osa(f'tell application "Finder" to make new folder at (POSIX file "{q(str(cur))}" as alias) with properties {{name:"{q(part)}"}}')
        cur = nxt
    return cur

def existe(path):
    try: osa(f'tell application "Finder" to return (POSIX file "{q(str(path))}") as alias'); return True
    except RuntimeError: return False

if "--apply" in sys.argv:
    solo = None
    if "--solo" in sys.argv: solo = sys.argv[sys.argv.index("--solo") + 1]   # MOVER o BORRAR
    log = open(S / "aplicado.log", "a")
    ok = err = 0
    for n, acc, dest, mot, i in filas:
        if acc != "FUSIONAR" or (solo and solo != "MOVER"): continue
        src = DL / n; base = DL / pathlib.Path(dest).name
        if not src.exists() or not base.exists(): continue
        for f in src.iterdir():
            if not (base / f.name).exists(): f.rename(base / f.name); log.write(f"{datetime.datetime.now().isoformat()}\tFUSIONAR\t{n}/{f.name}\t{base}\n")
        osa(f'tell application "Finder" to delete (POSIX file "{q(str(src))}" as alias)')
        log.write(f"{datetime.datetime.now().isoformat()}\tBORRAR(papelera, fusionada)\t{n}\n"); ok += 1
    for n, acc, dest, mot, i in filas:
        if acc not in ("MOVER", "BORRAR") or (solo and acc != solo): continue
        src = DL / n
        if not src.exists(): continue
        try:
            if acc == "BORRAR":
                osa(f'tell application "Finder" to delete (POSIX file "{q(str(src))}" as alias)')
                log.write(f"{datetime.datetime.now().isoformat()}\tBORRAR(papelera)\t{n}\n"); ok += 1; continue
            carpeta = finder_mkdirs(dest)
            nuevo = RENOMBRAR.get(n, n)
            base, ext = os.path.splitext(nuevo); k = 2
            while existe(carpeta / nuevo):
                nuevo = f"{base} ({k}){ext}"; k += 1
            if nuevo != n:   # renombrar primero en Downloads (ahí sí tenemos permiso)
                src2 = DL / nuevo; src.rename(src2); src = src2
            osa(f'tell application "Finder" to move (POSIX file "{q(str(src))}" as alias) to (POSIX file "{q(str(carpeta))}" as alias)')
            log.write(f"{datetime.datetime.now().isoformat()}\tMOVER\t{n}\t{carpeta / nuevo}\n"); ok += 1
        except Exception as e:
            log.write(f"{datetime.datetime.now().isoformat()}\tERROR\t{n}\t{e}\n"); err += 1
            print(f"ERROR {n}: {e}")
    log.close()
    print(f"\napplied: {ok} ok, {err} errores → {S/'aplicado.log'}")
