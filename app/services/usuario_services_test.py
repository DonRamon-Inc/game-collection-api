import secrets
import mock
import pytest
import jwt

from freezegun import freeze_time
from . import usuario_services as us
from..models import usuario
from ..utils import validacoes as val

@pytest.fixture(autouse=True)
def pre_testes():
    validar_body = val.validar_body
    validar_token = val.validar_token
    token_hex = secrets.token_hex
    jwt_decode = jwt.decode
    jwt_get_unverified_header = jwt.get_unverified_header
    yield
    secrets.token_hex = token_hex
    jwt.decode = jwt_decode
    jwt.get_unverified_header = jwt_get_unverified_header
    val.validar_token = validar_token
    val.validar_body = validar_body


@freeze_time("2022-08-09")
def test_esqueci_senha():
    body ={
        "email": "teste@teste.com",
        "data_nascimento": "2000-01-01"
    }
    usuario_mock = mock.NonCallableMock(
        email = body["email"], data_nascimento = body["data_nascimento"]
    )
    val.validar_body = mock.Mock(return_value=None)
    filter_by_result = mock.NonCallableMock(first=mock.Mock(return_value=usuario_mock))
    request=mock.NonCallableMock(get_json=mock.Mock(return_value=body))
    usuario.Usuario=mock.NonCallableMock(
        query=mock.NonCallableMock(filter_by=mock.Mock(return_value=filter_by_result))
    )
    val.validar_token=mock.Mock(return_value=False)
    secrets.token_hex = mock.Mock(return_value="token")

    resposta=us.validar_usuario(contexto={'request':request})

    assert resposta == ({"token": "token"+"16600032000"}, 201)
    val.validar_body.assert_called_once_with(body,
        ["email", "data_nascimento"],
        [val.validar_data_nascimento]
    )
    val.validar_token.assert_called_once_with(usuario_mock)
    secrets.token_hex.assert_called_once()

def test_auth_steam():
    body = {
        "id" : '137',
        "steam_id": 'teste1'
    }

    request = mock.NonCallableMock(
        get_json=mock.Mock(return_value=body),
        headers=mock.NonCallableMock(get=mock.Mock(return_value='a b'))
    )

    jwt.get_unverified_header = mock.Mock(return_value={'alg':''})

    salvar_mock = mock.Mock()

    jwt.decode = mock.Mock(return_value={'sub':body['id']})
    usuario_mock = mock.NonCallableMock(id=body['id'],steam_id='teste2',salvar=salvar_mock)

    val.validar_body = mock.Mock(return_value=None)

    filter_by_result = mock.NonCallableMock(one=mock.Mock(return_value=usuario_mock))
    usuario.Usuario = mock.NonCallableMock(
        query=mock.Mock(filter_by=mock.Mock(return_value=filter_by_result))
    )

    resposta = us.auth_steam(contexto={'request':request})

    assert resposta[0] ==  {'mensagem': 'ID da Steam registrado'}
    assert resposta[1] == 200
    assert usuario_mock.steam_id == body['steam_id']
    usuario_mock.salvar.assert_called_once()
