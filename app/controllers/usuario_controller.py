from ..models.usuario import Usuario
from ..views.usuario_view import serializar_usuario

def criar_usuario(request):
  body = request.get_json()
  try:
    usuario = Usuario(nome = body["nome"], email = body["email"], senha = body["senha"], data_nascimento = body["data_nascimento"])
    usuario.salvar()
    return serializar_usuario(usuario), 201
  except:
    return "Erro", 500
