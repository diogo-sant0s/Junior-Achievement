from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base
import uuid

# Banco SQLite
db = create_engine('sqlite:///database.db', echo=True)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

Base.metadata.create_all(bind=db)
