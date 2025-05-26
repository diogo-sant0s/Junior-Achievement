from sqlalchemy import create_engine, Column, String, Integer, Float, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Banco SQLite
db = create_engine('sqlite:///database.db', echo=True)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    weight = Column(Float)  # Corrigido aqui
    height = Column(Float)  # Adicionado
    old_email = Column(String)

# Cria a tabela se não existir
Base.metadata.create_all(bind=db)

# Verificar colunas existentes na tabela
inspector = inspect(db)
columns = [col['name'] for col in inspector.get_columns('user')]

with db.connect() as conn:
    if 'old_email' not in columns:
        conn.execute(text('ALTER TABLE user ADD COLUMN old_email VARCHAR'))
        print("Coluna 'old_email' adicionada na tabela 'user'.")

    if 'weight' not in columns:
        conn.execute(text('ALTER TABLE user ADD COLUMN weight FLOAT'))
        print("Coluna 'weight' adicionada na tabela 'user'.")

    if 'height' not in columns:
        conn.execute(text('ALTER TABLE user ADD COLUMN height FLOAT'))
        print("Coluna 'height' adicionada na tabela 'user'.")
