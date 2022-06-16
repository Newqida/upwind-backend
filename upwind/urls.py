from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.urls import auth_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Upwind API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

docs_urls = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]

api_urls = [
    path('', include('users.urls')),
    path('', include('habits.urls')),
    path('', include('relapses.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', include(docs_urls)),
    path('api/', include(api_urls)),
    path('', include('jwt_auth.urls')),
    path('auth/', include(auth_urls)),
]
