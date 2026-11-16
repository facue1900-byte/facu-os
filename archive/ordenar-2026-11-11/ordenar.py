#!/usr/bin/env python3
"""Ordena ~/Downloads (11/11/2026). No pisa nada; lo descartable va a la Papelera (recuperable).
Escribe manifest.csv (origen, destino, bytes, motivo) para poder deshacer."""
import csv, os, subprocess

H = os.path.expanduser("~")
DL, DK = H + "/Downloads", H + "/Desktop"
PN = DK + "/Paseo Nordelta"
FC = PN + "/Principio de mes/Facturas de Compra/2026"
EV = DK + "/Productoras/Astronomy/Eventos"
CL = DK + "/Clipping"
PAPELERA = "PAPELERA"

M = [
    ("affiliates_with_extra_data_1794413868052.pdf", EV + "/Obsession/Obsession - ventas por afiliado (reporte 11-11-2026).pdf", "Reporte de ventas por afiliado, Palacio Alsina"),
    ("MonkeyMusic logo sin fondo.png", EV + "/Sunset Monkey Studio 14-11/Logos Monkey Studio/MonkeyMusic logo sin fondo.png", "Logos de Monkey para el Sunset"),
    ("MONO CÍRCULO FONDO NEGRO.png", EV + "/Sunset Monkey Studio 14-11/Logos Monkey Studio/MONO CÍRCULO FONDO NEGRO.png", "idem"),
    ("MONO.png", EV + "/Sunset Monkey Studio 14-11/Logos Monkey Studio/MONO.png", "idem (el que se usó en el flyer)"),
    ("LOGO ENTERO FONDO TRANSPARENTE.png", EV + "/Sunset Monkey Studio 14-11/Logos Monkey Studio/LOGO ENTERO FONDO TRANSPARENTE.png", "idem"),
    ("Screenshot 2026-11-09 at 12.05.48.png", FC + "/Noviembre 2026/Mercado Libre - aire acondicionado $892.456,38 Visa 5782 3 cuotas (09-11-2026).png", "Comprobante del aire (memoria paseo-visa-5782)"),
    ("Screenshot 2026-11-09 at 12.10.29.png", FC + "/Octubre 2026/Mercado Libre - mis compras oct-26 (captura 09-11, 1 de 2).png", "Lista de compras ML de oct (membranas, silicona, sillas)"),
    ("Screenshot 2026-11-09 at 12.10.49-1.png", FC + "/Octubre 2026/Mercado Libre - mis compras oct-26 (captura 09-11, 2 de 2).png", "idem"),
    ("data.csv", PN + "/Documentación/Paseo - movimientos de caja (export 05-11-2026).csv", "Export de Movimientos, misma convención que los anteriores"),
    ("Tokyo Girl GTA 6 Campaign Brief.txt", CL + "/Tokyo Girl GTA 6 Campaign Brief.txt", "Clipping: brief de campaña"),
    ("MW4_S1_WARZONE_TRAILER_FULL_COD_Channel_ESRB_16x9_4K_REV01.mp4", CL + "/material/MW4_S1_WARZONE_TRAILER_FULL_COD_Channel_ESRB_16x9_4K_REV01.mp4", "Clipping: material fuente de Warzone, campaña activa"),
    ("Instagram thefacu__ - no te siguen VERIFICADA 2026-11-05.xlsx", DK + "/Facu/Instagram/Instagram thefacu__ - no te siguen VERIFICADA 2026-11-05.xlsx", "Personal: resultado del cruce de seguidos"),
    ("instagram-thefacu__-2026-11-05-cse6wJ6R.zip", PAPELERA, "Export crudo de IG ya procesado (el resultado es el xlsx); se puede volver a pedir"),
    ("Salida de provincia 32 novillos Camila - La Brava (09-11-2026).pdf", PAPELERA, "Duplicado byte a byte de Chaco/Guias de traslado/2026"),
    ("32 novillos Camila - La Brava (09-11-2026).pdf", PAPELERA, "idem"),
    ("Boleta 32 novillos Camila - La Brava (09-11-2026).pdf", PAPELERA, "idem"),
    ("Screenshot 2026-11-10 at 14.55.41.png", PAPELERA, "Captura de TikTok con vistas del 10/11: el dato ya está en la memoria de clipping"),
]

filas = []
for nombre, dst, why in M:
    src = os.path.join(DL, nombre)
    if not os.path.exists(src):
        print("NO ESTÁ:", nombre); continue
    tam = os.path.getsize(src)
    if dst == PAPELERA:
        r = subprocess.run(["osascript", "-e", f'tell application "Finder" to delete POSIX file "{src}"'], capture_output=True, text=True)
        if r.returncode: print("FALLÓ papelera:", nombre, r.stderr.strip()); continue
        dst = "~/.Trash"
    else:
        if os.path.exists(dst):
            print("YA EXISTE, no piso:", dst); continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        os.rename(src, dst)
    filas.append((src, dst, tam, why)); print("OK", nombre, "->", dst)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "manifest.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["origen", "destino", "bytes", "motivo"]); w.writerows(filas)
print(len(filas), "de", len(M), "hechos")
