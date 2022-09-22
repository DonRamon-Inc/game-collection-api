import re
from datetime import datetime

from ..models import usuario as u

def validar_parametros_obrigatorios(body, parametros_obrigatorios):
    parametros_vazios = []
    for parametro in parametros_obrigatorios:
        if (parametro not in body) or (body[parametro] == ""):
            parametros_vazios.append(parametro)
    return parametros_vazios

def validar_email(body):
    email = body["email"]
    email_regex = r"^\w+([\.!#$%&'*\/=?^_+\-`{|}~]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
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
    senha_regex_letra_minuscula = r"[a-z]"
    senha_regex_letra_maiuscula = r"[A-Z]"
    senha_regex_numeros = r"\d"
    senha_regex_caractere_especial = r"[!@#$%&\+\-_*\/=\\\s'`~´:?<>.,;{}()[\]]"

    if 8 > len(senha) < 100:
        return 'Senha inválida. Sua senha deve conter entre 8 a 100 caracteres'
    if re.search(senha_regex_numeros,senha) is not None:
        if re.search(senha_regex_letra_minuscula,senha) is not None:
            if re.search(senha_regex_letra_maiuscula,senha) is not None:
                if re.search(senha_regex_caractere_especial,senha) is not None:
                    return None
    return "Senha inválida. A senha precisa conter, oito ou mais caracteres " +\
        "com uma combinação de letras, números e símbolos"

def validar_confirmacao_senha(body):
    if body["senha"] != body["confirmacao_senha"]:
        return "As senhas informadas não coincidem"
    return None

def validar_data_nascimento(body):
    data_nascimento = body["data_nascimento"]
    try:
        data_formatada = datetime.strptime(data_nascimento, r"%Y-%m-%d")
        if data_formatada.year > (datetime.now().year - 13):
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
    if token_timestamp < datetime.utcnow():
        return False
    return True
