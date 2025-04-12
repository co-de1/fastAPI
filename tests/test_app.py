from http import HTTPStatus

import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
)


def test_read_root_ok(client):
    # client = TestClient(app)  # arrange
    response = client.get('/')  # act

    assert response.status_code == HTTPStatus.OK  # assert (return)
    assert response.json() == {'message': 'Ola, mundoo'}