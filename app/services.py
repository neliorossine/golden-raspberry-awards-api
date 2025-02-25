from sqlalchemy.sql import text
from collections import defaultdict


def calculate_awards(session):
    """
    Calcula os intervalos entre prêmios consecutivos para cada produtor.

    Parâmetros:
        session (Session): Sessão ativa do banco de dados.

    Retorna:
        dict: Um dicionário contendo os intervalos mínimos e máximos entre prêmios.
        O formato do resultado é:
        {
            "min": [
                {
                    "producer": "Produtor X",
                    "interval": 1,
                    "previousWin": 2001,
                    "followingWin": 2002
                },
                ...
            ],
            "max": [
                {
                    "producer": "Produtor Y",
                    "interval": 10,
                    "previousWin": 1990,
                    "followingWin": 2000
                },
                ...
            ]
        }

    Lógica:
        - Busca todos os produtores que venceram prêmios, juntamente com os anos de vitória.
        - Agrupa os anos de vitória por produtor.
        - Calcula os intervalos entre anos consecutivos de vitória para cada produtor.
        - Determina o menor e o maior intervalo encontrado.
        - Retorna os resultados organizados nos campos `min` e `max`.

    Exemplo de uso:
        >>> session = Session()
        >>> result = calculate_awards(session)
        >>> print(result)
    """
    # Consulta para obter os produtores vencedores e os anos de vitória
    query = session.execute(
        text(
            """
            SELECT producer, year 
            FROM movies 
            WHERE winner = 'yes'
            ORDER BY producer, year
            """
        )
    )

    # Agrupa os anos de vitória por produtor
    producer_awards = defaultdict(list)
    for row in query.mappings():
        producer_awards[row["producer"]].append(row["year"])

    # Calcula os intervalos entre prêmios consecutivos para cada produtor
    intervals = []
    for producer, years in producer_awards.items():
        for prev, curr in zip(years, years[1:]):
            intervals.append(
                {
                    "producer": producer,
                    "interval": curr - prev,
                    "previousWin": prev,
                    "followingWin": curr,
                }
            )

    # Determina os intervalos mínimos e máximos
    if intervals:
        min_interval_value = min(interval["interval"] for interval in intervals)
        max_interval_value = max(interval["interval"] for interval in intervals)

        min_intervals = [i for i in intervals if i["interval"] == min_interval_value]
        max_intervals = [i for i in intervals if i["interval"] == max_interval_value]
    else:
        min_intervals = []
        max_intervals = []

    # Retorna os resultados formatados
    return {"min": min_intervals, "max": max_intervals}
