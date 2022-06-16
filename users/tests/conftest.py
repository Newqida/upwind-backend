import pytest


@pytest.fixture
def register_user(api_client):
    def _register_user(data, expected_status_code=201):
        return api_client.post(
            "/auth/register/", data, format="json", expected_status_code=expected_status_code
        )

    return _register_user
