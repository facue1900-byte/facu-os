"""Corrige el cartel SCHOCK·BA → SHOCK·BA en el render de día: saca la C y corre la S. El original no se toca."""
import pathlib

import numpy as np
from PIL import Image

B = pathlib.Path(__file__).parent.parent.parent / "fichas-locales" / "img"
SALIDA = pathlib.Path(__file__).parent.parent / "img"

a = np.array(Image.open(B / "render-galeria-dia.jpg").convert("RGB")).astype(float)
Y0, Y1 = 602, 629
S0, S1 = 1822, 1842  # la S
C0, C1 = 1843, 1865  # la C
letra_s = a[Y0:Y1, S0:S1].copy()
# Se borra S y C estirando el fondo que hay justo a la izquierda y a la derecha.
izq = a[Y0:Y1, S0 - 3:S0].mean(axis=1)
der = a[Y0:Y1, C1 + 1:C1 + 3].mean(axis=1)
ancho = C1 - S0
for i in range(ancho):
    t = i / max(1, ancho - 1)
    a[Y0:Y1, S0 + i] = izq * (1 - t) + der * t
# La S vuelve a entrar, mezclada por luminosidad, pegada a la H.
d = C1 - S1 - 2
fondo = a[Y0:Y1, S0 + d:S1 + d]
a[Y0:Y1, S0 + d:S1 + d] = np.maximum(fondo, letra_s)
Image.fromarray(a.astype("uint8")).save(SALIDA / "render-galeria-dia-shock.jpg", quality=92)


# Render de noche: mismo arreglo. El cartel está apenas en pendiente, por eso la S sube 1 px.
n = np.array(Image.open(B / "render-galeria-noche.jpg").convert("RGB")).astype(float)
Y0, Y1 = 453, 471
S0, S1 = 1522, 1533
C1 = 1545
letra_s = n[Y0:Y1, S0:S1].copy()
izq = n[Y0:Y1, S0 - 3:S0].mean(axis=1)
der = n[Y0:Y1, C1:C1 + 2].mean(axis=1)
ancho = C1 - S0
for i in range(ancho):
    t = i / max(1, ancho - 1)
    n[Y0:Y1, S0 + i] = izq * (1 - t) + der * t
d = C1 - S1 - 1
fondo = n[Y0 - 1:Y1 - 1, S0 + d:S1 + d]
n[Y0 - 1:Y1 - 1, S0 + d:S1 + d] = np.maximum(fondo, letra_s)
Image.fromarray(n.astype("uint8")).save(SALIDA / "render-galeria-noche-shock.jpg", quality=92)
Image.fromarray(n.astype("uint8")).crop((1480, 420, 1800, 520)).resize((1600, 500), Image.LANCZOS).save(
    "/private/tmp/claude-501/-Users-Facu-facu-os/3c12277e-793c-4f0e-84bd-d56515b3696f/scratchpad/view/shock4.png"
)
