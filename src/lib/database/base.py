from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.settings.base import settings

DATABASE_URL: str = (
    "postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}".format(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        name=settings.DB_NAME,
    )
)

engine: Engine = create_engine(DATABASE_URL)

session: sessionmaker[Session] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()
