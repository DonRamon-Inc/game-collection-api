from flask import Flask
from flask_cors import CORS

from .models.db import db
from .rotas import declarar_rotas
from . import config

def iniciar_app():
    app = Flask(__name__)

    configurar_app(app)
    CORS(app)
    db.init_app(app)
    declarar_rotas(app)

    return app

def configurar_app(app):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
