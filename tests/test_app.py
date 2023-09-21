from fastapi.testclient import TestClient

from fast_api.app import app

client = TestClient(app)


# def test_root_deve_retornar_200_e_salve():
#     response = client.get('/')
#     assert response.status_code == 200
#     assert response.json() == {'message': 'salve! TwT'}


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


def test_read_users():
    response = client.get('users/')
    assert response.status_code == 200
    assert response.json() == {
        'users': [
            {
                'username': 'Geraldo',
                'email': 'geraldo@legal.com',
                'id': 1,
            }
        ]
    }


def test_update_user():
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


def test_delete_user():
    response = client.delete('users/1')
    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}
