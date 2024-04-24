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
