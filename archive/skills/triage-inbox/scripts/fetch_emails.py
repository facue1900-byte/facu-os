#!/usr/bin/env python3
"""
Baja los mails del inbox como JSON compacto, listo para clasificar.

    .venv/bin/python .claude/skills/triage-inbox/scripts/fetch_emails.py \
        --query "in:inbox is:unread" --limit 200 --output .tmp/triage/emails.json

Solo lee metadata (asunto, remitente, fecha, snippet): alcanza para clasificar y
mantiene el JSON chico. El cuerpo completo no entra nunca al contexto.
"""

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))

from googleapiclient.errors import HttpError  # noqa: E402

from execution.google_auth import gmail  # noqa: E402

HEADERS = ["Subject", "From", "Date"]


def ids_de_mensajes(service, query, limit):
    """Lista los IDs que matchean la query, paginando hasta llegar al límite."""
    ids = []
    page_token = None

    while len(ids) < limit:
        faltan = limit - len(ids)
        resp = service.users().messages().list(
            userId="me", q=query, pageToken=page_token,
            maxResults=min(500, faltan),
        ).execute()

        ids.extend(m["id"] for m in resp.get("messages", []))

        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return ids[:limit]


def metadata(service, ids):
    """Trae metadata de cada mensaje con el batch API (100 por request)."""
    encontrados = {}
    fallados = []

    def callback(request_id, response, exception):
        if exception is not None:
            fallados.append(request_id)
            return
        h = {x["name"]: x["value"]
             for x in response.get("payload", {}).get("headers", [])}
        encontrados[request_id] = {
            "id": response["id"],
            "asunto": h.get("Subject", "(sin asunto)"),
            "de": h.get("From", "(desconocido)"),
            "fecha": h.get("Date", ""),
            "snippet": response.get("snippet", "")[:200],
        }

    for i in range(0, len(ids), 100):
        batch = service.new_batch_http_request(callback=callback)
        for msg_id in ids[i:i + 100]:
            batch.add(
                service.users().messages().get(
                    userId="me", id=msg_id,
                    format="metadata", metadataHeaders=HEADERS,
                ),
                request_id=msg_id,
            )
        batch.execute()

    if fallados:
        # Un mail que no baja es un mail que no se clasifica: no se tapa.
        print(f"AVISO: {len(fallados)} mensajes no se pudieron leer: "
              f"{fallados[:5]}", file=sys.stderr)

    return [encontrados[i] for i in ids if i in encontrados]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query", "-q", default="in:inbox",
                   help="Query de Gmail (default: in:inbox)")
    p.add_argument("--limit", "-l", type=int, default=200,
                   help="Máximo de mails a bajar (default: 200)")
    p.add_argument("--output", "-o", required=True, help="JSON de salida")
    args = p.parse_args()

    salida = pathlib.Path(args.output)
    salida.parent.mkdir(parents=True, exist_ok=True)

    try:
        service = gmail()
        ids = ids_de_mensajes(service, args.query, args.limit)
        print(f"Query '{args.query}': {len(ids)} mensajes")
        mails = metadata(service, ids) if ids else []
    except HttpError as e:
        sys.exit(f"Gmail rechazó el pedido: {e}")

    if len(mails) != len(ids):
        print(f"AVISO: pedí {len(ids)} y bajé {len(mails)}.", file=sys.stderr)

    salida.write_text(json.dumps(mails, indent=2, ensure_ascii=False))
    print(f"{len(mails)} mails escritos en {salida}")

    # Un inbox vacío es raro. Que lo diga fuerte en vez de pasar por bueno.
    if not mails:
        print("OJO: cero mails. Revisá la query antes de dar esto por bueno.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
