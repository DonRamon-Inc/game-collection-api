import mock
import jwt
import pytest
import requests

from ..views import jogo_view as jv
from ..models import usuario as u
from ..models import jogo_favorito as jf
from ..models import db
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
    jwt.get_unverified_header = mock.Mock(return_value={"alg": None})
    jwt.decode = mock.Mock(return_value={"sub": None})

    usuario_mock = mock.NonCallableMock(
        steam_id=STEAM_ID,
        jogos_favoritos = mock.NonCallableMock(append = mock.Mock())
    )
    filter_by_result = mock.NonCallableMock(one=mock.Mock(return_value=usuario_mock))
    u.Usuario=mock.NonCallableMock(
        query=mock.NonCallableMock(
            filter_by=mock.Mock(return_value=filter_by_result)
        )
    )
    return usuario_mock

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
def test_favorita_jogo_se_ele_nao_esta_no_banco_de_dados():
    usuario_atual = mock_token_required_decorator()
    id_jogo = "500"
    jogo_favorito_mock = {}
    salvar_mock = mock.Mock()
    novo_jogo_favorito = mock.NonCallableMock(salvar = salvar_mock)
    query_filter_mock = mock.NonCallableMock(first=mock.Mock(return_value=jogo_favorito_mock))
    jf.JogoFavorito = mock.Mock(
        return_value = novo_jogo_favorito,
        query = mock.NonCallableMock(
            filter_by = mock.Mock(return_value=query_filter_mock)
        )
    )

    db.db = mock.NonCallableMock(
        session = mock.NonCallableMock(commit = mock.Mock())
    )
    retorno_api_steam = {id_jogo:
                    {"data":{
                        "name":"nome",
                        "header_image":"header"
                    }}
                }
    requests.get = mock.Mock(
        return_value=mock.NonCallableMock(json=mock.Mock(return_value=retorno_api_steam))
    )

    contexto={"request":create_mock_request(),"id_jogo":id_jogo}
    retorno = js.favoritar_jogo(contexto)

    assert retorno == ({"mensagem": "jogo favoritado com sucesso"}, 201)

    url_request = f"{config.STEAM_STORE_URL}/api/appdetails"
    requests.get.assert_called_once_with(
        url_request, params = {
                "appids": id_jogo,
                "cc": "br",
                "filters": "basic"
            },
            timeout=15
    )

    jf.JogoFavorito.assert_called_once_with(
        {
            "nome": retorno_api_steam[id_jogo]["data"]["name"],
            "steam_id_jogo": id_jogo,
            "url_capa": retorno_api_steam[id_jogo]["data"]["header_image"]
        }
    )

    salvar_mock.assert_called_once()

    jf.JogoFavorito.query.filter_by.assert_called_once_with(
        steam_id_jogo = id_jogo
    )

    usuario_atual.jogos_favoritos.append.assert_called_once_with(
        novo_jogo_favorito
    )

def test_favorita_jogo_se_ele_ja_esta_no_banco_de_dados():
    id_jogo = "500"
    usuario_atual = mock_token_required_decorator()
    novo_jogo_favorito = {"jogo_favorito": "jogo"}
    salvar_mock = mock.Mock()
    query_filter_mock = mock.NonCallableMock(first=mock.Mock(return_value=novo_jogo_favorito))
    jf.JogoFavorito = mock.Mock(
        return_value = mock.NonCallableMock(salvar = salvar_mock),
        query = mock.NonCallableMock(
            filter_by = mock.Mock(return_value=query_filter_mock)
        )
    )

    db.db = mock.NonCallableMock(
        session = mock.NonCallableMock(commit = mock.Mock())
    )

    contexto={"request":create_mock_request(),"id_jogo":id_jogo}
    retorno = js.favoritar_jogo(contexto)

    assert retorno == ({"mensagem": "jogo favoritado com sucesso"}, 201)

    jf.JogoFavorito.query.filter_by.assert_called_with(
        steam_id_jogo = id_jogo
    )

    usuario_atual.jogos_favoritos.append.assert_called_once_with(
        novo_jogo_favorito
    )

def test_desfavoritar_jogo():
    usuario_atual = mock_token_required_decorator()
    id_jogo = "500"
    jogo_favorito = {"jogo_favorito": "jogo"}
    query_filter_mock = mock.NonCallableMock(first=mock.Mock(return_value=jogo_favorito))
    jf.JogoFavorito = mock.Mock(
        return_value = jogo_favorito,
        query = mock.NonCallableMock(
            filter_by = mock.Mock(return_value=query_filter_mock)
        )
    )

    db.db = mock.NonCallableMock(
        session = mock.NonCallableMock(commit = mock.Mock())
    )

    contexto={"request":create_mock_request(),"id_jogo":id_jogo}
    retorno = js.desfavoritar_jogo(contexto)

    assert retorno == ({"mensagem": "jogo desfavoritado com sucesso"}, 202)

    jf.JogoFavorito.query.filter_by.assert_called_once_with(
        steam_id_jogo = id_jogo
    )

    usuario_atual.jogos_favoritos.remove.assert_called_once_with(
        jogo_favorito
    )
