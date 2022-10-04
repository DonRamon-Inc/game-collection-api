from werkzeug.security import generate_password_hash, check_password_hash

from .db import db
from ..utils.logger import Logger
from .jogo_favorito_usuario import jogo_favorito_usuario

logger = Logger("UsuarioModel")

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    senha = db.Column(db.String(255), nullable = False)
    data_nascimento = db.Column(db.DateTime, nullable = False)
    steam_id = db.Column(db.String(80), nullable = True)
    token_esqueci_senha = db.Column(db.String(255), nullable = True)
    token_valido_ate = db.Column(db.DateTime, nullable = True)
    jogos_favoritos = db.relationship(
        "JogoFavorito", secondary=jogo_favorito_usuario, backref="usuarios"
    )

    senha_alterada = False

    def __init__(self, usuario_dicionario):
        self.nome = usuario_dicionario.get("nome").strip()
        self.email = usuario_dicionario.get("email")
        self.senha = generate_password_hash(usuario_dicionario.get("senha"))
        self.data_nascimento = usuario_dicionario.get("data_nascimento")
        self.steam_id = usuario_dicionario.get("steam_id", None)
        self.token_esqueci_senha = usuario_dicionario.get("token_esqueci_senha", None)
        self.token_valido_ate = usuario_dicionario.get("token_valido_ate", None)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

    def salvar(self):
        logger.info(f"Salvando usuário {self.email}")
        if self.senha_alterada:
            self.senha_alterada = False
            self.senha = generate_password_hash(self.senha)
        db.session.add(self)
        db.session.commit()
        logger.info(f"Usuário {self.email} salvo com sucesso")
