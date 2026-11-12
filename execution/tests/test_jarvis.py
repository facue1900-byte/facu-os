"""
Tests de execution/jarvis/servidor.py y brief.py.

    /Users/Facu/facu-os/.venv/bin/python -m pytest execution/tests/test_jarvis.py -q

Nada real: el cerebro (`servidor.claude_completo`), el ejecutor de planes (`telegram_bot._correr_claude`),
`servidor.sintetizar`, `servidor.transcribir`, `subprocess.run` (osascript/open/pbcopy) y las fuentes del
brief están reemplazados. DATA/ESTADO/BRIEF/AUDIO/TAREAS apuntan a tmp_path (no se toca data/jarvis).
Los hilos de tareas NO corren solos: quedan en `srv.hilos` y el test decide cuándo (`srv.correr_hilos()`).
El server de test corre en un puerto efímero, aparte del 7777.
"""
import datetime as dt
import http.client
import json
import subprocess
import sys
import threading
import time
import types
from http.server import ThreadingHTTPServer

import pytest

sys.path.insert(0, "/Users/Facu/facu-os/execution/jarvis")
sys.path.insert(0, "/Users/Facu/facu-os/execution")

import brief  # noqa: E402
import servidor  # noqa: E402
import telegram_bot as tb  # noqa: E402

ID32 = "a" * 32
UUID1 = "123e4567-e89b-42d3-a456-426614174000"
UUID2 = "9b2f6c1a-0d3e-4f5a-8b7c-1234567890ab"


class HiloFalso:
    """Reemplaza threading.Thread en servidor: no arranca nada hasta que el test lo pide."""
    cola = None

    def __init__(self, target=None, args=(), kwargs=None, daemon=None):
        self.target, self.args, self.kwargs = target, args, kwargs or {}

    def start(self):
        HiloFalso.cola.append(self)

    def correr(self):
        self.target(*self.args, **self.kwargs)


@pytest.fixture(autouse=True)
def sin_voz_real(monkeypatch):
    """Los rellenos y avances sintetizan en hilos: ningún test le habla a Microsoft de verdad."""
    monkeypatch.setattr(servidor, "sintetizar", lambda t: "e" * 32 + ".mp3")
    monkeypatch.setattr(servidor, "_AUDIO_FIJO", {})
    monkeypatch.setattr(servidor, "sintetizar_en_vivo", lambda t: "d" * 32 + ".mp3")


@pytest.fixture
def srv(tmp_path, monkeypatch):
    monkeypatch.setattr(servidor, "DATA", tmp_path)
    monkeypatch.setattr(servidor, "AUDIO", tmp_path / "audio")
    monkeypatch.setattr(servidor, "ESTADO", tmp_path / "estado.json")
    monkeypatch.setattr(servidor, "BRIEF", tmp_path / "brief.json")
    monkeypatch.setattr(servidor, "TAREAS", tmp_path / "tareas.json")
    (tmp_path / "audio").mkdir()
    monkeypatch.setattr(servidor, "sintetizar", lambda t: "f" * 32 + ".ogg")
    monkeypatch.setattr(servidor, "transcribir", lambda d: "texto oído")
    monkeypatch.delenv("TELEGRAM_MODO_CAMBIOS", raising=False)
    # Sólo `servidor.threading.Thread` se reemplaza (el módulo global threading queda intacto).
    hilos = []
    HiloFalso.cola = hilos
    monkeypatch.setattr(servidor, "threading", types.SimpleNamespace(
        Thread=HiloFalso, Lock=threading.Lock))
    # Por si algo se escapa: ni Claude real ni procesos reales.
    def no_real(*a, **k):
        raise AssertionError(f"llamada real no mockeada: {a!r}")
    monkeypatch.setattr(servidor, "claude_completo", no_real)
    # El cerebro vivo delega en claude_completo: así los tests de preguntas mockean un solo lugar.
    monkeypatch.setattr(servidor, "CEREBRO", types.SimpleNamespace(
        turno=lambda texto, sid, limite: servidor.claude_completo(texto, sid, servidor.INSTRUCCIONES, "Jarvis", limite),
        apagar=lambda: None))
    monkeypatch.setattr(tb, "_correr_claude", no_real)
    monkeypatch.setattr(servidor.subprocess, "run", no_real)
    monkeypatch.setattr(servidor.subprocess, "Popen", no_real)
    s = ThreadingHTTPServer(("127.0.0.1", 0), servidor.Manejador)
    puerto = s.server_address[1]
    monkeypatch.setattr(servidor, "HOSTS_OK", {f"127.0.0.1:{puerto}", f"localhost:{puerto}"})
    threading.Thread(target=s.serve_forever, daemon=True).start()
    s.puerto, s.tmp, s.hilos = puerto, tmp_path, hilos

    def correr_hilos():
        while hilos:
            hilos.pop(0).correr()
    s.correr_hilos = correr_hilos
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


# --- preguntar (cerebro = servidor.claude_completo) ---------------------------------------------

def fake_cerebro(respuesta, sid="sess-1", llamadas=None):
    def f(texto, session_id, instrucciones, nombre, limite, **kw):
        if llamadas is not None:
            llamadas.append({"texto": texto, "sid": session_id, "instrucciones": instrucciones,
                             "nombre": nombre, "limite": limite})
        return respuesta, sid
    return f


def fake_plan(respuesta, sid=None, llamadas=None):
    """Para tb._correr_claude (ejecutor de planes)."""
    def f(texto, session_id, ejecutar=False, instrucciones=None):
        if llamadas is not None:
            llamadas.append({"texto": texto, "sid": session_id, "ejecutar": ejecutar})
        return respuesta, sid
    return f


def estado(srv):
    return json.loads((srv.tmp / "estado.json").read_text())


def tareas(srv):
    return json.loads((srv.tmp / "tareas.json").read_text())


def test_preguntar_json(srv, monkeypatch):
    ll = []
    monkeypatch.setattr(servidor, "claude_completo", fake_cerebro("Buen día, jefe.", llamadas=ll))
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "  hola  "})
    d = js(raw)
    assert st == 200
    assert d["respuesta"] == "Buen día, jefe."
    assert d["plan"] is None and d["audio"] == "f" * 32 + ".ogg" and d["tareas"] == []
    assert ll[0]["texto"] == "hola" and ll[0]["sid"] is None
    assert ll[0]["instrucciones"] == servidor.INSTRUCCIONES and ll[0]["nombre"] == "Jarvis"
    assert ll[0]["limite"] == servidor.TIEMPO_MAX_CHARLA
    assert estado(srv)["session_id"] == "sess-1"


def test_preguntar_reusa_session_id(srv, monkeypatch):
    ll = []
    monkeypatch.setattr(servidor, "claude_completo", fake_cerebro("ok", llamadas=ll))
    req(srv, "POST", "/api/preguntar", {"texto": "uno"})
    req(srv, "POST", "/api/preguntar", {"texto": "dos"})
    assert [x["sid"] for x in ll] == [None, "sess-1"]


def test_preguntar_texto_vacio_no_llama_claude(srv, monkeypatch):
    ll = []
    monkeypatch.setattr(servidor, "claude_completo", fake_cerebro("x", llamadas=ll))
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "   "})
    assert st == 200 and "No te escuché" in js(raw)["respuesta"]
    assert ll == []


def test_preguntar_audio_usa_transcribir(srv, monkeypatch):
    ll = []
    monkeypatch.setattr(servidor, "claude_completo", fake_cerebro("ok", llamadas=ll))
    st, raw = req(srv, "POST", "/api/preguntar", b"\x00\x01webm", ctype="audio/webm")
    d = js(raw)
    assert d["oido"] == "texto oído" and ll[0]["texto"].endswith("texto oído")
    assert "DICTADO POR VOZ" in ll[0]["texto"], "un dictado va marcado para que Jarvis limpie muletillas y autocorrecciones"


def test_preguntar_inyecta_numeros_del_dia(srv, monkeypatch):
    ll = []
    (srv.tmp / "numeros.json").write_text(json.dumps({
        "generado": "2026-11-11T09:30:00-03:00",
        "numeros": {"Paseo Nordelta": {"exigible_total": 5}, "Tareas programadas": {"problemas": 9}},
        "errores": [{"fuente": "Mails", "error": "boom"}]}))
    monkeypatch.setattr(servidor, "claude_completo", fake_cerebro("ok", llamadas=ll))
    req(srv, "POST", "/api/preguntar", {"texto": "cuánto?"})
    t = ll[0]["texto"]
    assert "09:30" in t and "11/11" in t and "exigible_total" in t
    assert "Tareas programadas" not in t and "Mails" in t and t.endswith("cuánto?")


