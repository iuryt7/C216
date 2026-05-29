import os
import time
from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/faculdade",
)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

CURSOS_VALIDOS = {"GES", "GEC", "GET", "GEP"}


class Base(DeclarativeBase):
    pass


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    curso = Column(String, nullable=False)
    matricula = Column(Integer, nullable=False)


class CursoCounter(Base):
    __tablename__ = "curso_counters"

    curso = Column(String, primary_key=True)
    contador = Column(Integer, nullable=False, default=0)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def criar_tabelas(retries: int = 10, delay: int = 3) -> None:
    for tentativa in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            Base.metadata.create_all(bind=engine)
            print("✅ Tabelas criadas/verificadas com sucesso.")
            return
        except OperationalError as e:
            print(f"⏳ Banco não disponível (tentativa {tentativa}/{retries}): {e}")
            if tentativa < retries:
                time.sleep(delay)
    raise RuntimeError("Não foi possível conectar ao banco de dados após várias tentativas.")
