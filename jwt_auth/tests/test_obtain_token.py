import json
from unittest.mock import patch

import pytest


pytestmark = pytest.mark.django_db


def _decode(response):
    return json.loads(response.content.decode("utf-8", errors="ignore"))


def test_getting_token_ok(authenticated_api_client, get_token):
    response = get_token(authenticated_api_client.user.email, "test123")

    assert "access_token" in response.data
    assert "refresh_token" in response.data


def test_getting_token_is_token(authenticated_api_client, get_token):
    response = get_token(authenticated_api_client.user.email, "test123")

    assert len(response.data["access_token"]) > 32
    assert len(response.data["refresh_token"]) > 32


def test_getting_token_with_incorrect_password(authenticated_api_client, get_token):
    response = get_token(
        authenticated_api_client.user.email, 'wrongPass', expected_status_code=401
    )
    
    assert "No active account found with the given credentials" in response.data["detail"]


@pytest.mark.parametrize(
    ("extract_token", "status_code"),
    [(lambda response: response.data["access_token"], 200),
     (lambda *args: "incorrectJWT", 401)],
)
def test_received_token_works(
    authenticated_api_client, get_token, api_client, extract_token, status_code
):
    token = extract_token(
        get_token(authenticated_api_client.user.email, "test123"))

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    api_client.get("/api/me/", expected_status_code=status_code)
