import requests

from ..views.jogo_view import serializar_jogos
from ..utils import auth
from .. import config
from ..models import jogo_favorito as jf
from ..models import db

@auth.token_required
def listar_jogos_steam(contexto):
    usuario = contexto["usuario"]
    if not usuario.steam_id:
        return {"erro": "nenhuma conta da steam associada a este usuario"}, 400
    headers = {"x-webapi-key": config.STEAM_API_KEY}
    parametros = {
      "steamid": usuario.steam_id,
      "include_appinfo": True,
      "include_played_free_games": True
    }
    resposta = requests.get(
      f'{config.STEAM_API_URL}/IPlayerService/GetOwnedGames/v1/',
      headers=headers,
      params=parametros,
      timeout=15
    )
    return serializar_jogos(resposta.json()), 200

@auth.token_required
def favoritar_jogo(contexto):
    usuario_atual = contexto["usuario"]
    id_jogo = str(contexto["id_jogo"])
    jogo = {}
    if not jf.JogoFavorito.query.filter_by(steam_id_jogo=id_jogo).first():
        resposta = requests.get(
            f'{config.STEAM_STORE_URL}/api/appdetails', params = {
                "appids": id_jogo,
                "cc": "br",
                "filters": "basic"
            },
            timeout=15
        ).json()
        jogo = jf.JogoFavorito({
            "nome": resposta[id_jogo]["data"]["name"],
            "steam_id_jogo": id_jogo,
            "url_capa": resposta[id_jogo]["data"]["header_image"]
        })
        jogo.salvar()
    else:
        jogo = jf.JogoFavorito.query.filter_by(steam_id_jogo=id_jogo).first()


    usuario_atual.jogos_favoritos.append(jogo)
    db.db.session.commit()


    return {"mensagem": "jogo favoritado com sucesso"}, 201
