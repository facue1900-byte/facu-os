#!/bin/bash
# Publica UNA vez, el 04/11/2026, pulgar-v4 como reel de prueba (Facu, 03/11: «subilo mañana dale»).
# Sólo ese día y sólo ese archivo. Si la Mac estuvo apagada todo el día, NO lo sube después: falla,
# y correr.sh avisa. La marca evita una segunda publicación aunque launchd dispare otra vez.
#   --ensayo: chequea todo menos la fecha, y no publica.
OS=/Users/Facu/facu-os
P="/Users/Facu/Desktop/Productoras/Astronomy/Academia/Contenido/Pauta Online/Reels-a-mano/02-pulgar"
VIDEO="$P/pulgar-v4.mp4"
SHA=40e4bf73a2c70edc333296aade16b383771dd2b43254e385db01b58d44d2ae97
MARCA="$P/.publicado-v4"
DIA=2026-11-04

if [[ -e $MARCA ]]; then echo "ya publicado: $(cat "$MARCA")"; exit 0; fi
HOY=$(date +%F)
if [[ $1 != --ensayo && $HOY > $DIA ]]; then
  echo "pulgar-v4 NO se publicó el $DIA (la Mac no corrió ese día). Hoy es $HOY: no se sube solo." >&2; exit 1
fi
if [[ $1 != --ensayo && $HOY != "$DIA" ]]; then echo "todavía no es $DIA"; exit 0; fi
for f in "$VIDEO" "$P/portada.jpg" "$P/texto-reel.txt"; do [[ -s $f ]] || { echo "falta $f" >&2; exit 1; }; done
ACTUAL=$(shasum -a 256 "$VIDEO" | cut -d' ' -f1)
[[ $ACTUAL == "$SHA" ]] || { echo "pulgar-v4 cambió desde que Facu lo aprobó ($ACTUAL): no se publica" >&2; exit 1; }
if [[ $1 == --ensayo ]]; then echo "ENSAYO_OK: archivos y hash bien, no se publicó nada"; exit 0; fi

SALIDA=$(mktemp)
"$OS/.venv/bin/python" "$OS/active/astronomy/contenido/publicar_reel.py" "$VIDEO" --texto "$P/texto-reel.txt" \
  --portada "$P/portada.jpg" --prueba auto --send 2>&1 | tee "$SALIDA"
ID=$(sed -n 's/^PUBLICADO_ID //p' "$SALIDA" | head -1)
LINK=$(sed -n 's/^PUBLICADO_LINK //p' "$SALIDA" | head -1)
[[ -n $ID ]] || { echo "Instagram no confirmó la publicación" >&2; exit 1; }
echo "$ID $LINK" > "$MARCA"
ID="$ID" LINK="$LINK" SHA="$ACTUAL" P="$P" "$OS/.venv/bin/python" - <<'PY'
import json, os
l = {"fecha": "2026-11-04", "carpeta": os.environ["P"], "slug": "pulgar-sin-city-a-mano",
     "formato": "Pulgar v4: mismo reel que v3 con Go Back de Sin City, todo a la grilla del tema",
     "tema": "go-back", "media_id": os.environ["ID"], "permalink": os.environ["LINK"],
     "sha": os.environ["SHA"][:20], "voz": "", "tomas": []}
open("/Users/Facu/facu-os/active/astronomy/contenido/reels_diarios/registro.jsonl", "a").write(json.dumps(l, ensure_ascii=False) + "\n")
PY
osascript -e 'on run a' -e 'display notification (item 1 of a) with title "Reel publicado" sound name "Ping"' -e 'end run' "Pulgar con Sin City: $LINK"
