import datetime
import re
import secrets

import jwt
import requests
from flask import jsonify, request

from ..models import usuario as u
from ..views.usuario_view import serializar_jogos, serializar_usuario
from .. import config
from ..utils import auth
from ..utils.logger import Logger

logger = Logger("UsuarioController")

def validar_parametros_obrigatorios(body, parametros_obrigatorios):
    parametros_vazios = []
    for parametro in parametros_obrigatorios:
        if (parametro not in body) or (body[parametro] == ""):
            parametros_vazios.append(parametro)
    return parametros_vazios

def validar_email(body):
    email = body["email"]
    email_regex = r"^[A-Za-z\d!@#$%&.+*\-\/<>?]+@\w+\.\w+.\w+$"
    if re.search(email_regex, email) is None:
        return "Email invalido, favor verificar email"
    return None

def validar_email_duplicado(body):
    email = body["email"]
    email_valido = u.Usuario.query.filter_by(email = email).first()
    if email_valido:
        return "Email já cadastrado"
    return None

def validar_confirmacao_email(body):
    if body["email"] != body["confirmacao_email"]:
        return "Os emails informados não coincidem"
    return None

def validar_senha(body):
    senha = body["senha"]
    senha_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#^?&])[A-Za-z\d@$!#%*?&]{8,}$"
    if len(senha) > 100:
        return 'Senha inválida. Use 100 caracteres ou menos para sua senha'
    if re.search(senha_regex,senha) is None:
        return "Senha inválida. A senha precisa conter, oito ou mais caracteres " +\
          "com uma combinação de letras, números e símbolos"
    return None

def validar_confirmacao_senha(body):
    if body["senha"] != body["confirmacao_senha"]:
        return "As senhas informadas não coincidem"
    return None

def validar_data_nascimento(body):
    data_nascimento = body["data_nascimento"]
    try:
        data_formatada = datetime.datetime.strptime(data_nascimento, r"%Y-%m-%d")
        if data_formatada.year > (datetime.datetime.now().year - 13):
            return "É preciso ter mais de 13 anos para criar uma conta."
    except ValueError:
        return "Formato de data inválido"
    return None

def validar_body(body, parametros_obrigatorios, validacoes=None):
    campos_invalidos = validar_parametros_obrigatorios(body, parametros_obrigatorios)
    if campos_invalidos:
        return {"erro": f"Campos não preenchidos: {campos_invalidos}"}

    if not validacoes:
        return None
    validacoes_result = []
    for funcao_validadora in validacoes:
        validacoes_result.append(funcao_validadora(body))

    erros_body = list(filter(None, validacoes_result))
    if erros_body:
        return {"erro": erros_body}
    return None

def validar_token(usuario):
    token = usuario.token_esqueci_senha
    token_timestamp = usuario.token_valido_ate
    if not token:
        return False
    if token_timestamp < datetime.datetime.utcnow():
        return False
    return True

def criar_usuario():
    body = request.get_json()
    logger.info(f"Chamada recebida com parâmetros {body.keys()}")
    body_invalido = validar_body(
      body,
      ["nome", "email", "confirmacao_email", "senha", "confirmacao_senha", "data_nascimento"],
      [
        validar_confirmacao_email,
        validar_confirmacao_senha,
        validar_data_nascimento,
        validar_email,
        validar_email_duplicado,
        validar_senha
      ]
    )
    if body_invalido:
        return jsonify(body_invalido), 400

    usuario = Usuario({
      "nome": body["nome"],
      "email": body["email"],
      "senha": body["senha"],
      "data_nascimento": body["data_nascimento"]
    })
    usuario.salvar()
    return serializar_usuario(usuario), 201

def logar_usuario():
    body = request.get_json()
    body_invalido = validar_body(body,["email","senha"],
    [validar_email])
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
def auth_steam(usuario):
    body = request.get_json()
    logger.info(f"Chamada recebida com parâmetros {body}")
    body_invalido = validar_body(body,["steam_id"])
    if body_invalido:
        return jsonify(body_invalido), 400
    steam_id = body["steam_id"]
    usuario.steam_id = steam_id
    usuario.salvar()
    return {'mensagem': 'ID da Steam registrado'}, 200

@auth.token_required
def auth_steam_delete(usuario):
    usuario.steam_id = None
    usuario.salvar()
    return '', 204

def validar_usuario(request):
    body = request.get_json()
    logger.info(f"Chamada recebida com parâmetros {body.keys()}")
    body_invalido = validar_body(body,
      ["email", "data_nascimento"],
      [validar_data_nascimento]
    )
    if body_invalido:
        return jsonify(body_invalido), 400
    email, data_nascimento = body['email'], body['data_nascimento']
    usuario = u.Usuario.query.filter_by(email=email).first()
    if not usuario:
        return {"erro": "usuário inválido"}, 400
    if str(usuario.data_nascimento) == data_nascimento and validar_token(usuario) is False:
        token_esqueci_senha = str(secrets.token_hex()) + str(
          datetime.datetime.timestamp(datetime.datetime.utcnow())).replace(".","")

        usuario.token_esqueci_senha = token_esqueci_senha
        usuario.token_valido_ate = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        usuario.salvar()
        return {"token": f"{token_esqueci_senha}"}, 201
    if str(usuario.data_nascimento) == data_nascimento and validar_token(usuario) is True:
        return {"token": f"{usuario.token_esqueci_senha}"}, 200
    return {"erro": "usuário inválido"}, 400

def atualizar_senha():
    body = request.get_json()
    body_invalido = validar_body(body,
      ["token_esqueci_senha", "senha","confirmacao_senha"],
      [validar_senha,validar_confirmacao_senha]
    )
    if body_invalido:
        return jsonify(body_invalido), 400
    logger.info(f"Chamada recebida com parâmetros {body.keys()}")
    token_esqueci_senha = body['token_esqueci_senha']
    senha = body['senha']
    usuario = u.Usuario.query.filter_by(token_esqueci_senha=token_esqueci_senha).first()
    if not usuario or validar_token(usuario) is False:
        return {"erro": "token inválido"}, 400
    usuario.token_esqueci_senha = None
    usuario.token_valido_ate = None
    usuario.senha = senha
    usuario.senha_alterada = True
    usuario.salvar()
    return {"mensagem": "senha alterada com sucesso"}, 201


@auth.token_required
def listar_jogos_steam(usuario):
    if not usuario.steam_id:
        return {"erro": "nenhuma conta da steam associada a este usuario"}, 400
    headers = {"x-webapi-key": config.STEAM_API_KEY}
    parametros = {
      "steamid": usuario.steam_id,
      "include_appinfo": True,
      "include_played_free_games": True
    }
    resposta = requests.get(
      'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/',
      headers=headers,
      params=parametros,
      timeout=15
    )
    return serializar_jogos(resposta.json()), 200
