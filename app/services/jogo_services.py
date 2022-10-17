import requests

from ..views import jogo_view as jv
from ..utils import auth
from .. import config
from ..models import jogo_favorito as jf
from ..models import db

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

    return jv.serializar_jogos(resposta), 200


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

    return (jv.serializar_detalhes_jogo(resposta, str(jogo_id), usuario_possui), 200)
    #return serializar_jogos(resposta.json()), 200

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

@auth.token_required
def desfavoritar_jogo(contexto):
    usuario_atual = contexto["usuario"]
    id_jogo = str(contexto["id_jogo"])
    jogo = jf.JogoFavorito.query.filter_by(steam_id_jogo=id_jogo).first()
    usuario_atual.jogos_favoritos.remove(jogo)
    db.db.session.commit()

    return {"mensagem": "jogo desfavoritado com sucesso"}, 202
