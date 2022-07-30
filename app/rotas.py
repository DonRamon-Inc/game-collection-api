from .controllers import usuario_controller

def declarar_rotas(app):
  app.add_url_rule("/cadastro", methods=["POST"], view_func=usuario_controller.criar_usuario)

  app.add_url_rule("/login", methods=["POST"], view_func=usuario_controller.logar_usuario)
