from functools import wraps
from sqlalchemy import exc as sql_exc
import jwt

from ..models import usuario as u
from .. import config

def token_required(function):
    @wraps(function)
    def decorated(contexto):
        try:
            token_type, token = contexto['request'].headers.get('Authorization').split()
            del token_type

            dados_header = jwt.get_unverified_header(token)
            dados_usuario = jwt.decode(
              token, config.SECRET_KEY, algorithms=[dados_header['alg']]
            )
            usuario_atual = u.Usuario.query.filter_by(id=dados_usuario['sub']).one()
            contexto['usuario'] = usuario_atual
        except (jwt.DecodeError, sql_exc.NoResultFound, ValueError):
            return {'mensagem': 'Token invalido'}, 401
        except AttributeError:
            return {'mensagem': 'Token não definido'}, 401
        else:
            return function(contexto)
    return decorated
