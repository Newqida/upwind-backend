import random

from datetime import timedelta

from django.utils import timezone


def delay_code_expiring():
    return timezone.now() + timedelta(hours=1)


def generate_token():
    return random.randint(100000, 999999)


def delay_activation_code_expiring():
    return timezone.now() + timedelta(hours=48)