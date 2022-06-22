from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import psycopg2
import sqlalchemy

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db = SQLAlchemy(app)

class Usuario(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(80), nullable = False)
  email = db.Column(db.String(100), nullable = False, unique = True)
  senha = db.Column(db.String(100), nullable = False)
  data_nascimento = db.Column(db.DateTime, nullable = False)

  def to_json(self):
    try:
      return {"id": self.id, "nome": self.nome, "email": self.email, "data_nascimento": self.data_nascimento}
    except Exception as e:
      return detectar_e_retornar_erro(e)

# Função para tratar erros
def detectar_e_retornar_erro(e):
  resposta_usuario = ({"Erro": "Erro Interno"}, 500)
  string_erro = str(e)
  erros_conhecidos = {
    "psycopg2.OperationalError": ({"Erro": "Erro Interno"}, 500),
    "psycopg2.errors.UniqueViolation": ({"Erro":"Email já cadastrado"}, 400),
    "psycopg2.errors.InvalidDatetimeFormat": ({"Erro": "Formato inválido para a data"}, 400),
    "psycopg2.errors.DatetimeFieldOverflow": ({"Erro": "Formato inválido para a data"}, 400),
    "NoneType": ({"Erro": "Usuário solicitado não existe"}, 400)
  }
  for erro in erros_conhecidos:
    if erro in string_erro:
      resposta_usuario = erros_conhecidos[erro]
      
  return resposta_usuario

def validar_body(body, parametros_obrigatorios):
  for dado in parametros_obrigatorios:
    if (dado not in body) or (body[dado] == ""):
      return ({"Erro": f"Campo {dado} não preenchido"}, 400)
  pass
  
# rota para listar todos os usuários
# @app.route("/usuarios", methods=["GET"])
@app.get("/usuarios")
def mostrar_todos_usuarios():
  try:
    usuarios_objetos = Usuario.query.all()
    return jsonify({"usuarios": [usuario.to_json() for usuario in usuarios_objetos]})
  except Exception as e:
    return detectar_e_retornar_erro(e)

# rota para listar um usuário
@app.get("/usuarios/<id>")
def mostrar_um_usuario(id):
  try:
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    return jsonify({"usuario": usuario_objeto.to_json()})
  except Exception as e:
    return detectar_e_retornar_erro(e)

#rota para cadastrar um usuário
@app.post("/usuarios")
def criar_usuario():
  body = request.get_json()
  body_valido = validar_body(body,["nome", "email", "senha", "data_nascimento"])
  if body_valido:
    return body_valido 
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
    if("nome" in body):
      usuario_objeto.nome = body["nome"]
    if("email" in body):
      usuario_objeto.email = body["email"]
    if("senha" in body):
      usuario_objeto.senha = body["senha"]
    if("data_nascimento" in body):
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
    
