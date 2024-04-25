# Guia Passo a Passo para Criar uma API de Teste com Flask e PostgreSQL usando Docker Compose

## Introdução

Essa documentação visa guiar o processo de criação de uma API de teste utilizando Flask, um framework web Python, juntamente com o banco de dados PostgreSQL.

O uso de contêineres Docker simplifica significativamente o processo de desenvolvimento, implantação e execução de aplicativos, garantindo a portabilidade e consistência do ambiente de desenvolvimento em diferentes sistemas operacionais.

Neste documento, será apresentado como configurar um ambiente de desenvolvimento com Docker Compose, a criar uma API simples usando Flask e a integrá-la com um banco de dados PostgreSQL.


## Configuração do Projeto

### Estrutura do Diretório

- `/app`: Contém os arquivos relacionados à aplicação Flask.
    - `/config`: Consigurações da aplicação, incluindo a conexão com o banco de dados.
    - `/models`: Definição dos modelos de dados da aplicação.
    - `.env`: Arquivo de configuração das variáveis de ambiente.
    - `app.py`: Ponto de entrada da aplicação Flask.
- `/sql`: Arquivos SQL para inicialização do banco de dados.
- `docker-compose.yml`: Configuração do Docker Compose para orquestrar os contêineres.
- `Dockerfile`: Configuração para construir a imagem do contêiner da aplicação.
- `README.md`: Documentação principal do projeto.
- `requirements.txt`: Lista de dependências do projeto.


### Criação de um Aplicativo Flask

Inicialmente criamos uma aplicação Flask simples, que apenas realiza uma consulta em um banco de dados retornando os usuários cadastrados no sistema.
Os códigos a seguir apresentam a aplicação construida utilizando a estrutura do diretório apresentada.

Começando pelos extremos da construção da aplicação, primeiro definimos a criação das tabelas e de dos dados de teste que utilizaremos na consulta da aplicação.

Código SQL utilizado no exemplo, localizado em `/sql` no diretório:
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

Esse código SQL cria uma tabela chamada `usuarios` e insere três dados nessa tabela.


Após definirmos o banco de dados que será utilizado na aplicação é necessário mapear a tabela dentro da aplicação, esse mapeamento é necessário pois o pacote Python que será utilizado, nomeado de `SQLAlchemy`, utiliza esse mapeamento para realizar as consultas e inserções no banco de dados PostgreSQL.

Mapeamento da tabela dentro da aplicação, localizado em `/app/models` no diretório:
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


Após mapearmos a tabela dentro da aplicação, agora será necessário criar o arquivo de código que será utilizado para conectarmos a aplicação ao banco de dados para realizarmos a consulta.

Código para criar a sessão do banco de dados para consulta, localizado em `/app/config` no diretório:
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


Depois de criamos a conexão com o banco de dados resta criar a interface da aplicação Flask, que será responsável por executar a aplicação, definindo as rotas das consultas para a versão web.

Código de entrada da aplicação Flask, localizado em `/app/app.py` no diretório:
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


Após configurarmos a rota, o corpo da aplicação Flask está praticamente pronta, restando a construção das dependências da aplicação e construção e execução dos contêineres que serão responsaveis por colocar a aplicação para funcionar.

Após a construção da aplicação é necessário definir as variáveis de ambiente que irá conter as informações para a conexão com o banco de dados outras informações necessárias para a aplicação.

```bash
PORT = 8000

DATABASE_URL='postgresql://seu_usuario:sua_senha@db/nome_do_banco_de_dados'
```


## Criação das Dependências da Aplicação Flask (requirements.txt)

As dependências do projeto são listadas no arquivo `requirements.txt` e são necessárias para o funcionamento correto da aplicação Flask. Aqui está a lista das dependências e suas finalidades:

- Flask==2.3.3: Framework web utilizado para construir a aplicação.
- SQLAlchemy==2.0.20: ORM (Object-Relational Mapping) utilizado para interagir com o banco de dados PostgreSQL.
- psycopg2-binary==2.9.7: Driver PostgreSQL para Python, necessário para realizar operações de banco de dados.
- python-dotenv==1.0.0: Biblioteca para carregar variáveis de ambiente a partir de um arquivo `.env`.


## Construção e Execução dos Contêineres

### Construção do Dockerfile

O Dockerfile define as instruções para construir a imagem do contêiner que executará a aplicação Flask.

