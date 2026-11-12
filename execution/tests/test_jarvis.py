"""
Tests de execution/jarvis/servidor.py y brief.py.

    /Users/Facu/facu-os/.venv/bin/python -m pytest execution/tests/test_jarvis.py -q

Nada real: Claude (`telegram_bot._correr_claude`), `servidor.sintetizar`, `servidor.transcribir` y las
fuentes del brief están reemplazados. DATA/ESTADO/BRIEF/AUDIO apuntan a tmp_path (no se toca
data/jarvis). El server de test corre en un puerto efímero, aparte del 7777.
"""
import http.client
import json
import sys
import threading
import time
from http.server import ThreadingHTTPServer

import pytest

sys.path.insert(0, "/Users/Facu/facu-os/execution/jarvis")
sys.path.insert(0, "/Users/Facu/facu-os/execution")

import brief  # noqa: E402
import servidor  # noqa: E402
import telegram_bot as tb  # noqa: E402

ID32 = "a" * 32


@pytest.fixture
def srv(tmp_path, monkeypatch):
    monkeypatch.setattr(servidor, "DATA", tmp_path)
    monkeypatch.setattr(servidor, "AUDIO", tmp_path / "audio")
    monkeypatch.setattr(servidor, "ESTADO", tmp_path / "estado.json")
    monkeypatch.setattr(servidor, "BRIEF", tmp_path / "brief.json")
    (tmp_path / "audio").mkdir()
    monkeypatch.setattr(servidor, "sintetizar", lambda t: "f" * 32 + ".ogg")
    monkeypatch.setattr(servidor, "transcribir", lambda d: "texto oído")
    monkeypatch.delenv("TELEGRAM_MODO_CAMBIOS", raising=False)
    s = ThreadingHTTPServer(("127.0.0.1", 0), servidor.Manejador)
    puerto = s.server_address[1]
    monkeypatch.setattr(servidor, "HOSTS_OK", {f"127.0.0.1:{puerto}", f"localhost:{puerto}"})
    threading.Thread(target=s.serve_forever, daemon=True).start()
    s.puerto, s.tmp = puerto, tmp_path
    yield s
    s.shutdown()
    s.server_close()


def req(s, metodo, ruta, cuerpo=None, token=True, host="ok", ctype="application/json"):
    c = http.client.HTTPConnection("127.0.0.1", s.puerto, timeout=10)
    h = {"Host": f"127.0.0.1:{s.puerto}" if host == "ok" else host}
    if token is True:
        h["X-Jarvis-Token"] = servidor.TOKEN
    elif token:
        h["X-Jarvis-Token"] = token
    data = None
    if cuerpo is not None:
        data = cuerpo if isinstance(cuerpo, bytes) else json.dumps(cuerpo).encode()
        h["Content-Type"] = ctype
    c.request(metodo, ruta, body=data, headers=h)
    r = c.getresponse()
    raw = r.read()
    c.close()
    return r.status, raw


def js(raw):
    return json.loads(raw)


# --- seguridad ---------------------------------------------------------------------------------

def test_get_raiz_host_malo_403(srv):
    st, _ = req(srv, "GET", "/", host="evil.com")
    assert st == 403


def test_get_raiz_inyecta_token(srv):
    st, raw = req(srv, "GET", "/", token=False)
    assert st == 200
    html = raw.decode()
    assert servidor.TOKEN in html
    assert "{{TOKEN}}" not in html


@pytest.mark.parametrize("tok", [False, "equivocado", ""])
def test_api_get_sin_token_o_malo_403(srv, tok):
    st, _ = req(srv, "GET", "/api/brief", token=tok)
    assert st == 403


def test_api_get_host_malo_con_token_bueno_403(srv):
    st, _ = req(srv, "GET", "/api/brief", host="evil.com")
    assert st == 403


@pytest.mark.parametrize("ruta", ["/api/preguntar", "/api/plan", "/api/nuevo", "/api/actualizar"])
def test_api_post_sin_token_403(srv, ruta):
    st, _ = req(srv, "POST", ruta, {}, token=False)
    assert st == 403
    st, _ = req(srv, "POST", ruta, {}, token="mal")
    assert st == 403


