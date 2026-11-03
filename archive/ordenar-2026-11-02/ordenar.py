#!/usr/bin/env python3
"""Ordena Downloads/Desktop/Documents (02/11/2026). Solo renombra: no borra ni pisa nada.
Dry-run por defecto; --apply mueve y escribe manifest.csv (origen, destino, bytes, motivo)."""
import csv, glob, os, sys

H = os.path.expanduser("~")
DL, DK, DOC = H + "/Downloads", H + "/Desktop", H + "/Documents"
PN = DK + "/Paseo Nordelta"
PM = PN + "/Principio de mes"
FC = PM + "/Facturas de Compra"
AS = DK + "/Productoras/Astronomy"
FA = DK + "/Facu"
SC = FA + "/Sin clasificar"
REV = DL + "/Para revisar"
R1, R2, R3 = REV + "/1 - Repetidos exactos", REV + "/2 - No se donde van", REV + "/3 - Poco valor"
TASA = PN + "/Documentación/Municipales/Facturas abr-2025 a nov-2026/Cuenta 70580200 - Tasa y obra"
OBRA = PN + "/Documentación/Obra /PLANOS"
OBS = AS + "/Eventos/Obsession"
SINEV = AS + "/Eventos/_sin-evento-asignado"
SINCITY = FA + "/SIN CITY"

def g(pat):
    r = glob.glob(glob.escape(os.path.dirname(pat)) + "/" + os.path.basename(pat))
    return r[0] if len(r) == 1 else pat

M = []  # (origen, destino, motivo)
def mv(src, dst, why=""):
    M.append((src, dst, why))

# --- Paseo: a su carpeta
for f in sorted(glob.glob(DL + "/*_factura_02_11_2026-*.pdf")):
    mv(f, FC + "/Edenor/Noviembre 2026/" + os.path.basename(f), "Edenor: 14 facturas vto 31/10, carpeta del mes en que se bajan")
mv(DL + "/datos_de_cuenta.csv", FC + "/Edenor/Noviembre 2026/datos_de_cuenta.csv", "Edenor: listado de cuentas")
mv(DL + "/MAHNI MANAGEMENT S.A. - A-00002-00004197.pdf", FC + "/2026/Octubre 2026/30707845682_001_00002_00004197 Redes y Servicios oct-26.pdf", "R&S A-4197, 27/10")
mv(DL + "/FV 0003-3494 Mahni.pdf", FC + "/2026/Octubre 2026/FV 0003-3494 Savini ingenieria de detalle $40.679.679,70.pdf", "Savini, 14/10")
mv(DL + "/FV 0003-3502 Mahni.pdf", FC + "/2026/Octubre 2026/FV 0003-3502 Savini anticipo acopio $122.348.917,68.pdf", "Savini, 26/10")
mv(DK + "/Portal de Autogestión _ Secretaría de Ingresos Públicos.pdf", TASA + "/2026-11 Fondo y Aridos $15.690.961 (liq 4273969).pdf", "Talon cuota 4, reemitido 17:15; misma cuota que liq 4272692")
mv(DL + "/data.csv", PN + "/Documentación/Paseo - movimientos de caja (export 21-10-2026).csv", "Export de Movimientos")
mv(DL + "/data (1).csv", PN + "/Documentación/Paseo - movimientos de caja (export 28-10-2026).csv", "Export de Movimientos")
mv(DL + "/Paseo Nordelta - etapa2.pdf", OBRA + "/Paseo Nordelta - etapa2.pdf", "Plano etapa 2")
mv(DL + "/PHOTO-2026-10-15-18-39-27.jpg", OBRA + "/Paseo Nordelta - plano marcado (foto 15-10-2026).jpg", "Plano marcado a mano")
for f in ("orden-paseo-nordelta.json", "extras-paseo.json", "extras-paseo-kiwi.json"):
    mv(DL + "/" + f, H + "/facu-os/data/musica-paseo/" + f, "Lista del pendrive 02/11")
