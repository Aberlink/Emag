from django.urls import path, include

from .views import ArticleList, ArticleDetail

app_name = "api/v1"

urlpatterns = [
    path("article/", ArticleList.as_view(), name="listcreate"),
    path("article/<int:pk>/", ArticleDetail.as_view(), name="detailcreate"),
]
