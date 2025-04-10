from models import User
from sqlalchemy import select


def test_create_user(session):
    user = User(username='jose', email='teste@gmail.com', password='senha123')

    session.add(user)
    session.commit()
    # session.refresh(user)

    result = session.scalar(
        select(User).where(User.email == 'teste@gmail.com')
    )

    assert result.id == 1
