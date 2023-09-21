from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import User
from fast_api.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()


@app.get('/')
def read_root():
    """returns a hello world message"""
    return {'message': 'Hello world! Im a root!'}


@app.get('/users/', response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """view all users registered in database"""
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    """view only one user, by his id"""
    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    else:
        return db_user


@app.post('/users/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):

    # checks if exists this user
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:   # if exists, raise
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )

    else:   # else, add him to database
        db_user = User(
            username=user.username, password=user.password, email=user.email
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    """update informations about one user, with his id"""

    # query
    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    else:
        db_user.username = user.username
        db_user.password = user.password
        db_user.email = user.email
        session.commit()
        session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """delete one user from the database, using his id"""
    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    else:
        session.delete(db_user)
        session.commit()
        return {'detail': 'User deleted'}
