import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, pk",
    [
        ("news:home", None),
        ("news:detail", "news_instance"),
        ("users:login", None),
        ("users:logout", None),
        ("users:signup", None),
    ],
)
def test_availability_pages_for_anonymous_user(client, name, pk,
                                               news_instance):
    if pk == "news_instance":
        pk = news_instance.pk
    url = reverse(name) if name != "news:detail" else reverse(
        name, kwargs={"pk": pk})
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize("name", ("news:edit", "news:delete"))
def test_edit_and_delete_comment_for_author(author_client, name,
                                            comment_instance):
    url = reverse(name, kwargs={"pk": comment_instance.pk})
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize("name", ("news:edit", "news:delete"))
def test_redirect_for_anonymous_user(client, name, comment_instance):
    url = reverse(name, kwargs={"pk": comment_instance.pk})
    login_url = reverse("users:login")
    assertRedirects(client.get(url), f"{login_url}?next={url}")


@pytest.mark.django_db
@pytest.mark.parametrize("name", ("news:edit", "news:delete"))
def test_edit_and_delete_comment_error(name, admin_client, comment_instance):
    url = reverse(name, kwargs={"pk": comment_instance.pk})
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
