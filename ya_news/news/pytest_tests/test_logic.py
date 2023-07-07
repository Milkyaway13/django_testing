import pytest
from django.urls import reverse

from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        client, news_instance, comment_form_data):
    initial_amount_of_comments = Comment.objects.count()
    client.post(
        reverse("news:detail", kwargs={"pk": news_instance.pk}),
        data=comment_form_data
    )
    assert initial_amount_of_comments == Comment.objects.count()


@pytest.mark.django_db
def test_authenticated_user_can_create_comment(
    admin_client, news_instance, comment_form_data
):
    initial_amount_of_comments = Comment.objects.count()
    admin_client.post(
        reverse("news:detail", kwargs={"pk": news_instance.pk}),
        data=comment_form_data
    )
    assert initial_amount_of_comments + 1 == Comment.objects.count()


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, news_instance, bad_words):
    initial_amount_of_comments = Comment.objects.count()
    bad_words_list, warning = bad_words
    bad_words_data = {"text": f"Какой-то текст,"
                      f"{bad_words_list[0]}, еще текст"}
    response = author_client.post(
        reverse("news:detail",
                kwargs={"pk": news_instance.pk}), data=bad_words_data
    )
    form = response.context["form"]
    assert "text" in form.errors
    assert form.errors["text"] == [warning]
    assert initial_amount_of_comments == Comment.objects.count()


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, comment_instance):
    author_client.post(
        reverse("news:edit", kwargs={"pk": comment_instance.pk}),
        data={"text": "Updated comment text"},
    )
    comment_instance.refresh_from_db()
    assert comment_instance.text == "Updated comment text"


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, comment_instance):
    initial_amount_of_comments = Comment.objects.count()
    author_client.post(reverse("news:delete",
                               kwargs={"pk": comment_instance.pk}))
    assert initial_amount_of_comments - 1 == Comment.objects.count()


@pytest.mark.django_db
def test_authenticated_user_cannot_edit_other_comment(
        admin_client, comment_instance):
    admin_client.post(
        reverse("news:edit", kwargs={"pk": comment_instance.pk}),
        data={"text": "Updated comment text"},
    )
    comment_instance.refresh_from_db()
    assert comment_instance.text != "Updated comment text"


@pytest.mark.django_db
def test_authenticated_user_delete_other_comment(
        admin_client, comment_instance):
    initial_amount_of_comments = Comment.objects.count()
    admin_client.post(reverse("news:delete",
                              kwargs={"pk": comment_instance.pk}))
    assert initial_amount_of_comments == Comment.objects.count()
