from .db import db

class Usuario(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(80), nullable = False)
  email = db.Column(db.String(100), nullable = False, unique = True)
  senha = db.Column(db.String(100), nullable = False)
  data_nascimento = db.Column(db.DateTime, nullable = False)

  def salvar(self):
    db.session.add(self)
    db.session.commit()
