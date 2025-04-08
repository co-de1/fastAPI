from sqlalchemy import create_engine
from src.fast_zero.settings import Settings
from sqlalchemy.orm import  Session

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session