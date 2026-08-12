from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

VERITABANI_URL = os.getenv("DATABASE_URL", "postgresql://sehermac@localhost/ecommerce")

if VERITABANI_URL.startswith("postgres://"):
    VERITABANI_URL = VERITABANI_URL.replace("postgres://", "postgresql://", 1)
    
engine = create_engine(VERITABANI_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
