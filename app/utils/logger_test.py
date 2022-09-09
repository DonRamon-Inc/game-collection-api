from . import logger

import builtins
import json
from datetime import datetime
from freezegun import freeze_time

import pytest
import mock

@pytest.fixture(autouse=False)
def run_around_tests():
  print_fn = builtins.print
  yield
  builtins.print = print_fn

@pytest.fixture
def logger_instancia():
  return logger.Logger(__file__)

def test_logger_info_deve_chamar_funcao_imprimir_log(logger_instancia):
  mensagem = "hello world"
  logger_instancia._imprimir_log = mock.Mock()

  resposta = logger_instancia.info(mensagem)

  assert resposta is None
  logger_instancia._imprimir_log.assert_called_once_with('INFO', mensagem)

def test_logger_warning_deve_chamar_funcao_imprimir_log(logger_instancia):
  mensagem = "hello world"
  logger_instancia._imprimir_log = mock.Mock()

  resposta = logger_instancia.warning(mensagem)

  assert resposta is None
  logger_instancia._imprimir_log.assert_called_once_with('WARNING', mensagem)

def test_logger_error_deve_chamar_funcao_imprimir_log(logger_instancia):
  mensagem = "hello world"
  logger_instancia._imprimir_log = mock.Mock()

  resposta = logger_instancia.error(mensagem)

  assert resposta is None
  logger_instancia._imprimir_log.assert_called_once_with('ERROR', mensagem)

@freeze_time("2022-09-09")
def test_imprimir_log_deve_imprimir_mensagem_severidade_e_timestamp_do_log(logger_instancia):
  mensagem = "hello world"
  severidade = "INFO"
  builtins.print = mock.Mock()

  resposta = logger_instancia._imprimir_log(severidade, mensagem)

  assert resposta is None
  log = json.dumps(
    {
      "timestamp": "2022-09-09T00:00:00",
      "severidade": severidade,
      "origem": __file__,
      "mensagem": mensagem
    },
    ensure_ascii=True
  )
  builtins.print.assert_called_once_with(log)