def test_contexto_numeros_viejos_avisa(srv):
    (srv.tmp / "numeros.json").write_text(json.dumps({
        "generado": "2020-01-02T09:30:00-03:00", "numeros": {"Paseo Nordelta": {"a": 1}}}))
    assert "VIEJOS" in servidor.contexto_del_dia()


def test_contexto_incluye_tareas(srv):
    (srv.tmp / "tareas.json").write_text(json.dumps([
        {"id": "abc123", "titulo": "Arreglar X", "estado": "lista", "session_id": UUID1, "para_decir": "Listo jefe"},
        {"id": "def456", "titulo": "Otra", "estado": "corriendo"}]))
    c = servidor.contexto_del_dia()
    assert "[abc123]" in c and "Arreglar X" in c and UUID1 in c and "Listo jefe" in c
    assert "[def456]" in c and "corriendo" in c


def test_contexto_vacio_sin_nada(srv):
    assert servidor.contexto_del_dia() == ""


def test_preguntar_con_plan(srv, monkeypatch):
    resp = "Te armo esto.\n<<<PLAN\n1. correr script X\nPLAN>>>"
    monkeypatch.setattr(servidor, "claude_completo", fake_cerebro(resp))
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "hacé X"})
    d = js(raw)
    assert d["plan"]["id"] and "correr script X" in d["plan"]["texto"]
    assert set(d["plan"]) == {"id", "texto"}      # no filtra el ts
    assert "<<<PLAN" not in d["respuesta"] and "PLAN>>>" not in d["respuesta"]
    assert "correr script X" not in d["respuesta"]
    assert "Te armo esto" in d["respuesta"]


def test_preguntar_resume_falla_reintenta_sin_sesion(srv, monkeypatch):
    (srv.tmp / "estado.json").write_text(json.dumps({"session_id": "vieja", "sesion_dia": time.strftime("%Y-%m-%d")}))
    ll = []

    def f(texto, sid, instrucciones, nombre, limite, **kw):
        ll.append(sid)
        if sid == "vieja":
            raise tb.ClaudeFallo("resume roto")
        return "ok", "nueva"
    monkeypatch.setattr(servidor, "claude_completo", f)
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "hola"})
    assert js(raw)["respuesta"] == "ok" and ll == ["vieja", None]
    assert estado(srv)["session_id"] == "nueva"


def test_preguntar_claude_falla_sin_sesion_da_500(srv, monkeypatch):
    def f(*a, **k):
        raise tb.ClaudeFallo("caído")
    monkeypatch.setattr(servidor, "claude_completo", f)
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "hola"})
    assert st == 500 and "error" in js(raw)


def test_preguntar_json_roto_500_no_cuelga(srv):
    st, raw = req(srv, "POST", "/api/preguntar", b"{no json", ctype="application/json")
    assert st == 500


# --- separar_bloques ---------------------------------------------------------------------------

def test_separar_bloques_todo_junto():
    r = ("Listo jefe.\n<<<TAREA Arreglar la app\nHacé A en B.\nVerificá C.\nTAREA>>>\n"
         "<<<ABRIR Terminal jarvis>>>\n<<<PLAN\nmandar mail\nPLAN>>>")
    hablado, plan, ts, ab = servidor.separar_bloques(r)
    assert hablado == "Listo jefe."
    assert plan == "mandar mail"
    assert ts == [("Arreglar la app", "Hacé A en B.\nVerificá C.")]
    assert ab == [("terminal", "jarvis")]


def test_separar_bloques_sin_bloques():
    assert servidor.separar_bloques("Hola jefe") == ("Hola jefe", None, [], [])


def test_separar_bloques_varias_tareas():
    r = "<<<TAREA uno\npedido 1\nTAREA>>>\n<<<TAREA dos\npedido 2\nTAREA>>>"
    _, _, ts, _ = servidor.separar_bloques(r)
    assert ts == [("uno", "pedido 1"), ("dos", "pedido 2")]


def test_separar_bloques_abrir_destino_invalido_no_matchea():
    _, _, _, ab = servidor.separar_bloques("<<<ABRIR firefox jarvis>>>")
    assert ab == []


def test_separar_bloques_abrir_sesion_con_caracteres_raros_no_matchea():
    _, _, _, ab = servidor.separar_bloques('<<<ABRIR terminal x"; do shell script "rm>>>')
    assert ab == []


# --- tareas en segundo plano ---------------------------------------------------------------------

def test_tarea_se_crea_corriendo_y_termina_lista(srv, monkeypatch):
    ll = []
    resp = "Ya lo lanzo.\n<<<TAREA Arreglar la app\nArreglá X en Y y verificá.\nTAREA>>>"
    reporte = ("Hice A y verifiqué B. Quedó pendiente C.\n\n"
               "PARA DECIR: Jefe, está arreglado y verificado.\nSegunda oración.")

    def cerebro(texto, sid, instrucciones, nombre, limite, **kw):
        ll.append({"texto": texto, "sid": sid, "instr": instrucciones, "nombre": nombre, "limite": limite})
        if instrucciones == servidor.INSTRUCCIONES:
            return resp, "sess-1"
        return reporte, UUID1
    monkeypatch.setattr(servidor, "claude_completo", cerebro)
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "arreglá X"})
    d = js(raw)
    assert d["respuesta"] == "Ya lo lanzo."
    assert "TAREA" not in d["respuesta"] and "Arreglá X" not in d["respuesta"]
    assert len(d["tareas"]) == 1
    tid = d["tareas"][0]
    # antes de correr el hilo: corriendo, sin sesión
    t = tareas(srv)[0]
    assert t["id"] == tid and t["estado"] == "corriendo" and t["session_id"] is None
    assert t["titulo"] == "Arreglar la app" and t["pedido"] == "Arreglá X en Y y verificá."
    assert len(srv.hilos) == 1
    srv.correr_hilos()
    t = tareas(srv)[0]
    assert t["estado"] == "lista" and t["session_id"] == UUID1 and t["fin"]
    assert t["para_decir"] == "Jefe, está arreglado y verificado.\nSegunda oración."
    assert "PARA DECIR" not in t["resultado"] and "Hice A y verifiqué B" in t["resultado"]
    assert t["audio"] == "f" * 32 + ".ogg" and t["visto"] is False
    # la sesión de la tarea es otra, con sus propias instrucciones, sin resume, y ve sólo el pedido
    llamada_tarea = ll[-1]
    assert llamada_tarea["instr"] == servidor.INSTRUCCIONES_TAREA and llamada_tarea["sid"] is None
    assert llamada_tarea["texto"] == "Arreglá X en Y y verificá." and llamada_tarea["limite"] == servidor.TIEMPO_MAX_TAREA
    assert llamada_tarea["nombre"].startswith("Jarvis · Arreglar la app")
    # y la sesión de charla no se pisó con la de la tarea
    assert estado(srv)["session_id"] == "sess-1"


def test_tarea_sin_para_decir_usa_el_resultado_recortado(srv, monkeypatch):
    larga = "x" * 1000
    monkeypatch.setattr(servidor, "claude_completo", lambda *a, **k: (larga, UUID1))
    t = servidor.lanzar_tarea("T", "pedido")
    srv.correr_hilos()
    r = tareas(srv)[0]
    assert r["estado"] == "lista" and len(r["para_decir"]) == 600 and r["resultado"] == larga


def test_solo_bloque_tarea_dice_lo_lance(srv, monkeypatch):
    monkeypatch.setattr(servidor, "claude_completo", fake_cerebro("<<<TAREA Algo\npedido\nTAREA>>>"))
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "hacelo"})
    d = js(raw)
    assert "lancé" in d["respuesta"] and len(d["tareas"]) == 1
    # y lo mismo quedó en la conversación
    assert "lancé" in estado(srv)["conversacion"][-1]["texto"]
    assert estado(srv)["conversacion"][-1]["tareas"] == d["tareas"]


def test_tarea_que_falla_queda_falló_con_error(srv, monkeypatch):
    def f(*a, **k):
        raise tb.ClaudeFallo("se rompió el mundo")
    monkeypatch.setattr(servidor, "claude_completo", f)
    t = servidor.lanzar_tarea("Rota", "pedido")
    srv.correr_hilos()
    r = tareas(srv)[0]
    assert r["estado"] == "falló" and "se rompió el mundo" in r["resultado"]
    assert "Rota" in r["para_decir"] and "falló" in r["para_decir"] and r["fin"]
    assert r["session_id"] is None


