import factory.fuzzy

from habits.models import Habit

class HabitFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText(length=12)
    time_spend_weekly = factory.fuzzy.FuzzyFloat(10.0, high=12.0)
    money_spend_weekly = factory.fuzzy.FuzzyFloat(10.0, high=600.0)

    class Meta:
        model = Habit