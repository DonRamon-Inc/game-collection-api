import pytest
import mock
import jwt

from sqlalchemy import exc as sql_exc

from . import auth
from .. import config
from ..models import usuario as u

@pytest.fixture(autouse=True)
def pre_testes():
    decode = jwt.decode
    get_unverified_header = jwt.get_unverified_header
    filter_usuario_by = u.Usuario.query.filter_by
    yield
    jwt.decode = decode
    jwt.get_unverified_header = get_unverified_header
    u.Usuario.query.filter_by = filter_usuario_by

def create_mock_request(headers):
    return mock.NonCallableMock(headers=headers)

def test_token_required_adiciona_o_usuario_atual_no_contexto():
    @auth.token_required
    def mock_function(contexto):
        return contexto

    jwt.get_unverified_header = mock.Mock(return_value={'alg': 'HS256'})
    usuario_id = 99
    jwt.decode = mock.Mock(return_value={'sub': usuario_id})
    usuario_mock = {'nome': 'Usuario Mock'}
    u.Usuario.query.filter_by = mock.Mock(
        return_value=mock.NonCallableMock(
            one=mock.Mock(return_value=usuario_mock)
        )
    )

    mock_request = create_mock_request({'Authorization': 'Bearer token'})

    contexto_resultado = mock_function({'request': mock_request})

    jwt.get_unverified_header.assert_called_once_with('token')
    jwt.decode.assert_called_once_with('token', config.SECRET_KEY, algorithms=['HS256'])
    u.Usuario.query.filter_by.assert_called_once_with(id=usuario_id)
    assert contexto_resultado.get('usuario') is usuario_mock

def test_token_required_retorna_erro_caso_usuario_nao_seja_encontrado():
    @auth.token_required
    def mock_function(contexto):
        return contexto

    jwt.get_unverified_header = mock.Mock(return_value={'alg': 'HS256'})
    usuario_id = 99
    jwt.decode = mock.Mock(return_value={'sub': usuario_id})
    u.Usuario.query.filter_by = mock.Mock(
        return_value=mock.NonCallableMock(
            one=mock.Mock(side_effect=sql_exc.NoResultFound)
        )
    )

    mock_request = create_mock_request({'Authorization': 'Bearer token'})

    resposta = mock_function({'request': mock_request})

    assert resposta == ({'mensagem': 'Token invalido'}, 401)

def test_token_required_retorna_erro_caso_token_nao_possa_ser_decodificado():
    @auth.token_required
    def mock_function(contexto):
        return contexto

    jwt.get_unverified_header = mock.Mock(return_value={'alg': 'HS256'})
    jwt.decode = mock.Mock(side_effect=jwt.DecodeError)
    mock_request = create_mock_request({'Authorization': 'Bearer token'})

    resposta = mock_function({'request': mock_request})

    assert resposta == ({'mensagem': 'Token invalido'}, 401)

def test_token_required_retorna_erro_caso_token_nao_venha_no_cabecalho():
    @auth.token_required
    def mock_function(contexto):
        return contexto

    jwt.get_unverified_header = mock.Mock(return_value={'alg': 'HS256'})
    mock_request = create_mock_request({'Authorization': 'Bearer '})

    resposta = mock_function({'request': mock_request})

    assert resposta == ({'mensagem': 'Token invalido'}, 401)

def test_token_required_retorna_erro_caso_token_nao_seja_definido_no_cabecalho():
    @auth.token_required
    def mock_function(contexto):
        return contexto

    jwt.get_unverified_header = mock.Mock(return_value={'alg': 'HS256'})
    mock_request = create_mock_request({})

    resposta = mock_function({'request': mock_request})

    assert resposta == ({'mensagem': 'Token não definido'}, 401)