mv(SC + "/Resultado_envio_comprobantes.xlsx", H + "/facu-os/data/facturas-venta/2026-09/Resultado_envio_comprobantes.xlsx", "Acuse Bejerman de septiembre")

# --- Campos
mv(DL + "/richi-audio-26-10-1.ogg", DK + "/Chaco/Otros/Audio Richi pastaje 26-10-2026.ogg", "Audio de Richi, contrato de pastaje")

# --- Astronomy
for f in ("OBSESSION - VID.mov", "OBSESSION - VID (para IG).mp4", "OBSESSION - VID 2.mp4"):
    mv(DL + "/" + f, OBS + "/" + f, "Videos de la campana Obsession")
mv(SC + "/0929 (1)(1).mov", OBS + "/Save the date 31-10-2026.mov", "Save the date Obsession")
mv(SC + "/Archivo", AS + "/Academia/Flyers Academy/Placas membresias Platinum Gold Silver", "Placas de membresias")
mv(DK + "/Chaco/Otros/Comunicado IMPORTANTE.pdf", SINEV + "/Comunicado IMPORTANTE (Dominé, 10-09).pdf", "De Astronomy, traspapelado en Chaco; evento sin confirmar")
mv(DK + "/Chaco/Otros/Crew Passport - Juana ;).pdf", SINEV + "/Crew Passport - Juana ;).pdf", "De un evento, traspapelado en Chaco; evento sin confirmar")

# --- Sin City
mv(DL + "/sin-city-promo", SINCITY + "/sin-city-promo", "Promo y MP3 de Sin City (enviar_demos_3.py actualizado)")
mv(DL + "/Sin City - Always In The Game.wav", SINCITY + "/Sin City - Always In The Game.wav", "Master")

# --- Personal
mv(DOC + "/dni.jpeg", FA + "/Documentos/dni.jpeg", "Documento personal")
mv(DOC + "/Vacuna COVID facu.jpeg", FA + "/Documentos/Vacuna COVID facu.jpeg", "Documento personal")
for f in ("[P][W] T. L. Adm. Schena, Victoria.pdf", "Clase roberto torres.docx", "Parcial Politica y Estrategia Estevez Facundo.pages.zip"):
    mv(DOC + "/" + f, FA + "/Formación/" + f, "Facultad")
mv(FA + "/KSHMR_sok5_snare_tight_solid_circuit.wav", FA + "/PRODUCCIÓN /SAMPLE PACKS/KSHMR_sok5_snare_tight_solid_circuit.wav", "Sample suelto")
mv(FA + "/KSHMR_sok5_snare_tight_solid_circuit.wav.asd", FA + "/PRODUCCIÓN /SAMPLE PACKS/KSHMR_sok5_snare_tight_solid_circuit.wav.asd", "Sample suelto")

# --- Para revisar 1: copia byte a byte ya archivada (motivo = donde esta la otra)
C = PM + "/Comprobantes de pago/2026/Octubre 2026/"
B = PM + "/Resumen de Banco Paseo Nordelta/2026/"
for f, otra in (
    ("PDF document-46B6-9B8E-9E-0.pdf", C + "2026-10-26 Transportes Olivos FCA 23970 $1.354.029,10.pdf"),
    ("PDF document-44B2-89DC-2D-0.pdf", C + "2026-10-26 Giaccio FC 191 $653.400.pdf"),
    ("PDF document-48C2-9AE6-FB-0.pdf", C + "2026-10-26 Redes y Servicios A-4028 y A-4108 $1.029.365.pdf"),
    ("PDF document-46FD-AE1B-58-0.pdf", C + "2026-10-26 Savini echeq diferido 25-11 $40.679.679,70.pdf"),
    ("Ultimos_Movimientos.pdf", B + "Octubre 2026 - ultimos movimientos al 26-10.pdf"),
    ("Ultimos_Movimientos (1).pdf", B + "Octubre 2026 - ultimos movimientos al 30-10.pdf"),
    ("WhatsApp Image 2026-07-07 at 12.40.19.jpeg", TASA + "/2026-07 Recibo pago tasa y hospital (5 periodos 2026) $5.527.103.jpeg"),
    ("cuota Plan de pagos noviembre .pdf", TASA + "/2026-11 Fondo y Aridos $15.690.961.pdf"),
    ("Portal de Autogestión _ Secretaría de Ingresos Públicos.pdf", TASA + "/2026-11 Tasa municipal $1.027.633.pdf"),
    ("Resultado_envio_comprobantes.xlsx", H + "/facu-os/data/facturas-venta/2026-11/Resultado_envio_comprobantes.xlsx"),
):
    mv(DL + "/" + f, R1 + "/" + f, otra)
