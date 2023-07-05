from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username="author", password="password")
        cls.note = Note.objects.create(
            title="Заголовок", text="Текст", author=cls.author
        )
        cls.reader = User.objects.create_user(
            username="reader", password="password")

    def test_status_code_for_anonymous_user(self):
        urls = [
            ("notes:home", HTTPStatus.OK),
            ("users:login", HTTPStatus.OK),
            ("users:logout", HTTPStatus.OK),
            ("users:signup", HTTPStatus.OK),
        ]
        for url, expected_status in urls:
            with self.subTest(name=url):
                response = self.client.get(reverse(url))
                self.assertEqual(response.status_code, expected_status)

    def test_redirect_for_anonymous_user_without_slug(self):
        urls = ["notes:list", "notes:success", "notes:add"]
        login_url = reverse("users:login")
        for url in urls:
            with self.subTest(name=url):
                response = self.client.get(reverse(url))
                expected_redirect_url = f"{login_url}?next={reverse(url)}"
                self.assertRedirects(response, expected_redirect_url)

    def test_redirect_for_anonymous_user_with_slug(self):
        urls = [
            ("notes:detail", self.note.slug),
            ("notes:edit", self.note.slug),
            ("notes:delete", self.note.slug),
        ]
        login_url = reverse("users:login")
        for url, slug in urls:
            with self.subTest(name=url):
                response = self.client.get(reverse(url, args=(slug,)))
                expected_redirect_url = (
                    f"{login_url}?next={reverse(url, args=(slug,))}")
                self.assertRedirects(response, expected_redirect_url)

    def test_access_for_author(self):
        self.client.force_login(self.author)
        urls = [
            ("notes:home", None, HTTPStatus.OK),
            ("notes:list", None, HTTPStatus.OK),
            ("notes:success", None, HTTPStatus.OK),
            ("notes:add", None, HTTPStatus.OK),
            ("notes:detail", self.note.slug, HTTPStatus.OK),
            ("notes:edit", self.note.slug, HTTPStatus.OK),
            ("notes:delete", self.note.slug, HTTPStatus.OK),
        ]
        for url, slug, expected_status in urls:
            with self.subTest(name=url):
                response = (
                    self.client.get(reverse(url, args=(slug,)))
                    if slug
                    else self.client.get(reverse(url))
                )
                self.assertEqual(response.status_code, expected_status)

    def test_pages_availability_for_authenticated_user(self):
        self.client.force_login(self.reader)
        urls = [
            ("notes:detail", self.note.slug, HTTPStatus.NOT_FOUND),
            ("notes:edit", self.note.slug, HTTPStatus.NOT_FOUND),
            ("notes:delete", self.note.slug, HTTPStatus.NOT_FOUND),
        ]
        for url, slug, expected_status in urls:
            with self.subTest(name=url):
                response = self.client.get(reverse(url, args=(slug,)))
                self.assertEqual(response.status_code, expected_status)
