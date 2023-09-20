from fastapi import FastAPI, HTTPException

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
def create_user(user: UserSchema):
    """add one new user to database"""
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return UserPublic(**user_with_id.model_dump())


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
