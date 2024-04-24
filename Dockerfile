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