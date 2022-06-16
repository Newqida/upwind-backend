from rest_framework import serializers

from users.models import User, UserActivateToken


class UserActivationCreator:
    def __init__(self, validated_data: dict = None, user: User = None):
        self.validated_data = validated_data
        self.user = user

    def __call__(self) -> User:
        self.resulting_user = self.user or self.create()

        self.after_creation()
        return self.resulting_user

    def create(self) -> User:
        return User.objects.create_user(
            email=self.validated_data.get('email'),
            password=self.validated_data.get('password'),
            first_name=self.validated_data.get('first_name'),
            is_active=False,
        )

    def after_creation(self) -> None:
        user_token = UserActivateToken().create_token(self.resulting_user)
        # TODO: Add sending email
        if user_token:
            pass


class UserAcivator:
    def __init__(self, token: str, email: str) -> None:
        self.data = {"token": token, "email": email}

    def __call__(self) -> User:
        self.activate()
        return self.get()

    def get(self) -> User:
        return User.objects.filter(email=self.data["email"]).first()

    def activate(self):
        try:
            user_activation_token = UserActivateToken.objects.active().get(
                token=self.data["token"], user__email=self.data["email"]
            )
        except (TypeError, ValueError, OverflowError, UserActivateToken.DoesNotExist):
            raise serializers.ValidationError({"token":"Invalid Token"})
        
        if user_activation_token and user_activation_token.user:
            user_activation_token.user.is_active = True
            user_activation_token.user.save()
            user_activation_token.is_used = True
            user_activation_token.save()
