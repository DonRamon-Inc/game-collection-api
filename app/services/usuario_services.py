import datetime
import secrets

import jwt
from flask import jsonify

from ..models import usuario as u
from ..views.usuario_view import serializar_usuario
from .. import config
from ..utils import validacoes as val
from ..utils import auth
from ..utils.logger import Logger

logger = Logger("UsuarioController")

def criar_usuario(contexto):
    body = contexto["request"].get_json()
    body = val.validar_excesso_espacamento_nome(body)
    logger.info(f"Chamada recebida com parâmetros {body.keys()}")
    body_invalido = val.validar_body(
      body,
      {
        "nome":80,
        "email":100,
        "confirmacao_email":100,
        "senha":100,
        "confirmacao_senha":100,
        "data_nascimento":10
      },
      [
        val.validar_confirmacao_email,
        val.validar_confirmacao_senha,
        val.validar_data_nascimento,
        val.validar_email,
        val.validar_email_duplicado,
        val.validar_senha
      ]
    )
    if body_invalido:
        return jsonify(body_invalido), 400

    usuario = u.Usuario({
      "nome": body["nome"],
      "email": body["email"],
      "senha": body["senha"],
      "data_nascimento": body["data_nascimento"]
    })
    usuario.salvar()
    return serializar_usuario(usuario), 201

def logar_usuario(contexto):
    body = contexto["request"].get_json()
    body_invalido = val.validar_body(body,{"email":100,"senha":100},
    [val.validar_email])
    if body_invalido:
        return jsonify(body_invalido),400

    email, senha = body['email'], body["senha"]
    usuario = u.Usuario.query.filter_by(email=email).first()
    if not usuario or not usuario.verificar_senha(senha):
        return {'mensagem': 'Email ou Senha não confere'}, 400

    token_autenticacao = jwt.encode({
      'sub' : usuario.id,
      'user' : usuario.nome,
      'iat' : datetime.datetime.utcnow(),
      'exp' :  datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, config.SECRET_KEY)
    return {'token' : token_autenticacao}

@auth.token_required
def auth_steam(contexto):
    usuario = contexto['usuario']
    body = contexto['request'].get_json()
    logger.info(f"Chamada recebida com parâmetros {body}")
    body_invalido = val.validar_body(body,{"steam_id":50})
    if body_invalido:
        return jsonify(body_invalido), 400
    steam_id = body["steam_id"]
    usuario.steam_id = steam_id
    usuario.salvar()
    return {'mensagem': 'ID da Steam registrado'}, 200

@auth.token_required
def auth_steam_delete(contexto):
    usuario = contexto['usuario']
    usuario.steam_id = None
    usuario.salvar()
    return '', 204

def validar_usuario(contexto):
    body = contexto['request'].get_json()
    logger.info(f"Chamada recebida com parâmetros {body.keys()}")
    body_invalido = val.validar_body(body,
        {"email":100, "data_nascimento":10},
        [val.validar_data_nascimento]
    )
    if body_invalido:
        return jsonify(body_invalido), 400
    email, data_nascimento = body['email'], body['data_nascimento']
    usuario = u.Usuario.query.filter_by(email=email).first()
    if not usuario:
        return {"erro": "usuário inválido"}, 400
    if str(usuario.data_nascimento) == data_nascimento and val.validar_token(usuario) is False:
        token_esqueci_senha = str(secrets.token_hex()) + str(
          datetime.datetime.timestamp(datetime.datetime.utcnow())).replace(".","")

        usuario.token_esqueci_senha = token_esqueci_senha
        usuario.token_valido_ate = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        usuario.salvar()
        return {"token": f"{token_esqueci_senha}"}, 201
    if str(usuario.data_nascimento) == data_nascimento and val.validar_token(usuario) is True:
        return {"token": f"{usuario.token_esqueci_senha}"}, 200
    return {"erro": "usuário inválido"}, 400

def atualizar_senha(contexto):
    body = contexto["request"].get_json()
    body_invalido = val.validar_body(body,
        {"token_esqueci_senha":100, "senha":100,"confirmacao_senha":100},
        [val.validar_senha,val.validar_confirmacao_senha]
    )
    if body_invalido:
        return jsonify(body_invalido), 400
    logger.info(f"Chamada recebida com parâmetros {body.keys()}")
    token_esqueci_senha = body['token_esqueci_senha']
    senha = body['senha']
    usuario = u.Usuario.query.filter_by(token_esqueci_senha=token_esqueci_senha).first()
    if not usuario or val.validar_token(usuario) is False:
        return {"erro": "token inválido"}, 400
    usuario.token_esqueci_senha = None
    usuario.token_valido_ate = None
    usuario.senha = senha
    usuario.senha_alterada = True
    usuario.salvar()
    return {"mensagem": "senha alterada com sucesso"}, 201
