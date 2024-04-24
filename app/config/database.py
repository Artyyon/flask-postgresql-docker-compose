from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv

import os


# Declaração da base
Base = declarative_base()


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


# Recupera a URL de conexão com o banco de dados PostgreSQL a partir das variáveis de ambiente
DATABASE_URL = os.environ.get('DATABASE_URL')


# Cria sessão do banco de dados para consulta
def create_session() -> Session:
    """
        Método para criação de uma sessão do banco de dados para realização de consultas

        Returns:
            Uma sessão do banco de dados para realização da consulta
    """
    # Cria uma engine de conexão com o banco de dados usando a URL definida
    _engine = create_engine("postgresql://seu_usuario:sua_senha@db/nome_do_banco_de_dados", echo = True)


    # Cria uma classe de sessão (session) para interagir com o banco de dados
    _session = sessionmaker(bind = _engine)


    # Retorna a sessão criada
    return _session