E = AS + "/Eventos/"
mv(DK + "/Municipal Mayo 2025.pdf", R1 + "/Municipal Mayo 2025.pdf", DK + "/Nordelta Plaza/Tigre Municipal/Servicios Municipales/Municipal Mayo 2025.pdf")
mv(SC + "/NachoReel_4 (1).mp4", R1 + "/NachoReel_4 (1).mp4", AS + "/Academia/Contenido/The Bunker/Reels/Natcheo Reel_4.mp4")
mv(SC + "/IMG_7238 (1).JPG", R1 + "/IMG_7238 (1).JPG", SINEV + "/IMG_7238.JPG")
mv(SINEV + "/NachoReel_4.mp4", R1 + "/NachoReel_4.mp4", AS + "/Academia/Contenido/The Bunker/Reels/Natcheo Reel_4.mp4")
for t in ("TOM06396", "TOM06632", "TOM06455", "TOM06506"):
    mv(SINEV + f"/{t}.JPG", R1 + f"/{t}.JPG", E + f"Theatre/FOTOS/{t}.JPG")
for t in ("DSC00830", "DSC00821"):
    mv(SINEV + f"/{t}.jpg", R1 + f"/{t}.jpg", AS + f"/Academia/Fotos del estudio/Fotos/{t}.jpg")
mv(E + "Mansion/Astronomy Mansion 2 (1).MP4", R1 + "/Astronomy Mansion 2 (1).MP4", E + "Mansion/Astronomy Mansion 2.MP4")
mv(E + "Theatre/MAXIMA-ASTRONOMY-TICKETS-EARLY-BIRDS (1).jpg", R1 + "/MAXIMA-ASTRONOMY-TICKETS-EARLY-BIRDS (1).jpg", E + "Theatre/MAXIMA-ASTRONOMY-TICKETS-EARLY-BIRDS.jpg")
mv(E + "Showcase CRETA/Astronomy Showcase Full LINE UP 2.mov", R1 + "/Astronomy Showcase Full LINE UP 2.mov", E + "Showcase CRETA/Astronomy Showcase Full LINE UP.MOV")
mv(E + "Dome/IMG_6216.jpg", R1 + "/IMG_6216.jpg", E + "Dome/Dome.jpg")
mv(AS + "/Academia/Contenido/Early Bird.png", R1 + "/Early Bird.png", E + "Mansion/Early Bird.png")

# --- Para revisar 2: no se donde van
for src, name, why in (
    (DL + "/casa-la-isla-renders", "casa-la-isla-renders", "Renders y maqueta de una casa (9/10). No se de quien es. 78 MB son node_modules"),
    (DL + "/IMG_4772.MOV", "IMG_4772.MOV", "Video del 7/10 filmando la pantalla: imagen de un micro abandonado"),
    (g(DK + "/Screenshot 2026-11-02 at 2.15*.png"), "Captura 02-11 recaudacion evento $64.574.000.png", "Entradas/Mesas/barra/SERNOVA. Parece Obsession, sin confirmar"),
    (SC + "/CamScanner 10-17-2022 19.59.pdf", "CamScanner 10-17-2022 19.59.pdf", "Escritura de compraventa Garcia a Valerio, 10 pags. Puede ser un original: mirar antes de tirar"),
    (g(SC + "/*Untitled"), "Catalogo Corporativo 2026 (Untitled).pdf", "Catalogo de 31 pags, sin autor claro"),
    (SC + "/facundo  Estevez.m4a", "facundo  Estevez.m4a", "Audio de 75 MB, enero 2025. Sin contexto"),
    (SC + "/IMG_5714.MOV", "IMG_5714.MOV", "Video de un evento, octubre 2024. No se cual"),
    (SC + "/clip_01KS0GRC6SRD8MS7NC68JXB0WR.mp4", "clip_01KS0GRC6SRD8MS7NC68JXB0WR.mp4", "Sesion de Ableton con gente en camara, mayo 2026"),
):
    mv(src, R2 + "/" + name, why)

