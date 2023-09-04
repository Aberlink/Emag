import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django

django.setup()


import pytest
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import Article


list_url = "api/v1:listcreate"
detail_url = "api/v1:detailcreate"
date_format = "%Y-%m-%dT%H:%M:%S.%fZ"


def create_authenticated_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    permissions = Permission.objects.filter(content_type__app_label="blog")
    user.user_permissions.set(permissions)
    return user


def create_authenticated_client(sample_user):
    client = APIClient()
    client.force_authenticate(user=sample_user)
    return client


@pytest.fixture
def sample_user():
    return create_authenticated_user("testuser1", "testpass")


@pytest.fixture
def sample_user_2():
    return create_authenticated_user("testuser2", "testpass")


@pytest.fixture
def authenticated_client(sample_user):
    return create_authenticated_client(sample_user)


@pytest.fixture
def authenticated_client_2(sample_user_2):
    return create_authenticated_client(sample_user_2)


@pytest.fixture
def unauthenticated_client():
    return APIClient()


@pytest.fixture
def sample_article(sample_user):
    return {
        "title": "Test Article",
        "author": sample_user,
        "published": timezone.now(),
        "content": "This is a test article content.",
    }


@pytest.fixture
def sample_article_db(sample_article):
    return Article.objects.create(**sample_article)


@pytest.fixture
def updated_artice(sample_article_db):
    return {
        "title": "Updated Title",
        "author": sample_article_db.author.id,
        "published": timezone.now(),
        "content": "Updated content.",
    }


@pytest.mark.django_db
def test_article_list_view(unauthenticated_client, authenticated_client):
    response = unauthenticated_client.get(reverse(list_url))
    assert response.status_code == status.HTTP_200_OK
    response = authenticated_client.get(reverse(list_url))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_article_post_authenticated(sample_article, authenticated_client):
    sample_article["author"] = sample_article["author"].id
    sample_article["published"] = sample_article["published"].strftime(date_format)
    response = authenticated_client.post(
        reverse(list_url), sample_article, format="json"
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Article.objects.count() == 1


@pytest.mark.django_db
def test_article_post_unauthenticated(sample_article, unauthenticated_client):
    sample_article["author"] = sample_article["author"].id
    sample_article["published"] = sample_article["published"].strftime(date_format)
    response = unauthenticated_client.post(
        reverse(list_url), sample_article, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Article.objects.count() == 0


@pytest.mark.django_db
def test_article_detail_view_authenticated(sample_article_db, authenticated_client):
    response = authenticated_client.get(
        reverse(detail_url, kwargs={"pk": sample_article_db.id})
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_article_detail_view_unauthenticated(sample_article_db, client):
    response = client.get(reverse(detail_url, kwargs={"pk": sample_article_db.id}))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_article_detail_view_delete_author(sample_article_db, authenticated_client):
    response = authenticated_client.delete(
        reverse(detail_url, kwargs={"pk": sample_article_db.id})
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_article_detail_view_delete_not_author(
    sample_article_db, authenticated_client_2
):
    response = authenticated_client_2.delete(
        reverse(detail_url, kwargs={"pk": sample_article_db.id})
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_article_detail_view_delete_unauthenticated(sample_article_db, client):
    response = client.delete(reverse(detail_url, kwargs={"pk": sample_article_db.id}))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_article_detail_view_edit_author(
    sample_article_db, updated_artice, authenticated_client
):
    response = authenticated_client.put(
        reverse(detail_url, kwargs={"pk": sample_article_db.id}),
        updated_artice,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    response = authenticated_client.get(
        reverse(detail_url, kwargs={"pk": sample_article_db.id})
    )
    assert response.data["title"] == updated_artice["title"]
    assert response.data["content"] == updated_artice["content"]
    assert response.data["published"] == updated_artice["published"].strftime(
        date_format
    )


@pytest.mark.django_db
def test_article_detail_view_edit_not_author(
    sample_article_db, updated_artice, authenticated_client_2
):
    response = authenticated_client_2.put(
        reverse(detail_url, kwargs={"pk": sample_article_db.id}),
        updated_artice,
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_article_detail_view_edit_unauthenticated(
    sample_article_db, updated_artice, unauthenticated_client
):
    response = unauthenticated_client.put(
        reverse(detail_url, kwargs={"pk": sample_article_db.id}),
        updated_artice,
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_article_detail_view_not_found(client):
    response = client.get(reverse(detail_url, kwargs={"pk": 0}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
