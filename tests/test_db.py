from models import User, table_registry
from sqlalchemy import create_engine
from  sqlalchemy.orm import Session


def test_create_user():
    engine = create_engine('sqlite:///:memory:')

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:

        user = User(username='jose',
            email='teste@gmail.com',
            password='senha123'
        )

        session.add(user)
        session.commit()
        session.refresh(user)

    assert user.id == 1
