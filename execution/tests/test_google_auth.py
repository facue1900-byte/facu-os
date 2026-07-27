"""
Tests para /Users/Facu/facu-os/execution/google_auth.py

Se corre con el Python del venv del OS:
    /Users/Facu/facu-os/.venv/bin/python -m pytest <este archivo> -v

Nada de red ni de navegador: InstalledAppFlow, build() y los servicios de Google
se mockean siempre. RAIZ y CREDENCIALES se monkeypatchean a un tmp_path por test,
así que nunca se lee ni se escribe un token-*.json o credentials.json real.
"""
import datetime
import importlib
import json
import sys
import pathlib
import pytest
from unittest.mock import MagicMock, patch

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

import execution.google_auth as google_auth_module  # noqa: E402


@pytest.fixture
def ga(monkeypatch, tmp_path):
    """Recarga el módulo y le apunta RAIZ/CREDENCIALES a un tmp_path aislado.

    RAIZ y CREDENCIALES son globals de módulo leídas en cada llamada (no se
    congelan en tiempo de import), así que monkeypatchearlas alcanza para que
    token_de(), credenciales() y _cuenta_con_email() operen enteramente sobre
    el directorio temporal. El repo real nunca se toca.
    """
    mod = importlib.reload(google_auth_module)
    monkeypatch.setattr(mod, "RAIZ", tmp_path)
    monkeypatch.setattr(mod, "CREDENCIALES", tmp_path / "credentials.json")
    yield mod


def _token_dict(token="tok", refresh="ref", client_id="cid", client_secret="csecret",
                scopes=None, expiry_iso=None):
    """Un token-<cuenta>.json parseable de verdad por Credentials.from_authorized_user_file.

    Sin `expiry` explícito la librería no lo interpreta como "sin vencimiento":
    queda `valid=False`. Por eso siempre mandamos uno, por default bien a futuro.
    """
    if expiry_iso is None:
        expiry_iso = (
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
        ).isoformat("T") + "Z"
    return {
        "token": token,
        "refresh_token": refresh,
        "client_id": client_id,
        "client_secret": client_secret,
        "scopes": scopes or ["https://www.googleapis.com/auth/spreadsheets"],
        "expiry": expiry_iso,
    }


# ---------------------------------------------------------------------------
# 1: regresión del bug de identidad — el flow de setup tiene que forzar el
#    selector de cuenta. Sin prompt="select_account" Google reusa la sesión
#    abierta y el login "miente en silencio" guardando la cuenta equivocada.
# ---------------------------------------------------------------------------

def test_setup_llama_al_flow_con_prompt_select_account(ga, tmp_path):
    mod = ga
    (tmp_path / "credentials.json").write_text('{"installed": {}}')

    fake_creds_nuevo = MagicMock(name="creds_del_login")
    fake_creds_nuevo.to_json.return_value = json.dumps(_token_dict(token="nuevo"))

    mock_flow = MagicMock()
    mock_flow.run_local_server.return_value = fake_creds_nuevo

    with patch.object(mod, "InstalledAppFlow") as mock_flow_cls, \
            patch.object(mod, "_email_de", return_value="facu@gmail.com"):
        mock_flow_cls.from_client_secrets_file.return_value = mock_flow
        mod.credenciales("facu", interactivo=True)

    mock_flow.run_local_server.assert_called_once_with(port=0, prompt="select_account")


# ---------------------------------------------------------------------------
# 2: regresión completa del bug real — si el mail que devuelve la API ya está
#    guardado bajo OTRA cuenta, no se guarda el token nuevo. Corre la lógica
#    real de _cuenta_con_email() (no se mockea), solo se mockea _email_de
#    (que pega contra Gmail) y el flow (que abre navegador).
# ---------------------------------------------------------------------------

