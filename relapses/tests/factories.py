import datetime

import factory.fuzzy

from relapses.models import Relapse


class RelapseFactory(factory.django.DjangoModelFactory):
    datetime = factory.fuzzy.FuzzyDateTime(
        start_dt=datetime.datetime(2001, 12, 12, tzinfo=datetime.timezone.utc))
    reason = factory.fuzzy.FuzzyText(length=12)

    class Meta:
        model = Relapse
