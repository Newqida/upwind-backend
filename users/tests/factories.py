import factory.fuzzy

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from users.models.activate_tokens import UserActivateToken

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.fuzzy.FuzzyText(length=12)
    email = factory.LazyAttribute(lambda user: "{}@example.com".format(user.first_name.lower()))
    password = factory.LazyFunction(lambda: make_password("test123"))
    
    class Meta:
        model = User

class UserActivateAccountTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserActivateToken