import os

from flask import Flask
from .models.db import db
from .rotas import declarar_rotas


def iniciar_app():
  app = Flask(__name__)

  configurar_app(app)
  db.init_app(app)
  declarar_rotas(app)

  return app

def configurar_app(app):
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://")
