from flask import request
from .controllers import usuario_controller

def auth_steam():
    return usuario_controller.auth_steam(contexto = {'request':request})

def auth_steam_delete():
    return usuario_controller.auth_steam_delete(contexto = {'request':request})

def validar_usuario():
    return usuario_controller.validar_usuario(contexto = {'request':request})

def declarar_rotas(app):
    app.add_url_rule("/cadastro", methods=["POST"], view_func=usuario_controller.criar_usuario)

    app.add_url_rule("/login", methods=["POST"], view_func=usuario_controller.logar_usuario)

    app.add_url_rule("/authSteam", methods=["POST"], view_func=auth_steam)

    app.add_url_rule(
      "/authSteam", methods=["DELETE"], view_func=auth_steam_delete
    )

    app.add_url_rule(
      "/esqueci_senha", methods=["POST"], view_func=validar_usuario
    )

    app.add_url_rule(
      "/atualizar_senha", methods=["POST"], view_func=usuario_controller.atualizar_senha
    )

    app.add_url_rule(
      "/listar_jogos_steam", methods=["GET"], view_func=usuario_controller.listar_jogos_steam
    )