def test_tarea_falla_aunque_la_voz_falle_igual_queda_lista(srv, monkeypatch):
    monkeypatch.setattr(servidor, "claude_completo", lambda *a, **k: ("PARA DECIR: ok", UUID1))

    def mal(t):
        raise RuntimeError("say roto")
    monkeypatch.setattr(servidor, "sintetizar", mal)
    servidor.lanzar_tarea("T", "p")
    srv.correr_hilos()
    r = tareas(srv)[0]
    assert r["estado"] == "lista" and r["audio"] is None and r["para_decir"] == "ok"


def test_max_tareas_a_la_vez(srv):
    assert servidor.MAX_TAREAS_A_LA_VEZ == 3
    ts = [servidor.lanzar_tarea(f"T{i}", "p") for i in range(3)]
    assert all(ts)
    assert servidor.lanzar_tarea("T4", "p") is None
    assert len(tareas(srv)) == 3 and len(srv.hilos) == 3


def test_max_tareas_se_libera_al_terminar(srv, monkeypatch):
    monkeypatch.setattr(servidor, "claude_completo", lambda *a, **k: ("PARA DECIR: ok", UUID1))
    for i in range(3):
        servidor.lanzar_tarea(f"T{i}", "p")
    srv.correr_hilos()
    assert servidor.lanzar_tarea("T4", "p") is not None


def test_cuarta_tarea_en_una_respuesta(srv, monkeypatch):
    bloques = "".join(f"<<<TAREA t{i}\np{i}\nTAREA>>>" for i in range(4))
    monkeypatch.setattr(servidor, "claude_completo", fake_cerebro("Va.\n" + bloques))
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "x"})
    assert st == 200 and len(js(raw)["tareas"]) == 3
    assert len(tareas(srv)) == 3


def test_tarea_rechazada_no_dice_que_la_lanzo(srv, monkeypatch):
    """Si la 4ª se rechaza y el modelo no habló, no se puede decir «lo lancé»."""
    for i in range(3):
        servidor.lanzar_tarea(f"T{i}", "p")
    monkeypatch.setattr(servidor, "claude_completo", fake_cerebro("<<<TAREA cuarta\npedido\nTAREA>>>"))
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "x"})
    d = js(raw)
    assert d["tareas"] == []
    assert "lancé" not in d["respuesta"], f"dice que lanzó una tarea que se rechazó: {d['respuesta']!r}"


def test_tarea_titulo_se_recorta_a_80(srv):
    t = servidor.lanzar_tarea("a" * 200, "p")
    assert len(t["titulo"]) == 80


def test_marcar_interrumpidas(srv):
    (srv.tmp / "tareas.json").write_text(json.dumps([
        {"id": "a1", "titulo": "A", "estado": "corriendo"},
        {"id": "b2", "titulo": "B", "estado": "lista", "resultado": "bien"},
        {"id": "c3", "titulo": "C", "estado": "falló"},
        {"id": "d4", "titulo": "D", "estado": "corriendo"}]))
    servidor.marcar_interrumpidas()
    r = {t["id"]: t for t in tareas(srv)}
    assert r["a1"]["estado"] == "interrumpida" and r["d4"]["estado"] == "interrumpida"
    assert "reinició" in r["a1"]["resultado"] and r["a1"]["fin"]
    assert r["b2"]["estado"] == "lista" and r["b2"]["resultado"] == "bien"
    assert r["c3"]["estado"] == "falló"


def test_marcar_interrumpidas_sin_archivo_no_crea_nada(srv):
    servidor.marcar_interrumpidas()
    assert not (srv.tmp / "tareas.json").exists()


def test_interrumpida_no_cuenta_para_el_maximo(srv):
    (srv.tmp / "tareas.json").write_text(json.dumps(
        [{"id": f"x{i}", "titulo": "t", "estado": "corriendo"} for i in range(3)]))
    servidor.marcar_interrumpidas()
    assert servidor.lanzar_tarea("nueva", "p") is not None


def test_tarea_visto(srv):
    t = servidor.lanzar_tarea("T", "p")
    st, raw = req(srv, "POST", "/api/tarea/visto", {"id": t["id"]})
    assert st == 200 and js(raw) == {"ok": True}
    assert tareas(srv)[0]["visto"] is True


def test_tarea_visto_id_inexistente_no_rompe(srv):
    t = servidor.lanzar_tarea("T", "p")
    st, _ = req(srv, "POST", "/api/tarea/visto", {"id": "nope"})
    assert st == 200 and tareas(srv)[0]["visto"] is False


def test_tarea_visto_sin_token_403(srv):
    st, _ = req(srv, "POST", "/api/tarea/visto", {"id": "x"}, token=False)
    assert st == 403


# --- abrir sesiones ----------------------------------------------------------------------------

@pytest.fixture
def procs(monkeypatch):
    """Registra cada subprocess.run en vez de ejecutarlo."""
    ll = []

    def f(args, **kw):
        ll.append({"args": args, **kw})
        return types.SimpleNamespace(returncode=0)
    monkeypatch.setattr(servidor.subprocess, "run", f)
    return ll


def poner_tarea(srv, tid="abc123", sid=UUID1, estado_="lista"):
    (srv.tmp / "tareas.json").write_text(json.dumps([
        {"id": tid, "titulo": "T", "estado": estado_, "session_id": sid}]))


def test_abrir_terminal_jarvis_usa_sid_guardado(srv, procs):
    (srv.tmp / "estado.json").write_text(json.dumps({"session_id": UUID2}))
    msg = servidor.abrir_sesion("terminal", "jarvis")
    assert "Terminal" in msg
    assert len(procs) == 1
    args = procs[0]["args"]
    assert args[0] == "/usr/bin/osascript"
    script = " ".join(args)
    assert f"--resume {UUID2}" in script and "cd /Users/Facu/facu-os" in script
    assert "Terminal" in script


def test_abrir_terminal_tarea_usa_su_sid(srv, procs):
    poner_tarea(srv)
    servidor.abrir_sesion("terminal", "abc123")
    assert f"--resume {UUID1}" in " ".join(procs[0]["args"])


def test_abrir_terminal_nueva_sin_resume(srv, procs):
    servidor.abrir_sesion("terminal", "nueva")
    assert len(procs) == 1 and "--resume" not in " ".join(procs[0]["args"])


def test_abrir_sid_con_forma_rara_se_rechaza(srv, procs):
    poner_tarea(srv, sid="no-es-un-uuid")
    msg = servidor.abrir_sesion("terminal", "abc123")
    assert "forma esperada" in msg and procs == []


@pytest.mark.parametrize("malo", [
    'x"; do shell script "rm',
    UUID1 + '"; do shell script "rm -rf ~',
    UUID1 + "\n",
    UUID1.upper(),
    "../../etc/passwd",
    "$(touch /tmp/pwn)",
    "`id`",
    UUID1 + " ",
    " " + UUID1,
])
def test_abrir_inyeccion_en_session_id_nunca_llega_a_osascript(srv, procs, malo):
    poner_tarea(srv, sid=malo)
    for destino in ("terminal", "antigravity"):
        msg = servidor.abrir_sesion(destino, "abc123")
        assert "forma esperada" in msg
    assert procs == []


def test_abrir_inyeccion_via_estado_jarvis(srv, procs):
    (srv.tmp / "estado.json").write_text(json.dumps({"session_id": 'x"; do shell script "rm'}))
    msg = servidor.abrir_sesion("terminal", "jarvis")
    assert "forma esperada" in msg and procs == []


def test_abrir_inyeccion_via_bloque_del_modelo(srv, monkeypatch, procs):
    """El modelo no puede meter comillas en el nombre de sesión: el bloque ni siquiera matchea."""
    monkeypatch.setattr(servidor, "claude_completo",
                        fake_cerebro('Va.\n<<<ABRIR terminal x"; do shell script "rm>>>'))
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "abrí"})
    assert st == 200 and procs == []


def test_abrir_tarea_desconocida_no_llama_subprocess(srv, procs):
    poner_tarea(srv)
    msg = servidor.abrir_sesion("terminal", "zzzzzz")
    assert "No conozco la sesión" in msg and "zzzzzz" in msg and procs == []


def test_abrir_tarea_sin_sid_todavia(srv, procs):
    poner_tarea(srv, sid=None, estado_="corriendo")
    msg = servidor.abrir_sesion("terminal", "abc123")
    assert "todavía no tiene id" in msg and procs == []


def test_abrir_jarvis_sin_sesion_guardada(srv, procs):
    msg = servidor.abrir_sesion("terminal", "jarvis")
    assert "todavía no tiene id" in msg and procs == []


