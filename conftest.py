import pytest
from freezegun import freeze_time

from django.contrib.auth import get_user_model

from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from jwt_auth.utils import get_jwt

from users.tests.factories import UserFactory

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client():
    class APIClientWithUser(APIClient):
        user = UserFactory(is_active=True)

    client = APIClientWithUser()
    client.force_authenticate(user=client.user)
    return client


@pytest.fixture()
def custom_admin_client(db):
    from django.test.client import Client

    user = User.objects.create_superuser("user@user.com", "password1234")

    client = Client()
    client.login(email=user.email, password="password1234")
    return


@pytest.fixture
def authenticated_inactive_api_client():
    class APIClientWithUser(APIClient):
        user = UserFactory(is_active=False)

    client = APIClientWithUser()
    client.force_authenticate(user=client.user)
    return client


def pytest_configure():
    pytest.first_name = "first_name"
    pytest.last_name = "last_name"
    pytest.email = "test@gm.com"
    pytest.birth_date = "1999-01-01"
    pytest.password1 = "HARDpasw123@"
    pytest.password2 = "HARDpasw123@"
    pytest.wrong_password = "HARDpasw123"
    pytest.weak_password = "qwerty123"
    pytest.error_required_field = [ErrorDetail(
        string="This field is required.", code="required")]



@pytest.fixture
def get_token(authenticated_api_client):
    def _get_token(email, password, expected_status_code=201):
        return authenticated_api_client.post(
            "/token/",
            {"email": email, "password": password},
            format="json",
            expected_status_code=expected_status_code,
        )

    return _get_token

@pytest.fixture
def refresh_token(authenticated_api_client):
    def _refresh_token(token, expected_status_code=201):
        return authenticated_api_client.post(
            "/token/refresh/",
            {"refresh_token": token},
            format="json",
            expected_status_code=expected_status_code,
        )

    return _refresh_token

@pytest.fixture
def initial_token(authenticated_api_client):
    with freeze_time("2049-01-03"):
        return get_jwt(authenticated_api_client.user)

