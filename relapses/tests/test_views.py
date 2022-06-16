import json
import zoneinfo
import pytest

import datetime

from relapses.tests.utils import get_expected_relapse_list
from relapses.tests.factories import RelapseFactory
from relapses.models import Relapse

from habits.tests.factories import HabitFactory

pytestmark = [pytest.mark.django_db]


def test_create_relapse_ok(authenticated_api_client):
    habit = HabitFactory(user=authenticated_api_client.user)
    data = {
        "habit": habit.id,
        "reason": "test"
    }

    response = authenticated_api_client.post(
        "/api/relapses/", data, format="json")

    expected_response = {
        "habit": habit.id,
        "reason": "test",
        "user": authenticated_api_client.user.pk
    }

    assert response.status_code == 201
    assert response.data == expected_response
    assert Relapse.objects.filter(
        habit=expected_response['habit'],
        reason=expected_response['reason'],
        user=expected_response['user']
    ).exists()


def test_create_relapse_unauthenticated(api_client):
    response = api_client.post(
        "/api/relapses/", {"test": "data"}, format="json")

    assert response.status_code == 401


def test_create_relapse_wrong_data(authenticated_api_client):
    data = {
        "reason": "test"
    }

    response = authenticated_api_client.post(
        "/api/relapses/", data, format="json")

    assert response.status_code == 400


def test_get_relapses_list_ok(authenticated_api_client):
    habit = HabitFactory(user=authenticated_api_client.user)

    relapses_list = []

    for i in range(5):
        relapses_list.append(RelapseFactory(
            reason=str(i),
            habit=habit, user=authenticated_api_client.user))

    response = authenticated_api_client.get('/api/relapses/')

    assert response.status_code == 200
    assert len(relapses_list) == len(response.data)


def test_get_relapses_list_unauthenticated(api_client):
    response = api_client.get('/api/relapses/')

    assert response.status_code == 401


def test_delete_relapse_ok(authenticated_api_client):
    habit = HabitFactory(user=authenticated_api_client.user)
    relapse = RelapseFactory(reason='test', habit=habit,
                             user=authenticated_api_client.user)

    response = authenticated_api_client.delete(f'/api/relapse/{relapse.id}/')

    assert response.status_code == 204
    assert not Relapse.objects.filter(id=relapse.id).exists()


def test_delete_relapse_unauthenticated(api_client):
    response = api_client.delete('/api/relapse/1/')

    assert response.status_code == 401


def test_delete_relapse_not_found(authenticated_api_client):
    response = authenticated_api_client.delete('/api/relapse/123/')

    assert response.status_code == 404


def test_general_relapse_report_ok(authenticated_api_client):
    user = authenticated_api_client.user
    relapses_list = []

    start_date = datetime.datetime(
        2020, 1, 1, tzinfo=zoneinfo.ZoneInfo(key='UTC'))
    end_date = datetime.datetime(
        2020, 12, 12, tzinfo=zoneinfo.ZoneInfo(key='UTC'))

    for i in range(10):
        habit = HabitFactory(user=user)
        if i < 6:
            relapse_reason = 'test relapse name'
        else:
            relapse_reason = str(i)

        relapse = RelapseFactory(
            reason=relapse_reason,
            habit=habit,
            user=user
        )

        relapse.datetime = (start_date + datetime.timedelta(weeks=i))
        relapse.save()
        relapses_list.append(relapse)

    data = {
        "date_start": start_date.isoformat(),
        "date_end": end_date.isoformat(),
    }
    expected_response = {
        "date_start": start_date,
        "date_end": end_date,
        "reasons_to_avoid": get_expected_relapse_list(relapses_list[:6]),
        "percentage": 60.0,
        "weekdays_report": {
            'Monday': 0,
            'Tuesday': 0,
            'Wednesday': 10,
            'Thursday': 0,
            'Friday': 0,
            'Saturday': 0,
            'Sunday': 0
        }
    }

    response = authenticated_api_client.generic(
        'GET',
        '/api/relapse/report/',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.data == expected_response


def test_general_relapse_report_unauthenticated(api_client):
    response = api_client.get('/api/relapse/report/')

    assert response.status_code == 401


def test_general_relapse_report_wrong_data(authenticated_api_client):
    date_end = datetime.datetime(
        2020, 12, 12, tzinfo=zoneinfo.ZoneInfo(key='UTC')).isoformat()

    data = {
        "date_end": date_end,
    }

    response = authenticated_api_client.generic(
        'GET',
        '/api/relapse/report/',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 400


def test_general_relapse_report_not_enough_data(authenticated_api_client):
    start_date = datetime.datetime(
        2020, 1, 1, tzinfo=zoneinfo.ZoneInfo(key='UTC'))
    end_date = datetime.datetime(
        2020, 12, 12, tzinfo=zoneinfo.ZoneInfo(key='UTC'))

    data = {
        "date_start": start_date.isoformat(),
        "date_end": end_date.isoformat(),
    }

    response = authenticated_api_client.generic(
        'GET',
        '/api/relapse/report/',
        data=json.dumps(data),
        content_type='application/json'
    )

    assert response.status_code == 416