```dockerfile
# Use a imagem base do Python 3.9.13
FROM python:3.9.13


# Define o diretório de trabalho dentro do contêiner
WORKDIR /app


# Copie os arquivos de dependências para o diretório de trabalho
COPY requirements.txt .


# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt


# Copie todo o conteúdo do diretório local para o diretório de trabalho no contêiner
COPY . .


# Exponha a porta em que o servidor GraphQL estará em execução
EXPOSE 8000


# Comando para iniciar o aplicativo quando o contêiner for iniciado
CMD ["python", "app/app.py"]
```

Aqui está uma explicação rápida sobre as etapas:

- `FROM python:3.9.13`: Usa a imagem base do Python 3.9.13 como ponto de partida.
- `WORKDIR /app`: Define o diretório de trabalho dentro do contêiner como `/app`.
- `COPY requirements.txt .`: Copia o arquivo `requirements.txt` para o diretório de trabalho.
- `RUN pip install --no-cache-dir -r requirements.txt`: Instala as dependências do projeto.
- `COPY . .`: Copia o restante do conteúdo do diretório local para o diretório de trabalho no contêiner.
- `EXPOSE 8000`: Expõe a porta em que o servidor Flask estará em execução.
- `CMD ["python", "app/app.py"]`: Comando para iniciar o aplicativo quando o contêiner for iniciado.


### Construção do Docker Compose (docker-compose.yml)

O Docker Compose é uma ferramenta que permite definir e executar aplicativos Docker com vários contêineres. Ele simplifica o processo de orquestração de contêineres, permitindo configurar e gerenciar vários serviços em um único arquivo YAML.

```yml
version: '1'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: nome_do_banco_de_dados
      POSTGRES_USER: seu_usuario
      POSTGRES_PASSWORD: sua_senha
    
    volumes:
      - ./sql:/docker-entrypoint-initdb.d

    ports:
      - "5432:5432"

    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U seu_usuario -d nome_do_banco_de_dados"]
      interval: 5s
      retries: 5

  web:
    build: .
    ports:
      - "8000:8000"

    depends_on:
      - db
```

Aqui está uma explicação rápida sobre as etapas:

- `version: '1'`: Indica a versão do formato do arquivo Docker Compose. No caso, estamos usando a versão 1.

- `services`: Define os serviços que compõem a aplicação. Neste caso, temos dois serviços: `db` (banco de dados PostgreSQL) e `web` (aplicação Flask).

- Serviço `db`:

    - `image: postgres:15`: Especifica a imagem Docker a ser usada para o serviço `db`. Neste caso, estamos usando a imagem oficial do PostgreSQL na versão 15.

    - `environment`: Define as variáveis de ambiente necessárias para configurar o banco de dados PostgreSQL. Aqui, estamos definindo o nome do banco de dados (`POSTGRES_DB`), o nome de usuário (`POSTGRES_USER`) e a senha (`POSTGRES_PASSWORD`).

    - `volumes`: Mapeia o diretório local `./sql` para o diretório `/docker-entrypoint-initdb.d` dentro do contêiner do banco de dados PostgreSQL. Isso permite que arquivos SQL sejam executados automaticamente durante a inicialização do banco de dados.

    - `ports`: Mapeia a porta 5432 do contêiner PostgreSQL para a porta 5432 do host. Isso permite que a aplicação Flask se conecte ao banco de dados.

    - `healthcheck`: Define um teste de saúde para verificar se o contêiner do PostgreSQL está pronto para aceitar conexões. Neste caso, estamos usando o comando `pg_isready` para verificar se o banco de dados está pronto.

- Serviço `web`:

    - `build: .`: Indica que o Docker deve construir a imagem do contêiner para o serviço `web` usando o Dockerfile localizado no diretório atual (`.`).

    - `ports`: Mapeia a porta 8000 do contêiner da aplicação Flask para a porta 8000 do host. Isso permite acessar a API Flask a partir do navegador ou de outras aplicações.

    - `depends_on`: Define a dependência do serviço `web` em relação ao serviço `db`. Isso garante que o contêiner do banco de dados seja iniciado antes do contêiner da aplicação Flask.

Essas são as principais configurações presentes no arquivo docker-compose.yml. Ele define a estrutura e as configurações dos contêineres necessários para executar a aplicação Flask com o banco de dados PostgreSQL.


### Execução dos Contêineres

Com todos os arquivos configurados, você pode construir e executar o contêiner usando o Docker Compose. No diretório onde estão seus arquivos (Dockerfile, requirements.txt e docker-compose.yml), execute:

```bash
docker-compose up --build
```

Isso irá criar e iniciar os contêineres do PostgreSQL e do Flask. Sua API Flask estará disponível em `http://localhost:5000`.


<sub>Ultima atualização 25/04/2024.</sub>
