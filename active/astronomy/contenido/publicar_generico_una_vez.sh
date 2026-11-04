#!/bin/bash
# Publica UNA vez, el 05/11/2026: el video genérico como reel de prueba, y prende su anuncio ya
# creado en pausa (Facu, 04/11: «dale te doy el ok»). Ni antes ni después de ese día.
# Cada parte tiene su marca: si una falla, relanzar no repite la otra.
#   --ensayo: chequea todo menos la fecha, y no publica ni prende nada.
OS=/Users/Facu/facu-os
P="/Users/Facu/Desktop/Productoras/Astronomy/Academia/Contenido/Pauta Online/Reels-a-mano/05-generico-membresia"
VIDEO="$P/generico-sin-capcut.mp4"
SHA=3de686b47453f0481c731b8a67e2a4ce3739efa3ddf7e7d385eff5c7d7d5c380
DIA=2026-11-05
PY="$OS/.venv/bin/python"

HOY=$(date +%F)
if [[ $1 != --ensayo && $HOY > $DIA ]]; then
  echo "El video genérico NO salió el $DIA (la Mac no corrió ese día). Hoy es $HOY: no sale solo." >&2; exit 1
fi
if [[ $1 != --ensayo && $HOY != "$DIA" ]]; then echo "todavía no es $DIA"; exit 0; fi
for f in "$VIDEO" "$P/portada.jpg" "$P/texto-reel.txt"; do [[ -s $f ]] || { echo "falta $f" >&2; exit 1; }; done
ACTUAL=$(shasum -a 256 "$VIDEO" | cut -d' ' -f1)
[[ $ACTUAL == "$SHA" ]] || { echo "el video cambió desde el OK de Facu ($ACTUAL): no se publica" >&2; exit 1; }
if [[ $1 == --ensayo ]]; then echo "ENSAYO_OK: archivos y hash bien, no se publicó nada"; exit 0; fi

FALLA=0
if [[ ! -e "$P/.publicado-reel" ]]; then
  SALIDA=$(mktemp)
  "$PY" "$OS/active/astronomy/contenido/publicar_reel.py" "$VIDEO" --texto "$P/texto-reel.txt" \
    --portada "$P/portada.jpg" --prueba auto --send 2>&1 | tee "$SALIDA"
  ID=$(sed -n 's/^PUBLICADO_ID //p' "$SALIDA" | head -1)
  LINK=$(sed -n 's/^PUBLICADO_LINK //p' "$SALIDA" | head -1)
  if [[ -n $ID ]]; then
    echo "$ID $LINK" > "$P/.publicado-reel"
    ID="$ID" LINK="$LINK" SHA="$ACTUAL" P="$P" "$PY" - <<'PY'
import json, os
l = {"fecha": "2026-11-05", "carpeta": os.environ["P"], "slug": "generico-membresia",
     "formato": "Video genérico de la academia de Facu, sin el cierre de CapCut",
     "tema": "audio-original", "media_id": os.environ["ID"], "permalink": os.environ["LINK"],
     "sha": os.environ["SHA"][:20], "voz": "", "tomas": []}
open("/Users/Facu/facu-os/active/astronomy/contenido/reels_diarios/registro.jsonl", "a").write(json.dumps(l, ensure_ascii=False) + "\n")
PY
  else
    echo "Instagram no confirmó la publicación del reel" >&2; FALLA=1
  fi
fi
if [[ ! -e "$P/.prendido-anuncio" ]]; then
  if (cd "$OS/active/astronomy/pauta" && "$PY" video_generico_wpp.py --send); then
    date > "$P/.prendido-anuncio"
  else
    echo "El anuncio no quedó prendido" >&2; FALLA=1
  fi
fi
exit $FALLA
