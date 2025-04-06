
import pytest
from src.fast_zero.app import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from models import table_registry
from  sqlalchemy.orm import Session

@pytest.fixture()  #Boas praticas
def client():
    return TestClient(app)

@pytest.fixture()
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)