from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

"""
Core Rozprava Business Logic Routes
"""

core_urls = [
    path('admin/', admin.site.urls),
    path('profile/', include('profiles.urls'), name='profile'),
    path('case/', include('case.urls'), name='case'),
    path('debate/', include('debate.urls'), name='debate'),
    path('notification/', include('notification.urls'), name='notification'),
    path('chat/', include('chat.urls'), name='chat')
]

"""
DRF Swagger Documentation Routes
"""

schema_view = get_schema_view(
   openapi.Info(
      title="Rozprava API",
      default_version='v1',
      description="The ultimate platform for debaters.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

swagger_urls = [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]

"""
Compile different Routes into singular list.
"""

urlpatterns = core_urls + swagger_urls

"""
Implement static and media routes for development purposes.
"""

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    ) + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
