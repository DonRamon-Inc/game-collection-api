import mock
import pytest

from . import validacoes as val

@pytest.fixture(autouse=True)
def pre_testes():
    validar_parametros_obrigatorios = val.validar_parametros_obrigatorios
    yield
    val.validar_parametros_obrigatorios = validar_parametros_obrigatorios

def test_validar_body():
    val.validar_parametros_obrigatorios = mock.Mock(return_value=[])

    validar_email = mock.Mock(return_value=None)
    validar_senha = mock.Mock(return_value=None)

    parametros_obrigatorios = ["nome","senha","email"]

    body = {
        "nome":"Ramon Cos",
        "senha":"123123",
        "email":"123456.com"
    }

    resposta = val.validar_body(body,parametros_obrigatorios,[validar_email,validar_senha])
    assert resposta is None
    val.validar_parametros_obrigatorios.assert_called_once_with(body,parametros_obrigatorios)
    validar_email.assert_called_once_with(body)
    validar_senha.assert_called_once_with(body)
