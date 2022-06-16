import pytest

from habits.tests.factories import HabitFactory
from habits.models import Habit

pytestmark = [pytest.mark.django_db]


def test_create_habit_ok(authenticated_api_client):
    data = {
        "name": "smoking",
        "time_spend_weekly": 15.0,
        "money_spend_weekly": 20.0
    }

    response = authenticated_api_client.post(
        "/api/habits/", data, format="json")

    expected_response = {
        "id": 1,
        "name": "smoking",
        "time_spend_weekly": 15.0,
        "money_spend_weekly": 20.0,
        "user": authenticated_api_client.user.id
    }

    assert response.status_code == 201
    assert response.data == expected_response
    assert Habit.objects.filter(id=1).exists()


def test_create_habit_unauthenticated(api_client):
    data = {
        "name": "smoking",
        "time_spend_weekly": 15.0,
        "money_spend_weekly": 20.0
    }

    response = api_client.post("/api/habits/", data, format="json")

    assert response.status_code == 401


def test_create_habit_wrong_data(create_habit):
    data = {
        "time_spend_weekly": 15.0,
        "money_spend_weekly": 20.0
    }

    response = create_habit(data)

    assert response.status_code == 400


def test_get_habits_list_ok(authenticated_api_client):
    test_habits = []

    for i in range(5):
        test_habits.append(HabitFactory(
            name=str(i), user=authenticated_api_client.user))

    response = authenticated_api_client.get("/api/habits/")

    assert response.status_code == 200
    assert len(response.data) == len(test_habits)


def test_get_habits_list_unauthenticated(api_client):
    response = api_client.get("/api/habits/")

    assert response.status_code == 401


def test_delete_habit_ok(authenticated_api_client):
    habit = HabitFactory(user=authenticated_api_client.user)

    response = authenticated_api_client.delete(f'/api/habit/{habit.id}/')

    assert response.status_code == 204
    assert not Habit.objects.filter(id=habit.id).exists()


def test_delete_habit_unauthenticated(api_client):
    response = api_client.delete('/api/habit/1/')

    assert response.status_code == 401


def test_delete_habit_not_found(authenticated_api_client):
    response = authenticated_api_client.delete('/api/habit/123/')

    assert response.status_code == 404
