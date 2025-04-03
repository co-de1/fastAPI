from http import HTTPStatus

import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
)

def test_read_root_ok(client):
    #client = TestClient(app)  # arrange
    response = client.get('/')  # act

    assert response.status_code == HTTPStatus.OK  # assert (return)
    assert response.json() == {'message': 'Ola, mundoo'}


def test_create_user(client):
    #client = TestClient(app) #arrange

    response = client.post(  # UserSchema
        '/users/',
        json={
            'username': 'testeusername',
            'password': 'password',
            'email': 'test@test.com',
        },
    )

    # Voltou o status code correto?
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testeusername',
        'email': 'test@test.com',
        'id': 1,
    }

def test_read_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'testeusername',
                'email': 'test@test.com',
                'id': 1,
            }
        ]
    }

def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'testeusername2',
            'email': 'test@test.com',
            'password': 'mynewpssword'
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert  response.json() == {
        'username': 'testeusername2',
        'email': 'test@test.com',
        'id': 1,
    }

def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User deleted'}