def test_abrir_antigravity_llama_open_y_pbcopy(srv, procs):
    poner_tarea(srv)
    msg = servidor.abrir_sesion("antigravity", "abc123")
    assert "Antigravity" in msg and len(procs) == 2
    assert procs[0]["args"][0] == "/usr/bin/open" and "Antigravity IDE" in procs[0]["args"]
    assert procs[1]["args"] == ["/usr/bin/pbcopy"]
    assert procs[1]["input"] == f"cd /Users/Facu/facu-os && /Users/Facu/.local/node/bin/claude --resume {UUID1}"


def test_abrir_antigravity_nueva_copia_comando_sin_resume(srv, procs):
    servidor.abrir_sesion("antigravity", "nueva")
    assert procs[1]["input"] == "cd /Users/Facu/facu-os && /Users/Facu/.local/node/bin/claude"


def test_abrir_si_osascript_falla_devuelve_mensaje(srv, monkeypatch):
    def f(*a, **k):
        raise servidor.subprocess.CalledProcessError(1, "osascript")
    monkeypatch.setattr(servidor.subprocess, "run", f)
    msg = servidor.abrir_sesion("terminal", "nueva")
    assert msg.startswith("No pude abrir la sesión")


def test_api_abrir_destino_malo_400(srv, procs):
    for d in ("firefox", None, "", "Terminal"):
        st, raw = req(srv, "POST", "/api/abrir", {"destino": d, "sesion": "nueva"})
        assert st == 400, d
    assert procs == []


def test_api_abrir_terminal_ok(srv, procs):
    poner_tarea(srv)
    st, raw = req(srv, "POST", "/api/abrir", {"destino": "terminal", "sesion": "abc123"})
    assert st == 200 and "Terminal" in js(raw)["respuesta"]
    assert f"--resume {UUID1}" in " ".join(procs[0]["args"])


def test_api_abrir_sin_sesion_es_nueva(srv, procs):
    st, raw = req(srv, "POST", "/api/abrir", {"destino": "terminal"})
    assert st == 200 and "--resume" not in " ".join(procs[0]["args"])


def test_api_abrir_sesion_inyectada_no_llega(srv, procs):
    st, raw = req(srv, "POST", "/api/abrir", {"destino": "terminal", "sesion": 'x"; do shell script "rm'})
    assert st == 200 and "No conozco" in js(raw)["respuesta"] and procs == []


def test_api_abrir_sin_token_403(srv, procs):
    st, _ = req(srv, "POST", "/api/abrir", {"destino": "terminal"}, token=False)
    assert st == 403 and procs == []


def test_bloque_abrir_en_respuesta_ejecuta_y_suma_aviso(srv, monkeypatch, procs):
    poner_tarea(srv)
    monkeypatch.setattr(servidor, "claude_completo",
                        fake_cerebro("Ahí va.\n<<<ABRIR terminal abc123>>>"))
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "abrime la tarea"})
    d = js(raw)
    assert "Ahí va." in d["respuesta"] and "Terminal" in d["respuesta"] and "<<<" not in d["respuesta"]
    assert f"--resume {UUID1}" in " ".join(procs[0]["args"])


# --- /api/estado y /api/numeros ------------------------------------------------------------------

def test_api_estado_vacio(srv):
    st, raw = req(srv, "GET", "/api/estado")
    d = js(raw)
    assert st == 200 and d["conversacion"] == [] and d["tareas"] == [] and d["plan"] is None
    assert d["modo_cambios"] is False and d["sesion"] is None


def test_api_estado_completo(srv, monkeypatch):
    monkeypatch.setenv("TELEGRAM_MODO_CAMBIOS", "1")
    (srv.tmp / "estado.json").write_text(json.dumps({
        "session_id": "s", "conversacion": [{"quien": "facu", "texto": "hola", "ts": 1}],
        "plan": {"id": "p1", "texto": "hacer cosa", "ts": time.time()}}))
    (srv.tmp / "tareas.json").write_text(json.dumps([
        {"id": "t1", "titulo": "T", "estado": "lista", "pedido": "SECRETO-INTERNO", "session_id": UUID1,
         "resultado": "r", "para_decir": "d", "audio": "a.ogg", "visto": False, "inicio": 1, "fin": 2}]))
    st, raw = req(srv, "GET", "/api/estado")
    d = js(raw)
    assert st == 200
    assert d["conversacion"][0]["texto"] == "hola"
    assert d["plan"] == {"id": "p1", "texto": "hacer cosa"}       # sin ts
    assert d["tareas"][0]["id"] == "t1" and d["tareas"][0]["session_id"] == UUID1
    assert "pedido" not in d["tareas"][0]
    assert d["sesion"] == "s" and d["modo_cambios"] is True


def test_api_estado_sin_token_403(srv):
    st, _ = req(srv, "GET", "/api/estado", token=False)
    assert st == 403


def test_api_numeros_sin_archivo_404(srv):
    st, raw = req(srv, "GET", "/api/numeros")
    assert st == 404 and "error" in js(raw)


def test_api_numeros_con_archivo_200(srv):
    datos = {"generado": "2026-11-11T09:30:00-03:00", "numeros": {"Paseo Nordelta": {"x": 1}}}
    (srv.tmp / "numeros.json").write_text(json.dumps(datos))
    st, raw = req(srv, "GET", "/api/numeros")
    assert st == 200 and js(raw) == datos


def test_api_numeros_sin_token_403(srv):
    (srv.tmp / "numeros.json").write_text('{"a": 1}')
    st, _ = req(srv, "GET", "/api/numeros", token=False)
    assert st == 403


# --- conversación ------------------------------------------------------------------------------

def test_conversacion_se_registra_en_orden(srv, monkeypatch):
    monkeypatch.setattr(servidor, "claude_completo", fake_cerebro("Respuesta ñandú."))
    req(srv, "POST", "/api/preguntar", {"texto": "pregunta"})
    c = estado(srv)["conversacion"]
    assert [(x["quien"], x["texto"]) for x in c] == [("facu", "pregunta"), ("jarvis", "Respuesta ñandú.")]


def test_conversacion_capada_a_max(srv):
    for i in range(servidor.MAX_CONVERSACION + 15):
        servidor.anotar("facu", f"m{i}")
    c = estado(srv)["conversacion"]
    assert len(c) == servidor.MAX_CONVERSACION
    assert c[-1]["texto"] == f"m{servidor.MAX_CONVERSACION + 14}" and c[0]["texto"] == "m15"


def test_conversacion_capada_via_preguntar_conserva_session(srv, monkeypatch):
    monkeypatch.setattr(servidor, "claude_completo", fake_cerebro("ok"))
    for i in range(servidor.MAX_CONVERSACION):
        req(srv, "POST", "/api/preguntar", {"texto": f"p{i}"})
    e = estado(srv)
    assert len(e["conversacion"]) == servidor.MAX_CONVERSACION and e["session_id"] == "sess-1"


def test_nuevo_borra_sesion_y_conversacion_pero_no_plan(srv):
    poner_plan(srv)
    servidor.anotar("facu", "hola")
    st, raw = req(srv, "POST", "/api/nuevo", {})
    assert js(raw) == {"ok": True}
    assert "session_id" not in estado(srv) and estado(srv)["conversacion"] == []
    assert estado(srv)["plan"]["id"] == "plan123"


# --- plan --------------------------------------------------------------------------------------

def poner_plan(srv, edad=0, pid="plan123"):
    (srv.tmp / "estado.json").write_text(json.dumps(
        {"session_id": "s", "plan": {"id": pid, "texto": "hacer cosa", "ts": time.time() - edad}}))


def test_plan_si_ejecuta_una_sola_vez(srv, monkeypatch):
    monkeypatch.setenv("TELEGRAM_MODO_CAMBIOS", "1")
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_plan("hecho", llamadas=ll))
    poner_plan(srv)
    st1, r1 = req(srv, "POST", "/api/plan", {"id": "plan123", "si": True})
    st2, r2 = req(srv, "POST", "/api/plan", {"id": "plan123", "si": True})
    assert js(r1)["respuesta"] == "hecho"
    assert "ya no está" in js(r2)["respuesta"]
    assert len(ll) == 1 and ll[0]["ejecutar"] is True
    assert "hacer cosa" in ll[0]["texto"] and ll[0]["sid"] is None
    assert "plan" not in estado(srv)
    quienes = [(x["quien"], x["texto"]) for x in estado(srv)["conversacion"]]
    assert ("jarvis", "hecho") in quienes


