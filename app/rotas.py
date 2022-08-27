from .controllers import usuario_controller

def declarar_rotas(app):
  app.add_url_rule("/cadastro", methods=["POST"], view_func=usuario_controller.criar_usuario)

  app.add_url_rule("/login", methods=["POST"], view_func=usuario_controller.logar_usuario)

  app.add_url_rule("/authSteam", methods=["POST"], view_func=usuario_controller.auth_steam)

  app.add_url_rule("/authSteam", methods=["DELETE"], view_func=usuario_controller.auth_steam_delete)


  app.add_url_rule("/esqueci_senha", methods=["POST"], view_func=usuario_controller.validar_usuario)

  app.add_url_rule("/atualizar_senha", methods=["POST"], view_func=usuario_controller.atualizar_senha)