def test_brief_sin_archivo_devuelve_error_legible(srv):
    st, raw = req(srv, "GET", "/api/brief")
    assert st == 200 and "error" in js(raw)


def test_brief_con_archivo(srv):
    (srv.tmp / "brief.json").write_text(json.dumps({"texto": "hola ñandú"}))
    st, raw = req(srv, "GET", "/api/brief")
    assert js(raw)["texto"] == "hola ñandú"


# --- audio -------------------------------------------------------------------------------------

@pytest.mark.parametrize("ruta", [
    "/api/audio/../estado.json",
    "/api/audio/..%2Festado.json",
    "/api/audio/%2e%2e/estado.json",
    "/api/audio/../../etc/passwd",
    "/api/audio/" + "a" * 31 + ".ogg",
    "/api/audio/" + "A" * 32 + ".ogg",
    "/api/audio/" + "a" * 32 + ".wav",
    "/api/audio/" + "a" * 32 + ".ogg/../x",
    "/api/audio/",
])
def test_audio_traversal_404(srv, ruta):
    (srv.tmp / "estado.json").write_text("{}")
    (srv.tmp / "audio" / ("a" * 32 + ".ogg")).write_bytes(b"x")
    st, _ = req(srv, "GET", ruta)
    assert st == 404


def test_audio_valido_se_sirve(srv):
    (srv.tmp / "audio" / f"{ID32}.ogg").write_bytes(b"OggS-fake")
    st, raw = req(srv, "GET", f"/api/audio/{ID32}.ogg")
    assert st == 200 and raw == b"OggS-fake"


def test_audio_valido_inexistente_404(srv):
    st, _ = req(srv, "GET", f"/api/audio/{'b' * 32}.ogg")
    assert st == 404


def test_audio_sin_token_403(srv):
    (srv.tmp / "audio" / f"{ID32}.ogg").write_bytes(b"x")
    st, _ = req(srv, "GET", f"/api/audio/{ID32}.ogg", token=False)
    assert st == 403


# --- preguntar ---------------------------------------------------------------------------------

def fake_claude(respuesta, sid="sess-1", llamadas=None):
    def f(texto, session_id, ejecutar=False, instrucciones=None):
        if llamadas is not None:
            llamadas.append({"texto": texto, "sid": session_id, "ejecutar": ejecutar})
        return respuesta, sid
    return f


def test_preguntar_json(srv, monkeypatch):
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_claude("Buen día, jefe.", llamadas=ll))
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "  hola  "})
    d = js(raw)
    assert st == 200
    assert d["respuesta"] == "Buen día, jefe."
    assert d["plan"] is None and d["audio"] == "f" * 32 + ".ogg"
    assert ll[0]["texto"] == "hola" and ll[0]["ejecutar"] is False
    # el session_id queda guardado
    assert js((srv.tmp / "estado.json").read_bytes())["session_id"] == "sess-1"


def test_preguntar_texto_vacio_no_llama_claude(srv, monkeypatch):
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_claude("x", llamadas=ll))
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "   "})
    assert st == 200 and "No te escuché" in js(raw)["respuesta"]
    assert ll == []


def test_preguntar_audio_usa_transcribir(srv, monkeypatch):
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_claude("ok", llamadas=ll))
    st, raw = req(srv, "POST", "/api/preguntar", b"\x00\x01webm", ctype="audio/webm")
    d = js(raw)
    assert d["oido"] == "texto oído" and ll[0]["texto"] == "texto oído"


def test_preguntar_inyecta_numeros_del_dia(srv, monkeypatch):
    ll = []
    (srv.tmp / "numeros.json").write_text(json.dumps({
        "generado": "2026-11-11T09:30:00-03:00",
        "numeros": {"Paseo Nordelta": {"exigible_total": 5}, "Tareas programadas": {"problemas": 9}},
        "errores": [{"fuente": "Mails", "error": "boom"}]}))
    monkeypatch.setattr(tb, "_correr_claude", fake_claude("ok", llamadas=ll))
    req(srv, "POST", "/api/preguntar", {"texto": "cuánto?"})
    t = ll[0]["texto"]
    assert "09:30" in t and "11/11" in t and "exigible_total" in t
    assert "Tareas programadas" not in t and "Mails" in t and t.endswith("cuánto?")


