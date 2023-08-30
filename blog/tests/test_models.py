import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Article


@pytest.fixture
def sample_user():
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def sample_article(sample_user):
    return {
        'title': 'Test Article',
        'author': sample_user,
        'published': timezone.now(),
        'content': 'This is a test article content.',
        'id': 1
    }
    
@pytest.fixture   
def push_article_db(sample_article):
    return Article.objects.create(**sample_article)
    

@pytest.mark.django_db
def test_article_creation(push_article_db):    
    retrieved_article = Article.objects.get(id=1)
    
    assert retrieved_article.title == push_article_db.title
    assert retrieved_article.author == push_article_db.author
    assert retrieved_article.published == push_article_db.published
    assert retrieved_article.content == push_article_db.content

@pytest.mark.django_db
def test_article_str_method(push_article_db):
    assert str(push_article_db) == f'Test Article || testuser || {push_article_db.published}'
