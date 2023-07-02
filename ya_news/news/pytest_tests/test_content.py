from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_news_count(client, news_instances):
    url = reverse("news:home")
    response = client.get(url)
    assert len(response.context["object_list"]) == len(news_instances)


@pytest.mark.django_db
def test_news_order(client):
    response = client.get(reverse("news:home"))
    object_list = response.context["object_list"]
    assert [news.date for news in object_list] == sorted(
        [news.date for news in object_list], reverse=True
    )


@pytest.mark.django_db
def test_comment_order(client, news_instance_with_comments):
    response = client.get(
        reverse("news:detail", kwargs={"pk": news_instance_with_comments.pk})
    )
    assert "news" in response.context
    news = response.context["news"]
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news_instance):
    response = client.get(
        reverse("news:detail", kwargs={"pk": news_instance.pk}))
    assert "form" not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, news_instance):
    response = author_client.get(
        reverse("news:detail", kwargs={"pk": news_instance.pk})
    )
    assert "form" in response.context
