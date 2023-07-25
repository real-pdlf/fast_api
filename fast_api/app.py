from fastapi import FastAPI

from fast_api.schemas import UserSchema, UserPublic

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'salve! TwT'}


@app.post('/users/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema):
    return UserPublic(**user.model_dump())
