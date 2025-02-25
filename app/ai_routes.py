from flask_restx import Namespace, Resource, fields
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
from utils import split_by_comma_and_and
import os
import logging

# Configuração de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho do arquivo CSV
csv_path = os.getenv(
    "CSV_PATH",
    os.path.join(os.path.dirname(__file__), "data/movielist.csv"),
)

# Namespace para rotas de IA
api = Namespace("Rotas IA", description="Operações relacionadas ao processo de IA")


# Carrega o arquivo CSV e formata os dados
def load_csv_data():
    """
    Carrega os dados do arquivo CSV e formata a coluna 'winner'.

    Returns:
        pd.DataFrame: DataFrame contendo os dados carregados.
    """
    try:
        df = pd.read_csv(csv_path, delimiter=';')
        df['winner'] = df['winner'].apply(lambda x: 1 if x == 'yes' else 0)
        return df
    except Exception as e:
        logger.error(f"Erro ao carregar CSV: {e}")
        return None


# Inicialização dos modelos e codificadores
recommendation_model = None


# Treina o modelo de recomendação
def train_recommendation_model():
    """
    Treina o modelo de recomendação baseado em clustering KMeans.

    Returns:
        None
    """
    global recommendation_model
    df = load_csv_data()
    if df is None:
        return None
    features = df[['year', 'winner']].values
    recommendation_model = KMeans(n_clusters=2, random_state=42, n_init=10)
    recommendation_model.fit(features)


# Modelo para entrada no endpoint /predict-bad-movie
bad_movie_model = api.model("BadMoviePrediction", {
    "producer": fields.String(required=True, description="Nome do produtor"),
    "studio": fields.String(required=True, description="Nome do estúdio"),
})


# Rota para recomendação de filmes
@api.route("/recommendations")
class Recommendations(Resource):
    """Recomendações baseadas em padrões de premiações"""

    def get(self):
        """
        Retorna recomendações de filmes com base em padrões de premiações.

        Returns:
            dict: Cluster e lista de filmes recomendados.
        """
        try:
            global recommendation_model
            df = load_csv_data()
            if df is None:
                return {"error": "Erro ao carregar os dados CSV."}, 500

            features = df[['year', 'winner']].values
            if recommendation_model is None:
                train_recommendation_model()

            user_input = np.array([[2023, 8]])  # Exemplo: ano atual e número de prêmios
            cluster = recommendation_model.predict(user_input)
            movies_in_cluster = df[recommendation_model.labels_ == cluster[0]]['title'].tolist()

            return {
                "cluster": int(cluster[0]),
                "movies_in_cluster": movies_in_cluster,
                "message": "Recomendação gerada"
            }, 200
        except Exception as e:
            logger.error(f"Erro na recomendação de filmes: {e}")
            return {"error": str(e)}, 500


# Rota para prever se um filme é ruim
@api.route("/predict-bad-movie")
class PredictBadMovie(Resource):
    """Predição de filmes ruins baseada em produtor e estúdio"""

    @api.expect(bad_movie_model)
    def post(self):
        """
        Prever se o filme é ruim baseado no produtor e estúdio.

        Returns:
            dict: Resultado da predição.
        """
        try:
            data = api.payload
            producer = data.get("producer")
            studio = data.get("studio")

            if not producer or not studio:
                return {"error": "Parâmetros 'producer' e 'studio' são obrigatórios."}, 400

            df = load_csv_data()
            if df is None:
                return {"error": "Erro ao carregar dados para verificação."}, 500

            # Normaliza os dados para comparação
            df['producers'] = df['producers'].str.strip().str.lower()
            df['studios'] = df['studios'].str.strip().str.lower()
            producer = producer.strip().lower()
            studio = studio.strip().lower()

            # Conta combinações produtor-estúdio
            combination_counts = Counter()
            for _, row in df.iterrows():
                producers = split_by_comma_and_and(row['producers'])
                studios = split_by_comma_and_and(row['studios'])
                for producer_item in producers:
                    for studio_item in studios:
                        combination_counts[(producer_item, studio_item)] += 1

            combination = (producer, studio)
            if combination_counts[combination] > 1:
                return {"prediction": "Probabilidade de ser ruim"}, 200
            else:
                return {"prediction": "Não é provável ser ruim"}, 200

        except Exception as e:
            logger.error(f"Erro ao prever filme ruim: {e}")
            return {"error": str(e)}, 500
