
import pytest
from src.fast_zero.app import app
from fastapi.testclient import TestClient

@pytest.fixture()  #Boas praticas
def client():
    return TestClient(app)

