from flask import request
from ..services import jogo_services as js

def listar_jogos_steam():
    return js.listar_jogos_steam(contexto = {'request': request})