def test_plan_no_usa_el_cerebro_de_charla(srv, monkeypatch):
    monkeypatch.setenv("TELEGRAM_MODO_CAMBIOS", "1")
    monkeypatch.setattr(tb, "_correr_claude", fake_plan("hecho"))
    poner_plan(srv)
    req(srv, "POST", "/api/plan", {"id": "plan123", "si": True})   # claude_completo es no_real: fallaría


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
    monkeypatch.setattr(tb, "_correr_claude", fake_plan("no debería", llamadas=ll))
    poner_plan(srv)
    st, raw = req(srv, "POST", "/api/plan", {"id": "plan123", "si": True})
    assert "apagado" in js(raw)["respuesta"]
    assert ll == []
    assert estado(srv)["plan"]["id"] == "plan123"      # sigue ahí


@pytest.mark.parametrize("valor", ["0", "", "true", "yes"])
def test_plan_modo_cambios_solo_con_1(srv, monkeypatch, valor):
    monkeypatch.setenv("TELEGRAM_MODO_CAMBIOS", valor)
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_plan("x", llamadas=ll))
    poner_plan(srv)
    req(srv, "POST", "/api/plan", {"id": "plan123", "si": True})
    assert ll == []


def test_plan_vencido_no_se_ejecuta(srv, monkeypatch):
    monkeypatch.setenv("TELEGRAM_MODO_CAMBIOS", "1")
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_plan("x", llamadas=ll))
    poner_plan(srv, edad=tb.VENCE_PLAN + 60)
    st, raw = req(srv, "POST", "/api/plan", {"id": "plan123", "si": True})
    assert "más de dos horas" in js(raw)["respuesta"]
    assert ll == [] and "plan" not in estado(srv)


def test_plan_id_equivocado_no_ejecuta(srv, monkeypatch):
    monkeypatch.setenv("TELEGRAM_MODO_CAMBIOS", "1")
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_plan("x", llamadas=ll))
    poner_plan(srv)
    st, raw = req(srv, "POST", "/api/plan", {"id": "otro", "si": True})
    assert "ya no está" in js(raw)["respuesta"] and ll == []
    assert estado(srv)["plan"]["id"] == "plan123"


def test_plan_no_descarta(srv, monkeypatch):
    ll = []
    monkeypatch.setattr(tb, "_correr_claude", fake_plan("x", llamadas=ll))
    poner_plan(srv)
    st, raw = req(srv, "POST", "/api/plan", {"id": "plan123", "si": False})
    assert js(raw)["respuesta"] == "Descartado."
    assert "plan" not in estado(srv) and estado(srv)["session_id"] == "s" and ll == []


def test_plan_no_con_id_ajeno_no_descarta(srv):
    poner_plan(srv)
    req(srv, "POST", "/api/plan", {"id": "otro", "si": False})
    assert estado(srv)["plan"]["id"] == "plan123"


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
            "en_curso_total": 1500000, "sin_dato": [], "al_dia": 5, "con_regla": 1,
            "movimientos_leidos": 7, "fuente": "Ctas Ctes · pestañas por local"}


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


# ---------------- arreglos de la revisión v2 (11/11/2026) ----------------

class _ProcFalso:
    def __init__(self, salida):
        self.pid, self.returncode, self._salida = 424242, 0, salida

    def communicate(self, timeout=None):
        return json.dumps(self._salida), ""


def _capturar_popen(monkeypatch, salida):
    vistos = []

    def popen(cmd, **kw):
        vistos.append(cmd)
        return _ProcFalso(salida)
    monkeypatch.setattr(servidor.subprocess, "Popen", popen)
    return vistos


def test_claude_completo_bloquea_salida_al_mundo(monkeypatch):
    vistos = _capturar_popen(monkeypatch, {"result": "ok", "session_id": "s"})
    servidor.claude_completo("hola", None, "i", "Jarvis", 10)
    cmd = vistos[0]
    i = cmd.index("--disallowedTools")
    bloqueadas = cmd[i + 1:i + 1 + len(servidor.SIN_SALIDA)]
    assert "Bash(*--send*)" in bloqueadas and "mcp__claude_ai_Gmail__send_message" in bloqueadas
    assert cmd[cmd.index("--permission-mode") + 1] == "auto"


def test_claude_completo_respuesta_vacia_es_error(monkeypatch):
    _capturar_popen(monkeypatch, {"result": "   ", "session_id": "s"})
    with pytest.raises(tb.ClaudeFallo):
        servidor.claude_completo("hola", None, "i", "Jarvis", 10)


def test_claude_completo_libera_pid(monkeypatch):
    _capturar_popen(monkeypatch, {"result": "ok", "session_id": "s"})
    servidor.claude_completo("hola", None, "i", "Jarvis", 10)
    assert 424242 not in servidor.PIDS_VIVOS


def test_timeout_no_se_reintenta(srv, monkeypatch):
    servidor.guardar_json(servidor.ESTADO, {"session_id": UUID1})
    llamadas = []

    def cerebro(*a, **kw):
        llamadas.append(a)
        raise servidor.ClaudeTimeout("tardó")
    monkeypatch.setattr(servidor, "claude_completo", cerebro)
    with pytest.raises(servidor.ClaudeTimeout):
        servidor.preguntar("arreglá algo")
    assert len(llamadas) == 1, "un timeout reintentado duplica lo que ya hizo a medias"


def test_para_decir_toma_la_ultima(srv, monkeypatch):
    monkeypatch.setattr(servidor, "claude_completo", lambda *a, **kw: (
        "Reporte. Al final va «PARA DECIR:» como pide la consigna.\nDetalle.\nPARA DECIR: Jefe, listo.", UUID1))
    t = servidor.lanzar_tarea("Prueba", "hacé algo")
    srv.correr_hilos()
    t = json.loads(servidor.TAREAS.read_text())[0]
    assert t["para_decir"] == "Jefe, listo."
    assert "Detalle." in t["resultado"]


def test_paneles_paseo_fuente_atrasada_no_muestra_el_numero():
    # 11/11/2026: la consolidada clavada en jul-26 mostraba deuda vieja como de hoy
    s = ok_paseo() | {"exigible_total": None,
                      "sin_dato": [{"local": "Fabric", "motivo": "fuente atrasada: último período cargado 2026-07"}]}
    items = brief.paneles({"Paseo Nordelta": s})[0]["items"]
    total = [i for i in items if i["etiqueta"] == "Deuda exigible"][0]
    assert total["valor"] == "sin dato" and total["tono"] == "mal"
    assert "Fabric" in total["nota"] and "2026-07" in total["nota"]


def test_paseo_lee_pestanas_y_no_la_consolidada(monkeypatch):
    sys.path.insert(0, "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts")
    import radar_deudores as rd
    import google_auth
    monkeypatch.setattr(google_auth, "bajar_xlsx", lambda *a, **k: None)
    mov = [{"local": "Fabric", "tipo": "cargo", "periodo": (2026, 6), "mes_cobro": (2026, 6), "monto": 5.0}]
    monkeypatch.setattr(rd, "leer_xlsx", lambda x: (mov, {}))
    monkeypatch.setattr(rd, "leer_cuenta_corriente", lambda x: pytest.fail("leyó la consolidada"), raising=False)
    s = brief.paseo()
    assert s["exigible_total"] is None and s["sin_dato"][0]["local"] == "Fabric"


# ---------------- cerebro vivo (stream-json) ----------------

class _StdinFalso:
    def __init__(self): self.escrito = []
    def write(self, x): self.escrito.append(x)
    def flush(self): pass


class _VivoFalso:
    def __init__(self, eventos, codigo=None):
        self.pid, self.stdin, self.stderr = 515151, _StdinFalso(), iter([])
        self.stdout = iter(json.dumps(e) + "\n" for e in eventos)
        self._codigo = codigo
    def poll(self): return self._codigo


def _vivo(monkeypatch, eventos):
    procs = []
    def popen(cmd, **kw):
        procs.append((cmd, _VivoFalso(eventos)))
        return procs[-1][1]
    monkeypatch.setattr(servidor.subprocess, "Popen", popen)
    monkeypatch.setattr(servidor.os, "killpg", lambda *a: None)
    return procs


def test_cerebro_vivo_devuelve_resultado_y_actividad(monkeypatch):
    vistos = []
    procs = _vivo(monkeypatch, [
        {"type": "system", "subtype": "init", "session_id": UUID1},
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "input": {"description": "Consultando la base"}}]}},
        {"type": "result", "subtype": "success", "result": "Son tres, jefe.", "session_id": UUID1}])
    monkeypatch.setattr(servidor, "_describir_herramienta", lambda n, i: vistos.append(n) or "x")
    c = servidor.CerebroVivo()
    r, sid = c.turno("¿cuántos?", None, 30)
    assert (r, sid) == ("Son tres, jefe.", UUID1) and vistos == ["Bash"]
    cmd = procs[0][0]
    assert "--input-format" in cmd and "Bash(*--send*)" in cmd, "el cerebro vivo también lleva la llave de la regla 10"
    assert json.loads(procs[0][1].stdin.escrito[0])["message"]["content"] == "¿cuántos?"


