from fast_api.schemas import UserPublic


def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello world! Im a root!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Geraldo',
            'email': 'geraldo@legal.com',
            'password': 'senha123',
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        'username': 'Geraldo',
        'email': 'geraldo@legal.com',
        'id': 1,
    }


def test_user_created(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Username already registered'}


def test_read_users(client):
    response = client.get('users/')
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_user_found(client, user):
    response = client.get(f'/users/{user.id}')
    assert response.status_code == 200
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_user_not_found(client):
    response = client.get('/users/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'buddie',
            'email': 'buddie@exemplo.com',
            'password': 'nova senha 321',
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'username': 'buddie',
        'email': 'buddie@exemplo.com',
        'id': 1,
    }


def test_not_updated(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'teste testilson',
            'email': 'test@test.com',
            'password': 'senha nova 123',
        },
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete(f'users/{user.id}')
    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}


def test_not_deleted(client):
    response = client.delete('users/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
