from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import psycopg2
import sqlalchemy

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
<<<<<<< Updated upstream
    return {"id": self.id, "nome": self.nome, "email": self.email}

#função mostrar todos os usuários
# @app.get("/usuarios")
@app.route("/usuarios", methods=["GET"])
def mostrar_todos_usuarios():
  usuarios_objetos = Usuario.query.all()
  return jsonify({'usuarios': [usuario.to_json() for usuario in usuarios_objetos]})
=======
    return {"id": self.id, "nome": self.nome, "email": self.email, "data_nascimento": self.data_nascimento}

# Função para tratar erros
def detectar_e_retornar_erro(e):
  print(type(e))
  if type(e) == sqlalchemy.exc.OperationalError:
    print(e)
    return {"Erro": "Erro Interno"}, 500
  elif type(e) == AttributeError:
    print(e)
    return {"Erro": "Usuário não cadastrado"}, 400
  elif "psycopg2.errors.InvalidDatetimeFormat" in str(e):
    print(e)
    return {"Erro": "Formato inválido para a data"}, 400
  else:
    print(e)
    return {"Erro": "Erro Desconhecido"}, 400
  
# rota para listar todos os usuários
# @app.route("/usuarios", methods=["GET"])
@app.get("/usuarios")
def mostrar_todos_usuarios():
  try:
    usuarios_objetos = Usuario.query.all()
    return jsonify({'usuarios': [usuario.to_json() for usuario in usuarios_objetos]})
  except Exception as e:
    return detectar_e_retornar_erro(e)

# rota para listar um usuário
@app.get("/usuarios/<id>")
def mostrar_um_usuario(id):
  try:
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    return jsonify({'usuario': usuario_objeto.to_json()})
  except Exception as e:
    return detectar_e_retornar_erro(e)

#rota para cadastrar um usuário
@app.post("/usuarios")
def criar_usuario():
  body = request.get_json()
  try:
    usuario = Usuario(nome = body["nome"], email = body["email"], senha = body["senha"], data_nascimento = body["data_nascimento"])
    db.session.add(usuario)
    db.session.commit()
    return usuario.to_json(), 201
  except Exception as e:
   return detectar_e_retornar_erro(e)

#rota para atualizar um usuário
@app.put("/usuarios/<id>")
def atualizar_usuario(id):
  usuario_objeto = Usuario.query.filter_by(id=id).first()
  body = request.get_json()

  try:
    if('nome' in body):
      usuario_objeto.nome = body["nome"]
    if('email' in body):
      usuario_objeto.email = body["email"]
    if('senha' in body):
      usuario_objeto.senha = body["senha"]
    if('data_nascimento' in body):
      usuario_objeto.data_nascimento = body["data_nascimento"]
    
    db.session.add(usuario_objeto)
    db.session.commit()
    return usuario_objeto.to_json()

  except Exception as e:
    return detectar_e_retornar_erro(e)

#rota para deletar um usuário
@app.delete("/usuarios/<id>")
def deletar_usuario(id):
  usuario_objeto = Usuario.query.filter_by(id=id).first()

  try:
    db.session.delete(usuario_objeto)
    db.session.commit()
    return "", 204
  
  except Exception as e:
    return detectar_e_retornar_erro(e)
    
>>>>>>> Stashed changes
