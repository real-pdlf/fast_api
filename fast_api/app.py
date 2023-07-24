from fastapi import FastAPI

from fast_api.schemas import UserSchema

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'salve! TwT'}


@app.post('/users/', status_code=201)
def create_user(user: UserSchema):
    return user
