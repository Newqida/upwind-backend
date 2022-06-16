from django.urls import path
from users.api.views import RegisterAPIView, UserDataAPIView, AccountActivationView

auth_urls = [
    path('register/', RegisterAPIView.as_view()),
    path('confirm/', AccountActivationView.as_view())
]

urlpatterns = [
    path('me/', UserDataAPIView.as_view())
]
