from django.contrib import admin
from users.models import User, UserActivateToken

admin.site.register(User)
admin.site.register(UserActivateToken)
