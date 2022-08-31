from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.logger import Logger

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

  def __init__(self, nome, email, senha, data_nascimento, steam_id = None, token_esqueci_senha = None, token_valido_ate = None):
    self.nome = nome
    self.email = email
    self.senha = generate_password_hash(senha)
    self.data_nascimento = data_nascimento
    self.steam_id = steam_id
    self.token_esqueci_senha = token_esqueci_senha
    self.token_valido_ate = token_valido_ate

  def verificar_senha(self, senha):
    return check_password_hash(self.senha, senha)

  def salvar(self, senha = None):
    if senha != None:
      logger.info(f"Salvando a alteração de senha do usuário {self.email}")
      self.senha = generate_password_hash(senha)
      db.session.add(self)
      db.session.commit()
      logger.info(f"Senha do usuário {self.email} alterada com sucesso")
    else:
      logger.info(f"Salvando usuário {self.email}")
      db.session.add(self)
      db.session.commit()
      logger.info(f"Usuário {self.email} salvo com sucesso")
