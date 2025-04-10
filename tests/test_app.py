from http import HTTPStatus

import sys
import os

from src.fast_zero.schemas import UserPublic

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
)


def test_read_root_ok(client):
    # client = TestClient(app)  # arrange
    response = client.get('/')  # act

    assert response.status_code == HTTPStatus.OK  # assert (return)
    assert response.json() == {'message': 'Ola, mundoo'}


def test_create_user(client):
    # client = TestClient(app) #arrange

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
    assert response.json() == {'users': []}


def test_read_user_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'testeusername2',
            'email': 'test@test.com',
            'password': 'mynewpssword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testeusername2',
        'email': 'test@test.com',
        'id': 1,
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_invalid_id(client):
    response = client.delete('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_out_of_range(client):
    response = client.delete('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_put_user_invalid(client):
    response = client.put(
        '/users/0',
        json={  # Adicionando um JSON válido
            'username': 'new_name',
            'password': 'new_password',
            'email': 'new@email.com',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_put_user_out_of_range(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'new_name',
            'password': 'new_password',
            'email': 'new@email.com',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
