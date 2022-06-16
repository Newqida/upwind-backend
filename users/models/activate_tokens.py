from datetime import timedelta
import uuid

from typing import Optional

from model_utils.models import TimeStampedModel

from django.db import models
from django.utils import timezone

from users.models import User
from users.utils import (
    delay_code_expiring,
    generate_token,
    delay_activation_code_expiring
)


class BaseUserTokenCodeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_used=False, expires_at__gt=timezone.now())


class BaseUserToken(TimeStampedModel):
    user = models.ForeignKey(
        User, related_name='restore_codes',
        on_delete=models.CASCADE
    )
    expires_at = models.DateTimeField(
        "Expires at", default=delay_code_expiring)
    is_used = models.BooleanField("Is used", default=False)
    token = models.UUIDField('Token', default=uuid.uuid4, unique=True)

    objects = BaseUserTokenCodeQuerySet.as_manager()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.token} expires at {self.expires_at}"

    def deactivate(self) -> None:
        self.is_used = True
        self.save()


class UserActivateToken(BaseUserToken):
    token = models.IntegerField(default=generate_token)
    expires_at = models.DateTimeField(
        'Expires at', default=delay_activation_code_expiring)
    user = models.ForeignKey(
        User, verbose_name='Name',
        related_name='activation_codes',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "User token for account activation"
        verbose_name_plural = "User tokens for account activation"

    def create_token(self, user) -> Optional["UserActivateToken"]:
        if UserActivateToken.objects.filter(
            user=user, is_used=False, created__gte=timezone.now() - timedelta(minutes=5)
        ).exists():
            return None

        UserActivateToken.objects.filter(user=user, is_used=False).delete()
        return UserActivateToken.objects.create(user=user)
