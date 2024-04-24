from flask import Flask

import os
from dotenv import load_dotenv

from .config import create_session
from .models import UsuariosModel



# Cria uma instância do aplicativo Flask
_app = Flask(__name__)



# Definição da rota de consulta de teste
@_app.route('/query')
def query():
    # Recupera a sessão para a consulta
    _session = create_session()


    # Realiza a consulta no banco de dados
    _usuarios_model = (
        _session.query(
            UsuariosModel
        )
        .all()
    )


    # Extrai os resultados e salva em uma lista
    _usuarios_list = list

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



# Carrega as variáveis de ambiente
load_dotenv()



# Inicializa o aplicativo Flask
if __name__ == '__main__':
    # Incialização da API
    _app.run(
        debug = True,  
        host = '0.0.0.0', 
        port = int(os.environ.get("PORT", 8000))
    )
