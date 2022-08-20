from .controllers import usuario_controller
from flask import request, jsonify

def login_usuario():
  resposta, status = usuario_controller.logar_usuario(request)
  return jsonify(resposta), status

def criar_usuario():
  resposta, status = usuario_controller.criar_usuario(request)
  return jsonify(resposta), status

def declarar_rotas(app):
  app.add_url_rule("/cadastro", methods=["POST"], view_func=criar_usuario)

  app.add_url_rule("/login", methods=["POST"], view_func=login_usuario)
