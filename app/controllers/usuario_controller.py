from ..models.usuario import Usuario
from ..views.usuario_view import serializar_usuario
import os
import jwt
import datetime

def criar_usuario(request):
  body = request.get_json()
  try:
    usuario = Usuario(nome = body["nome"], email = body["email"], senha = body["senha"], data_nascimento = body["data_nascimento"])
    usuario.salvar()
    return serializar_usuario(usuario), 201
  except:
    return "Erro", 500

def logar_usuario(request):
  body = request.get_json()
  email, senha = body['email'], body["senha"]
  usuario = Usuario.query.filter_by(email=email).first()
  if not usuario or not usuario.verificar_senha(senha):
    return 'Email ou Senha não confere'

  tokenAutenticacao = jwt.encode({'sub' : usuario.id, 'user' : usuario.nome, 'iat' : datetime.datetime.utcnow(),'exp' :  datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, os.getenv('SECRET_KEY'))
  return {'token' : tokenAutenticacao }
