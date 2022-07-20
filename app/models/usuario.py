from .db import db
from ..utils.logger import Logger

from werkzeug.security import generate_password_hash

logger = Logger("UsuarioModel")

class Usuario(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(80), nullable = False)
  email = db.Column(db.String(100), nullable = False, unique = True)
  senha = db.Column(db.String(255), nullable = False)
  data_nascimento = db.Column(db.DateTime, nullable = False)

  def __init__(self, nome, email, senha, data_nascimento):
    self.nome = nome
    self.email = email
    self.senha = generate_password_hash(senha)
    self.data_nascimento = data_nascimento

  def salvar(self):
    logger.info(f"Salvando usuário {self.email}")
    db.session.add(self)
    db.session.commit()
    logger.info(f"Usuário {self.email} salvo com sucesso")
