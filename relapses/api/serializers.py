from rest_framework import serializers

from relapses.models import Relapse
from relapses.services import RelapseReportCreator
from users.models.user import User


class RelapseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relapse
        fields = [
            'datetime',
            'reason',
        ]


class RelapseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relapse
        fields = [
            'reason',
            'habit',
            'user',
        ]


class RelapseReportSerializer(serializers.Serializer):
    date_start = serializers.DateTimeField()
    date_end = serializers.DateTimeField()
    habit = serializers.IntegerField(required=False)

    def generate_report(self, user: User):
        return RelapseReportCreator(self.validated_data, user)()
