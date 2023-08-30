import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()


import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import Article


@pytest.fixture
def sample_user():
    return 
    
@pytest.fixture   
def sample_article():
    sample_article = {
        'title': 'Test Article',
        'author': User.objects.create_user(username='testuser', password='testpass'),
        'published': timezone.now(),
        'content': 'This is a test article content.'
    }
    return Article.objects.create(**sample_article)

@pytest.fixture  
def client():
    return APIClient()

@pytest.mark.django_db
def test_article_list_view(client):
    response = client.get(reverse('api:listcreate'))
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_article_detail_view(sample_article, client):
    response = client.get(reverse('api:detailcreate', kwargs={'pk': sample_article.id}))
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_article_detail_view_not_found(client):
    response = client.get(reverse('api:detailcreate', kwargs={'pk': 0}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
