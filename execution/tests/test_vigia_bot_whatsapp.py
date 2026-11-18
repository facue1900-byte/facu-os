from datetime import datetime, timedelta

from execution.vigia_bot_whatsapp import decidir

T0 = datetime(2026, 11, 18, 17, 56)


def test_sano_no_avisa():
    nuevo, texto = decidir({}, "open", T0)
    assert texto is None and nuevo["estado"] == "open"


def test_se_cae_avisa_una_vez_y_recuerda_a_las_2_horas():
    s, texto = decidir({"estado": "open"}, "close", T0)
    assert texto and "DESCONECTADO" in texto
    s, texto = decidir(s, "close", T0 + timedelta(minutes=10))
    assert texto is None
    s, texto = decidir(s, "close", T0 + timedelta(minutes=110))
    assert texto is None
    s, texto = decidir(s, "close", T0 + timedelta(minutes=121))
    assert texto and "hace 121 min" in texto


def test_vuelve_avisa_cuanto_estuvo_caido():
    s, _ = decidir({}, "close", T0)
    s, texto = decidir(s, "open", T0 + timedelta(minutes=45))
    assert texto and "~45 min" in texto
    assert "caido_desde" not in s
    s, texto = decidir(s, "open", T0 + timedelta(minutes=55))
    assert texto is None


def test_servidor_sin_respuesta_avisa_a_la_segunda():
    s, texto = decidir({"estado": "open"}, None, T0)
    assert texto is None
    s, texto = decidir(s, None, T0 + timedelta(minutes=10))
    assert texto and "no responde" in texto
    s, texto = decidir(s, None, T0 + timedelta(minutes=20))
    assert texto is None  # no repite cada 10 minutos
    s, texto = decidir(s, "open", T0 + timedelta(minutes=30))
    assert s["sin_respuesta"] == 0


def test_caido_sin_respuesta_del_servidor_no_pierde_la_caida():
    s, _ = decidir({}, "close", T0)
    s, _ = decidir(s, None, T0 + timedelta(minutes=10))
    assert s["caido_desde"] == T0.isoformat()
    s, texto = decidir(s, "open", T0 + timedelta(minutes=20))
    assert texto and "volvió" in texto
