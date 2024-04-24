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

É possível criar um contêiner Docker que armazene uma API Flask junto com um banco de dados PostgreSQL. Aqui está uma abordagem básica de como você pode fazer isso:

1. **Crie uma aplicação Flask**: Comece criando um aplicativo Flask que atue como sua API.

```py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://seu_usuario:sua_senha@endereco_do_banco_de_dados/nome_do_banco_de_dados'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do SQLAlchemy
db = SQLAlchemy(app)

# Definição do modelo da tabela (se necessário)
class Exemplo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

```

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
