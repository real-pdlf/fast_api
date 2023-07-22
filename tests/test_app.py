from fastapi.testclient import TestClient

from fast_api.app import app

client = TestClient(app)


def test_root_deve_retornar_200_e_salve():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'salve! TwT'}