def test_credenciales_no_guarda_el_token_si_el_mail_ya_es_de_otra_cuenta(ga, tmp_path):
    mod = ga
    (tmp_path / "credentials.json").write_text('{"installed": {}}')
    # "studio" ya está autorizada con un mail. El bug: pedís --setup --cuenta
    # facu, el navegador reusa la sesión de studio, y sin el fix se guardaría
    # igual como token-facu.json.
    (tmp_path / "token-studio.json").write_text(json.dumps(_token_dict(token="tok_studio")))

    fake_creds_nuevo = MagicMock(name="creds_del_login_que_reusa_sesion")
    fake_creds_nuevo.to_json.return_value = json.dumps(_token_dict(token="nuevo"))

    mock_flow = MagicMock()
    mock_flow.run_local_server.return_value = fake_creds_nuevo

    # _email_de mockeado para devolver siempre el mismo mail, tanto para el
    # token-studio.json ya guardado en disco como para el login recién hecho:
    # es exactamente el escenario del bug, la misma persona autorizando dos
    # veces sin que el selector apareciera.
    with patch.object(mod, "InstalledAppFlow") as mock_flow_cls, \
            patch.object(mod, "_email_de", return_value="misma.persona@gmail.com"):
        mock_flow_cls.from_client_secrets_file.return_value = mock_flow
        with pytest.raises(SystemExit) as exc_info:
            mod.credenciales("facu", interactivo=True)

    mensaje = str(exc_info.value)
    assert "studio" in mensaje
    assert "misma.persona@gmail.com" in mensaje
    # Lo que importa: NUNCA se escribió token-facu.json.
    assert not (tmp_path / "token-facu.json").exists()


def test_cuenta_con_email_detecta_el_mail_duplicado_en_otro_token(ga, tmp_path):
    """Unidad de _cuenta_con_email(): sin mockearla, solo _email_de."""
    mod = ga
    (tmp_path / "token-studio.json").write_text(json.dumps(_token_dict(token="tok_studio")))
    (tmp_path / "token-facu.json").write_text(json.dumps(_token_dict(token="tok_facu")))

    email_por_token = {"tok_studio": "estudio@empresa.com", "tok_facu": "facu@personal.com"}

    def fake_email_de(creds):
        return email_por_token[creds.token]

    with patch.object(mod, "_email_de", side_effect=fake_email_de):
        resultado = mod._cuenta_con_email("estudio@empresa.com", excepto="nueva_cuenta")

    assert resultado == "studio"


def test_cuenta_con_email_excluye_la_propia_cuenta_via_excepto(ga, tmp_path):
    """Si el mail coincide con el token de la MISMA cuenta que se está pidiendo,
    no es un conflicto — `excepto` tiene que filtrarlo."""
    mod = ga
    (tmp_path / "token-facu.json").write_text(json.dumps(_token_dict(token="tok_facu")))

    with patch.object(mod, "_email_de", return_value="facu@personal.com"):
        resultado = mod._cuenta_con_email("facu@personal.com", excepto="facu")

    assert resultado is None


# ---------------------------------------------------------------------------
# 3: cada cuenta lee su propio token-<cuenta>.json, nunca el de otra.
# ---------------------------------------------------------------------------

def test_cada_cuenta_lee_su_propio_token_y_no_el_de_otra(ga, tmp_path):
    mod = ga
    (tmp_path / "token-facu.json").write_text(json.dumps(_token_dict(token="TOKEN_FACU")))
    (tmp_path / "token-studio.json").write_text(json.dumps(_token_dict(token="TOKEN_STUDIO")))

    creds_facu = mod.credenciales("facu")
    creds_studio = mod.credenciales("studio")

    assert creds_facu.token == "TOKEN_FACU"
    assert creds_studio.token == "TOKEN_STUDIO"


def test_cuentas_configuradas_lista_solo_los_token_ordenados(ga, tmp_path):
    mod = ga
    (tmp_path / "token-studio.json").write_text("{}")
    (tmp_path / "token-facu.json").write_text("{}")
    (tmp_path / "credentials.json").write_text("{}")  # no es un token, no debe aparecer

    assert mod.cuentas_configuradas() == ["facu", "studio"]


