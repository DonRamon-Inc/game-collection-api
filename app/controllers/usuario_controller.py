from ..models.usuario import Usuario
from ..views.usuario_view import serializar_usuario
from .. import config
from ..utils import auth
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
    parametro_apenas = body[parametro].strip()
    if (parametro not in body) or (parametro_apenas == ""):
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

def validar_email_duplicado(body):
  email = body["email"]
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

def validar_body(body, parametros_obrigatorios, validacoes=[]):
  campos_invalidos = validar_parametros_obrigatorios(body, parametros_obrigatorios)
  if campos_invalidos != []:
    return {"Erro - Campos não preenchidos": campos_invalidos}

  validacoes_result = []
  for funcao_validadora in validacoes:
    validacoes_result.append(funcao_validadora(body))

  erros_body = list(filter(None, validacoes_result))
  if erros_body:
    return {"Erro": erros_body}

def validar_token(usuario):
  token = usuario.token_esqueci_senha
  token_timestamp = usuario.token_valido_ate
  if not token:
    return False
  elif token_timestamp < datetime.datetime.utcnow():
    return False
  else:
    return True

def criar_usuario():
  body = request.get_json()
  logger.info(f"Chamada recebida com parâmetros {body.keys()}")
  body_invalido = validar_body(body,
  ["nome", "email", "confirmacao_email", "senha", "confirmacao_senha", "data_nascimento"],
  [validar_confirmacao_email,validar_confirmacao_senha,validar_data_nascimento,validar_email,
  validar_email_duplicado,validar_senha])
  if body_invalido:
    return jsonify(body_invalido), 400
  try:
    usuario = Usuario(nome = body["nome"], email = body["email"], senha = body["senha"],
    data_nascimento = body["data_nascimento"])
    usuario.salvar()
    return serializar_usuario(usuario), 201
  except Exception as e:
      return detectar_e_retornar_erro(e)

def logar_usuario():
  body = request.get_json()
  body_invalido = validar_body(body,["email","senha"],
  [validar_email,validar_senha])
  if body_invalido:
    return jsonify(body_invalido),400

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

@auth.token_required
def auth_steam(usuario):
  body = request.get_json()
  logger.info(f"Chamada recebida com parâmetros {body}")
  body_invalido = validar_body(body,["steam_id"])
  if body_invalido:
    return jsonify(body_invalido), 400
  steam_id = body["steam_id"]
  usuario.steam_id = steam_id
  usuario.salvar()
  return {'mensagem': 'ID da Steam registrado'}, 200

@auth.token_required
def auth_steam_delete(usuario):
  usuario.steam_id = None
  usuario.salvar()
  return {'mensagem': 'ID da Steam deletado'}, 200

def validar_usuario():
  #TODO VALIDAR BODY
  body = request.get_json()
  logger.info(f"Chamada recebida com parâmetros {body.keys()}")
  email, data_nascimento = body['email'], body['data_nascimento']
  usuario = Usuario.query.filter_by(email=email).first()
  if not usuario:
    return {"Erro": "Email não cadastrado"}
  elif str(usuario.data_nascimento) == data_nascimento and validar_token(usuario) == False:
    token_esqueci_senha = str(secrets.token_hex()) + str(
      datetime.datetime.timestamp(datetime.datetime.utcnow())).replace(".","")

    usuario.token_esqueci_senha = token_esqueci_senha
    usuario.token_valido_ate = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    usuario.salvar()
    return {"Token": f"{token_esqueci_senha}"}
  elif str(usuario.data_nascimento) == data_nascimento and validar_token(usuario) == True:
    return {"Token": f"{usuario.token_esqueci_senha}"}
  else:
    return {"Erro": "Usuário inválido"}

def atualizar_senha():
  #TODO VALIDAR BODY
  body = request.get_json()
  logger.info(f"Chamada recebida com parâmetros {body.keys()}")
  token_esqueci_senha = body['token_esqueci_senha']
  senha, confirmacao_senha = body['senha'], body['confirmacao_senha']
  usuario = Usuario.query.filter_by(token_esqueci_senha=token_esqueci_senha).first()
  if not usuario or validar_token(usuario) == False:
    return {"Erro": "Token inválido"}
  elif senha == confirmacao_senha:
    usuario.token_esqueci_senha = None
    usuario.token_valido_ate = None
    usuario.salvar(senha)
    return {"Mensagem": "Senha alterada com sucesso"}
  else:
    return {"Erro": "Senha e confirmação de senha não coincidem"}
