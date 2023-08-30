from django.urls import path
from django.views.generic import TemplateView

app_name = 'blog'

urlpatterns = [
    path('', TemplateView.asview(template_name='blog/index.html')),
]
