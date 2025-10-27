from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserViewsTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("users:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bienvenue sur la GMAO")

    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("users:register"),
            {
                "username": "nouvel_user",
                "email": "user@example.com",
                "first_name": "Nouvel",
                "last_name": "Utilisateur",
                "password1": "TestPass123!",
                "password2": "TestPass123!",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="nouvel_user").exists())
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertContains(response, "Bienvenue sur la GMAO")

    def test_login_view_authenticates(self):
        User.objects.create_user(username="demo", password="DemoPass123")

        response = self.client.post(
            reverse("users:login"),
            {"username": "demo", "password": "DemoPass123"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertContains(response, "Bienvenue sur la GMAO")

    def test_admin_dashboard_requires_staff(self):
        user = User.objects.create_user(username="basic", password="UserPass123")
        self.client.login(username="basic", password="UserPass123")

        response = self.client.get(reverse("users:admin-dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:home"))

    def test_admin_dashboard_allows_staff(self):
        staff = User.objects.create_user(username="staff", password="StaffPass123", is_staff=True)
        self.client.login(username="staff", password="StaffPass123")

        response = self.client.get(reverse("users:admin-dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tableau de bord administrateur")
