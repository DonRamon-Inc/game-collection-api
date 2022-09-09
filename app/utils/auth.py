from functools import wraps
from flask import request
from sqlalchemy import exc as sql_exc
import jwt
from ..models import usuario as u
from .. import config

def token_required(function):
    @wraps(function)
    def decorated(request):
        token_autenticacao = request.headers.get('Authorization').split()[-1]
        dados_header = jwt.get_unverified_header(token_autenticacao)

        if not token_autenticacao:
            return {'mensagem': 'Token não definido'}, 401

        try:
            dados_usuario = jwt.decode(
              token_autenticacao, config.SECRET_KEY, algorithms=[dados_header['alg']]
            )
            usuario_atual = u.Usuario.query.filter_by(id=dados_usuario['sub']).one()
        except (jwt.DecodeError, sql_exc.NoResultFound):
                return {'mensagem': 'Token invalido'}, 401

        return function(request, usuario_atual)
    return decorated
