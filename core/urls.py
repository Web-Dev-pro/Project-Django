from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from schema_graph.views import Schema

schema_view = get_schema_view(
    openapi.Info(
        title="CRM Design Api",
        default_version="v1",
        description="Great Tool for every business owners",
        terms_of_service="https://later-on-add-website.com/terms/",
        contact=openapi.Contact(email="contact@verification.local"),
        license=openapi.License(name="Verify License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    # update admin login address url
    path('marsteam/admin/1nLoN>=-BH(Si&[/', admin.site.urls),
    # local urls
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/', include('apps.initialization.urls')),
    # swagger document uchun
    re_path(r"^api/v2/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("schema/", Schema.as_view()),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

# to make not found and other exceptions
handler404 = 'apps.initialization.views.not_found'