def test_preguntar_con_plan(srv, monkeypatch):
    resp = "Te armo esto.\n<<<PLAN\n1. correr script X\nPLAN>>>"
    monkeypatch.setattr(tb, "_correr_claude", fake_claude(resp))
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "hacé X"})
    d = js(raw)
    assert d["plan"]["id"] and "correr script X" in d["plan"]["texto"]
    assert set(d["plan"]) == {"id", "texto"}      # no filtra el ts
    assert "<<<PLAN" not in d["respuesta"] and "PLAN>>>" not in d["respuesta"]
    assert "correr script X" not in d["respuesta"]
    assert "Te armo esto" in d["respuesta"]


def test_preguntar_resume_falla_reintenta_sin_sesion(srv, monkeypatch):
    (srv.tmp / "estado.json").write_text(json.dumps({"session_id": "vieja"}))
    ll = []

    def f(texto, sid, ejecutar=False, instrucciones=None):
        ll.append(sid)
        if sid == "vieja":
            raise tb.ClaudeFallo("resume roto")
        return "ok", "nueva"
    monkeypatch.setattr(tb, "_correr_claude", f)
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "hola"})
    assert js(raw)["respuesta"] == "ok" and ll == ["vieja", None]


def test_preguntar_claude_falla_sin_sesion_da_500(srv, monkeypatch):
    def f(*a, **k):
        raise tb.ClaudeFallo("caído")
    monkeypatch.setattr(tb, "_correr_claude", f)
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "hola"})
    assert st == 500 and "error" in js(raw)


def test_preguntar_json_roto_500_no_cuelga(srv):
    st, raw = req(srv, "POST", "/api/preguntar", b"{no json", ctype="application/json")
    assert st == 500


# --- plan --------------------------------------------------------------------------------------

def poner_plan(srv, edad=0, pid="plan123"):
    (srv.tmp / "estado.json").write_text(json.dumps(
        {"session_id": "s", "plan": {"id": pid, "texto": "hacer cosa", "ts": time.time() - edad}}))


def estado(srv):
    return json.loads((srv.tmp / "estado.json").read_text())


def test_plan_si_ejecuta_una_sola_vez(srv, monkeypatch):
    monkeypatch.setenv("TELEGRAM_MODO_CAMBIOS", "1")
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_claude("hecho", llamadas=ll))
    poner_plan(srv)
    st1, r1 = req(srv, "POST", "/api/plan", {"id": "plan123", "si": True})
    st2, r2 = req(srv, "POST", "/api/plan", {"id": "plan123", "si": True})
    assert js(r1)["respuesta"] == "hecho"
    assert "ya no está" in js(r2)["respuesta"]
    assert len(ll) == 1 and ll[0]["ejecutar"] is True
    assert "hacer cosa" in ll[0]["texto"] and ll[0]["sid"] is None
    assert "plan" not in estado(srv)


def test_plan_si_concurrente_ejecuta_una_vez(srv, monkeypatch):
    """Dos POST casi simultáneos: ¿se ejecuta una sola vez?"""
    monkeypatch.setenv("TELEGRAM_MODO_CAMBIOS", "1")
    ll = []

    def lenta(texto, sid, ejecutar=False, instrucciones=None):
        ll.append(1)
        time.sleep(0.3)
        return "hecho", None
    monkeypatch.setattr(tb, "_correr_claude", lenta)
    poner_plan(srv)
    res = []
    ths = [threading.Thread(target=lambda: res.append(req(srv, "POST", "/api/plan", {"id": "plan123", "si": True})))
           for _ in range(2)]
    [t.start() for t in ths]
    [t.join() for t in ths]
    assert len(ll) == 1, f"el plan se ejecutó {len(ll)} veces con dos POST simultáneos"


