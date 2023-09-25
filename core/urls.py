from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
    path("api/v1/", include("api.urls", namespace="api/v1")),
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name="api-schema")),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('api/user/', include("users.urls", namespace="users")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
