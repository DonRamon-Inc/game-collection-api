from flask import request
from ..services import jogo_services as js

def listar_jogos_steam():
    return js.listar_jogos_steam(contexto = {'request': request})

def favoritar_jogo(id_jogo):
    return js.favoritar_jogo(contexto = {'request': request, 'id_jogo': id_jogo})
