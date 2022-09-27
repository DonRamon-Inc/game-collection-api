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

def test_validar_email_deve_aceitar_email_valido():
    email_comum = 'EmailComum@email.com'
    email_comum_com_dominio_de_regiao = 'EmailComum@email.com.br'
    email_comum_com_caractere_especial = 'Ema!l.Co+mum@email.com.br'
    email_comum_com_caractere_especial_e_numero = 'Ema!l.C0+mum@email.com.br'
    emails_validos = [
        email_comum,
        email_comum_com_dominio_de_regiao,
        email_comum_com_caractere_especial,
        email_comum_com_caractere_especial_e_numero
    ]

    for email in emails_validos:
        body = {'email' : email}
        resposta = val.validar_email(body)

        assert resposta is None

def test_validar_email_deve_rejeitar_email_incompleto():
    email_incompleto_dominio_de_topo_incompleto = 'Email.Comum@email.c'
    email_incompleto_codigo_do_pais_incompleto = 'Email.Comum@email.com.b'
    email_incompleto_sem_dominio_de_topo = 'Email.Comum@email'
    email_incompleto_sem_dominio = 'Email.Comum@'

    emails_invalidos = [
        email_incompleto_dominio_de_topo_incompleto,
        email_incompleto_codigo_do_pais_incompleto,
        email_incompleto_sem_dominio_de_topo,
        email_incompleto_sem_dominio
    ]

    for email in emails_invalidos:
        body = {'email' : email}
        resposta = val.validar_email(body)

        assert resposta == "Email invalido, favor verificar email"

def test_validar_email_deve_rejeitar_email_encerrando_com_ponto():
    email_encerrando_com_ponto = 'Email.Comum@email.'
    email_encerrando_com_ponto = 'Email.Comum@email.com.'
    emails_invalidos = [
        email_encerrando_com_ponto,
        email_encerrando_com_ponto
    ]

    for email in emails_invalidos:
        body = {'email' : email}
        resposta = val.validar_email(body)

        assert resposta == "Email invalido, favor verificar email"

def test_validar_email_deve_rejeitar_email_com_dois_ou_mais_arroba():
    email_com_dois_ou_mais_arroba = 'Email@Comum@email.com.br'
    body = {'email' : email_com_dois_ou_mais_arroba}
    resposta = val.validar_email(body)

    assert resposta == "Email invalido, favor verificar email"

def test_validar_email_deve_rejeitar_email_sem_conteudo_antes_do_arroba():
    email_sem_conteudo_antes_do_arroba = '@email.com.br'
    body = {'email' : email_sem_conteudo_antes_do_arroba}
    resposta = val.validar_email(body)

    assert resposta == "Email invalido, favor verificar email"

def test_validar_email_deve_rejeitar_email_sem_arroba():
    email_sem_arroba = 'EmailComumemail.com.br'
    body = {'email' : email_sem_arroba}
    resposta = val.validar_email(body)

    assert resposta == "Email invalido, favor verificar email"

def test_validar_email_deve_rejeitar_email_sem_dominio():
    email_sem_dominio = 'EmailComum@.com.br'
    body = {'email' : email_sem_dominio}
    resposta = val.validar_email(body)

    assert resposta == "Email invalido, favor verificar email"

def test_validar_tamanho_da_senha():
    senha_abaixo_de_oito_caracteres = 'S3nh@'
    senha_acima_de_cem_caracteres = 'SenhaP3rfeit@' * 10
    body_senhas = [
        senha_abaixo_de_oito_caracteres,
        senha_acima_de_cem_caracteres,
    ]

    for senha in body_senhas:
        body = {'senha' : senha}
        erro = val.validar_senha(body)

        assert erro == "Senha inválida. Sua senha deve conter entre 8 a 100 caracteres"

def test_validar_senha_deve_aceitar_senha_que_cumpre_requisitos():
    senha_que_cumpre_requisitos = 'Senh@P3rfeita'
    body = {'senha' : senha_que_cumpre_requisitos}
    erro = val.validar_senha(body)

    assert erro is None

def test_validar_senha_deve_rejeitar_senha_abaixo_de_oito_caracteres():
    senha_abaixo_de_oito_caracteres = 'S3nh@'
    body = {'senha' : senha_abaixo_de_oito_caracteres}
    erro = val.validar_senha(body)

    assert erro == "Senha inválida. Sua senha deve conter entre 8 a 100 caracteres"

def test_validar_senha_deve_rejeitar_senha_acima_de_cem_caracteres():
    senha_acima_de_cem_caracteres = 'SenhaP3rfeit@' * 10
    body = {'senha' : senha_acima_de_cem_caracteres}
    erro = val.validar_senha(body)

    assert erro == "Senha inválida. Sua senha deve conter entre 8 a 100 caracteres"

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
