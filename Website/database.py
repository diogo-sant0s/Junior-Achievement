from sqlalchemy import create_engine, Column, String, Integer, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
import uuid

# Banco SQLite
db = create_engine('sqlite:///database.db', echo=True)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)  # id autoincrementado
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    old_email = Column(String)  # campo para guardar o email anterior

# Cria tabela se não existir
Base.metadata.create_all(bind=db)

# ======== Atualiza tabela user para adicionar coluna old_email se não existir ========
inspector = inspect(db)
columns = [col['name'] for col in inspector.get_columns('user')]

if 'old_email' not in columns:
    with db.connect() as conn:
        conn.execute('ALTER TABLE user ADD COLUMN old_email VARCHAR')
        print("Coluna 'old_email' adicionada na tabela 'user'.")
else:
    print("Coluna 'old_email' já existe na tabela 'user'.")
