# Implementação do Docker-Compose para APIs de Desenvolvimento Locais


- Objetivos:
    - Criar essa documentação simplificada de como funciona a operação do docker-compose.
    - Melhorar a documentação por completo.
    - Publicar documentação.
    - Implementar o docker-compose.
    - Testar o docker-compose de forma local.
    - Testar comunicação do docker-compose com o hamachi para ver se funciona.
        - Isso permite centralizar os erros gerados, caso tenham, no meu PC, então sempre consigo ver os erros direto.
    - Disponibilizar para a equipe.


## Guia Passo a Passo para Criar uma API de Teste com Flask e PostgreSQL usando Docker Compose

### Introdução

Essa documentação foi elaborada para orientar no processo de criação de uma API de teste utilizando Flask, um framework web Python, juntamente com o banco de dados PostgreSQL, tudo isso empacotado em contêineres Docker gerenciados pelo Docker Compose.

O uso de contêineres Docker simplifica significativamente o processo de desenvolvimento, implantação e execução de aplicativos, garantindo a portabilidade e consistência do ambiente de desenvolvimento em diferentes sistemas operacionais.

Neste documento, será apresnetado como configurar um ambiente de desenvolvimento com Docker Compose, a criar uma API simples usando Flask e a integrá-la com um banco de dados PostgreSQL.


### Configuração do Projeto

#### Organização do Diretório

```bash
/app
    /config
		__init__.py
        database.py
    /models
        __init__.py
        usuarios_model.py
    .env
    app.py
/sql
    create_tables.sql
docker-compose.yml
Dockerfile
README.md
requirements.txt
```

#### Criação de um Aplicativo Flask

Vamos iniciar criando um aplicativo Flask para servir como nossa API. O exemplo a seguir baseia-se em parte na ideia de implementar uma arquitetura limpa para a programação, porém, é apenas um ponto de partida. Utilizaremos o SQLAlchemy para realizar consultas de forma simplificada.


##### app.py

Código principal da API, responsavel por criar as rotas e a inicializar.

```python
import time
from flask import Flask

import os
from dotenv import load_dotenv

from config.database import create_session
from models.usuarios_model import UsuariosModel

from typing import Optional, List



# Cria uma instância do aplicativo Flask
_app = Flask(__name__)



# Definição da rota de consulta de teste
@_app.route('/query')
def query():
    # Recupera a sessão para a consulta
    _session = create_session()


    with _session() as session:
        # Realiza a consulta no banco de dados
        _usuarios_model = (
            session.query(
                UsuariosModel
            )
            .all()
        )

        _usuarios_model: Optional[List[UsuariosModel]] = _usuarios_model


        # Extrai os resultados e salva em uma lista
        _usuarios_list = []

        for _usuario in _usuarios_model:
            _aux = {
                'id': _usuario.id, 
                'nome': _usuario.nome, 
                'email': _usuario.email, 
                'idade': _usuario.idade, 
                'cidade': _usuario.cidade
            }

            _usuarios_list.append(_aux)


        # Imprime a lista recuperada no terminal
        print(
            "\n\nLista de Usuários Registrados:\n"
            f"{_usuarios_list}\n"
            "\n\n"
        )

        return _usuarios_list



# Carrega as variáveis de ambiente
load_dotenv()



# Inicializa o aplicativo Flask
if __name__ == '__main__':
    # Adiciona um atraso de 10 segundos para garantir que o contêiner do PostgreSQL esteja pronto
    time.sleep(10)
    

    # Incialização da API
    _app.run(
        debug = True,  
        host = '0.0.0.0', 
        port = int(os.environ.get("PORT", 8000))
    )
```


##### database.py

#######################################################################################

```python
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
```


##### usuarios_model.py

```python
from sqlalchemy import Column, Integer, String, Sequence
from config import Base


class UsuariosModel(Base):
    """
        Definição da tabela
    """
    __tablename__ = 'usuarios'

    id = Column(
        Integer, 
        Sequence('usuarios_id_seq'),
        primary_key = True, 
        autoincrement = True
    )

    nome = Column(String(100), unique = False, nullable = True)
    email = Column(String(100), unique = True, nullable = True)
    idade = Column(Integer, unique = False, nullable = True)
    cidade = Column(String(100), unique = False, nullable = True)
```


##### .env

```bash
PORT = 8000

DATABASE_URL='postgresql://seu_usuario:sua_senha@db/nome_do_banco_de_dados'
```


##### create_tables.sql

```sql
-- Criação da tabela para o exemplo
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    idade INTEGER,
    cidade VARCHAR(100)
);


-- Inserção de dados de exemplo
INSERT INTO usuarios (nome, email, idade, cidade)
VALUES 
    ('Maria Oliveira', 'maria@example.com', 25, 'Rio de Janeiro'),
    ('Pedro Santos', 'pedro@example.com', 35, 'Salvador'),
    ('Ana Costa', 'ana@example.com', 28, 'Belo Horizonte');
```


##### requirements.txt

```text
Flask==2.3.3
SQLAlchemy==2.0.20
psycopg2-binary==2.9.7  # Para interagir com o PostgreSQL
python-dotenv==1.0.0
```


#### Criação do Dockerfile


""""
  Continuar aqui
""""


2. **Crie o Dockerfile**: Agora, você precisa criar um Dockerfile para empacotar sua aplicação Flask e suas dependências.

```dockerfile
# Use a imagem base do Python 3.9.13
FROM python:3.9.13

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos de dependências para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install -r requirements.txt

# Copie todo o conteúdo do diretório local para o diretório de trabalho no contêiner
COPY . .

# Exponha a porta em que o servidor GraphQL estará em execução
EXPOSE 8000

# Comando para iniciar o servidor GraphQL (substitua pelo comando correto do seu aplicativo)
CMD ["python", "app/main.py"]
```

3. **Crie o arquivo requirements.txt**: Este arquivo deve conter as dependências do seu aplicativo Flask.

```text
Flask==2.3.3
Flask-GraphQL==2.0.1
SQLAlchemy==2.0.20
psycopg2-binary==2.9.7  # Para interagir com o PostgreSQL
graphene==2.1.9
requests==2.31.0
python-dotenv==1.0.0
unidecode==1.3.6
firebase-admin==6.2.0
pandas==2.1.2
apscheduler==3.10.4
```

4. **Crie o arquivo docker-compose.yml**: O Docker Compose é uma ferramenta para definir e executar aplicativos Docker com vários contêineres.

```yml
version: '3'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
  db:
    image: postgres
    environment:
      POSTGRES_DB: nome_do_banco_de_dados
      POSTGRES_USER: seu_usuario
      POSTGRES_PASSWORD: sua_senha
    ports:
      - "5432:5432"
```

5. **Construa e execute o contêiner**: Com todos os arquivos configurados, você pode construir e executar o contêiner usando o Docker Compose. No diretório onde estão seus arquivos (Dockerfile, requirements.txt, app.py e docker-compose.yml), execute:

```bash
docker-compose up --build
```

Isso irá criar e iniciar os contêineres do PostgreSQL e do Flask. Sua API Flask estará disponível em `http://localhost:5000`. Certifique-se de ajustar as configurações de conexão do banco de dados no seu aplicativo Flask de acordo com as configurações do contêiner PostgreSQL.


<sub>Ultima atualização 24/04/2024.</sub>
