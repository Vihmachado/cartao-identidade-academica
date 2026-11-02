from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="aluno-teste",
            email="aluno@example.com",
            password="senha-forte-123",
        )

    def test_root_redirects_to_login(self):
        response = self.client.get("/")

        self.assertRedirects(response, reverse("login"))

    def test_login_page_renders(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'action="/login/"')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard_aluno"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard_aluno')}",
            fetch_redirect_response=False,
        )

    def test_login_accepts_username_and_remembers_session(self):
        response = self.client.post(
            reverse("login"),
            {"username": "aluno-teste", "password": "senha-forte-123", "remember": "1"},
        )

        self.assertRedirects(
            response,
            reverse("listar_alunos"),
            fetch_redirect_response=False,
        )
        self.assertFalse(self.client.session.get_expire_at_browser_close())

    def test_login_accepts_unique_email_and_uses_browser_session_by_default(self):
        response = self.client.post(
            reverse("login"),
            {"username": "ALUNO@example.com", "password": "senha-forte-123"},
        )

        self.assertRedirects(
            response,
            reverse("listar_alunos"),
            fetch_redirect_response=False,
        )
        self.assertTrue(self.client.session.get_expire_at_browser_close())

    def test_password_reset_page_renders(self):
        response = self.client.get(reverse("password_reset"))

        self.assertEqual(response.status_code, 200)

    def test_logout_ends_session(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
