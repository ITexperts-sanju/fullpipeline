# tests/test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello this is out first devops pipeline!" in response.data