def test_plan_modo_cambios_apagado_no_ejecuta(srv, monkeypatch):
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_claude("no debería", llamadas=ll))
    poner_plan(srv)
    st, raw = req(srv, "POST", "/api/plan", {"id": "plan123", "si": True})
    assert "apagado" in js(raw)["respuesta"]
    assert ll == []
    assert estado(srv)["plan"]["id"] == "plan123"      # sigue ahí


@pytest.mark.parametrize("valor", ["0", "", "true", "yes"])
def test_plan_modo_cambios_solo_con_1(srv, monkeypatch, valor):
    monkeypatch.setenv("TELEGRAM_MODO_CAMBIOS", valor)
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_claude("x", llamadas=ll))
    poner_plan(srv)
    req(srv, "POST", "/api/plan", {"id": "plan123", "si": True})
    assert ll == []


def test_plan_vencido_no_se_ejecuta(srv, monkeypatch):
    monkeypatch.setenv("TELEGRAM_MODO_CAMBIOS", "1")
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_claude("x", llamadas=ll))
    poner_plan(srv, edad=tb.VENCE_PLAN + 60)
    st, raw = req(srv, "POST", "/api/plan", {"id": "plan123", "si": True})
    assert "más de dos horas" in js(raw)["respuesta"]
    assert ll == [] and "plan" not in estado(srv)


def test_plan_id_equivocado_no_ejecuta(srv, monkeypatch):
    monkeypatch.setenv("TELEGRAM_MODO_CAMBIOS", "1")
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_claude("x", llamadas=ll))
    poner_plan(srv)
    st, raw = req(srv, "POST", "/api/plan", {"id": "otro", "si": True})
    assert "ya no está" in js(raw)["respuesta"] and ll == []
    assert estado(srv)["plan"]["id"] == "plan123"


def test_plan_no_descarta(srv, monkeypatch):
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_claude("x", llamadas=ll))
    poner_plan(srv)
    st, raw = req(srv, "POST", "/api/plan", {"id": "plan123", "si": False})
    assert js(raw)["respuesta"] == "Descartado."
    assert "plan" not in estado(srv) and estado(srv)["session_id"] == "s" and ll == []


def test_plan_no_con_id_ajeno_no_descarta(srv):
    poner_plan(srv)
    req(srv, "POST", "/api/plan", {"id": "otro", "si": False})
    assert estado(srv)["plan"]["id"] == "plan123"


def test_nuevo_borra_sesion_pero_no_plan(srv):
    poner_plan(srv)
    st, raw = req(srv, "POST", "/api/nuevo", {})
    assert js(raw) == {"ok": True}
    assert "session_id" not in estado(srv)


def test_post_ruta_desconocida_404(srv):
    st, _ = req(srv, "POST", "/api/nada", {})
    assert st == 404


# --- brief -------------------------------------------------------------------------------------

def ok_astro():
    return {"mes": "2026-11", "ingresos_mes": 1500000, "movimientos_mes": 10, "ingresos_7d": 200000,
            "movimientos_7d": 3, "activos": 29, "vencidos": 1,
            "vencidos_detalle": [{"plan": "Silver", "vencia": "2026-11-05"}]}


def ok_pauta():
    return {"moneda": "USD", "gasto_7d": 50.0, "chats_7d": 10, "costo_chat_7d": 5.0,
            "gasto_mes": 120.0, "anuncios_activos": 2}


def ok_paseo():
    return {"exigible_total": 900000, "deudores": [{"local": "Local 7", "exigible": 900000, "por_banco": False}],
            "al_dia": 5, "con_regla": 1, "filas_leidas": 7}


def ok_mails():
    return {"facu": 12}


def ok_tareas():
    return {"problemas": 0, "detalle": "todo bien"}


def boom(msg="se cayó"):
    def f():
        raise RuntimeError(msg)
    return f


