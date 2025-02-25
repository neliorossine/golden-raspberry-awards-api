import unittest
from unittest.mock import Mock
from services import calculate_awards


class TestServices(unittest.TestCase):
    """
    Testes de unidade para os serviços.
    """

    def test_calculate_awards_empty_data(self):
        """
        Testa o comportamento da função calculate_awards com dados vazios.
        Cenário positivo.
        """
        # Mock de sessão retornando dados vazios
        mock_session = Mock()
        mock_session.execute.return_value.mappings.return_value = []

        # Chama a função que calcula os prêmios
        result = calculate_awards(mock_session)

        # Verifica se o retorno contém listas vazias
        self.assertEqual(result, {"min": [], "max": []}, "O resultado deve conter listas vazias para 'min' e 'max' quando não há dados.")

    def test_calculate_awards_with_data(self):
        """
        Testa o comportamento da função calculate_awards com dados válidos.
        Cenário positivo.
        """
        mock_session = Mock()
        # Dados de teste com dois produtores e seus anos de vitórias
        mock_session.execute.return_value.mappings.return_value = [
            {"producer": "Producer 1", "year": 2000},
            {"producer": "Producer 1", "year": 2005},
            {"producer": "Producer 2", "year": 2010},
            {"producer": "Producer 2", "year": 2012},
        ]

        result = calculate_awards(mock_session)

        # Verifica o menor intervalo
        self.assertEqual(len(result['min']), 1, "O campo 'min' deve conter 1 entrada.")
        self.assertEqual(result['min'][0]['producer'], "Producer 2", "O produtor com o menor intervalo deve ser 'Producer 2'.")
        self.assertEqual(result['min'][0]['interval'], 2, "O menor intervalo deve ser 2.")
        self.assertEqual(result['min'][0]['previousWin'], 2010, "O 'previousWin' do menor intervalo deve ser 2010.")
        self.assertEqual(result['min'][0]['followingWin'], 2012, "O 'followingWin' do menor intervalo deve ser 2012.")

        # Verifica o maior intervalo
        self.assertEqual(len(result['max']), 1, "O campo 'max' deve conter 1 entrada.")
        self.assertEqual(result['max'][0]['producer'], "Producer 1", "O produtor com o maior intervalo deve ser 'Producer 1'.")
        self.assertEqual(result['max'][0]['interval'], 5, "O maior intervalo deve ser 5.")
        self.assertEqual(result['max'][0]['previousWin'], 2000, "O 'previousWin' do maior intervalo deve ser 2000.")
        self.assertEqual(result['max'][0]['followingWin'], 2005, "O 'followingWin' do maior intervalo deve ser 2005.")

    def test_calculate_awards_multiple_intervals(self):
        """
        Testa o comportamento da função calculate_awards quando há múltiplos intervalos iguais.
        Cenário positivo.
        """
        mock_session = Mock()
        # Dados de teste com múltiplos intervalos iguais para diferentes produtores
        mock_session.execute.return_value.mappings.return_value = [
            {"producer": "Producer 1", "year": 2000},
            {"producer": "Producer 1", "year": 2003},
            {"producer": "Producer 2", "year": 2005},
            {"producer": "Producer 2", "year": 2008},
            {"producer": "Producer 3", "year": 2010},
            {"producer": "Producer 3", "year": 2013},
        ]

        result = calculate_awards(mock_session)

        # Verifica múltiplos intervalos iguais no menor intervalo
        self.assertEqual(len(result['min']), 3, "O campo 'min' deve conter 3 entradas.")
        self.assertTrue(
            all(interval['interval'] == 3 for interval in result['min']),
            "Todos os intervalos no campo 'min' devem ser iguais a 3.",
        )

        # Verifica múltiplos intervalos iguais no maior intervalo
        self.assertEqual(len(result['max']), 3, "O campo 'max' deve conter 3 entradas.")
        self.assertTrue(
            all(interval['interval'] == 3 for interval in result['max']),
            "Todos os intervalos no campo 'max' devem ser iguais a 3.",
        )

    def test_calculate_awards_single_producer(self):
        """
        Testa o comportamento da função calculate_awards com um único produtor com múltiplas vitórias.
        Cenário positivo.
        """
        mock_session = Mock()
        # Dados de teste com um único produtor
        mock_session.execute.return_value.mappings.return_value = [
            {"producer": "Producer 1", "year": 2000},
            {"producer": "Producer 1", "year": 2010},
            {"producer": "Producer 1", "year": 2015},
        ]

        result = calculate_awards(mock_session)

        # Verifica o menor intervalo
        self.assertEqual(len(result['min']), 1, "O campo 'min' deve conter 1 entrada.")
        self.assertEqual(result['min'][0]['interval'], 5, "O menor intervalo deve ser 5.")

        # Verifica o maior intervalo
        self.assertEqual(len(result['max']), 1, "O campo 'max' deve conter 1 entrada.")
        self.assertEqual(result['max'][0]['interval'], 10, "O maior intervalo deve ser 10.")

    def test_calculate_awards_no_consecutive_wins(self):
        """
        Testa o comportamento da função calculate_awards quando não há vitórias consecutivas para nenhum produtor.
        Cenário negativo.
        """
        mock_session = Mock()
        # Dados de teste onde não há vitórias consecutivas
        mock_session.execute.return_value.mappings.return_value = [
            {"producer": "Producer 1", "year": 2000},
            {"producer": "Producer 2", "year": 2005},
            {"producer": "Producer 3", "year": 2010},
        ]

        result = calculate_awards(mock_session)

        # Verifica que os campos 'min' e 'max' estão vazios
        self.assertEqual(result['min'], [], "O campo 'min' deve ser vazio quando não há vitórias consecutivas.")
        self.assertEqual(result['max'], [], "O campo 'max' deve ser vazio quando não há vitórias consecutivas.")


if __name__ == "__main__":
    unittest.main()
