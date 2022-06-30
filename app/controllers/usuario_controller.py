from ..models.usuario import Usuario
from ..views.usuario_view import serializar_usuario
from ..models.db import db

def detectar_e_retornar_erro(erros):
  resposta_usuario = ({"Erro": "Erro Interno"}, 500)
  erros_conhecidos = {
    "psycopg2.OperationalError": {"Erro": "Erro Interno"},
    "psycopg2.errors.UniqueViolation": {"Erro":"Email já cadastrado"},
    "psycopg2.errors.InvalidDatetimeFormat": {"Erro": "Formato inválido para a data"},
    "psycopg2.errors.DatetimeFieldOverflow": {"Erro": "Formato inválido para a data"},
    "NoneType": {"Erro": "Usuário solicitado não existe"}
  }
  lista_de_erros = []
  for key, value in erros_conhecidos.items():
    for e in erros:
      if key in e:
        lista_de_erros.append(value)
        print(value)
  return {"Erros": lista_de_erros}

def validar_body(body, parametros_obrigatorios):
  for dado in parametros_obrigatorios:
    if (dado not in body) or (body[dado] == ""):
      return ({"Erro": f"Campo {dado} não preenchido"}, 400)
  pass

def criar_usuario(request):
  body = request.get_json()
  body_valido = validar_body(body,["nome", "email", "senha", "data_nascimento"])
  if body_valido:
    return body_valido
  erros = []
  for e in range (7):
    try:
      usuario = Usuario(nome = body["nome"], email = body["email"], senha = body["senha"], data_nascimento = body["data_nascimento"])
      usuario.salvar()
      return usuario.to_json(), 201
    except Exception as e:
      erros.append(str(e))
  if erros:
    return detectar_e_retornar_erro(erros)

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
    return usuario.to_json()
  except Exception as e:
    return detectar_e_retornar_erro(e)
