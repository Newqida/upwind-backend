from venv import create
from rest_framework import serializers

from habits.models import Habit
from relapses.api.serializers import RelapseSerializer
from relapses.models import Relapse
from habits.utils import value_saved_with_relapses


def get_saved_money(habit: Habit) -> float:
    relapses_count = Relapse.objects.filter(habit=habit.id).count()
    if (relapses_count > 0):
        return value_saved_with_relapses(habit.saved_money, habit.money_per_day, relapses_count)
    return habit.saved_money


def get_saved_time(habit: Habit) -> float:
    relapses_count = Relapse.objects.filter(habit=habit.id).count()
    if (relapses_count > 0):
        return value_saved_with_relapses(habit.saved_time, habit.time_per_day, relapses_count)
    return habit.saved_time


class HabitSerializer(serializers.ModelSerializer):
    relapses = RelapseSerializer(many=True)
    saved_money = serializers.SerializerMethodField('get_saved_money')
    saved_time = serializers.SerializerMethodField('get_saved_time')

    class Meta:
        model = Habit
        fields = [
            'id',
            'name',
            'time_spend_weekly',
            'money_spend_weekly',
            'days',
            'start_date',
            'saved_money',
            'saved_time',
            'relapses'
        ]

    def get_saved_money(self, habit: Habit):
        return get_saved_money(habit)

    def get_saved_time(self, habit: Habit):
        return get_saved_time(habit)


class HabitsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'id',
            'name',
            'time_spend_weekly',
            'money_spend_weekly',
            'user',
        ]


class HabitsListSerializer(serializers.ModelSerializer):
    saved_money = serializers.SerializerMethodField('get_saved_money')
    saved_time = serializers.SerializerMethodField('get_saved_time')

    class Meta:
        model = Habit
        fields = [
            'id',
            'name',
            'time_spend_weekly',
            'money_spend_weekly',
            'days',
            'start_date',
            'saved_money',
            'saved_time',
        ]

    def get_saved_money(self, habit: Habit):
        return get_saved_money(habit)

    def get_saved_time(self, habit: Habit):
        return get_saved_time(habit)
