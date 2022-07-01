from ..models.usuario import Usuario
from ..views.usuario_view import serializar_usuario
import re
from datetime import datetime

def detectar_e_retornar_erro(erro):
  erro = str(erro)
  erros_conhecidos = {
    "psycopg2.OperationalError": ({"Erro": "Erro Interno"}, 500),
    "NoneType": ({"Erro": "Usuário solicitado não existe"}, 400)
  }
  for key in erros_conhecidos.keys():
    if key in erro:
      return erros_conhecidos[key]
  return {"Erro": "Erro Interno"}, 500

def validar_body(body, parametros_obrigatorios):
  # padroes = {
  #   "nome": "",
  #   "email": "",
  #   "senha": "",
  #   "data_nascimento": ""
  # }
  # for parametro in parametros_obrigatorios:
  #   for keys in padroes.keys():
  #     if parametro:
  #       pass
  for parametro in parametros_obrigatorios:
    if (parametro not in body) or (body[parametro] == ""):
      return ({"Erro": f"Campo {parametro} não preenchido"}, 400)
  pass

def criar_usuario(request):
  body = request.get_json()
  body_valido = validar_body(body,["nome", "email", "senha", "data_nascimento"])
  if body_valido:
    return body_valido
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
