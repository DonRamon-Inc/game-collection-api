from flask import request
from functools import wraps
import jwt
from ..models.usuario import Usuario
from .. import config

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token_autenticacao = request.headers.get('Authorization').split()[-1]
    dados_header = jwt.get_unverified_header(token_autenticacao)

    if not token_autenticacao:
      return {'mensagem': 'Token não definido'}, 401

    try:
      dados_usuario = jwt.decode(token_autenticacao, config.SECRET_KEY, algorithms=[dados_header['alg']])
      usuario_atual = Usuario.query.filter_by(id=dados_usuario['sub']).one()
    except:
      return {'mensagem': 'Token invalido'}, 401

    return f(usuario_atual)
  return decorated
