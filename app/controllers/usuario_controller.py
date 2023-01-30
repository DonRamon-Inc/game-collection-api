from flask import request
from ..services import usuario_services as us

def cadastrar_usuario():
    return us.criar_usuario(contexto = {"request": request})

def logar_usuario():
    return us.logar_usuario(contexto = {"request": request})

def atualizar_senha():
    return us.atualizar_senha(contexto = {"request": request})

def auth_steam():
    return us.auth_steam(contexto = {"request": request})

def auth_steam_delete():
    return us.auth_steam_delete(contexto = {"request": request})

def validar_usuario():
    return us.validar_usuario(contexto = {"request": request})
