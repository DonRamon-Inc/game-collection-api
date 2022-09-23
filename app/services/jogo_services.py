import requests

from ..views.jogo_view import serializar_jogos, serializar_detalhes_jogo
from ..utils import auth
from .. import config

def lista_jogos(contexto, info_extra=True):
    usuario = contexto["usuario"]
    if not usuario.steam_id:
        return {"erro": "nenhuma conta da steam associada a este usuario"}, 400
    headers = {"x-webapi-key": config.STEAM_API_KEY}
    parametros = {
      "steamid": usuario.steam_id,
      "include_appinfo": info_extra,
      "include_played_free_games": True
    }
    resposta = requests.get(
      f'{config.STEAM_API_URL}/IPlayerService/GetOwnedGames/v1/',
      headers=headers,
      params=parametros,
      timeout=15
    )
    return resposta.json()


@auth.token_required
def listar_jogos_steam(contexto):
    resposta = lista_jogos(contexto)

    return serializar_jogos(resposta), 200


@auth.token_required
def detalhes_jogo(contexto):
    jogo_id = contexto["jogo_id"]
    parametros_request = {
      "appids": jogo_id,
      "cc":"br",
      "l":"brazilian"
    }
    jogos_usuario = lista_jogos(contexto, info_extra=False)
    resposta = requests.get(
      f"{config.STEAM_STORE_URL}/api/appdetails", params= parametros_request, timeout=15).json()

    jogo_id = int(jogo_id)
    usuario_possui = False

    for jogo in jogos_usuario["response"]["games"]:
        if jogo_id == jogo["appid"]:
            usuario_possui = True
            break

    return (serializar_detalhes_jogo(resposta, str(jogo_id), usuario_possui), 200)
