import secrets
import mock
import pytest
from freezegun import freeze_time
from . import usuario_controller as uc
from..models import usuario

@pytest.fixture(autouse=True)
def pre_testes():
    validar_body = uc.validar_body
    validar_parametros_obrigatorios = uc.validar_parametros_obrigatorios
    validar_senha = uc.validar_senha
    validar_email = uc.validar_email
    yield
    uc.validar_body = validar_body
    uc.validar_parametros_obrigatorios=validar_parametros_obrigatorios
    uc.validar_senha = validar_senha
    uc.validar_email = validar_email


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
