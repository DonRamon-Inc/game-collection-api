from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)

class Usuario(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(80), nullable = False)
  email = db.Column(db.String(100), nullable = False, unique = True)
  senha = db.Column(db.String(100), nullable = False)
  data_nascimento = db.Column(db.DateTime, nullable = False)

  def to_json(self):
    return {"id": self.id, "nome": self.nome, "email": self.email}

#função mostrar todos os usuários
# @app.get("/usuarios")
@app.route("/usuarios", methods=["GET"])
def mostrar_todos_usuarios():
  usuarios_objetos = Usuario.query.all()
  return jsonify({'usuarios': [usuario.to_json() for usuario in usuarios_objetos]})
