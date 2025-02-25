import unittest
from app import app
from routes import Session, init_db
from models import Movie


class TestRoutes(unittest.TestCase):
    """
    Testes de integração para os endpoints da API.
    """

    def setUp(self):
        """
        Configuração inicial para cada teste.
        """
        self.app = app.test_client()
        self.app.testing = True

        # Usando um banco de dados de teste separado
        self.session = Session()  # Aqui você pode configurar uma base de dados separada de teste
        self.session.query(Movie).delete()
        self.session.commit()

    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        self.session.query(Movie).delete()
        self.session.commit()
        self.session.close()

    def test_awards_empty_database(self):
        """
        Testa o comportamento do endpoint quando o banco de dados está vazio.
        """
        response = self.app.get('/app/awards')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['min'], [])
        self.assertEqual(data['max'], [])

    def test_awards_with_data(self):
        """
        Testa o comportamento do endpoint com dados no banco.
        """
        movies = [
            Movie(title="Movie 1", producer="Producer 1", year=2000, winner="yes"),
            Movie(title="Movie 2", producer="Producer 1", year=2005, winner="yes"),
            Movie(title="Movie 3", producer="Producer 2", year=2010, winner="yes"),
            Movie(title="Movie 4", producer="Producer 2", year=2012, winner="yes"),
        ]
        self.session.bulk_save_objects(movies)
        self.session.commit()

        response = self.app.get('/app/awards')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Verificar o menor intervalo
        self.assertEqual(len(data['min']), 1)
        self.assertEqual(data['min'][0]['producer'], "Producer 2")
        self.assertEqual(data['min'][0]['interval'], 2)

        # Verificar o maior intervalo
        self.assertEqual(len(data['max']), 1)
        self.assertEqual(data['max'][0]['producer'], "Producer 1")
        self.assertEqual(data['max'][0]['interval'], 5)

    def test_awards_multiple_producers_same_interval(self):
        """
        Testa o comportamento do endpoint quando múltiplos produtores têm o mesmo intervalo mínimo ou máximo.
        """
        movies = [
            Movie(title="Movie 1", producer="Producer 1", year=2000, winner="yes"),
            Movie(title="Movie 2", producer="Producer 1", year=2003, winner="yes"),
            Movie(title="Movie 3", producer="Producer 2", year=2005, winner="yes"),
            Movie(title="Movie 4", producer="Producer 2", year=2008, winner="yes"),
            Movie(title="Movie 5", producer="Producer 3", year=2010, winner="yes"),
            Movie(title="Movie 6", producer="Producer 3", year=2013, winner="yes"),
        ]
        self.session.bulk_save_objects(movies)
        self.session.commit()

        response = self.app.get('/app/awards')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Verificar múltiplos produtores com o mesmo menor intervalo
        self.assertEqual(len(data['min']), 3)
        self.assertTrue(
            all(interval['interval'] == 3 for interval in data['min'])
        )

        # Verificar múltiplos produtores com o mesmo maior intervalo
        self.assertEqual(len(data['max']), 3)
        self.assertTrue(
            all(interval['interval'] == 3 for interval in data['max'])
        )

    def test_get_details(self):
        """Testa o endpoint /app/details"""
        response = self.app.get('/app/details')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('min', json_data)
        self.assertIn('max', json_data)
        self.assertIn('_links', json_data)

    def test_get_producer_details(self):
        """Testa o endpoint /app/producers/<producer>"""
        producer = "Producer 1"
        response = self.app.get(f'/app/producers/{producer}')
        self.assertEqual(response.status_code, 404)  # Se o produtor não existir
        json_data = response.get_json()
        self.assertIn('error', json_data)

    def test_list_movies(self):
        """Testa o endpoint /app/movies"""
        response = self.app.get('/app/movies')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)  # Espera-se que retorne uma lista de filmes

    def test_get_winners(self):
        """Testa o endpoint /app/winners"""
        movie_2020 = Movie(title="Movie 2020", producer="Producer 1", year=2020, winner="yes")
        self.session.add(movie_2020)
        self.session.commit()

        # Teste para ano com vencedores
        response = self.app.post('/app/winners', json={'year': '2020'})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('winners', json_data)
        self.assertIn('Movie 2020', json_data['winners'])

        # Testar com ano sem vencedores
        response = self.app.post('/app/winners', json={'year': '2021'})
        self.assertEqual(response.status_code, 404)
        json_data = response.get_json()
        self.assertIn('message', json_data)
        self.assertEqual(json_data['message'], "Não há vencedores registrados para o ano 2021.")

    def test_recommend_movies(self):
        """Testa o endpoint /ai/recommendations"""
        response = self.app.get('/ai/recommendations')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('movies_in_cluster', json_data)
        self.assertIsInstance(json_data['movies_in_cluster'], list)

    def test_predict_bad_movie(self):
        """Testa o endpoint /ai/predict-bad-movie"""
        response = self.app.post('/ai/predict-bad-movie', json={
            'producer': 'Producer 1',
            'studio': 'Studio 1'
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('prediction', json_data)


if __name__ == '__main__':
    unittest.main()
