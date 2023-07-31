from sqlalchemy import select

from fast_api.models import User


def test_create_user(session):
    new_user = User(
        username='matheus', password='senha123', email='matheus@test'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'matheus'))

    assert user.username == 'matheus'
