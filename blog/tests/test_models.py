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
    return Article.objects.create(
        title='Test Article',
        author=sample_user,
        published=timezone.now(),
        content='This is a test article content.'
    )

@pytest.mark.django_db
def test_article_creation(sample_article):
    assert sample_article.title == 'Test Article'
    assert sample_article.author.username == 'testuser'
    assert isinstance(sample_article.published, timezone.datetime)
    assert sample_article.content == 'This is a test article content.'

@pytest.mark.django_db
def test_article_str_method(sample_article):
    assert str(sample_article) == f'Test Article || testuser || {sample_article.published}'
