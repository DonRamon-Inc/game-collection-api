from sqlalchemy import null
from ..models.usuario import Usuario
from ..views.usuario_view import serializar_usuario
import re
from datetime import datetime
from flask import jsonify

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
  if parametros_vazios:
    campos_vazios = f"Campo(s) {parametros_vazios} não preenchido(s)"
    return campos_vazios

def validar_confirmacoes_email_senha(body):
  erros_confirmacao = []
  if body["email"] != body["confirmacao_email"]:
    erros_confirmacao.append("Os emails informados não coincidem")
  if body["senha"] != body["confirmacao_senha"]:
    erros_confirmacao.append("As senhas informadas não coincidem")
  return erros_confirmacao

def validar_email(body):
  email = body["email"]
  email_regex = r"^\w+@\w+\.\w+$"
  if re.search(email_regex, email) == None:
    return "Email não existe"
  email_existe = Usuario.query.filter_by(email = email).first()
  if email_existe:
    return "Email já cadastrado"

def validar_body(body, parametros_obrigatorios):
  retornos_funcoes = [
                validar_parametros_obrigatorios(body, parametros_obrigatorios),
                validar_confirmacoes_email_senha(body),
                validar_email(body)
  ]
  erros_body = list(filter(None, retornos_funcoes))
  if erros_body:
    return {"Erro": erros_body}

def criar_usuario(request):
  body = request.get_json()
  body_invalido = validar_body(body,["nome", "email", "confirmacao_email", "senha", "confirmacao_senha", "data_nascimento"])
  if body_invalido:
    return jsonify(body_invalido), 400
  try:
    usuario = Usuario(nome = body["nome"], email = body["email"], senha = body["senha"], data_nascimento = body["data_nascimento"])
    usuario.salvar()
    return serializar_usuario(usuario), 201
  except Exception as e:
    return detectar_e_retornar_erro(e)

def editar_usuario(request, id):
  usuario = Usuario.query.filter_by(id=id).first()
  body = request.get_json()
  try:
    if("nome" in body):
      usuario.nome = body["nome"]
    if("email" in body):
      usuario.email = body["email"]
    if("senha" in body):
      usuario.senha = body["senha"]
    if("data_nascimento" in body):
      usuario.data_nascimento = body["data_nascimento"]

    usuario.salvar()
    return serializar_usuario(usuario)
  except Exception as e:
    return detectar_e_retornar_erro(e)
