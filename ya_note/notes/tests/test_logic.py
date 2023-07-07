from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from pytils.translit import slugify as pytils_slugify
from notes.models import Note


class NoteCreationTest(TestCase):
    TEST_NOTE = "Какой-то текст"

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="Loly")
        self.url = reverse("notes:add")
        self.form_data = {"title": "Заголовок", "text": self.TEST_NOTE}
        self.auth_client = Client()
        self.auth_client.force_login(self.user)
        self.user1 = User.objects.create(username="User1")
        self.user2 = User.objects.create(username="User2")
        self.note_user1 = Note.objects.create(
            title="Заголовок 1",
            text="Текст 1", author=self.user1
        )
        self.note_user2 = Note.objects.create(
            title="Заголовок 2", text="Текст 2", author=self.user2
        )

    def test_anonymous_user_cant_create_note(self):
        initial_amount_of_notes = Note.objects.count()
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), initial_amount_of_notes)

    def test_authenticated_user_can_create_note(self):
        initial_amount_of_notes = Note.objects.count()
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            Note.objects.count(),
            initial_amount_of_notes + 1)

    def test_cannot_create_duplicate_slug(self):
        initial_amount_of_notes = Note.objects.count()
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            Note.objects.count(),
            initial_amount_of_notes + 1)

    def test_auto_generate_slug(self):
        title = "Заголовок заметки"
        slug = pytils_slugify(title)
        note = Note.objects.create(title=title, slug=slug, author=self.user)
        self.assertIsNotNone(note.slug)
        self.assertEqual(note.slug, slug)

    def test_user_can_edit_own_note(self):
        self.auth_client.force_login(self.user1)
        edit_url = reverse("notes:edit", args=[self.note_user1.slug])
        response = self.auth_client.get(edit_url)
        self.assertEqual(
            response.status_code, HTTPStatus.OK
        )

        updated_data = {"title": "Новый заголовок", "text": "Новый текст"}
        response = self.auth_client.post(edit_url, data=updated_data)
        self.assertEqual(
            response.status_code, HTTPStatus.FOUND
        )
        self.note_user1.refresh_from_db()
        self.assertEqual(
            self.note_user1.title, updated_data["title"]
        )
        self.assertEqual(
            self.note_user1.text, updated_data["text"]
        )

    def test_user_cannot_edit_other_users_note(self):
        self.auth_client.force_login(self.user1)
        edit_url = reverse("notes:edit", args=[self.note_user2.slug])
        response = self.auth_client.get(edit_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        updated_data = {"title": "Новый заголовок", "text": "Новый текст"}
        response = self.auth_client.post(edit_url, data=updated_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_user_can_delete_own_note(self):
        self.auth_client.force_login(self.user1)
        delete_url = reverse("notes:delete", args=[self.note_user1.slug])
        response = self.auth_client.get(delete_url)
        self.assertEqual(
            response.status_code, HTTPStatus.OK
        )

        response = self.auth_client.post(delete_url)
        self.assertEqual(
            response.status_code, HTTPStatus.FOUND
        )
        self.assertEqual(
            Note.objects.filter(slug=self.note_user1.slug).exists(), False
        )

    def test_user_cannot_delete_other_users_note(self):
        self.auth_client.force_login(self.user1)
        delete_url = reverse("notes:delete", args=[self.note_user2.slug])
        response = self.auth_client.get(delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = self.auth_client.post(delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
