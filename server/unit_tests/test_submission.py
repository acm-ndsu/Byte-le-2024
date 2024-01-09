from fastapi import FastAPI
from fastapi.testclient import TestClient
from server.main import app
import pytest

client = TestClient(app=app)


# Test Submission methods in main.py

# Test post method


def test_post_submission() -> None:
    """
    Tests posting a submission via the URL.
    :return: None
    """
    response = client.post('/submission/',
                           json={"team_uuid": '1',
                                 "submission_id": 2,
                                 "submission_time": "2000-10-31T01:30:00-05:00",
                                 "file_txt": 'test'}
                           )
    assert response.status_code == 200
    assert response.json() == {"submission_id": 2,
                               "submission_time": "2000-10-31T06:30:00Z",
                               "file_txt": "test"}


# Test get methods

def test_get_submission() -> None:
    """
    Tests getting a submission via the submission id and team uuid in the URL.
    :return: None
    """
    response = client.get('/submission?submission_id=1&team_uuid=1')
    assert response.status_code == 200
    assert response.json() == {"submission_id": 1,
                               "submission_time": "2000-10-31T06:30:00Z",
                               "file_txt": "test",
                               "team": {"uni_id": 1,
                                        "team_type_id": 1,
                                        "team_name": "Noobs"},
                               "submission_run_infos": [{"submission_run_info_id": 1,
                                                         "run_id": 1,
                                                         "submission_id": 1,
                                                         "error_txt": "error",
                                                         "player_num": 1,
                                                         "points_awarded": 100,
                                                         "run": {"run_id": 1,
                                                                 "tournament_id": 1,
                                                                 "run_time": "2000-10-31T06:30:00Z",
                                                                 "seed": 1,
                                                                 "results": "test"}}]}


def test_get_submissions() -> None:
    """
    Tests getting all submissions given a team uuid in the URL.
    :return: None
    """
    response = client.get('/submissions?team_uuid=1')
    assert response.status_code == 200
    assert response.json() == [
        {
            "submission_id": 1,
            "submission_time": "2000-10-31T06:30:00Z",
            "file_txt": "test",
            "team": {
                "uni_id": 1,
                "team_type_id": 1,
                "team_name": "Noobs"
            },
            "submission_run_infos": [
                {
                    "submission_run_info_id": 1,
                    "run_id": 1,
                    "submission_id": 1,
                    "error_txt": "error",
                    "player_num": 1,
                    "points_awarded": 100,
                    "run": {
                        "run_id": 1,
                        "tournament_id": 1,
                        "run_time": "2000-10-31T06:30:00Z",
                        "seed": 1,
                        "results": "test"
                    }
                }
            ]
        },
        {
            "submission_id": 2,
            "submission_time": "2000-10-31T06:30:00Z",
            "file_txt": "test",
            "team": {
                "uni_id": 1,
                "team_type_id": 1,
                "team_name": "Noobs"
            },
            "submission_run_infos": []
        }
    ]


# Test read nonexistent submission/s

def test_get_nonexistent_submission() -> None:
    """
    Tests that a non-existent submission cannot be retrieved; raises an error.
    :return: None
    """
    with pytest.raises(IndexError):
        client.get('/submission?submission_id=2&team_uuid=2')
