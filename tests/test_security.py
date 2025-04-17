from http import HTTPStatus

from src.fast_zero.security import create_access_token, settings
from jwt import decode


def test_jwt():
    data = {'sub': 'test@tets.com'}
    token = create_access_token(data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert result['exp']


def tes_jwt_invalid_token(client):
    response = client.delete(
        'users/1', headers={'Authorization': 'Bearer token-invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
