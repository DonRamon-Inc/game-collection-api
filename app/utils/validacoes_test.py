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

def test_validar_senha_deve_rejeitar_senha_abaixo_de_oito_caracteres():
    senha_abaixo_de_oito_caracteres = 'S3nh@'
    body = {'senha' : senha_abaixo_de_oito_caracteres}
    erro = val.validar_senha(body)

    assert erro == 'Senha inválida. Sua senha deve conter entre 8 a 100 caracteres'

def test_validar_senha_deve_rejeitar_acima_de_cem_caracteres():
    senha_acima_de_cem_caracteres = 'SenhaP3rfeit@' * 10
    body = {'senha' : senha_acima_de_cem_caracteres}
    erro = val.validar_senha(body)

    assert erro == 'Senha inválida. Sua senha deve conter entre 8 a 100 caracteres'

def test_validar_senha_deve_rejeitar_senha_sem_letras_minuscula():
    senha_sem_letras_minuscula = 'SEMLETRAM1NUSCUL@'
    body = {'senha' : senha_sem_letras_minuscula}
    erro = val.validar_senha(body)

    assert erro == "Senha inválida. A senha precisa conter, oito ou mais caracteres " +\
                "com uma combinação de letras, números e símbolos"

def test_validar_senha_deve_rejeitar_senha_sem_letras_maiuscula():
    senha_sem_letras_maiuscula = 'semletrasma1uscul@'
    body = {'senha' : senha_sem_letras_maiuscula}
    erro = val.validar_senha(body)

    assert erro == "Senha inválida. A senha precisa conter, oito ou mais caracteres " +\
                "com uma combinação de letras, números e símbolos"

def test_validar_senha_deve_rejeitar_senha_sem_numero():
    senha_sem_numero = 'Sem_Numeros'
    body = {'senha' : senha_sem_numero}
    erro = val.validar_senha(body)

    assert erro == "Senha inválida. A senha precisa conter, oito ou mais caracteres " +\
                "com uma combinação de letras, números e símbolos"

def test_validar_senha_deve_rejeitar_senha_sem_caractere_especial():
    senha_sem_caractere_especial = 'SemCractereEspec1al'
    body = {'senha' : senha_sem_caractere_especial}
    erro = val.validar_senha(body)

    assert erro == "Senha inválida. A senha precisa conter, oito ou mais caracteres " +\
                "com uma combinação de letras, números e símbolos"
