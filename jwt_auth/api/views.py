from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jwt_auth.api.serializers import (
    CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
)
from jwt_auth.exceptions import InvalidRefreshToken


class ObtainTokensAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class RefreshTokensAPIView(TokenRefreshView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidRefreshToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
