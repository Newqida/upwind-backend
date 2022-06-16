from datetime import datetime
from django.db.models.query import QuerySet

from relapses.exceptions import NoDataForReport
from users.models.user import User
from relapses.models import Relapse
from relapses.utils import get_all_weekdays_dict

from difflib import get_close_matches


class RelapseReportCreator:

    def __init__(self, validated_data: dict = None, user: User = None):
        self.user = user
        self.validated_data = validated_data

    def __call__(self, *args, **kwds):
        return self.create_report()

    def get_response_data(self, relapses: list[Relapse], percentage: float, weekdays_report: dict) -> dict:
        return {
            'date_start': self.validated_data.get('date_start'),
            'date_end': self.validated_data.get('date_end'),
            'reasons_to_avoid': [relapse.as_json() for relapse in relapses],
            'percentage': percentage,
            'weekdays_report': weekdays_report,
        }

    def get_relapses(self) -> list[Relapse]:
        start_date = self.validated_data.get('date_start')
        end_date = self.validated_data.get('date_end')
        habit = self.validated_data.get('habit')
        query = Relapse.objects.filter(
            datetime__range=(start_date, end_date),
            user=self.user,
        )

        if habit:
            return query.filter(habit=habit)
        else:
            return query

    def get_most_often_relapses(self, relapses: QuerySet) -> list[Relapse]:
        reasons = []
        matches = []

        for relapse in relapses:
            reasons.append(relapse.reason)

        for reason in reasons:
            matches.append(get_close_matches(reason, reasons, cutoff=0.65))

        best_match = max(enumerate(matches), key=(lambda x: len(x[1])))[1]

        best_match_objects = [
            relapse for relapse in relapses if relapse.reason in best_match
        ]

        return best_match_objects

    def get_percentage(self, best_match_objects: list[Relapse], relapses: list[Relapse]) -> float:
        return round(len(best_match_objects) * 100 / len(relapses), 1)

    def weekdays_report(self, relapses: list[Relapse]) -> dict:
        weekdays = get_all_weekdays_dict()

        for relapse in relapses:
            weekday_name = relapse.datetime.strftime('%A')
            weekdays[weekday_name] = weekdays[weekday_name] + 1

        return weekdays

    def create_report(self):
        relapses = self.get_relapses()

        if len(relapses) == 0:
            raise NoDataForReport()

        best_match_objects = self.get_most_often_relapses(relapses)
        percentage_of_match = self.get_percentage(best_match_objects, relapses)
        weekdays_report = self.weekdays_report(relapses)

        response_data = self.get_response_data(
            best_match_objects,
            percentage_of_match,
            weekdays_report
        )

        return response_data
