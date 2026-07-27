"""
Tests para /Users/Facu/facu-os/execution/gemini.py

Se corre con el Python del venv del OS:
    /Users/Facu/facu-os/.venv/bin/python -m pytest <este archivo> -v

No hace llamadas reales a la API de Gemini: genai.Client se mockea siempre.
"""
import importlib
import sys
import pathlib
import httpx
import pytest
from google.genai import errors as genai_errors
from unittest.mock import MagicMock, patch

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

import execution.gemini as gemini_module  # noqa: E402


@pytest.fixture
def gem(monkeypatch):
    """Recarga el módulo con un _CLIENTE limpio para cada test.

    _CLIENTE es una global de módulo cacheada entre llamadas a cliente() (es
    justamente el fix que estamos validando), así que si no se resetea acá,
    el primer test que llama a cliente() contamina a todos los que siguen:
    verían el Client ya cacheado en vez de construir uno nuevo. Recargar el
    módulo entero (en vez de solo pisar _CLIENTE = None a mano) también
    reinstancia limpio cualquier otro estado de módulo.
    """
    mod = importlib.reload(gemini_module)
    yield mod
    mod._CLIENTE = None


def _mock_client_cls():
    """Un mock de genai.Client que devuelve una instancia MagicMock nueva
    cada vez que se lo llama, para poder distinguir instancias entre sí."""
    return MagicMock(side_effect=lambda **kwargs: MagicMock(name="client_instance"))


# ---------------------------------------------------------------------------
# 1 y 2: singleton — misma instancia, Client construido una sola vez
# ---------------------------------------------------------------------------

def test_cliente_devuelve_siempre_la_misma_instancia(gem, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "AQ.testkey")
    with patch.object(gem, "genai") as mock_genai:
        mock_genai.Client.side_effect = lambda **kw: MagicMock()
        c1 = gem.cliente()
        c2 = gem.cliente()
        c3 = gem.cliente()
    assert c1 is c2
    assert c2 is c3


def test_genai_client_se_construye_una_sola_vez(gem, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "AQ.testkey")
    with patch.object(gem, "genai") as mock_genai:
        mock_genai.Client.side_effect = lambda **kw: MagicMock()
        gem.cliente()
        gem.cliente()
        gem.cliente()
        assert mock_genai.Client.call_count == 1


# ---------------------------------------------------------------------------
# 3: la key se pasa con .strip() aplicado
# ---------------------------------------------------------------------------

