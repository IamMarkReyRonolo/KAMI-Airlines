from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView
from drf_yasg.utils import swagger_auto_schema

schema_view = get_schema_view(
    openapi.Info(
        title="KAMI Airlines API",
        default_version="v1",
        description="The apis for KAMI Airlines",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ronolomarkrey@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", RedirectView.as_view(url="/api/docs/")),
    path("admin/", admin.site.urls),
    path("api/airplanes/", include("api.airplanes.urls")),
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
