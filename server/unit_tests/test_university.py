from fastapi import FastAPI
from fastapi.testclient import TestClient
from server.main import app
import pytest

client = TestClient(app=app)


# Test University methods in main.py

# Test get method

def test_get_universities() -> None:
    """
    Tests that getting the universities in from the database works.
    :return: None
    """
    response = client.get('/universities/')

    assert response.status_code == 200
    assert response.json() == [{"uni_id": 1,
                                "uni_name": "NDSU"},
                               {"uni_id": 2,
                                "uni_name": "UND"}]
