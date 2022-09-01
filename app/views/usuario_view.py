def serializar_usuario(usuario):
  return {
    "id": usuario.id,
    "nome": usuario.nome,
    "email": usuario.email,
    "data_nascimento": usuario.data_nascimento.isoformat()
  }

def serializar_jogos(jogos):
  jogos_serializados = {}
  for jogo in jogos:
    pass
  return {"":""}
