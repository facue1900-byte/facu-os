#!/usr/bin/env python3
"""Reporte del embudo de pauta de Astronomy Academy — de dónde viene cada lead y cada cliente.

Junta en un solo lugar lo que hoy vive en cuatro:

  1. Meta (API): gasto, impresiones, clics y conversaciones POR ANUNCIO.
  2. La web (`lead_events`): visitantes, cuentas creadas y quiénes pagaron, por la
     marca UTM con la que llegaron. La cuenta se atribuye al último UTM ANTES del alta,
     igual que /admin/leads/pauta (lib/atribucion.ts).
  3. Instagram (`instagram_comentarios`): cada comentario a los videos y qué pasó con
     él (DM mandado, ya respondido, apagado, fallo).
  4. Clientes nuevos del mes (primera compra en el mes) con su origen: la marca web
     antes de la primera compra, o el primer mensaje de WhatsApp (export del bot de
     Gonza, `whatsapp_primer_contacto`), o «sin dato».

Base: Supabase de ASTRONOMY (`qeakrjnseboiulcojlcw`), sólo lectura. Nada sale a nadie.
Plata en ARS tal como está en la base, sin redondear; la pauta en USD (moneda de la
cuenta de Meta). No se cruzan monedas, así que no hay tipo de cambio.

    .venv/bin/python active/astronomy/pauta/reporte_embudo.py                 # mes en curso
    .venv/bin/python active/astronomy/pauta/reporte_embudo.py --mes 2026-10
    .venv/bin/python active/astronomy/pauta/reporte_embudo.py --chequeo       # ¿se está registrando todo?

`--chequeo` sale con código 1 si alguna pieza dejó de registrar (regla final: nada se
rompe en silencio).
"""

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys

import httpx
from dotenv import load_dotenv

RAIZ = pathlib.Path(__file__).resolve().parents[3]
load_dotenv(RAIZ / ".env", override=True)

REF = "qeakrjnseboiulcojlcw"  # Astronomy. El Paseo es otro ref: no confundir.
TOKEN_META = os.getenv("META_ACCESS_TOKEN")
CUENTA = os.getenv("META_AD_ACCOUNT_ID", "")
CUENTA = CUENTA if CUENTA.startswith("act_") else f"act_{CUENTA}"
SB = os.getenv("SUPABASE_ACCESS_TOKEN")
AR = dt.timezone(dt.timedelta(hours=-3))
CONV = "onsite_conversion.messaging_conversation_started_7d"


def sql(cli, q):
    # La Management API pide curl-like UA: con el de Python Cloudflare devuelve 403 (1010).
    r = cli.post(f"https://api.supabase.com/v1/projects/{REF}/database/query",
                 headers={"Authorization": f"Bearer {SB}", "User-Agent": "curl/8.7.1"},
                 json={"query": q}, timeout=60)
    if r.status_code >= 300:
        sys.exit(f"Supabase rechazó la consulta ({r.status_code}): {r.text[:300]}")
    return r.json()


def meta(cli, path, **q):
    q["access_token"] = TOKEN_META
    out, url = [], f"https://graph.facebook.com/v21.0/{path}"
    while url:
        j = cli.get(url, params=q, timeout=60).json()
        q = {}
        if "error" in j:
            sys.exit(f"Meta rechazó {path}: {j['error'].get('message')}")
        if "data" not in j:
            return j
        out += j["data"]
        url = j.get("paging", {}).get("next")
    return out


def utm_de_anuncio(creative):
    """utm_content del link del anuncio, o 'whatsapp' si manda a WhatsApp."""
    s = json.dumps(creative or {})
    m = re.search(r"utm_content=([a-z0-9_-]+)", s)
    if m:
        return m.group(1)
    return "whatsapp" if "WHATSAPP" in s else "-"