def test_cerebro_vivo_resultado_vacio_es_error(monkeypatch):
    _vivo(monkeypatch, [{"type": "result", "subtype": "success", "result": "  "}])
    with pytest.raises(tb.ClaudeFallo):
        servidor.CerebroVivo().turno("hola", None, 30)


def test_cerebro_vivo_proceso_muerto_es_error(monkeypatch):
    _vivo(monkeypatch, [{"type": "system", "subtype": "init"}])   # se cierra sin resultado
    with pytest.raises(tb.ClaudeFallo):
        servidor.CerebroVivo().turno("hola", None, 30)


def test_dictado_reemplaza_lo_que_dijo_por_lo_que_entendio(srv, monkeypatch):
    monkeypatch.setattr(servidor, "claude_completo",
                        lambda *a, **kw: ("ENTENDÍ: cuántos alumnos activos hay\nSon diecinueve, jefe.", UUID1))
    hablado, _, _ = servidor.preguntar("eh… cuántos alumnos, no, mentira, cuántos activos hay", dictado=True)
    assert hablado == "Son diecinueve, jefe."
    conv = json.loads(servidor.ESTADO.read_text())["conversacion"]
    assert conv[-2] == {**conv[-2], "quien": "facu", "texto": "cuántos alumnos activos hay"}


# ---------------- Paseo: efectivo y banco no se cancelan entre sí (12/11/2026) ----------------

def _bigg_mov(tipo, monto, medio, mes_cobro=None):
    x = {"local": "Bigg", "tipo": tipo, "monto": monto, "medio": medio}
    if tipo == "cargo":
        x |= {"periodo": mes_cobro, "mes_cobro": mes_cobro}
    else:
        x["fecha"] = dt.date(2026, 11, 6)
    return x


def test_radar_pago_en_efectivo_no_tapa_deuda_de_banco():
    # Bigg 12/11: ND 11 (recupero sep, banco) $471.465 impaga; el 06/11 pagó $800.000 EN MANO
    # contra la diferencia de nov. El radar los netea y decía exigible $0.
    sys.path.insert(0, "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts")
    import radar_deudores as rd
    movs = [_bigg_mov("cargo", 471_465.66, "banco", (2026, 10)),
            _bigg_mov("cargo", 2_029_303.44, "efectivo", (2026, 11)),
            _bigg_mov("cargo", 3_826_831.42, "banco", (2026, 11)),
            _bigg_mov("pago", 800_000, "efectivo")]
    deudores, *_ = rd.clasificar(movs, (2026, 11))
    assert [n for n, _ in deudores] == ["Bigg"]
    b = deudores[0][1]
    assert round(b["exigible"], 2) == 471_465.66
    assert round(b["medios"]["banco"]["exigible"], 2) == 471_465.66
    assert round(b["medios"]["efectivo"]["en_curso"], 2) == 1_229_303.44
    # invariante: efectivo + banco = saldo de la pestaña
    assert round(b["exigible"] + b["en_curso"], 2) == round(b["saldo"], 2)


def test_radar_excedente_en_efectivo_se_derrama_a_banco():
    # Bigg mar-26: pagó en mano la diferencia Y expensas de banco. El sobrante sí cancela banco.
    sys.path.insert(0, "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts")
    import radar_deudores as rd
    movs = [_bigg_mov("cargo", 1_000_000, "efectivo", (2026, 10)),
            _bigg_mov("cargo", 500_000, "banco", (2026, 10)),
            _bigg_mov("pago", 1_500_000, "efectivo")]
    _, al_dia, *_ = rd.clasificar(movs, (2026, 11))
    assert al_dia and al_dia[0][1]["exigible"] == 0


def test_brief_paseo_separa_efectivo_y_banco(monkeypatch):
    sys.path.insert(0, "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts")
    import radar_deudores as rd
    import google_auth
    hoy = dt.date.today()
    cur = (hoy.year, hoy.month)
    prev = (cur[0] - 1, 12) if cur[1] == 1 else (cur[0], cur[1] - 1)
    movs = [_bigg_mov("cargo", 400_000, "banco", prev),
            _bigg_mov("cargo", 2_000_000, "efectivo", cur),
            _bigg_mov("cargo", 3_000_000, "banco", cur),
            _bigg_mov("pago", 800_000, "efectivo")]
    monkeypatch.setattr(google_auth, "bajar_xlsx", lambda *a, **k: None)
    monkeypatch.setattr(rd, "leer_xlsx", lambda x: (movs, {}))
    s = brief.paseo()
    assert s["exigible_total"] == 400_000
    assert s["deudores"][0] == {"local": "Bigg", "exigible": 400_000, "efectivo": 0,
                                      "banco": 400_000, "por_banco": True}
    ec = s["en_curso"][0]
    assert (ec["efectivo"], ec["banco"], ec["por_banco"]) == (1_200_000, 3_000_000, False)
    nota = [i for i in brief.paneles({"Paseo Nordelta": s})[0]["items"] if i["etiqueta"] == "Bigg"][0]["nota"]
    assert "tránsito" in nota


def test_brief_paseo_pendiente_a_hoy_por_local(monkeypatch):
    # 12/11/2026, Facu: «no importa si es vencido o no: lo que tiene que pagar cada uno; si pagó todo, 0»
    sys.path.insert(0, "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts")
    import radar_deudores as rd
    import google_auth
    hoy = dt.date.today()
    cur = (hoy.year, hoy.month)
    prev = (cur[0] - 1, 12) if cur[1] == 1 else (cur[0], cur[1] - 1)
    movs = [_bigg_mov("cargo", 400_000, "banco", prev),
            _bigg_mov("cargo", 2_000_000, "efectivo", cur),
            _bigg_mov("cargo", 3_000_000, "banco", cur),
            _bigg_mov("pago", 800_000, "efectivo")]
    pagado = [dict(m, local="Boss") for m in (_bigg_mov("cargo", 1_000_000, "efectivo", cur),
                                               _bigg_mov("pago", 1_000_000, "efectivo"))]
    monkeypatch.setattr(google_auth, "bajar_xlsx", lambda *a, **k: None)
    monkeypatch.setattr(rd, "leer_xlsx", lambda x: (movs + pagado, {}))
    s = brief.paseo()
    assert s["pendiente_total"] == 4_600_000 == s["exigible_total"] + s["en_curso_total"]
    bigg, boss = s["por_local"]
    assert (bigg["local"], bigg["debe"], bigg["vencido"], bigg["efectivo"], bigg["banco"]) == \
        ("Bigg", 4_600_000, 400_000, 1_200_000, 3_400_000)
    assert (boss["local"], boss["debe"]) == ("Boss", 0)


# --- «Hey Jarvis» (12/11/2026) ------------------------------------------------------------------

def test_oido_apagado_por_defecto_no_escucha(srv):
    st, raw = req(srv, "POST", "/api/oido", b"\x00\x00" * 4000, ctype="application/octet-stream")
    assert st == 409
    st, raw = req(srv, "GET", "/api/estado")
    assert js(raw)["escucha"] is False


def test_oido_prendido_silencio_no_dispara_y_pedazo_impar_400(srv):
    assert js(req(srv, "POST", "/api/escucha", {"on": True})[1])["escucha"] is True
    assert js(req(srv, "GET", "/api/estado")[1])["escucha"] is True
    st, raw = req(srv, "POST", "/api/oido?nuevo=1", b"\x00\x00" * 8000, ctype="application/octet-stream")
    assert st == 200 and js(raw)["detectado"] is False
    st, _ = req(srv, "POST", "/api/oido", b"\x00" * 3, ctype="application/octet-stream")
    assert st == 400
    req(srv, "POST", "/api/escucha", {"on": False})
    st, _ = req(srv, "POST", "/api/oido", b"\x00\x00" * 4000, ctype="application/octet-stream")
    assert st == 409


def test_oido_detecta_hey_jarvis_en_pedazos(tmp_path):
    # Voz sintética en inglés (la que mejor anda); se manda en pedazos de ¼ s como el panel.
    import imageio_ffmpeg
    aiff = tmp_path / "hj.aiff"
    subprocess.run(["say", "-v", "Samantha", "-o", str(aiff), "Hey Jarvis"], check=True)
    pcm = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "quiet", "-i", str(aiff), "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    audio = b"\x00\x00" * 16000 + pcm + b"\x00\x00" * 16000
    servidor.reiniciar_oido()
    detectado = False
    for i in range(0, len(audio), 8000):
        d, _ = servidor.escuchar_pedazo(audio[i:i + 8000])
        detectado = detectado or d
    assert detectado
    servidor.reiniciar_oido()


