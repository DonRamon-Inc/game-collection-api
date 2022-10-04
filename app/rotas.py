from .controllers import usuario_controller as uc
from .controllers import jogo_controller as jc

def declarar_rotas(app):
    app.add_url_rule("/cadastro", methods=["POST"], view_func=uc.cadastrar_usuario)

    app.add_url_rule("/login", methods=["POST"], view_func=uc.logar_usuario)

    app.add_url_rule("/authSteam", methods=["POST"], view_func=uc.auth_steam)

    app.add_url_rule(
      "/authSteam", methods=["DELETE"], view_func=uc.auth_steam_delete
    )

    app.add_url_rule(
      "/esqueci_senha", methods=["POST"], view_func=uc.validar_usuario
    )

    app.add_url_rule(
      "/atualizar_senha", methods=["POST"], view_func=uc.atualizar_senha
    )

    app.add_url_rule(
      "/listar_jogos_steam", methods=["GET"], view_func=jc.listar_jogos_steam
    )

    app.add_url_rule(
      "/jogo/<id_jogo>", methods=["GET"], view_func=jc.detalhes_jogo_steam
    )

    app.add_url_rule("/favoritar_jogo", methods=["POST"], view_func=jc.favoritar_jogo)
