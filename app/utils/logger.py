import json

from datetime import datetime

class Logger:
  def __init__(self, origem):
    self._origem = origem

  def _pegar_hora_atual(self):
    return datetime.now().isoformat(timespec='seconds')

  def _imprimir_log(self, tipo_log, msg):
    data_atual = self._pegar_hora_atual()
    conteudo = json.dumps(
      {
        "timestamp": data_atual,
        "severidade": tipo_log,
        "origem": self._origem,
        "mensagem": msg
      },
      ensure_ascii=False
    )
    print(conteudo)

  def info(self, msg):
    self._imprimir_log('INFO', msg)

  def warning(self, msg):
    self._imprimir_log('WARNING', msg)

  def error(self, msg):
    self._imprimir_log('ERROR', msg)
