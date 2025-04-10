import pytest
from fastapi.testclient import TestClient
from models import table_registry, User
from src.fast_zero.app import app
from database import get_session
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.fast_zero.security import get_password_hash


@pytest.fixture()  # Boas praticas
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd = 'testtest'
    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash(pwd),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # MOnkey Patch

    return user
