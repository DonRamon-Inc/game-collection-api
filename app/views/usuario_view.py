def serializar_usuario(usuario):
    return {
      "id": usuario.id,
      "nome": usuario.nome,
      "email": usuario.email,
      "data_nascimento": usuario.data_nascimento.isoformat()
    }
