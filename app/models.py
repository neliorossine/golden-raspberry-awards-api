import os
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Session
from utils import split_by_comma_and_and

# Base para os modelos SQLAlchemy
Base = declarative_base()

class Movie(Base):
    """
    Representa a tabela 'movies' no banco de dados.
    """
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    studios = Column(Text)
    producer = Column(String, nullable=False)
    winner = Column(String)


def populate_data(db_session: Session):
    """
    Popula a tabela 'movies' com os dados do arquivo CSV.
    """
    # Caminho do arquivo CSV
    csv_path = os.getenv(
        "CSV_PATH",
        os.path.join(os.path.dirname(__file__), "data/movielist.csv"),
    )
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_path}")

    # Carrega os dados do CSV em um DataFrame do pandas
    try:
        df = pd.read_csv(csv_path, sep=";")
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo CSV: {e}")

    # Contador para novos registros
    new_records = 0

    # Itera sobre cada linha do CSV
    for _, row in df.iterrows():
        # Normaliza os produtores
        producers = split_by_comma_and_and(str(row.get("producers", "")))

        # Normaliza o campo 'winner' (padrão: 'yes' ou 'no')
        winner = "yes" if str(row.get("winner", "")).strip().lower() == "yes" else "no"

        for producer in producers:
            # Verifica se o registro já existe no banco
            exists = db_session.query(Movie).filter_by(
                year=int(row["year"]),
                title=row["title"],
                producer=producer,
                winner=winner,
            ).first()

            # Adiciona o registro se ele ainda não existir
            if not exists:
                movie = Movie(
                    year=int(row["year"]),
                    title=row["title"],
                    studios=row.get("studios", ""),
                    producer=producer,
                    winner=winner,
                )
                db_session.add(movie)
                new_records += 1

    # Confirma as alterações no banco
    db_session.commit()
    print(f"{new_records} novos registros adicionados ao banco de dados.")
