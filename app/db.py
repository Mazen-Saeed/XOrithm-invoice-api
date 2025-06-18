from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# the SQLAlchemy engine
engine = create_engine(
    settings.POSTGRE_URL,
    echo=True,
    future=True
)

# configured Session class
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)

# base class for ORM models
Base = declarative_base()