# --- Jarvis rápido y conversado (12/11/2026) ----------------------------------------------------

def test_cerebro_vivo_dice_avances_y_no_repite_la_respuesta(monkeypatch):
    anotados = []
    monkeypatch.setattr(servidor, "anotar", lambda q, t, **kw: anotados.append((t, kw)))
    monkeypatch.setattr(servidor, "sintetizar_seguro", lambda t: "a" * 32 + ".mp3")
    monkeypatch.setattr(servidor, "threading", types.SimpleNamespace(
        Thread=lambda target, daemon=True, name=None, **k: types.SimpleNamespace(
            start=(lambda: None) if name == "relleno" else target), Event=threading.Event, Lock=threading.Lock))
    procs = _vivo(monkeypatch, [
        {"type": "system", "subtype": "init", "session_id": UUID1},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "ENTENDÍ: deuda de Bigg\nMe fijo en la pestaña de Bigg…"}]}},
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "input": {}}]}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "Debe cuatrocientos setenta mil, jefe."}]}},
        {"type": "result", "subtype": "success", "result": "Debe cuatrocientos setenta mil, jefe.", "session_id": UUID1}])
    r, _ = servidor.CerebroVivo().turno("¿Bigg?", None, 30)
    assert r == "Debe cuatrocientos setenta mil, jefe."
    assert anotados == [("Me fijo en la pestaña de Bigg…", {"avance": True})], "sólo el texto previo a una herramienta es avance"
    assert [i["texto"] for i in servidor.AVANCES["items"]] == ["Me fijo en la pestaña de Bigg…"]
    assert servidor.AVANCES["items"][0]["audio"]
    cmd = procs[0][0]
    assert cmd[cmd.index("--model") + 1] == servidor.MODELO_CHARLA and "--effort" in cmd


def test_dia_nuevo_arranca_conversacion_con_la_charla_reciente(srv, monkeypatch):
    (srv.tmp / "estado.json").write_text(json.dumps({"session_id": "de-ayer", "sesion_dia": "2000-01-01",
        "conversacion": [{"quien": "facu", "texto": "¿cuánto debe Bigg?", "ts": 1},
                         {"quien": "jarvis", "texto": "Me fijo…", "ts": 2, "avance": True},
                         {"quien": "jarvis", "texto": "Cuatrocientos setenta mil.", "ts": 3}]}))
    vistos = []
    monkeypatch.setattr(servidor, "claude_completo", lambda texto, sid, *a, **k: vistos.append((texto, sid)) or ("De nada, jefe.", UUID1))
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "gracias"})
    texto, sid = vistos[0]
    assert sid is None, "la conversación de ayer no se retoma"
    assert "CHARLA RECIENTE" in texto and "¿cuánto debe Bigg?" in texto and "Cuatrocientos setenta mil." in texto
    assert "Me fijo…" not in texto, "los avances no van a la memoria"
    assert estado(srv)["sesion_dia"] == time.strftime("%Y-%m-%d")


def test_sesion_del_dia_se_retoma_sin_charla_reciente(srv, monkeypatch):
    (srv.tmp / "estado.json").write_text(json.dumps({"session_id": UUID1, "sesion_dia": time.strftime("%Y-%m-%d"),
                                                     "conversacion": [{"quien": "facu", "texto": "hola", "ts": 1}]}))
    vistos = []
    monkeypatch.setattr(servidor, "claude_completo", lambda texto, sid, *a, **k: vistos.append((texto, sid)) or ("ok", UUID1))
    req(srv, "POST", "/api/preguntar", {"texto": "¿y Bigg?"})
    assert vistos[0][1] == UUID1 and "CHARLA RECIENTE" not in vistos[0][0]


def test_mandarme_solo_va_al_mail_de_facu(monkeypatch):
    sys.path.insert(0, "/Users/Facu/facu-os/execution/jarvis")
    import mandarme
    m = mandarme.armar({"area": "paseo", "titulo": "Lo que vimos", "resumen": "x",
                        "para": "otro@ejemplo.com", "to": "otro@ejemplo.com"})
    assert m.asunto.startswith("PASEO")
    with pytest.raises(SystemExit):
        mandarme.armar({"titulo": "vacío"})
    src = open("/Users/Facu/facu-os/execution/jarvis/mandarme.py").read()
    assert 'para = os.environ["MAIL_FACU"]' in src and "argv" not in src.split("para = ")[0].split("def main")[1]


# --- «el trabajando no me dice nada» (12/11/2026) ------------------------------------------------

class _VivoLento(_VivoFalso):
    """Como _VivoFalso pero cada evento tarda: deja ver los rellenos."""
    def __init__(self, eventos, demoras):
        super().__init__(eventos)
        def gen():
            for e, d in zip(eventos, demoras):
                time.sleep(d)
                yield json.dumps(e) + "\n"
        self.stdout = gen()


def test_relleno_cuando_tarda_y_herramienta_sin_aviso(monkeypatch):
    monkeypatch.setattr(servidor, "SEG_PRIMER_RELLENO", 0.5)
    monkeypatch.setattr(servidor, "SEG_ENTRE_RELLENOS", 100)
    monkeypatch.setattr(servidor, "SEG_MIN_ENTRE_AVANCES", 1)
    monkeypatch.setattr(servidor, "anotar", lambda *a, **k: pytest.fail("un relleno no va a la conversación"))
    monkeypatch.setattr(servidor.os, "killpg", lambda *a: None)
    eventos = [{"type": "system", "subtype": "init", "session_id": UUID1},
               {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash",
                                                              "input": {"description": "Count unread", "command": "python -c 'gmail()'"}}]}},
               {"type": "result", "subtype": "success", "result": "Son dieciocho, jefe.", "session_id": UUID1}]
    monkeypatch.setattr(servidor.subprocess, "Popen", lambda cmd, **kw: _VivoLento(eventos, [0, 2.5, 0]))
    r, _ = servidor.CerebroVivo().turno("¿mails?", None, 30)
    textos = [i["texto"] for i in servidor.AVANCES["items"]]
    assert r == "Son dieciocho, jefe."
    assert textos[0] in servidor.RELLENO_PRIMERO, textos
    assert "Me fijo en el mail, jefe." in textos, "la herramienta sin aviso la cuenta el código, en español"


def test_respuesta_rapida_no_lleva_relleno(monkeypatch):
    monkeypatch.setattr(servidor.os, "killpg", lambda *a: None)
    eventos = [{"type": "system", "subtype": "init", "session_id": UUID1},
               {"type": "result", "subtype": "success", "result": "De nada, jefe.", "session_id": UUID1}]
    monkeypatch.setattr(servidor.subprocess, "Popen", lambda cmd, **kw: _VivoLento(eventos, [0, 0.3]))
    servidor.CerebroVivo().turno("ok gracias", None, 30)
    time.sleep(0.2)
    assert servidor.AVANCES["items"] == []


def test_cerebro_lleva_modelo_de_respaldo(monkeypatch):
    procs = _vivo(monkeypatch, [{"type": "result", "subtype": "success", "result": "ok", "session_id": UUID1}])
    servidor.CerebroVivo().turno("hola", None, 30)
    cmd = procs[0][0]
    assert cmd[cmd.index("--fallback-model") + 1] == servidor.MODELO_RESPALDO != servidor.MODELO_CHARLA


def test_tarea_en_stream_avisa_cada_paso(monkeypatch):
    eventos = [{"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Read",
                                                              "input": {"file_path": "/x/facturas.xlsx"}}]}},
               {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "mcp__claude_ai_Gmail__search_threads", "input": {}}]}},
               {"type": "result", "subtype": "success", "result": "PARA DECIR: listo", "session_id": UUID1}]
    vistos = []

    class P(_VivoFalso):
        returncode = 0
        def wait(self): return 0
    monkeypatch.setattr(servidor.subprocess, "Popen", lambda cmd, **kw: vistos.append(cmd) or P(eventos))
    pasos = []
    r, sid = servidor.claude_completo("x", None, "i", "Jarvis", 30, al_paso=pasos.append)
    assert (r, sid) == ("PARA DECIR: listo", UUID1)
    assert pasos == ["leyendo facturas.xlsx", "leyendo mails"]
    assert "stream-json" in vistos[0] and "Bash(*--send*)" in vistos[0]


