def serializar_jogos(resposta):
    quantidade_jogos = resposta["response"]["game_count"]
    jogos = [jogo["name"] for jogo in resposta["response"]["games"]]
    jogos.sort()
    return {
      "quantidade_jogos": quantidade_jogos,
      "jogos": jogos
    }

def serializar_detalhes_jogo(resposta, jogo_id):

    return {
      "jogo_id":resposta[jogo_id]["data"]["steam_appid"],
      "nome": resposta[jogo_id]["data"]["name"],
      "descricao": resposta[jogo_id]["data"]["short_description"],
      "capa": resposta[jogo_id]["data"]["header_image"],
      "preco_atual": resposta[jogo_id]["data"]["price_overview"]["final_formatted"],
      "preco_base": resposta[jogo_id]["data"]["price_overview"]["initial_formatted"],
      "desconto": resposta[jogo_id]["data"]["price_overview"]["discount_percent"]
    }
    