# ---------------------------------------------------------------------------
# 4: sin credentials.json falla con mensaje claro, no traceback críptico.
# ---------------------------------------------------------------------------

def test_credenciales_sin_credentials_json_sale_con_mensaje_claro(ga, tmp_path):
    mod = ga
    # Ni token ni credentials.json en el tmp_path.
    with pytest.raises(SystemExit) as exc_info:
        mod.credenciales("facu", interactivo=True)

    mensaje = str(exc_info.value)
    assert "credentials.json" in mensaje
    # El mensaje es el string armado a mano por el sys.exit(), no una excepción
    # sin procesar ni un traceback.
    assert isinstance(exc_info.value.code, str)


def test_credenciales_no_interactivo_sin_token_no_cuelga_sale_con_systemexit(ga, tmp_path):
    """Simula correr desde launchd/cron: sin terminal, sin token, no puede
    quedarse esperando un click que nunca llega — tiene que cortar."""
    mod = ga
    with patch.object(mod, "InstalledAppFlow") as mock_flow_cls:
        with pytest.raises(SystemExit) as exc_info:
            mod.credenciales("facu", interactivo=False)
        mock_flow_cls.from_client_secrets_file.assert_not_called()

    mensaje = str(exc_info.value)
    assert "facu" in mensaje
    assert "--setup" in mensaje


def test_credenciales_refresca_token_expirado_sin_abrir_navegador(ga, tmp_path):
    """Token vencido pero con refresh_token: se refresca y se persiste, sin
    pasar por el flow interactivo."""
    mod = ga
    vencido = _token_dict(token="TOKEN_VIEJO", expiry_iso="2000-01-01T00:00:00Z")
    (tmp_path / "token-facu.json").write_text(json.dumps(vencido))

    def fake_refresh(self, request):
        self.token = "TOKEN_REFRESCADO"
        self.expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)

    with patch.object(mod.Credentials, "refresh", fake_refresh), \
            patch.object(mod, "InstalledAppFlow") as mock_flow_cls:
        resultado = mod.credenciales("facu", interactivo=True)

    assert resultado.token == "TOKEN_REFRESCADO"
    mock_flow_cls.from_client_secrets_file.assert_not_called()
    guardado = json.loads((tmp_path / "token-facu.json").read_text())
    assert guardado["token"] == "TOKEN_REFRESCADO"


# ---------------------------------------------------------------------------
# 5: bajar_xlsx() escribe el archivo pedido, usando export (no get_media,
#    que trunca hojas largas — ver docstring del código fuente).
# ---------------------------------------------------------------------------

def test_bajar_xlsx_escribe_el_archivo_pedido(ga, tmp_path):
    mod = ga
    destino = tmp_path / "salida.xlsx"
    contenido_falso = b"PK\x03\x04contenido de un xlsx falso"

    fake_drive_service = MagicMock()
    fake_drive_service.files.return_value.export.return_value.execute.return_value = (
        contenido_falso
    )

    with patch.object(mod, "drive", return_value=fake_drive_service) as mock_drive:
        resultado = mod.bajar_xlsx("id_del_sheet_123", str(destino), cuenta="facu")

    mock_drive.assert_called_once_with("facu")
    fake_drive_service.files.return_value.export.assert_called_once_with(
        fileId="id_del_sheet_123",
        mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    assert resultado == destino
    assert destino.read_bytes() == contenido_falso


def test_bajar_xlsx_usa_la_cuenta_pedida_no_el_default(ga, tmp_path):
    """Si se pide bajar con la cuenta 'studio', drive() tiene que llamarse con
    'studio', no con el CUENTA_DEFAULT ('facu')."""
    mod = ga
    destino = tmp_path / "otra_salida.xlsx"
    fake_drive_service = MagicMock()
    fake_drive_service.files.return_value.export.return_value.execute.return_value = b"x"

    with patch.object(mod, "drive", return_value=fake_drive_service) as mock_drive:
        mod.bajar_xlsx("otro_id", str(destino), cuenta="studio")

    mock_drive.assert_called_once_with("studio")
