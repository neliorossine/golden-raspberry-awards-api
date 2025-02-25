import logging
from flask import request
from flask_restx import Resource, Namespace, fields
from services import calculate_awards
from models import Base, Movie, populate_data
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool

# Configuração de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace
api = Namespace("Rotas Default", description="Operações relacionadas ao processo principal")

# Variáveis globais para o banco de dados
engine = None
Session = None

def init_db(database_uri):
    """
    Inicializa o banco de dados:
    - Cria as tabelas no banco, caso ainda não existam.
    - Popula os dados do arquivo CSV no banco, evitando duplicação de registros.

    Args:
        database_uri (str): URI do banco de dados.

    Exibe mensagens de sucesso ou erro durante a inicialização.
    """
    global engine, Session
    engine = create_engine(
        database_uri,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool  # Garante que o banco em memória seja compartilhado
    )
    Session = scoped_session(sessionmaker(bind=engine))

    # Criação das tabelas
    Base.metadata.create_all(bind=engine)
    logger.info("Tabelas criadas com sucesso!")

    # População dos dados
    session = Session()
    try:
        populate_data(session)  # Chama a função de população de dados
        logger.info("Dados populados com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao popular dados: {e}")
    finally:
        session.close()


@api.route("/health")
class HealthCheck(Resource):
    """Endpoint de verificação de saúde"""

    def get(self):
        """Verifica se o serviço está operacional"""
        return {"status": "healthy"}, 200


@api.route("/awards")
class Awards(Resource):
    """Endpoint para calcular e obter os intervalos entre prêmios consecutivos"""

    def get(self):
        """Calcula os intervalos mínimos e máximos entre prêmios consecutivos"""
        session = Session()
        try:
            movie_count = session.query(Movie).count()
            if movie_count == 0:
                return {"min": [], "max": []}, 200

            awards = calculate_awards(session)
            return awards, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()


@api.route("/details")
class Details(Resource):
    """Endpoint para obter os intervalos entre prêmios consecutivos, com HATEOAS"""

    def get(self):
        """Retorna os intervalos entre prêmios consecutivos, com suporte a HATEOAS"""
        session = Session()
        try:
            movie_count = session.query(Movie).count()
            if movie_count == 0:
                return {
                    "min": [],
                    "max": [],
                    "_links": {
                        "all_movies": {"href": "/movies", "method": "GET"}
                    }
                }, 200

            awards = calculate_awards(session)

            # Adiciona HATEOAS
            for award_type in ["min", "max"]:
                for item in awards[award_type]:
                    item["_links"] = {
                        "producer_details": {"href": f"/producers/{item['producer']}", "method": "GET"},
                        "movie_details": {
                            "href": f"/movies?year={item['previousWin']}&producer={item['producer']}",
                            "method": "GET"
                        }
                    }

            awards["_links"] = {"all_movies": {"href": "/movies", "method": "GET"}}
            return awards, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()


@api.route("/movies")
class MovieList(Resource):
    """Endpoint para listar filmes"""

    @api.expect(api.parser().add_argument("year", type=int, help="Filtrar por ano")
                               .add_argument("producer", type=str, help="Filtrar por produtor")
                               .add_argument("title", type=str, help="Filtrar por título"))
    def get(self):
        """Lista filmes com filtros opcionais"""
        session = Session()
        try:
            args = request.args
            query = session.query(Movie)

            if "year" in args:
                query = query.filter_by(year=int(args.get("year")))
            if "producer" in args:
                query = query.filter_by(producer=args.get("producer"))
            if "title" in args:
                query = query.filter_by(title=args.get("title"))

            movies = query.all()
            return [
                {
                    "title": movie.title,
                    "year": movie.year,
                    "studios": movie.studios,
                    "producer": movie.producer,
                    "winner": movie.winner,
                }
                for movie in movies
            ], 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()


@api.route("/producers/<string:producer>")
class ProducerDetails(Resource):
    """Endpoint para retornar informações detalhadas sobre um produtor"""

    def get(self, producer):
        """Retorna detalhes dos filmes de um produtor"""
        session = Session()
        try:
            movies = session.query(Movie).filter_by(producer=producer).all()
            if not movies:
                return {"error": f"Produtor '{producer}' não encontrado."}, 404

            return {
                "producer": producer,
                "movies": [
                    {
                        "title": movie.title,
                        "year": movie.year,
                        "studios": movie.studios,
                        "winner": movie.winner,
                    }
                    for movie in movies
                ],
            }, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()


@api.route("/winners")
class Winners(Resource):
    """Endpoint para retornar os filmes vencedores de um determinado ano"""

    winners_request = api.model("WinnersRequest", {
        "year": fields.Integer(required=True, description="Ano do qual queremos obter os vencedores")
    })

    @api.expect(winners_request)
    def post(self):
        """
        Retorna os filmes vencedores de um determinado ano.

        Parâmetros:
            - year (int): Ano para buscar os vencedores.
        """
        data = request.get_json()
        year = data.get("year")
        if not year:
            return {"error": "Parâmetro 'year' é obrigatório."}, 400

        session = Session()
        try:
            winners = session.query(Movie).filter_by(year=year, winner="yes").all()

            if not winners:
                return {"message": f"Não há vencedores registrados para o ano {year}."}, 404

            return {
                "year": year,
                "winners": [movie.title for movie in winners]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()
