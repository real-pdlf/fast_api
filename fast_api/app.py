from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import User
from fast_api.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []   # only for tests


@app.get('/')
def read_root():
    """returns a hello world message"""
    return {'message': 'Hello World! Im a root!'}


@app.get('/users/')
def read_users():
    """view all users registered in database"""
    return {'users': database}


@app.get('/users/{user_id}')
def read_user(user_id: int):
    return


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

    """
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return UserPublic(**user_with_id.model_dump())
    """


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    """update informations about one user, with his id"""
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    user_with_id = UserPublic(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    """delete one user from the database, using his id"""
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')
    del database[user_id - 1]
    return {'detail': 'User deleted'}
