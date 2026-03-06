from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Client


class ClientTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="safe-pass-123",
        )
        self.business_client = Client.objects.create(
            name="Acme",
            company="Acme Corp",
            email="hello@acme.com",
        )

    def test_client_string_representation(self):
        self.assertEqual(str(self.business_client), "Acme (Acme Corp)")

    def test_client_list_requires_login(self):
        response = self.client.get(reverse("clients:client_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)

    def test_authenticated_user_can_access_client_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("clients:client_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Acme")

