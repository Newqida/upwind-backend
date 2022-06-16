import pytest
from freezegun import freeze_time

pytestmark = [pytest.mark.django_db, pytest.mark.freeze_time("2049-01-05")]


def test_refresh_token_ok(initial_token, refresh_token):
    response = refresh_token(initial_token["refresh_token"])
    assert 'access_token' in response.data
    assert 'refresh_token' in response.data


def test_refreshed_token_is_a_token(initial_token, refresh_token):
    response = refresh_token(initial_token["refresh_token"])

    assert len(response.data["access_token"]) > 32
    assert len(response.data["refresh_token"]) > 32


def test_refreshed_token_is_new_one(initial_token, refresh_token):
    response = refresh_token(initial_token["refresh_token"])

    assert response.data["access_token"] != initial_token["access_token"]


def test_refresh_token_fails_with_incorrect_previous_token(refresh_token):
    response = refresh_token(
        "some-invalid-previous-token", expected_status_code=401)

    assert response.data["code"] == "refresh_token_not_valid"


def test_token_is_not_allowed_to_refresh_if_expired(initial_token, refresh_token):
    with freeze_time("2049-02-05"):
        response = refresh_token(
            initial_token["refresh_token"], expected_status_code=400)

    assert "expired" in response.data["detail"]


def test_received_token_works(api_client, refresh_token, initial_token):
    token_response = refresh_token(initial_token["refresh_token"])
    token = token_response.data["access_token"]

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = api_client.get("/api/me/")
    assert response.status_code == 200
    assert response is not None
