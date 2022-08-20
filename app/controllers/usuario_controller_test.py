import mock as m

import jwt

from .usuario_controller import logar_usuario
from ..models import usuario
from .. import config

def test_logar_usuario_retorna_erro_400_caso_o_body_nao_tenha_senha():
  body_invalido = {"email": "tchutchuca@email.com"}
  request = m.Mock(get_json=m.Mock(return_value=body_invalido))
  resposta, status = logar_usuario(request)

  assert status == 400
  assert resposta == {"Erro - Campos não preenchidos": ["senha"]}

def test_logar_usuario_retorna_erro_400_caso_o_body_nao_tenha_email():
  body_invalido = {"senha": "123456789"}
  request = m.Mock(get_json=m.Mock(return_value=body_invalido))
  resposta, status = logar_usuario(request)

  assert status == 400
  assert resposta == {"Erro - Campos não preenchidos": ["email"]}

def test_logar_usuario_retorna_erro_400_caso_o_email_nao_esteja_no_formato_certo():
  body_invalido = {"email": "joaquim", "senha": "t1234567"}
  request = m.Mock(get_json=m.Mock(return_value=body_invalido))
  resposta, status = logar_usuario(request)

  assert status == 400
  assert resposta == {"Erro": ["Email inválido"]}

def test_logar_usuario_retorna_erro_400_caso_a_senha_nao_esteja_no_formato_certo():
  body_invalido = {"email": "joaquim@gmail.com", "senha": "1321321"}
  request = m.Mock(get_json=m.Mock(return_value=body_invalido))
  resposta, status = logar_usuario(request)

  assert status == 400
  assert resposta == {"Erro": ["Senha inválida"]}

def test_logar_usuario_retorna_erro_400_caso_o_email_e_senha_estejam_invalidos():
  body_invalido = {"email": "joao", "senha": "1321321"}
  request = m.Mock(get_json=m.Mock(return_value=body_invalido))
  resposta, status = logar_usuario(request)

  assert status == 400
  assert resposta == {"Erro": ["Email inválido", "Senha inválida"]}

def test_logar_usuario_retorna_erro_400_caso_usuario_nao_seja_encontrado():
  body = {"email": "ramon@gmail.com", "senha": "t12341233"}
  request = m.Mock(get_json=m.Mock(return_value=body))

  usuario_fake = None # usuario não foi encontrado no banco
  first_mock = m.Mock(return_value=usuario_fake)
  filter_by_mock = m.Mock(return_value=m.NonCallableMock(first=first_mock))
  usuario.Usuario = m.NonCallableMock(query=m.NonCallableMock(filter_by=filter_by_mock))

  resposta, status = logar_usuario(request)

  filter_by_mock.assert_called_once_with(email=body["email"])

  assert status == 400
  assert resposta == {"mensagem": "Email ou Senha não confere"}

def test_logar_usuario_retorna_erro_400_caso_senha_nao_corresponda():
  body = {"email": "ramon@gmail.com", "senha": "t12341233"}
  request = m.Mock(get_json=m.Mock(return_value=body))

  usuario_fake = m.NonCallableMock(verificar_senha=m.Mock(return_value=False)) # usuario foi encontrado no banco, mas a senha não bate
  first_mock = m.Mock(return_value=usuario_fake)
  filter_by_mock = m.Mock(return_value=m.NonCallableMock(first=first_mock))
  usuario.Usuario = m.NonCallableMock(query=m.NonCallableMock(filter_by=filter_by_mock))

  resposta, status = logar_usuario(request)

  assert status == 400
  assert resposta == {"mensagem": "Email ou Senha não confere"}

def test_logar_usuario_retorna_token_de_acesso():
  body = {"email": "ramon@gmail.com", "senha": "t12341233"}
  request = m.Mock(get_json=m.Mock(return_value=body))

  usuario_fake = m.NonCallableMock(
    verificar_senha=m.Mock(return_value=True),
    id="usuario_id",
    nome="matheus"
  )
  first_mock = m.Mock(return_value=usuario_fake)
  filter_by_mock = m.Mock(return_value=m.NonCallableMock(first=first_mock))
  usuario.Usuario = m.NonCallableMock(query=m.NonCallableMock(filter_by=filter_by_mock))

  jwt.encode = m.Mock(return_value="bilu")
  config.SECRET_KEY = "secret"

  resposta, status = logar_usuario(request)

  primeira_chamada = jwt.encode.mock_calls[0]

  assert primeira_chamada.args[0]["sub"] == "usuario_id"
  assert primeira_chamada.args[0]["user"] == "matheus"
  assert primeira_chamada.args[1] == "secret"
  assert status == 200
  assert resposta == {"token": "bilu"}
