from . import usuario_controller as uc
from..models import usuario
import mock
import secrets
import datetime
from freezegun import freeze_time

@freeze_time("2022-08-09")
def test_esqueci_senha():
  body ={
    "email": "teste@teste.com",
    "data_nascimento": "2000-01-01"
  }
  usuario_mock = mock.NonCallableMock(email = body["email"], data_nascimento = body["data_nascimento"])
  uc.validar_body = mock.Mock(return_value=None)
  filter_by_result = mock.NonCallableMock(first=mock.Mock(return_value=usuario_mock))
  request=mock.NonCallableMock(get_json=mock.Mock(return_value=body))
  usuario.Usuario=mock.NonCallableMock(query=mock.NonCallableMock(filter_by=mock.Mock(return_value=filter_by_result)))
  uc.validar_token=mock.Mock(return_value=False)
  secrets.token_hex = mock.Mock(return_value="token")

  resposta=uc.validar_usuario(request)

  assert resposta == ({"token": "token"+"16600032000"}, 201)
  uc.validar_body.assert_called_once_with(body,
    ["email", "data_nascimento"],
    [uc.validar_data_nascimento]
  )
  uc.validar_token.assert_called_once_with(usuario_mock)
  secrets.token_hex.assert_called_once()