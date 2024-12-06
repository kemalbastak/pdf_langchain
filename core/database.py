from core import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

DATABASE_URL = settings.DATABASE_URI

# Create a synchronous engine
engine = create_engine(DATABASE_URL, echo=True)

# Session factory for synchronous interactions
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
