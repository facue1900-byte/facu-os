"""Le avisa a Facu (a él solo) que algo se rompió: mail a MAIL_FACU con la cola de un log.

Lo usa `execution/launchd/correr.sh` cuando una tarea programada sale con error. No es
"salir al mundo" (regla 10): el único destinatario posible es MAIL_FACU del .env.

    .venv/bin/python execution/avisar.py "reporte-equipo salió con 1" data/logs/x.log
"""
import base64
import os
import pathlib
import sys
from email.mime.text import MIMEText

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from dotenv import load_dotenv  # noqa: E402

load_dotenv(RAIZ / ".env")
from execution.google_auth import gmail  # noqa: E402


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: avisar.py <motivo> [archivo_de_log]")
    motivo = sys.argv[1]
    cola = ""
    if len(sys.argv) > 2 and pathlib.Path(sys.argv[2]).is_file():
        cola = pathlib.Path(sys.argv[2]).read_text(errors="replace")[-6000:]
    para = os.environ["MAIL_FACU"]
    m = MIMEText(f"{motivo}\n\n--- últimas líneas del log ---\n{cola or '(vacío)'}")
    m["to"], m["subject"] = para, f"🔴 Tarea programada: {motivo[:80]}"
    gmail().users().messages().send(
        userId="me", body={"raw": base64.urlsafe_b64encode(m.as_bytes()).decode()}).execute()
    print(f"aviso mandado a {para}")


if __name__ == "__main__":
    main()
