from fastapi import FastAPI
from fastapi.testclient import TestClient
from server.main import app
import pytest

client = TestClient(app=app)


# Test Team Types methods in main.py

# Test get method


def test_get_team_types() -> None:
    """
    Tests that the team types are returned correctly.
    :return: None
    """
    response = client.get('/team_types/')

    assert response.status_code == 200
    assert response.json() == [{"team_type_id": 1,
                                "team_type_name": "Undergrad",
                                "eligible": True},
                               {"team_type_id": 2,
                                "team_type_name": "Grad",
                                "eligible": False}]
