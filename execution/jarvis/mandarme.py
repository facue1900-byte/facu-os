"""Manda un resumen de la charla con Jarvis al mail de FACU, y a nadie más.

Pedido de Facu (12/11/2026): «todo lo que acabamos de ver, mandámelo a mi mail». No es «salir al
mundo» (regla 10): el destinatario es fijo, MAIL_FACU del .env, y no se puede cambiar por argumento.
Por eso no pasa por PLAN ni lleva --send. Formato: execution/mail_format.py (asunto ÁREA · nivel).

Uso (el JSON entra por stdin):
  echo '{"area": "paseo", "titulo": "...", "resumen": "...",
         "kpis": [["Bigg vencido", "$471.466", "rojo"]],
         "secciones": [["Lo que vimos", ["punto 1", "punto 2"]]]}' \
    | .venv/bin/python execution/jarvis/mandarme.py
  --prueba: arma el mail y lo imprime, sin mandar.
"""
import base64
import json
import os
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))


def armar(d):
    from execution.mail_format import AREAS, render
    area = d.get("area") if d.get("area") in AREAS else "sistema"
    titulo = (d.get("titulo") or "").strip()
    if not titulo:
        raise SystemExit("falta «titulo»")
    secciones = [(str(t), [str(p) for p in ps]) for t, ps in (d.get("secciones") or [])]
    kpis = [tuple(k) for k in (d.get("kpis") or [])]
    if not (d.get("resumen") or secciones or kpis):
        raise SystemExit("el mail está vacío: mandá «resumen», «secciones» o «kpis»")
    return render(area, "reporte", titulo, resumen=d.get("resumen") or "", kpis=kpis,
                  secciones=secciones, origen="Jarvis · pedido de Facu")


def main():
    d = json.loads(sys.stdin.read())
    mail = armar(d)
    from dotenv import load_dotenv
    load_dotenv(RAIZ / ".env")
    para = os.environ["MAIL_FACU"]                 # único destinatario posible
    m = mail.mime(para)
    if "--prueba" in sys.argv:
        print(m["Subject"])
        print(mail.texto if hasattr(mail, "texto") else "")
        return
    from execution.google_auth import gmail
    gmail().users().messages().send(
        userId="me", body={"raw": base64.urlsafe_b64encode(m.as_bytes()).decode()}).execute()
    print(f"mandado a tu mail: {m['Subject']}")


if __name__ == "__main__":
    main()
