import os

class Config:
    """
    Classe de configuração padrão para a aplicação.

    Atributos:
        SQLALCHEMY_DATABASE_URI (str): URI do banco de dados, configurada pelo ambiente ou com valor padrão.
        FLASK_ENV (str): Ambiente de execução do Flask, podendo ser 'development', 'production', etc.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Desabilita o rastreamento de modificações do SQLAlchemy para melhorar desempenho.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data/database.db")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """
    Classe de configuração para o ambiente de testes.

    Atributos:
        SQLALCHEMY_DATABASE_URI (str): URI do banco de dados em memória, usada exclusivamente para testes.
        TESTING (bool): Habilita o modo de teste no Flask.
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:?check_same_thread=False"
    TESTING = True