@pytest.fixture
def bf(tmp_path, monkeypatch):
    monkeypatch.setattr(brief, "DATA", tmp_path)
    monkeypatch.setattr(servidor, "DATA", tmp_path)
    monkeypatch.setattr(servidor, "AUDIO", tmp_path / "audio")
    monkeypatch.setattr(tb, "cargar_env", lambda: None)
    monkeypatch.setattr(sys, "argv", ["brief.py", "--sin-claude", "--sin-voz"])
    llamado = []
    monkeypatch.setattr(servidor, "sintetizar", lambda t: llamado.append(t) or "x.ogg")
    monkeypatch.setattr(tb, "_correr_claude", lambda *a, **k: pytest.fail("llamó a Claude real"))
    return tmp_path


def fuentes(monkeypatch, **fns):
    base = {"Astronomy Academy": ok_astro, "Pauta Meta": ok_pauta, "Paseo Nordelta": ok_paseo,
            "Mails": ok_mails, "Tareas programadas": ok_tareas}
    base.update({k.replace("_", " "): v for k, v in fns.items()})
    monkeypatch.setattr(brief, "FUENTES", list(base.items()))


def test_brief_todo_ok(bf, monkeypatch):
    fuentes(monkeypatch)
    assert brief.main() == 0
    b = json.loads((bf / "brief.json").read_text())
    assert b["errores"] == [] and len(b["paneles"]) == 4
    assert (bf / "numeros.json").exists()
    assert b["audio"] is None


def test_brief_una_fuente_falla(bf, monkeypatch):
    fuentes(monkeypatch, Pauta_Meta=boom("sin token"))
    assert brief.main() == 0
    b = json.loads((bf / "brief.json").read_text())
    assert [e["fuente"] for e in b["errores"]] == ["Pauta Meta"]
    assert "sin token" in b["errores"][0]["error"]
    titulos = [p["titulo"] for p in b["paneles"]]
    assert "Pauta · Meta Ads" not in titulos
    # y ningún valor de pauta aparece como 0 en otro panel
    for p in b["paneles"]:
        for it in p["items"]:
            assert "Gasto" not in it["etiqueta"] and "Anuncios" not in it["etiqueta"]
    nums = json.loads((bf / "numeros.json").read_text())
    assert "Pauta Meta" not in nums["numeros"] and nums["errores"][0]["fuente"] == "Pauta Meta"


def test_brief_todas_fallan_devuelve_1_sin_brief(bf, monkeypatch):
    fuentes(monkeypatch, Astronomy_Academy=boom(), Pauta_Meta=boom(), Paseo_Nordelta=boom(),
            Mails=boom(), Tareas_programadas=boom())
    assert brief.main() == 1
    assert not (bf / "brief.json").exists()


def test_brief_todas_fallan_no_pisa_brief_viejo(bf, monkeypatch):
    (bf / "brief.json").write_text('{"viejo": true}')
    fuentes(monkeypatch, Astronomy_Academy=boom(), Pauta_Meta=boom(), Paseo_Nordelta=boom(),
            Mails=boom(), Tareas_programadas=boom())
    brief.main()
    assert json.loads((bf / "brief.json").read_text()) == {"viejo": True}


def test_brief_sin_voz_no_sintetiza(bf, monkeypatch):
    fuentes(monkeypatch)
    ll = []
    monkeypatch.setattr(servidor, "sintetizar", lambda t: ll.append(t))
    brief.main()
    assert ll == []


def test_brief_con_voz_llama_sintetizar_mockeado(bf, monkeypatch):
    fuentes(monkeypatch)
    monkeypatch.setattr(sys, "argv", ["brief.py", "--sin-claude"])
    monkeypatch.setattr(servidor, "sintetizar", lambda t: "z.ogg")
    brief.main()
    assert json.loads((bf / "brief.json").read_text())["audio"] == "z.ogg"


def test_brief_con_claude_mockeado(bf, monkeypatch):
    fuentes(monkeypatch)
    monkeypatch.setattr(sys, "argv", ["brief.py", "--sin-voz"])
    pedidos = []
    monkeypatch.setattr(tb, "_correr_claude", lambda t, s, **k: pedidos.append(t) or ("  Buen día, jefe.  ", None))
    assert brief.main() == 0
    assert json.loads((bf / "brief.json").read_text())["texto"] == "Buen día, jefe."
    assert "Tareas programadas" in pedidos[0] and "ninguna" in pedidos[0]


