from flask import request
from .controllers import usuario_controller

"""
TODO: Melhorar essa forma de declarar as rotas, as funções declaradas dentro de `declarar_rotas` não são usadas diretamente.
"""
def declarar_rotas(app):
  @app.post("/cadastro")
  def cadastrar_usuario():
    return usuario_controller.criar_usuario(request)
