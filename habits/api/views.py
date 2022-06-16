from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated

from habits.api.serializers import HabitSerializer, HabitsCreateSerializer, HabitsListSerializer
from habits.models import Habit


class HabitsListAPIView(ListCreateAPIView):

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return HabitsCreateSerializer
        else:
            return HabitsListSerializer

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.data['user'] = request.user.pk
            return super().create(request, *args, **kwargs)
        else:
            raise NotAuthenticated()


class HabitAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HabitSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
