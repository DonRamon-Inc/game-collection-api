from ..models.usuario import Usuario
from ..views.usuario_view import serializar_usuario
from .. import config
import jwt
import datetime
import secrets
from ..utils.logger import Logger

import re
from flask import jsonify, request

logger = Logger("UsuarioController")

def detectar_e_retornar_erro(erro):
  erro = str(erro)
  erros_conhecidos = {
    "psycopg2.OperationalError": ({"Erro": "Erro Interno"}, 500),
    "NoneType": ({"Erro": "Usuário solicitado não existe"}, 400)
  }
  for key in erros_conhecidos.keys():
    if key in erro:
      return erros_conhecidos[key]
  print(erro)
  return {"Erro": "Erro Interno"}, 500

def validar_parametros_obrigatorios(body, parametros_obrigatorios):
  parametros_vazios = []
  for parametro in parametros_obrigatorios:
    if (parametro not in body) or (body[parametro] == ""):
      parametros_vazios.append(parametro)
  return parametros_vazios

def validar_confirmacao_email(body):
  if body["email"] != body["confirmacao_email"]:
    return "Os emails informados não coincidem"

def validar_confirmacao_senha(body):
  if body["senha"] != body["confirmacao_senha"]:
    return "As senhas informadas não coincidem"

def validar_email(body):
  email = body["email"]
  email_regex = r"^\w+@\w+\.\w+$"
  if re.search(email_regex, email) == None:
    return "Email não existe"
  email_valido = Usuario.query.filter_by(email = email).first()
  if email_valido:
    return "Email já cadastrado"

def validar_senha(body):
  senha = body["senha"]
  senha_regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
  if re.search(senha_regex,senha) == None:
    return ("Senha inválida. A senha precisa conter, no mínimo, 8 caracteres,"+
     " 1 letra e 1 número.")

def validar_data_nascimento(body):
  data_nascimento = body["data_nascimento"]
  try:
    data_formatada = datetime.datetime.strptime(data_nascimento, r"%Y-%m-%d")
    if data_formatada.year > (datetime.datetime.now().year - 13):
      return "É preciso ter mais de 13 anos para criar uma conta."
  except ValueError:
    return "Formato de data inválido"
  except Exception:
    return "Erro interno"

def validar_body(body, parametros_obrigatorios):
  campos_invalidos = validar_parametros_obrigatorios(body, parametros_obrigatorios)
  if campos_invalidos != []:
    return f"Campo(s) {campos_invalidos} não preenchido(s)"
  validacoes = [
  validar_confirmacao_email(body),
  validar_confirmacao_senha(body),
  validar_email(body),
  validar_senha(body),
  validar_data_nascimento(body)
  ]
  erros_body = list(filter(None, validacoes))
  if erros_body:
    return {"Erro": erros_body}

def criar_usuario():
  body = request.get_json()
  logger.info(f"Chamada recebida com parâmetros {body.keys()}")
  body_invalido = validar_body(body,["nome", "email", "confirmacao_email", "senha", "confirmacao_senha", "data_nascimento"])
  if body_invalido:
    return jsonify(body_invalido), 400
  try:
    usuario = Usuario(nome = body["nome"], email = body["email"], senha = body["senha"], data_nascimento = body["data_nascimento"])
    usuario.salvar()
    return serializar_usuario(usuario), 201
  except Exception as e:
      return detectar_e_retornar_erro(e)

def logar_usuario():
  body = request.get_json()
  # TODO validar body

  email, senha = body['email'], body["senha"]
  usuario = Usuario.query.filter_by(email=email).first()
  if not usuario or not usuario.verificar_senha(senha):
    return {'mensagem': 'Email ou Senha não confere'}, 400

  token_autenticacao = jwt.encode({
    'sub' : usuario.id,
    'user' : usuario.nome,
    'iat' : datetime.datetime.utcnow(),
    'exp' :  datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
   }, config.SECRET_KEY)
  return {'token' : token_autenticacao}

def validar_usuario():
  body = request.get_json()
  logger.info(f"Chamada recebida com parâmetros {body.keys()}")
  email, data_nascimento = body['email'], body['data_nascimento']
  usuario = Usuario.query.filter_by(email=email).first()
  if not usuario:
    return {"Erro": "Email não cadastrado"}
  if str(usuario.data_nascimento) == data_nascimento:
    token_usuario = secrets.token_hex(16)
    return {"Token": f"{token_usuario}"}
  else:
    return {"Erro": "Usuário não validado"}
