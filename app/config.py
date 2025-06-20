# app/config.py

import os

class Config:
    """Configurações base da aplicação."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-bem-dificil'
    # SQLALCHEMY_DATABASE_URI = ...