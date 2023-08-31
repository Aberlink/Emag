import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()


import pytest
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import Article


list_url = 'api:listcreate'
detail_url = 'api:detailcreate'
date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

@pytest.fixture
def sample_user():
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def sample_article(sample_user):
    return {
        'title': 'Test Article',
        'author': sample_user,
        'published': timezone.now(),
        'content': 'This is a test article content.'
    }
    
@pytest.fixture   
def sample_article_db(sample_article):
    return Article.objects.create(**sample_article)

@pytest.fixture  
def client():
    return APIClient()

@pytest.mark.django_db
def test_article_list_view(client):
    response = client.get(reverse(list_url))
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db    
def test_article_post(sample_article, client):
    sample_article['author'] = sample_article['author'].id
    sample_article['published'] = sample_article['published'].strftime(date_format)
    response = client.post(reverse(list_url), sample_article, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Article.objects.count() == 1
    

@pytest.mark.django_db
def test_article_detail_view(sample_article_db, client):
    response = client.get(reverse(detail_url, kwargs={'pk': sample_article_db.id}))
    assert response.status_code == status.HTTP_200_OK
    
@pytest.mark.django_db
def test_article_detail_view_delete(sample_article_db, client):
    response = client.delete(reverse(detail_url, kwargs={'pk': sample_article_db.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
@pytest.mark.django_db
def test_article_detail_view_edit(sample_article_db, client):
    updated_data = {
        'title': 'Updated Title',
        'author': sample_article_db.author.id, 
        'published': timezone.now(),
        'content': 'Updated content.'
    }
    response = client.put(reverse(detail_url, kwargs={'pk': sample_article_db.id}), updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    response = client.get(reverse(detail_url, kwargs={'pk': sample_article_db.id}))
    assert response.data['title'] == updated_data['title']
    assert response.data['content'] == updated_data['content']
    assert response.data['published'] == updated_data['published'].strftime(date_format)
        
    

@pytest.mark.django_db
def test_article_detail_view_not_found(client):
    response = client.get(reverse(detail_url, kwargs={'pk': 0}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
