from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register_user_api'),
    path('token/blacklist/', views.BlacklistTokenView.as_view(), name='blacklist_token'),
]
