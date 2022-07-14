from .db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(80), nullable = False)
  email = db.Column(db.String(100), nullable = False, unique = True)
  senha = db.Column(db.String(255), nullable = False)
  data_nascimento = db.Column(db.DateTime, nullable = False)

  #passa os parametros apenas cryptografando a senha na hora do cadastro.
  def __init__(self, nome, email, senha, data_nascimento):
    self.nome = nome
    self.email = email
    self.senha = generate_password_hash(senha)
    self.data_nascimento = data_nascimento

  def verificar_senha(self, senha):
    return check_password_hash(self.senha, senha)

  def salvar(self):
    db.session.add(self)
    db.session.commit()

