import pytest

from django.contrib.auth import get_user_model

from rest_framework.exceptions import ErrorDetail

from users.tests.factories import UserActivateAccountTokenFactory, UserFactory


User = get_user_model()

pytestmark = [pytest.mark.django_db]


def test_user_register_valid(register_user):
    data = {
        'first_name': pytest.first_name,
        'email': pytest.email,
        'password': pytest.password1,
    }

    response = register_user(data)

    expected_response = {
        'first_name': pytest.first_name,
        'email': pytest.email,
        'password': pytest.password1,
    }

    assert response.status_code == 201
    assert response.data == expected_response
    assert User.objects.filter(email=pytest.email).exists()


def test_user_register_already_exists(register_user):
    user = UserFactory(email='test@gm.com')
    data = {
        'first_name': pytest.first_name,
        'email': pytest.email,
        'password': pytest.password1,
    }
    response = register_user(data)

    expected_response = {
        "email": [ErrorDetail(string="user with this email already exists.", code="unique")]
    }

    assert response.status_code == 400
    assert response.data == expected_response


def test_activate_user_by_code(api_client):
    user = UserFactory(email='test@gm.com', is_active=False)
    assert not user.is_active
    token = UserActivateAccountTokenFactory(user=user)

    data = {
        "email": user.email,
        "token": token.token,
    }

    response = api_client.post('/auth/confirm/', data)

    user.refresh_from_db()

    assert response.status_code == 200
    assert user.is_active


def test_activete_user_by_code_invalid(api_client):
    user = UserFactory(email='test@gm.com', is_active=False)
    assert not user.is_active
    token = UserActivateAccountTokenFactory(user=user)

    data = {
        "email": user.email,
        "token": '111',
    }

    response = api_client.post('/auth/confirm/', data)

    user.refresh_from_db()

    assert response.status_code == 400


def test_user_data_ok(authenticated_api_client):
    expected_data = {
        "email": authenticated_api_client.user.email,
        "first_name": authenticated_api_client.user.first_name,
        "is_active": authenticated_api_client.user.is_active,
    }

    response = authenticated_api_client.get('/api/me/')
    assert response.status_code == 200
    assert response.data == expected_data

def test_user_data_unauthenticated(api_client):
    response = api_client.get('/api/me/')
    assert response.status_code == 401
