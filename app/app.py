import logging
from flask import Flask
from flask_restx import Api
from config import Config, TestConfig
from ai_routes import api as ai_namespace
from routes import api as app_namespace, init_db

# Configuração de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa o Flask
app = Flask(__name__)

# Configurações
env = app.config.get("FLASK_ENV", "development")
app.config.from_object(TestConfig if env == "testing" else Config)

# Inicializa o banco de dados
init_db(app.config["SQLALCHEMY_DATABASE_URI"])

# Configura o objeto Api
api = Api(app, title="API de Filmes", description="API para manipular informações de filmes e prêmios")

# Adiciona os namespaces
api.add_namespace(app_namespace, path="/app")
api.add_namespace(ai_namespace, path="/ai")

# Inicializa a aplicação
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
