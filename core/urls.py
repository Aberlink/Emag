from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
    path("api/v1/", include("api.urls", namespace="api/v1")),
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name="api-schema")),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]
