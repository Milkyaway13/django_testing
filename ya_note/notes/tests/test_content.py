from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm


User = get_user_model()


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username="author", password="password")
        cls.reader = User.objects.create_user(
            username="reader", password="password")
        cls.note = Note.objects.create(
            title="Заголовок", text="Текст", author=cls.author, slug="slug"
        )

    def test_note_list_contains_single_note(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse("notes:list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(self.note, response.context["object_list"])

    def test_note_list_excludes_notes_from_other_users(self):
        self.client.force_login(self.author)
        other_author = User.objects.create_user(
            username="other_author", password="password"
        )
        other_note = Note.objects.create(
            title="Заголовок", text="Текст", author=other_author
        )
        response = self.client.get(reverse("notes:list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn(other_note, response.context["object_list"])

    def test_note_create_pages_contain_forms(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse("notes:add"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.context["form"], NoteForm)

    def test_note_edit_pages_contain_forms(self):
        self.client.force_login(self.author)
        response = self.client.get(
            reverse("notes:edit", args=(self.note.slug,)))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.context["form"], NoteForm)

    def test_access_for_note_author(self):
        self.client.force_login(self.author)
        urls = ["notes:edit", "notes:delete"]
        for url in urls:
            response = self.client.get(reverse(url, args=(self.note.slug,)))
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_access_for_non_author(self):
        self.client.force_login(self.reader)
        urls = ["notes:edit", "notes:delete"]
        for url in urls:
            response = self.client.get(reverse(url, args=(self.note.slug,)))
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