def test_tarea_en_stream_sin_resultado_es_error(monkeypatch):
    class P(_VivoFalso):
        returncode = 1
        def wait(self): return 1
    monkeypatch.setattr(servidor.subprocess, "Popen", lambda cmd, **kw: P([]))
    with pytest.raises(tb.ClaudeFallo):
        servidor.claude_completo("x", None, "i", "Jarvis", 30, al_paso=lambda p: None)


def test_contexto_trae_reporte_entero_y_paso_en_curso(srv):
    ahora = time.time()
    servidor.guardar_json(servidor.TAREAS, [
        {"id": "aaa111", "titulo": "Facturas", "estado": "lista", "inicio": ahora - 400, "fin": ahora - 60,
         "resultado": "AVN $28.954.654,88 vencido", "para_decir": "Debés 51 millones"},
        {"id": "bbb222", "titulo": "Deudas", "estado": "corriendo", "inicio": ahora - 130, "paso": "leyendo mails", "pasos": 4}])
    c = servidor.contexto_del_dia()
    assert "REPORTE: AVN $28.954.654,88 vencido" in c
    assert "hace 2 min, 4 pasos, ahora: leyendo mails" in c


# --- habla mientras escribe y se lo puede cortar (12/11/2026, «como ChatGPT») ---------------------

def _locutor(trozos):
    dichas = []
    loc = servidor.Locutor(dichas.append)
    loc.nuevo_bloque()
    for t in trozos:
        loc.agregar(t)
    loc.flush()
    return dichas


def test_locutor_dice_por_oracion_y_saltea_entendi():
    assert _locutor(["ENTEN", "DÍ: quiere la deuda\nJefe, hoy le deben veintidós millones. Lo vencido ",
                     "son cuatrocientos mil pesos. ¿Quiere el detalle?"]) == [
        "Jefe, hoy le deben veintidós millones.", "Lo vencido son cuatrocientos mil pesos.", "¿Quiere el detalle?"]


def test_locutor_no_dice_bloques_aunque_lleguen_partidos():
    assert _locutor(["Dale, jefe, lo mando a hacer. <<", "<TAREA Algo\npedido largo\nTA", "REA>>> Le aviso."]) == [
        "Dale, jefe, lo mando a hacer.", "Le aviso."]
    assert _locutor(["ENTENDÍ: sólo esto"]) == []
    assert _locutor(["De nada, jefe."]) == ["De nada, jefe."]
    assert _locutor(["$22.594.386 en total, jefe."]) == ["$22.594.386 en total, jefe."], "un punto de miles no corta"


def _delta(t):
    return {"type": "stream_event", "event": {"type": "content_block_delta", "delta": {"type": "text_delta", "text": t}}}


def test_cerebro_dice_en_vivo_y_no_repite(monkeypatch):
    anotados = []
    monkeypatch.setattr(servidor, "anotar", lambda q, t, **kw: anotados.append((t, kw)))
    monkeypatch.setattr(servidor.os, "killpg", lambda *a: None)
    inicio = {"type": "stream_event", "event": {"type": "content_block_start", "content_block": {"type": "text"}}}
    fin = {"type": "stream_event", "event": {"type": "content_block_stop"}}
    eventos = [{"type": "system", "subtype": "init", "session_id": UUID1},
               inicio, _delta("Me fijo en la pestaña de Bigg, jefe."), fin,
               {"type": "assistant", "message": {"content": [{"type": "text", "text": "Me fijo en la pestaña de Bigg, jefe."}]}},
               {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "input": {}}]}},
               inicio, _delta("Debe cuatrocientos setenta mil pesos. "), _delta("Todo vencido."), fin,
               {"type": "assistant", "message": {"content": [{"type": "text", "text": "Debe cuatrocientos setenta mil pesos. Todo vencido."}]}},
               {"type": "result", "subtype": "success", "result": "Debe cuatrocientos setenta mil pesos. Todo vencido.", "session_id": UUID1}]
    procs = []
    monkeypatch.setattr(servidor.subprocess, "Popen", lambda cmd, **kw: procs.append(cmd) or _VivoFalso(eventos))
    c = servidor.CerebroVivo()
    r, _ = c.turno("¿Bigg?", None, 30)
    assert r.startswith("Debe") and c.en_vivo is True
    assert [i["texto"] for i in servidor.AVANCES["items"]] == [
        "Me fijo en la pestaña de Bigg, jefe.", "Debe cuatrocientos setenta mil pesos.", "Todo vencido."]
    assert anotados == [("Me fijo en la pestaña de Bigg, jefe.", {"avance": True})], "el avance va al feed una sola vez"
    assert "--include-partial-messages" in procs[0]


def test_preguntar_en_vivo_solo_sintetiza_lo_que_agrego_el_codigo(srv, monkeypatch):
    sintetizados = []
    monkeypatch.setattr(servidor, "sintetizar_seguro", lambda t: sintetizados.append(t) or "b" * 32 + ".mp3")
    monkeypatch.setattr(servidor, "claude_completo", fake_cerebro("Son tres, jefe."))
    monkeypatch.setattr(servidor.CEREBRO, "en_vivo", True, raising=False)
    st, raw = req(srv, "POST", "/api/preguntar", {"texto": "¿cuántos?"})
    d = js(raw)
    assert st == 200 and d["en_vivo"] is True and d["audio"] is None and sintetizados == []
    assert d["respuesta"] == "Son tres, jefe."
    monkeypatch.setattr(servidor.CEREBRO, "en_vivo", False, raising=False)
    d = js(req(srv, "POST", "/api/preguntar", {"texto": "¿y ahora?"})[1])
    assert d["audio"] and sintetizados == ["Son tres, jefe."], "sin vivo, se sintetiza entera como antes"


def test_audio_en_stream_con_token_en_la_url(srv, tmp_path, monkeypatch):
    nombre = "c" * 32 + ".mp3"
    (tmp_path / "audio" / nombre).write_bytes(b"ID3" + b"x" * 500)
    listo = threading.Event()
    monkeypatch.setitem(servidor.AUDIO_EN_CURSO, nombre, listo)
    threading.Timer(0.3, lambda: ((tmp_path / "audio" / nombre).open("ab").write(b"y" * 300), listo.set())).start()
    st, raw = req(srv, "GET", f"/api/audio/{nombre}?t={servidor.TOKEN}", token=False)
    assert st == 200 and raw == b"ID3" + b"x" * 500 + b"y" * 300, "lo que se escribió después también llega"
    st, _ = req(srv, "GET", f"/api/audio/{nombre}?t=malo", token=False)
    assert st == 403
    st, _ = req(srv, "GET", f"/api/estado?t={servidor.TOKEN}", token=False)
    assert st == 403, "el token en la URL vale sólo para el audio"


# --- fixes de la revisión del 12/11 -------------------------------------------------------------

def test_locutor_bloque_sin_cerrar_no_se_traga_el_bloque_siguiente():
    dichas = []
    loc = servidor.Locutor(dichas.append)
    loc.nuevo_bloque(); loc.agregar("Va, jefe, lo preparo. <<<PLAN sin cierre"); loc.flush()
    loc.nuevo_bloque(); loc.agregar("Listo, ya quedó preparado."); loc.flush()
    assert dichas == ["Va, jefe, lo preparo.", "Listo, ya quedó preparado."]


def test_oracion_sin_voz_queda_lista_y_no_traba(monkeypatch):
    monkeypatch.setattr(servidor, "sintetizar_en_vivo", lambda t: (_ for _ in ()).throw(RuntimeError("sin red")))
    monkeypatch.setattr(servidor, "threading", types.SimpleNamespace(
        Thread=lambda target, daemon=True, **k: types.SimpleNamespace(start=target), Lock=threading.Lock))
    servidor.AVANCES.update(turno="t", items=[])
    servidor._publicar_avance("Una oración que falla.", al_feed=False, en_vivo=True)
    it = servidor.AVANCES["items"][0]
    assert it["audio"] is None and it["listo"] is True


def test_turno_con_excepcion_rara_apaga_el_proceso(monkeypatch):
    apagados = []
    eventos = [{"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "input": {}}]}}]
    _vivo(monkeypatch, eventos)
    monkeypatch.setattr(servidor, "_describir_herramienta", lambda n, i: 1 / 0)
    c = servidor.CerebroVivo()
    monkeypatch.setattr(c, "apagar", lambda: apagados.append(1))
    with pytest.raises(ZeroDivisionError):
        c.turno("hola", None, 30)
    assert apagados, "un turno roto a la mitad no puede dejar el proceso con eventos sin leer"
