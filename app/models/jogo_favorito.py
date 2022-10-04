from .db import db
from ..utils.logger import Logger

logger = Logger("JogoFavoritoModel")

class JogoFavorito(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(80), nullable = False)
    steam_id_jogo = db.Column(db.String(50), nullable = False)
    url_capa = db.Column(db.String(50), nullable = False)

    def __init__(self, jogo_favorito_dicionario):
        self.nome = jogo_favorito_dicionario.get("nome")
        self.steam_id_jogo = jogo_favorito_dicionario.get("steam_id_jogo")
        self.url_capa = jogo_favorito_dicionario.get("url_capa")


    def salvar(self):
        logger.info(f"Salvando jogo favorito {self.nome}")
        db.session.add(self)
        db.session.commit()
        logger.info(f"Jogo favorito {self.nome} salvo com sucesso")
