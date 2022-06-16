import pytest


@pytest.fixture
def create_habit(authenticated_api_client):
    def _create_habit(data, expected_status_code=201):
        return authenticated_api_client.post(
            "/api/habits/", data, format="json", expected_status_code=expected_status_code
        )

    return _create_habit
