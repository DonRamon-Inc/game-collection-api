from .db import db
from ..utils.logger import Logger

logger = Logger("JogoFavoritoModel")

jogo_favorito_usuario = db.Table(
    'jogo_favorito_usuario',
    db.Column('id', db.Integer, primary_key = True),
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('jogo_favorito_id', db.Integer, db.ForeignKey('jogo_favorito.id'))
    )