def rango(mes):
    a = dt.date.fromisoformat(mes + "-01")
    b = (a.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    return a, b


def pauta(cli, a, b):
    hasta = min(b - dt.timedelta(days=1), dt.date.today())
    filas = meta(cli, f"{CUENTA}/insights", level="ad",
                 time_range=json.dumps({"since": a.isoformat(), "until": hasta.isoformat()}),
                 fields="ad_id,ad_name,spend,impressions,inline_link_clicks,actions", limit=500)
    ids = [f["ad_id"] for f in filas]
    creat = {}
    for i in range(0, len(ids), 50):
        d = meta(cli, "", ids=",".join(ids[i:i + 50]), fields="creative{object_story_spec,call_to_action,asset_feed_spec}")
        for k, v in (d or {}).items():
            creat[k] = utm_de_anuncio(v.get("creative"))
    out = []
    for f in filas:
        acc = {x["action_type"]: float(x["value"]) for x in f.get("actions", [])}
        out.append({"anuncio": f["ad_name"], "utm": creat.get(f["ad_id"], "-"), "usd": float(f["spend"]),
                    "impresiones": int(f["impressions"]), "clics": int(f.get("inline_link_clicks", 0) or 0),
                    "conversaciones": int(acc.get(CONV, 0))})
    return sorted(out, key=lambda x: -x["usd"])


# Quién pagó algo alguna vez y cuándo fue su primera compra (sales ∪ libro ∪ manuales).
PRIMERA = """
  primera as (
    select user_id, min(f) primera from (
      select user_id, (paid_at at time zone 'America/Argentina/Buenos_Aires')::date f from sales where user_id is not null
      union all select user_id, paid_on from payment_links where user_id is not null and confirmed
      union all select user_id, (paid_at at time zone 'America/Argentina/Buenos_Aires')::date from manual_payments where user_id is not null
    ) x group by user_id)
"""


def web(cli, a, b):
    return sql(cli, f"""
    with {PRIMERA},
    vis as (
      select coalesce(utm_source,'') s, coalesce(utm_medium,'') m, coalesce(utm_campaign,'') c, coalesce(utm_content,'') k,
             count(distinct anon_id) visitantes
      from lead_events where utm_source is not null
        and created_at >= '{a}'::date at time zone 'America/Argentina/Buenos_Aires'
        and created_at <  '{b}'::date at time zone 'America/Argentina/Buenos_Aires'
      group by 1,2,3,4),
    alta as (select id, created_at from profiles where not coalesce(es_interno,false)
             and created_at >= '{a}'::date at time zone 'America/Argentina/Buenos_Aires'
             and created_at <  '{b}'::date at time zone 'America/Argentina/Buenos_Aires'),
    origen as (
      select distinct on (al.id) al.id, coalesce(e.utm_source,'') s, coalesce(e.utm_medium,'') m,
             coalesce(e.utm_campaign,'') c, coalesce(e.utm_content,'') k
      from alta al join lead_events e on e.user_id = al.id and e.created_at <= al.created_at and e.utm_source is not null
      order by al.id, e.created_at desc),
    cuentas as (
      select o.s, o.m, o.c, o.k, count(*) cuentas, count(p.user_id) pagaron
      from origen o left join primera p on p.user_id = o.id group by 1,2,3,4)
    select coalesce(v.s,c.s) utm_source, coalesce(v.m,c.m) utm_medium, coalesce(v.c,c.c) utm_campaign, coalesce(v.k,c.k) utm_content,
           coalesce(v.visitantes,0) visitantes, coalesce(c.cuentas,0) cuentas, coalesce(c.pagaron,0) pagaron
    from vis v full join cuentas c on (v.s,v.m,v.c,v.k) = (c.s,c.m,c.c,c.k)
    order by visitantes desc""")


def altas_sin_utm(cli, a, b):
    return sql(cli, f"""
    select count(*) altas,
           count(*) filter (where not exists (select 1 from lead_events e where e.user_id=p.id and e.created_at<=p.created_at and e.utm_source is not null)) sin_utm
    from profiles p where not coalesce(es_interno,false)
      and created_at >= '{a}'::date at time zone 'America/Argentina/Buenos_Aires'
      and created_at <  '{b}'::date at time zone 'America/Argentina/Buenos_Aires'""")[0]


def comentarios(cli, a, b):
    return sql(cli, f"""
    select coalesce(plan,'(sin palabra)') plan, estado, count(*) n
    from instagram_comentarios
    where recibido_en >= '{a}'::date at time zone 'America/Argentina/Buenos_Aires'
      and recibido_en <  '{b}'::date at time zone 'America/Argentina/Buenos_Aires'
    group by 1,2 order by 1,2""")


def clientes(cli, a, b):
    return sql(cli, f"""
    with {PRIMERA},
    nuevos as (select p.user_id, p.primera from primera p join profiles pr on pr.id=p.user_id
               where not coalesce(pr.es_interno,false) and p.primera >= '{a}' and p.primera < '{b}'),
    web as (
      select distinct on (n.user_id) n.user_id,
             concat_ws(' · ', e.utm_source, e.utm_medium, e.utm_campaign, e.utm_content) marca
      from nuevos n join lead_events e on e.user_id=n.user_id and e.utm_source is not null
        and (e.created_at at time zone 'America/Argentina/Buenos_Aires')::date <= n.primera
      order by n.user_id, e.created_at desc),
    wa as (
      select n.user_id, w.primer_mensaje_at, w.primer_texto
      from nuevos n join profiles pr on pr.id=n.user_id
      join whatsapp_primer_contacto w on right(regexp_replace(coalesce(pr.phone,''),'\\D','','g'),10) = right(w.phone,10)
      where length(regexp_replace(coalesce(pr.phone,''),'\\D','','g')) >= 10)
    select pr.full_name, n.primera,
           (select string_agg(distinct coalesce(s.plan_id,''), ',') from sales s where s.user_id=n.user_id
              and (s.paid_at at time zone 'America/Argentina/Buenos_Aires')::date = n.primera) plan_sales,
           (select sum(s.amount) from sales s where s.user_id=n.user_id
              and (s.paid_at at time zone 'America/Argentina/Buenos_Aires')::date = n.primera) monto_sales,
           w.marca web, wa.primer_mensaje_at::date wa_fecha, left(wa.primer_texto, 60) wa_texto
    from nuevos n join profiles pr on pr.id=n.user_id
    left join web w on w.user_id=n.user_id left join wa on wa.user_id=n.user_id
    order by n.primera""")


def chequeo(cli):
    """Cada pieza que puede dejar de registrar sin que nadie lo note. Devuelve fallos."""
    fallos, avisos = [], []
    activos = meta(cli, f"{CUENTA}/ads", fields="name,effective_status",
                   filtering=json.dumps([{"field": "effective_status", "operator": "IN", "value": ["ACTIVE"]}]), limit=100)
    print(f"Anuncios activos en Meta: {len(activos)}")
    for x in activos:
        print(f"   · {x['name']}")
    v = sql(cli, """select count(*) n, max(created_at) ultimo from lead_events
                    where utm_source='meta' and created_at > now() - interval '48 hours'""")[0]
    print(f"Visitas de pauta (utm_source=meta) en 48 h: {v['n']} · última {v['ultimo']}")
    if activos and not v["n"]:
        fallos.append("hay anuncios activos y la web no registró NINGUNA visita de pauta en 48 h: el tracker o los links están rotos")
    t = sql(cli, "select vence_en, renovado_en, array_length(media_ids,1) posts from instagram_cuenta where id=1")
    if not t:
        fallos.append("instagram_cuenta vacía: el bot de comentarios no tiene token")
    else:
        t = t[0]
        print(f"Token de Instagram: renovado {t['renovado_en']} · vence {t['vence_en'] or 'sin fecha (60 días desde el alta)'} · posteos en la lista: {t['posts']}")
        if t["vence_en"] and dt.datetime.fromisoformat(t["vence_en"].replace("Z", "+00:00")) < dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=15):
            fallos.append("el token de Instagram vence en menos de 15 días y no se renovó")
    c = sql(cli, """select estado, count(*) n, max(recibido_en) ultimo from instagram_comentarios
                    where recibido_en > now() - interval '7 days' group by 1 order by 2 desc""")
    print("Comentarios de Instagram en 7 días: " + (", ".join(f"{x['estado']} {x['n']}" for x in c) or "ninguno"))
    malos = sum(x["n"] for x in c if x["estado"] in ("fallo", "fallo_incierto"))
    if malos:
        fallos.append(f"{malos} comentario(s) en fallo/fallo_incierto en 7 días: mirar `detalle` en instagram_comentarios")
    # `apagado` no es una falla: es el bot haciendo lo que tiene que hacer con
    # INSTAGRAM_AUTORESPUESTA sin prender. Sí es un aviso, por si alguien lo apagó.
    apag = [x for x in c if x["estado"] == "apagado"]
    if apag:
        avisos.append(f"{apag[0]['n']} comentario(s) llegaron con el bot APAGADO (último {apag[0]['ultimo']}); si es posterior a la prueba del 05/10, alguien lo apagó")
    if not c:
        avisos.append("ningún comentario en 7 días: puede ser normal con US$3/día, pero si los videos tienen comentarios en Instagram, el webhook no está llegando")
    w = sql(cli, "select max(export_hasta) hasta from whatsapp_primer_contacto")[0]
    print(f"WhatsApp: último export del bot cargado hasta {w['hasta']}")
    if not w["hasta"] or dt.date.fromisoformat(str(w["hasta"])[:10]) < dt.date.today() - dt.timedelta(days=10):
        avisos.append("el origen de los leads de WhatsApp está viejo: hace falta un export nuevo del bot de Gonza")
    return fallos, avisos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mes", default=dt.date.today().strftime("%Y-%m"))
    ap.add_argument("--chequeo", action="store_true")
    args = ap.parse_args()
    if not (TOKEN_META and SB):
        sys.exit("Faltan META_ACCESS_TOKEN o SUPABASE_ACCESS_TOKEN en el .env de facu-os")
    with httpx.Client() as cli:
        if args.chequeo:
            fallos, avisos = chequeo(cli)
            for x in avisos:
                print("AVISO  " + x)
            for x in fallos:
                print("FALLA  " + x)
            print("\nOK: todo se está registrando." if not fallos else f"\n{len(fallos)} FALLA(S).")
            sys.exit(1 if fallos else 0)

        a, b = rango(args.mes)
        print(f"# Embudo de pauta — Astronomy Academy — {args.mes}   (base {REF}, solo lectura)\n")

        p = pauta(cli, a, b)
        print("## 1. Meta: gasto por anuncio (USD)")
        print(f"{'USD':>9} {'impr':>8} {'clics':>6} {'conv':>5}  utm_content        anuncio")
        for x in p:
            print(f"{x['usd']:9.2f} {x['impresiones']:8d} {x['clics']:6d} {x['conversaciones']:5d}  {x['utm']:<18} {x['anuncio'][:60]}")
        print(f"{sum(x['usd'] for x in p):9.2f}  TOTAL ({len(p)} anuncios)\n")

        print("## 2. Web: visitantes → cuentas → pagaron, por marca UTM")
        print(f"{'visit':>6} {'cuentas':>7} {'pagaron':>7}  marca (source · medium · campaign · content)")
        for x in web(cli, a, b):
            marca = " · ".join(v for v in (x["utm_source"], x["utm_medium"], x["utm_campaign"], x["utm_content"]) if v)
            print(f"{x['visitantes']:6d} {x['cuentas']:7d} {x['pagaron']:7d}  {marca}")
        s = altas_sin_utm(cli, a, b)
        print(f"Cuentas nuevas del mes (sin internos): {s['altas']} · sin ninguna marca UTM antes del alta: {s['sin_utm']}\n")

        print("## 3. Instagram: comentarios a los videos")
        cm = comentarios(cli, a, b)
        for x in cm:
            print(f"   {x['plan']:<14} {x['estado']:<15} {x['n']}")
        if not cm:
            print("   (ninguno)")
        print()

        print("## 4. Clientes nuevos (primera compra en el mes) y de dónde vinieron")
        cl = clientes(cli, a, b)
        for x in cl:
            origen = x["web"] or (f"WhatsApp {x['wa_fecha']}: «{x['wa_texto']}»" if x["wa_fecha"] else "SIN DATO")
            monto = f"${x['monto_sales']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if x["monto_sales"] else "(fuera de sales)"
            print(f"   {x['primera']}  {x['full_name']:<28} {x['plan_sales'] or '-':<10} {monto:>14}  ← {origen}")
        print(f"   Total: {len(cl)} cliente(s) nuevo(s). «SIN DATO» = no pasó por un link con marca ni está en el export de WhatsApp.")


if __name__ == "__main__":
    main()