def test_api_key_se_pasa_sin_espacios(gem, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", " AQ.testkey ")
    with patch.object(gem, "genai") as mock_genai:
        mock_genai.Client.side_effect = lambda **kw: MagicMock()
        gem.cliente()
        mock_genai.Client.assert_called_once_with(api_key="AQ.testkey")


# ---------------------------------------------------------------------------
# 4: sin GEMINI_API_KEY -> SystemExit con mensaje util
# ---------------------------------------------------------------------------

def test_cliente_sin_api_key_sale_con_systemexit(gem, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(SystemExit) as exc_info:
        gem.cliente()
    mensaje = str(exc_info.value)
    assert "GEMINI_API_KEY" in mensaje
    assert mensaje.strip() != ""


def test_cliente_con_api_key_vacia_o_solo_espacios_sale_con_systemexit(gem, monkeypatch):
    # Caso borde no listado explícitamente pero cubierto por el mismo `if not key`
    # tras el .strip(): una key de puros espacios debe fallar igual que ausente.
    monkeypatch.setenv("GEMINI_API_KEY", "   ")
    with pytest.raises(SystemExit) as exc_info:
        gem.cliente()
    assert "GEMINI_API_KEY" in str(exc_info.value)


# ---------------------------------------------------------------------------
# 5: sin GEMINI_MODEL -> SystemExit
# ---------------------------------------------------------------------------

def test_modelo_sin_gemini_model_sale_con_systemexit(gem, monkeypatch):
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    with pytest.raises(SystemExit) as exc_info:
        gem.modelo()
    assert "GEMINI_MODEL" in str(exc_info.value)


# ---------------------------------------------------------------------------
# 6: listar_modelos() con lista vacia -> SystemExit (no exito silencioso)
# ---------------------------------------------------------------------------

def test_listar_modelos_lista_vacia_sale_con_systemexit(gem, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "AQ.testkey")
    fake_client = MagicMock()
    fake_client.models.list.return_value = []
    with patch.object(gem, "cliente", return_value=fake_client):
        with pytest.raises(SystemExit) as exc_info:
            gem.listar_modelos()
    mensaje = str(exc_info.value)
    assert "CERO" in mensaje or "cero" in mensaje.lower()


# ---------------------------------------------------------------------------
# 7: listar_modelos() cuando la API tira excepcion -> SystemExit con el
#    mensaje de la excepcion en el texto de salida, sin traceback
# ---------------------------------------------------------------------------

def test_listar_modelos_excepcion_de_api_sale_con_systemexit_y_mensaje(gem, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "AQ.testkey")
    fake_client = MagicMock()
    # Tiene que ser un error REAL de la API, no un RuntimeError generico: el
    # except esta acotado a proposito para no disfrazar bugs propios de
    # respuestas de la API.
    fake_client.models.list.side_effect = genai_errors.ClientError(
        401, {"error": {"message": "UNAUTHENTICATED: bad key", "status": "UNAUTHENTICATED"}}
    )
    with patch.object(gem, "cliente", return_value=fake_client):
        with pytest.raises(SystemExit) as exc_info:
            gem.listar_modelos()
    mensaje = str(exc_info.value)
    assert "UNAUTHENTICATED" in mensaje
    # El SystemExit.code es el string armado a mano por el except, no un
    # objeto traceback ni una excepcion sin procesar.
    assert isinstance(exc_info.value.code, str)


def test_listar_modelos_error_de_red_sale_con_systemexit(gem, monkeypatch):
    """Un timeout o corte de red tambien tiene que dar mensaje limpio."""
    monkeypatch.setenv("GEMINI_API_KEY", "AQ.testkey")
    fake_client = MagicMock()
    fake_client.models.list.side_effect = httpx.ConnectError("no route to host")
    with patch.object(gem, "cliente", return_value=fake_client):
        with pytest.raises(SystemExit) as exc_info:
            gem.listar_modelos()
    assert "no route to host" in str(exc_info.value)


def test_listar_modelos_bug_propio_no_se_disfraza_de_error_de_api(gem, monkeypatch):
    """Un bug del script tiene que reventar con traceback, no salir como 'la API contesto'.

    Es el mismo modo de falla que motivo todo este fix: un error cuyo mensaje
    apunta al lugar equivocado hace perder el tiempo buscando donde no es.
    """
    monkeypatch.setenv("GEMINI_API_KEY", "AQ.testkey")
    fake_client = MagicMock()
    fake_client.models.list.side_effect = AttributeError("typo en el codigo")
    with patch.object(gem, "cliente", return_value=fake_client):
        with pytest.raises(AttributeError):
            gem.listar_modelos()


def test_listar_modelos_sin_generatecontent_sale_con_systemexit(gem, monkeypatch):
    """Lista llena pero filtrada a cero: no puede salir con exito y cero lineas."""
    monkeypatch.setenv("GEMINI_API_KEY", "AQ.testkey")
    solo_embeddings = MagicMock()
    solo_embeddings.name = "models/text-embedding-004"
    solo_embeddings.display_name = "Embeddings"
    solo_embeddings.supported_actions = ["embedContent"]
    fake_client = MagicMock()
    fake_client.models.list.return_value = [solo_embeddings]
    with patch.object(gem, "cliente", return_value=fake_client):
        with pytest.raises(SystemExit) as exc_info:
            gem.listar_modelos()
    assert "NINGUNO soporta generateContent" in str(exc_info.value)


# ---------------------------------------------------------------------------
# 8: leer_imagen() con extension desconocida -> SystemExit
# ---------------------------------------------------------------------------

def test_leer_imagen_extension_desconocida_sale_con_systemexit(gem, monkeypatch, tmp_path):
    monkeypatch.setenv("GEMINI_API_KEY", "AQ.testkey")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-test-model")
    archivo_txt = tmp_path / "nota.txt"
    archivo_txt.write_text("esto no es una imagen")
    with patch.object(gem, "genai") as mock_genai:
        mock_genai.Client.side_effect = lambda **kw: MagicMock()
        with pytest.raises(SystemExit) as exc_info:
            gem.leer_imagen(str(archivo_txt), "que dice esto")
    mensaje = str(exc_info.value)
    assert ".txt" in mensaje


# ---------------------------------------------------------------------------
# Extra: leer_imagen() con una extension valida SI llama a generate_content
# (chequeo de que el happy path sigue mockeado end-to-end, sin red real).
# ---------------------------------------------------------------------------

def test_leer_imagen_extension_valida_no_hace_red_real(gem, monkeypatch, tmp_path):
    monkeypatch.setenv("GEMINI_API_KEY", "AQ.testkey")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-test-model")
    archivo_png = tmp_path / "foto.png"
    archivo_png.write_bytes(b"\x89PNG\r\n\x1a\n")

    fake_response = MagicMock()
    fake_response.text = "resultado mockeado"
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response

    with patch.object(gem, "cliente", return_value=fake_client):
        resultado = gem.leer_imagen(str(archivo_png), "que dice esto")

    assert resultado == "resultado mockeado"
    fake_client.models.generate_content.assert_called_once()
