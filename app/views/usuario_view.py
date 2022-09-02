def serializar_usuario(usuario):
  return {
    "id": usuario.id,
    "nome": usuario.nome,
    "email": usuario.email,
    "data_nascimento": usuario.data_nascimento.isoformat()
  }

def serializar_jogos(resposta):
  quantidade_jogos = resposta["response"]["game_count"]
  jogos = []
  for game in resposta["response"]["games"]:
    jogos.append(game["name"])
  return {
    "quantidade_jogos": quantidade_jogos,
    "jogos": jogos
    }
