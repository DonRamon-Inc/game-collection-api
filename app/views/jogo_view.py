def serializar_jogos(resposta):
    quantidade_jogos = resposta["response"]["game_count"]
    jogos = []
    for game in resposta["response"]["games"]:
        jogos.append(game["name"])
    jogos.sort()
    return {
      "quantidade_jogos": quantidade_jogos,
      "jogos": jogos
    }
