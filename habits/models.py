from django.db import models

from django.utils import timezone
from habits.utils import (value_per_day, value_saved)
from users.models import User


class Habit(models.Model):
    name = models.CharField(max_length=40)
    time_spend_weekly = models.FloatField(blank=True, default=None)
    money_spend_weekly = models.FloatField(blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)

    @property
    def days(self) -> int:
        return (timezone.now() - self.start_date).days

    @property
    def money_per_day(self) -> float:
        return value_per_day(self.money_spend_weekly)

    @property
    def time_per_day(self) -> float:
        return value_per_day(self.time_spend_weekly)

    @property
    def saved_money(self) -> float:
        return value_saved(self.money_per_day, self.days)

    @property
    def saved_time(self) -> float:
        return value_saved(self.time_per_day, self.days)

