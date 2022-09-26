def serializar_jogos(resposta):
    quantidade_jogos = resposta["response"]["game_count"]
    jogos = [jogo["name"] for jogo in resposta["response"]["games"]]
    jogos.sort()
    return {
      "quantidade_jogos": quantidade_jogos,
      "jogos": jogos
    }
