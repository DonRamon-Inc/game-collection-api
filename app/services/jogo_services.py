import requests

from ..views.jogo_view import serializar_jogos
from ..utils import auth
from .. import config

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
def detalhes_jogo(contexto):

    jogo_id = contexto["jogo_id"]

    parametros_request = {
      "appids": jogo_id,
      "cc":"br",
      "l":"brazilian"
    }

    resposta = requests.get(
      f"{config.STEAM_STORE_URL}/api/appdetails", params= parametros_request, timeout=15).json()

    detalhes = {
      "jogo_id":resposta[str(jogo_id)]["data"]["steam_appid"],
      "nome": resposta[str(jogo_id)]["data"]["name"],
      "descricao": resposta[str(jogo_id)]["data"]["short_description"],
      "capa": resposta[str(jogo_id)]["data"]["header_image"],
      "preco_atual": resposta[str(jogo_id)]["data"]["price_overview"]["final_formatted"],
      "preco_base": resposta[str(jogo_id)]["data"]["price_overview"]["initial_formatted"],
      "desconto": resposta[str(jogo_id)]["data"]["price_overview"]["discount_percent"]
    }

    return (detalhes, 200)
    