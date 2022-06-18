from flask import Flask, jsonify, request
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
    return {"id": self.id, "nome": self.nome, "email": self.email, "senha": self.senha, "data_nascimento":self.data_nascimento}
  
#função mostrar todos os usuários
@app.get("/usuarios")
def mostrar_todos_usuarios():
  usuarios_objetos = Usuario.query.all()
  return jsonify({'usuarios': [usuario.to_json() for usuario in usuarios_objetos]})

@app.get("/usuario/<id>")
def seleciona_usuario(id):
  try:
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    return usuario_objeto.to_json()
  except Exception as e:
    print(e)
    return {"erro":"Erro na consulta"}, 400

@app.post("/cadastrar_usuario")
def cadastrar_usuario():
  body = request.get_json()
  usuario = Usuario(nome=body["nome"],email=body["email"], senha=body["senha"],data_nascimento=body["data_nascimento"])
  try:
    db.session.add(usuario)
    #db.session.add(Usuario(nome=body["nome"],email=body["email"], senha=body["senha"],data_nascimento=body["data_nascimento"]))
    # linha acima adiciona as informações da classe no banco
    db.session.commit() # insere no banco
    return  usuario.to_json()
  except Exception as e:
    print(e)
    return {"erro":"Erro no cadastro"}, 400


@app.put("/usuario/<id>")
def atualizar_usuario(id):
  usuario_objeto = Usuario.query.filter_by(id=id).first()
  body = request.get_json() # código só rodou após essa linha e a anterior irem pro TRY
  try:
    if 'nome' in body:
      usuario_objeto.nome = body['nome']
    if 'email' in body:
      usuario_objeto.email = body['email']
    if 'data_nascimento' in body:
      usuario_objeto.data_nascimento = body['data_nascimento']
    if 'senha' in body:
      usuario_objeto.senha = body['senha']
    
    db.session.add(usuario_objeto)
    db.session.commit()
    return usuario_objeto.to_json()
  except Exception as e:
    print(e)
    return {"erro":"Erro na atualização"}, 400
  
@app.delete("/usuario/<id>")
def deleta_usuario(id):
  try:
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    db.session.delete(usuario_objeto)
    db.session.commit()
    return ''
  except Exception as e:
    print(e)
    return {"erro":"Erro na remoção"}, 400

# todo - ajustar retornos, tratar erros,
# criptografia LIB - PKDF2
# Rotas sempre no plural - padrão rest
# retornos TUDO em JSON