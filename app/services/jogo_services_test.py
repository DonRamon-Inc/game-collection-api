import mock
import jwt
import pytest
import requests

from ..views import jogo_view as jv
from ..models import usuario as u
from . import jogo_services as js
from .. import config


@pytest.fixture(autouse=True)
def pre_testes():
    decode = jwt.decode
    get_unverified_headers = jwt.get_unverified_header
    usuario_classe_mock = u.Usuario
    requests_get = requests.get
    serializar_jogos = jv.serializar_jogos
    yield
    jwt.decode = decode
    jwt.get_unverified_header = get_unverified_headers
    u.Usuario = usuario_classe_mock
    requests.get = requests_get
    jv.serializar_jogos = serializar_jogos

STEAM_ID = "123123123"

def create_mock_request(headers = None):
    if not isinstance(headers,dict):
        headers = {"Authorization": "Bearer token"}
    return mock.NonCallableMock(headers=headers)

def mock_token_required_decorator():
    jwt.get_unverified_header = mock.Mock(return_value={'alg': None})
    jwt.decode = mock.Mock(return_value={'sub': None})

    usuario_mock = mock.NonCallableMock(steam_id=STEAM_ID)
    filter_by_result = mock.NonCallableMock(one=mock.Mock(return_value=usuario_mock))
    u.Usuario=mock.NonCallableMock(
        query=mock.NonCallableMock(
            filter_by=mock.Mock(return_value=filter_by_result)
        )
    )

def test_detalhes_jogo():

    mock_token_required_decorator()
    jogo_id = 500

    contexto={"request":create_mock_request(),"jogo_id":jogo_id}

    lista_de_jogos = {
        "response":{
            "games":[{"appid":500},{"appid":367520}]
        }
    }
    parametros_request = {
        "appids": jogo_id,
        "cc":"br",
        "l":"brazilian"
    }
    usuario_possui = True
    resposta_steam_store = None

    js.lista_jogos = mock.Mock(return_value=lista_de_jogos)
    requests.get = mock.Mock(
        return_value=mock.NonCallableMock(json=mock.Mock(return_value=resposta_steam_store))
    )
    jv.serializar_detalhes_jogo = mock.Mock(return_value="Serializado")
    resposta = js.detalhes_jogo(contexto)

    assert resposta == ("Serializado", 200)
    js.lista_jogos.assert_called_once_with(contexto,info_extra=False)
    requests.get.assert_called_once_with(
        f"{config.STEAM_STORE_URL}/api/appdetails", params= parametros_request, timeout=15
    )
    jv.serializar_detalhes_jogo.assert_called_once_with(
        resposta_steam_store, str(jogo_id), usuario_possui
    )

def test_detalhes_jogo_usuario_nao_possui():

    mock_token_required_decorator()
    jogo_id = 500

    contexto={"request":create_mock_request(),"jogo_id":jogo_id}

    lista_de_jogos = {
        "response":{
            "games":[{"appid":70},{"appid":367520}]
        }
    }
    parametros_request = {
        "appids": jogo_id,
        "cc":"br",
        "l":"brazilian"
    }
    usuario_possui = False
    resposta_steam_store = None

    js.lista_jogos = mock.Mock(return_value=lista_de_jogos)
    requests.get = mock.Mock(
        return_value=mock.NonCallableMock(
            json=mock.Mock(return_value=resposta_steam_store)
        )
    )
    jv.serializar_detalhes_jogo = mock.Mock(return_value="Serializado")
    resposta = js.detalhes_jogo(contexto)

    assert resposta == ("Serializado", 200)
    js.lista_jogos.assert_called_once_with(contexto,info_extra=False)
    requests.get.assert_called_once_with(
        f"{config.STEAM_STORE_URL}/api/appdetails",
        params= parametros_request,
        timeout=15
    )
    jv.serializar_detalhes_jogo.assert_called_once_with(
        resposta_steam_store,
        str(jogo_id),
        usuario_possui
    )
