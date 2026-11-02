"""Formato y frecuencia de los mails automáticos (Facu, 02/11/2026)."""
from datetime import datetime, timedelta, timezone

from execution.avisar import armar, decidir, lineas_clave
from execution.mail_format import AREAS, NIVELES, render

AHORA = datetime(2026, 11, 2, 12, 0, tzinfo=timezone(timedelta(hours=-3)))


def corrida(horas_atras, codigo):
    return {"inicio": (AHORA - timedelta(hours=horas_atras)).strftime("%Y-%m-%dT%H:%M:%S%z"), "codigo": codigo}


def test_el_asunto_arranca_por_el_area_y_el_color():
    for area, nombre in AREAS.items():
        for nivel, datos in NIVELES.items():
            assert render(area=area, nivel=nivel, titulo="X").asunto == f"{nombre} · {datos[0]} X"


def test_lo_que_viene_de_afuera_se_escapa():
    m = render(area="paseo", nivel="urgente", titulo="<b>t</b>", resumen="<script>", kpis=[("<k>", "<v>")],
               accion="<a>", secciones=[("<s>", ["<p>"])], detalle="<d>")
    for crudo in ("<script>", "<b>t</b>", "<k>", "<v>", "<p>", "<d>", "<s>"):
        assert crudo not in m.html


def test_el_mime_lleva_texto_y_html():
    m = render(area="cripto", nivel="bueno", titulo="T", resumen="R").mime("a@b.c")
    assert {p.get_content_type() for p in m.iter_parts()} == {"text/plain", "text/html"}


def test_tarea_diaria_primera_falla_no_manda_mail():
    assert decidir("radar-diario", 1, [corrida(24, 0), corrida(0, 1)], None, AHORA)[0] is False


def test_tarea_diaria_segunda_falla_seguida_manda_mail():
    assert decidir("radar-diario", 1, [corrida(48, 0), corrida(24, 1), corrida(0, 1)], None, AHORA)[0] is True


def test_tarea_semanal_avisa_a_la_primera():
    assert decidir("reporte-pauta", 1, [corrida(168, 0), corrida(0, 1)], None, AHORA)[0] is True


def test_tarea_sin_historia_avisa():
    assert decidir("alerta-rampa", 1, [corrida(0, 1)], None, AHORA)[0] is True


def test_las_criticas_avisan_a_la_primera_aunque_sean_diarias():
    for t in ("chequeo-pauta", "efectivo-diario"):
        assert decidir(t, 1, [corrida(24, 0), corrida(0, 1)], None, AHORA)[0] is True


def test_no_repite_el_mail_antes_de_3_dias_y_despues_si():
    fallas = [corrida(48, 1), corrida(24, 1), corrida(0, 1)]
    assert decidir("radar-diario", 1, fallas, AHORA - timedelta(days=2), AHORA)[0] is False
    assert decidir("radar-diario", 1, fallas, AHORA - timedelta(days=3, minutes=1), AHORA)[0] is True


def test_sin_red_nunca_manda_mail():
    assert decidir("reporte-pauta", 75, [corrida(0, 75)], None, AHORA)[0] is False


def test_la_carpeta_ficticia_nunca_manda_mail_por_falla():
    fallas = [corrida(8, 1), corrida(4, 1), corrida(0, 1)]
    assert decidir("paper-trading", 1, fallas, None, AHORA)[0] is False


def test_sin_log_el_mail_no_muestra_jerga():
    m = armar("reporte-equipo", 1, "")
    assert "código" not in m.texto and "Detalle técnico" not in m.html
    assert "Qué hacer" in m.texto


def test_una_tarea_desconocida_igual_arma_el_mail():
    m = armar("tarea-nueva", 1, "algo\n!!! se rompió esto\n")
    assert m.asunto.startswith("SISTEMA · 🟡")
    assert "se rompió esto" in m.html


def test_lineas_clave_saca_lo_importante_sin_repetir():
    log = "todo bien\nFALLA  no registra\nFALLA  no registra\n!!! frenado\nnormal\n"
    assert lineas_clave(log) == ["FALLA  no registra", "frenado"]