# --- Para revisar 3: poco valor
for src, why in (
    (DL + "/Claude.dmg", "Instalador; Claude ya esta en Aplicaciones"),
    (DL + "/Descargar Binance App  Crypto Trading App for Mobile & Desktop.png", "Captura de la pagina de Binance"),
    (DL + "/Screenshot 2026-10-07 at 17.16.35.png", "Captura del App Store: app no disponible"),
    (SC + "/2093af9c5b8d449a89bab7ed4d51f022.MP4", "Reel ajeno: Hice esta web con Claude"),
    (SC + "/e0edb9b5370c42baa0eea0ee9456a323.MP4", "Reel ajeno: @vallaoxres, UI UX"),
    (FA + "/Sin_City_Demos_y_Sellos.xlsx", "Version vieja (18/07); la vigente esta en SIN CITY/"),
    (DOC + "/Microsoft Office 2019 Mac v16.33.zip", "Instalador viejo"),
    (DOC + "/Microsoft Office 2019 Mac v16.33", "Instalador viejo, descomprimido"),
    (DOC + "/MS Office v16.40 by MS Tube (youtube.com_msalauddins).pkg", "Instalador viejo"),
    (DOC + "/OFxC32O19", "Instalador viejo de Office"),
    (DOC + "/VolumeLicense.pkg", "Instalador viejo de Office"),
    (DOC + "/Serato DJ Pro 2.5.5.pkg", "Instalador 2021"),
    (DOC + "/Traktor Pro 2 v2.6.2 MAC OS.zip", "Instalador 2021"),
    (DOC + "/Zoom.pkg", "Instalador 2021"),
    (DOC + "/~$acundo.docx", "Lock de Word, 162 bytes"),
    (DOC + "/~$r.parcial TT 2do. semestre 2021 (2).doc", "Lock de Word, 162 bytes"),
    (DOC + "/~$r.parcial TT 2do. semestre 2021 Facundo Estevez.doc", "Lock de Word, 162 bytes"),
    (DOC + "/~$rcial Teoria y tecnica impositiva Estevez Facundo.doc", "Lock de Word, 162 bytes"),
):
    mv(src, R3 + "/" + os.path.basename(src), why)

def size(p):
    if os.path.isdir(p):
        return sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(p) for f in fs)
    return os.path.getsize(p)

apply = "--apply" in sys.argv
falta, choca, ok = [], [], []
dest = set()
for s, d, w in M:
    if not os.path.exists(s): falta.append(s)
    elif os.path.exists(d) or d in dest: choca.append(d)
    else: ok.append((s, d, w)); dest.add(d)
print("total", len(M), "ok", len(ok), "falta", len(falta), "choca", len(choca))
for x in falta: print("  FALTA", x)
for x in choca: print("  CHOCA", x)
if not apply:
    sys.exit(0)
if choca:
    sys.exit("Frena: hay destinos que ya existen; no se mueve nada.")
out = os.path.dirname(os.path.abspath(__file__)) + "/manifest.csv"
with open(out, "w", newline="") as fh:
    c = csv.writer(fh); c.writerow(["origen", "destino", "bytes", "motivo"])
    for s, d, w in ok:
        n = size(s)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        os.rename(s, d)
        assert os.path.exists(d) and not os.path.exists(s) and size(d) == n, s
        c.writerow([s.replace(H, "~"), d.replace(H, "~"), n, w.replace(H, "~")])
print("movidos", len(ok), "->", out)
