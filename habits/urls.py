from django.urls import path
from habits.api.views import HabitsListAPIView
from habits.api.views import HabitAPIView

urlpatterns = [
    path('habits/', HabitsListAPIView.as_view()),
    path('habit/<int:id>/', HabitAPIView.as_view())
]
