import secrets
import mock
import pytest
import jwt

from freezegun import freeze_time
from . import usuario_controller as uc
from..models import usuario

@pytest.fixture(autouse=True)
def pre_testes():
    validar_body = uc.validar_body
    validar_parametros_obrigatorios = uc.validar_parametros_obrigatorios
    yield
    uc.validar_body = validar_body
    uc.validar_parametros_obrigatorios=validar_parametros_obrigatorios


@freeze_time("2022-08-09")
def test_esqueci_senha():
    body ={
      "email": "teste@teste.com",
      "data_nascimento": "2000-01-01"
    }
    usuario_mock = mock.NonCallableMock(
      email = body["email"], data_nascimento = body["data_nascimento"]
    )
    uc.validar_body = mock.Mock(return_value=None)
    filter_by_result = mock.NonCallableMock(first=mock.Mock(return_value=usuario_mock))
    request=mock.NonCallableMock(get_json=mock.Mock(return_value=body))
    usuario.Usuario=mock.NonCallableMock(
      query=mock.NonCallableMock(filter_by=mock.Mock(return_value=filter_by_result))
    )
    uc.validar_token=mock.Mock(return_value=False)
    secrets.token_hex = mock.Mock(return_value="token")

    resposta=uc.validar_usuario(request)

    assert resposta == ({"token": "token"+"16600032000"}, 201)
    uc.validar_body.assert_called_once_with(body,
      ["email", "data_nascimento"],
      [uc.validar_data_nascimento]
    )
    uc.validar_token.assert_called_once_with(usuario_mock)
    secrets.token_hex.assert_called_once()


def test_validar_body():
    uc.validar_parametros_obrigatorios = mock.Mock(return_value=[])

    validar_email = mock.Mock(return_value=None)
    validar_senha = mock.Mock(return_value=None)

    parametros_obrigatorios = ["nome","senha","email"]

    body = {
        "nome":"Ramon Cos",
        "senha":"123123",
        "email":"123456.com"
    }

    resposta = uc.validar_body(body,parametros_obrigatorios,[validar_email,validar_senha])
    assert resposta is None
    uc.validar_parametros_obrigatorios.assert_called_once_with(body,parametros_obrigatorios)
    validar_email.assert_called_once_with(body)
    validar_senha.assert_called_once_with(body)

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

    uc.validar_body = mock.Mock(return_value=None)

    filter_by_result = mock.NonCallableMock(one=mock.Mock(return_value=usuario_mock))
    usuario.Usuario = mock.NonCallableMock(
        query=mock.Mock(filter_by=mock.Mock(return_value=filter_by_result))
    )

    resposta = uc.auth_steam(request)

    assert resposta[0] ==  {'mensagem': 'ID da Steam registrado'}
    assert resposta[1] == 200
    assert usuario_mock.steam_id == body['steam_id']
    usuario_mock.salvar.assert_called_once()


