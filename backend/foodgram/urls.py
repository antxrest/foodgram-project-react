from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title='Yamdb API',
        default_version='v1',
        description='Auto docs project api_yamdb',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui("swagger")),
]
