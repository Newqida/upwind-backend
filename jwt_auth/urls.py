from django.urls import path
from jwt_auth.api.views import (
    ObtainTokensAPIView, RefreshTokensAPIView,
)

urlpatterns = [
    path('token/', ObtainTokensAPIView.as_view()),
    path('token/refresh/', RefreshTokensAPIView.as_view()),
]
