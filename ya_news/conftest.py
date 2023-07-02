from datetime import datetime
from django.utils import timezone
from news.models import News, Comment
from news.forms import BAD_WORDS, WARNING
from django.conf import settings
import pytest


@pytest.fixture
def news_instance():
    return News.objects.create(title='Test News', text='bla bla')


@pytest.fixture
def news_instances():
    today = timezone.now().date()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timezone.timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE)
    ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def news_instance_with_comments(author):
    news = News.objects.create(title='Test News', text='bla bla')
    Comment.objects.create(
        news=news,
        text='Comment 1',
        created=timezone.make_aware(datetime(2023, 7, 2, 17, 17, 14)),
        author=author)
    Comment.objects.create(
        news=news,
        text='Comment 2',
        created=timezone.make_aware(datetime(2023, 7, 2, 17, 17, 15)),
        author=author)
    return news


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def comment_instance(author, news_instance):
    return Comment.objects.create(
        text='haha classic', author=author, news=news_instance)


@pytest.fixture
def comment_form_data():
    return {'text': 'Тестовый коммент'}


@pytest.fixture
def bad_words():
    return BAD_WORDS, WARNING
