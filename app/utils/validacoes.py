import re
from datetime import datetime

from ..models import usuario as u

def validar_parametros_obrigatorios(body, parametros_obrigatorios):
    parametros_vazios = []
    for parametro in parametros_obrigatorios:
        if (parametro not in body) or (body[parametro] == ""):
            parametros_vazios.append(parametro)
    return parametros_vazios

def validar_limite_de_caracteres(body,limites):
    campos_longos = []
    for campo in body:
        if len(str(body[campo])) > limites[campo]:
            campos_longos.append(campo)
    if campos_longos:
        return campos_longos
    return None

def validar_excesso_espacamento_nome(body):
    body["nome"] = body["nome"].strip()
    regex_excesso_espacos = r"\s{2,}"
    if re.findall(regex_excesso_espacos, body["nome"]):
        body["nome"] = re.sub(regex_excesso_espacos," ",body["nome"])
    return body

def validar_email(body):
    email = body["email"]
    email_regex = r"^\w+([\.!#$%&'*\/=?^_+\-`{|}~]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if re.search(email_regex, email) is None:
        return "email invalido, favor verificar email"
    return None

def validar_email_duplicado(body):
    email = body["email"]
    email_valido = u.Usuario.query.filter_by(email = email).first()
    if email_valido:
        return "email ja cadastrado"
    return None

def validar_confirmacao_email(body):
    if body["email"] != body["confirmacao_email"]:
        return "os emails informados nao coincidem"
    return None

def validar_senha(body):
    senha = body["senha"]
    if not 8 <= len(senha) < 100:
        return "Senha inválida. Sua senha deve conter entre 8 a 100 caracteres"

    regex_letra_minuscula = r"[a-z]"
    regex_letra_maiuscula = r"[A-Z]"
    regex_numeros = r"\d"
    regex_caractere_especial = r"[!@#$%&\+\-_*\/=\\\s'`~´:?<>.,;{}()[\]]"
    senha_regex = [
        regex_numeros,
        regex_letra_maiuscula,
        regex_letra_minuscula,
        regex_caractere_especial
    ]

    for regex in senha_regex:
        if re.search(regex, senha) is None:
            return "senha invalida. a senha precisa conter, oito ou mais caracteres " +\
                "com uma combinação de letras, numeros e simbolos"
    return None

def validar_confirmacao_senha(body):
    if body["senha"] != body["confirmacao_senha"]:
        return "as senhas informadas nao coincidem"
    return None

def validar_data_nascimento(body):
    data_nascimento = body["data_nascimento"]
    try:
        data_formatada = datetime.strptime(data_nascimento, r"%Y-%m-%d")
        if data_formatada.year > (datetime.now().year - 13):
            return "e preciso ter mais de 13 anos para criar uma conta."
    except ValueError:
        return "formato de data invalido"
    return None

def validar_body(body, parametros_obrigatorios, validacoes=None):
    campos_invalidos = validar_parametros_obrigatorios(body, parametros_obrigatorios.keys())
    if campos_invalidos:
        return {"erro": f"campos nao preenchidos: {campos_invalidos}"}
    campos_longos = validar_limite_de_caracteres(body,parametros_obrigatorios)
    if campos_longos:
        return {"erro":f"limite de caracteres excedido em: {campos_longos}"}

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
