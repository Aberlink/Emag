from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('blog.urls', namespace='blog')),
    path("api/", include('api.urls', namespace='api')),
    
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('schema/docs/', SpectacularSwaggerView.as_view(url_name='api-schema')),
    
]