# --- paneles: sin mezclar negocios --------------------------------------------------------------

def test_paneles_cada_uno_con_su_fuente():
    n = {"Astronomy Academy": ok_astro(), "Pauta Meta": ok_pauta(), "Paseo Nordelta": ok_paseo(),
         "Mails": ok_mails(), "Tareas programadas": ok_tareas()}
    ps = {p["titulo"]: p for p in brief.paneles(n)}
    assert set(ps) == {"Astronomy Academy", "Pauta · Meta Ads", "Paseo Nordelta", "Bandeja y sistema"}
    vals = lambda t: {i["etiqueta"]: i["valor"] for i in ps[t]["items"]}
    assert vals("Astronomy Academy")["Ingresos 2026-11"] == "$1.500.000"
    assert vals("Astronomy Academy")["Alumnos activos"] == "29"
    assert vals("Pauta · Meta Ads")["Gasto del mes"] == "US$120,00"
    assert vals("Paseo Nordelta")["Deuda exigible"] == "$900.000"
    assert vals("Bandeja y sistema")["Sin leer · facu"] == "12"
    # los números del Paseo no aparecen en Astronomy ni al revés
    assert "Deuda exigible" not in vals("Astronomy Academy")
    assert "Local 7" not in vals("Astronomy Academy") and "Local 7" in vals("Paseo Nordelta")
    assert "Alumnos activos" not in vals("Paseo Nordelta")
    # Meta en USD, Astronomy/Paseo en ARS: sin conversión
    assert all(v.startswith("$") for v in vals("Paseo Nordelta").values())
    assert all(v.startswith("US$") for k, v in vals("Pauta · Meta Ads").items() if "Anuncios" not in k and k != "")


def test_paneles_solo_una_fuente_solo_su_panel():
    ps = brief.paneles({"Paseo Nordelta": ok_paseo()})
    assert [p["titulo"] for p in ps] == ["Paseo Nordelta"]
    ps = brief.paneles({"Pauta Meta": ok_pauta()})
    assert [p["titulo"] for p in ps] == ["Pauta · Meta Ads"]


def test_paneles_vacio():
    assert brief.paneles({}) == []


def test_paneles_pauta_en_ars_no_usa_techo_usd():
    p = ok_pauta() | {"moneda": "ARS", "gasto_mes": 99999.0}
    items = brief.paneles({"Pauta Meta": p})[0]["items"]
    mes = [i for i in items if i["etiqueta"] == "Gasto del mes"][0]
    assert mes["valor"].startswith("ARS") and mes["tono"] is None


def test_paneles_pauta_techo_usd_alerta():
    p = ok_pauta() | {"gasto_mes": 501.0}
    items = brief.paneles({"Pauta Meta": p})[0]["items"]
    assert [i for i in items if i["etiqueta"] == "Gasto del mes"][0]["tono"] == "mal"


def test_paneles_pauta_sin_chats_no_divide():
    p = ok_pauta() | {"chats_7d": 0, "costo_chat_7d": None}
    brief.paneles({"Pauta Meta": p})   # no debe tirar


def test_paneles_pauta_valor_cero_se_muestra():
    """Un 0 real (gasto 0) es dato válido y debe mostrarse; el dict no está vacío."""
    p = ok_pauta() | {"gasto_7d": 0.0, "gasto_mes": 0.0, "anuncios_activos": 0, "chats_7d": 0, "costo_chat_7d": None}
    items = brief.paneles({"Pauta Meta": p})[0]["items"]
    assert [i for i in items if i["etiqueta"] == "Anuncios prendidos"][0]["tono"] == "alerta"


def test_formato_montos():
    assert brief.pesos(1234567.6) == "$1.234.568"
    assert brief.usd(1234.5) == "US$1.234,50"
