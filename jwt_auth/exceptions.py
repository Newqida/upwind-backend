from rest_framework_simplejwt.exceptions import AuthenticationFailed

from rest_framework import status


class InvalidRefreshToken(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Token is invalid or expired"
    default_code = "refresh_token_not_valid"