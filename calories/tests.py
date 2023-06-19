from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Entry

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

    def test_add_entry(self):
        url = reverse("add_entry")
        data = {
            "add_meal_name": "Test Meal",
            "add_cal_num": 500
        }
        headers = {
            "HTTP_AUTHORIZATION": f"Token {self.token.key}"
        }
        response = self.client.post(url, data, **headers, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        entry = Entry.objects.last()
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.name, "Test Meal")
        self.assertEqual(entry.number, 500)

    def test_add_entry_empty_name(self):
        url = reverse("add_entry")
        data = {
            "add_meal_name": "",
            "add_cal_num": 500
        }
        headers = {
            "HTTP_AUTHORIZATION": f"Token {self.token.key}"
        }
        response = self.client.post(url, data, **headers, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_delete_entry(self):
        entry = Entry.objects.create(user=self.user, name="Test Entry", number=500)
        url = reverse("delete_entry")
        data = {
            "entry_id": entry.id
        }
        headers = {
            "HTTP_AUTHORIZATION": f"Token {self.token.key}"
        }
        response = self.client.delete(url, data, **headers, content_type="application/json")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Entry.objects.filter(id=entry.id).exists())


class EntryModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

    def test_entry_creation(self):
        entry = Entry.objects.create(user=self.user, name="Test Entry", number=500)
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.name, "Test Entry")
        self.assertEqual(entry.number, 500)
        self.assertFalse(entry.expected)

    def test_entry_serialization(self):
        entry = Entry.objects.create(user=self.user, name="Test Entry", number=500)
        serialized_data = entry.serialize()
        self.assertEqual(serialized_data["id"], entry.id)
        self.assertEqual(serialized_data["user_id"], self.user.id)
        self.assertEqual(serialized_data["name"], "Test Entry")
        self.assertEqual(serialized_data["number"], 500)
        self.assertEqual(serialized_data["expected"], False)


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.per_day, 0)

    def test_user_authentication(self):
        authenticated = self.user.is_authenticated
        self.assertTrue(authenticated)

