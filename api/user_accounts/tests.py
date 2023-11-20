from django.core.management import call_command
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.user_accounts.models import KAMIUser
from api.user_accounts.serializers import UserSerializer
import json


class TestRegisterAPI(APITestCase):
    def setUp(self):
        self.valid_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "iamjohndoe",
            "password": "iamjohndoe",
        }

        super().setUp()

    def test_valid_registration(self):
        response = self.client.post(reverse("register"), self.valid_payload)
        json_response = response.data
        expected_status_code = 201
        expected_message = "Successfully added user"

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["message"])

        user = KAMIUser.objects.get(username=json_response["user"]["username"])
        serializer = UserSerializer(user)

        self.assertEqual(
            serializer.data["first_name"], json_response["user"]["first_name"]
        )
        self.assertEqual(
            serializer.data["last_name"], json_response["user"]["last_name"]
        )
        self.assertEqual(serializer.data["username"], json_response["user"]["username"])

    def test_registration_missing_first_name(self):
        del self.valid_payload["first_name"]
        response = self.client.post(reverse("register"), self.valid_payload)
        json_response = response.data
        expected_status_code = 400
        expected_message = "This field is required."

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["first_name"][0]))

    def test_registration_missing_last_name(self):
        del self.valid_payload["last_name"]
        response = self.client.post(reverse("register"), self.valid_payload)
        json_response = response.data
        expected_status_code = 400
        expected_message = "This field is required."

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["last_name"][0]))

    def test_registration_missing_username(self):
        del self.valid_payload["username"]
        response = self.client.post(reverse("register"), self.valid_payload)
        json_response = response.data
        expected_status_code = 400
        expected_message = "This field is required."

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["username"][0]))

    def test_registration_missing_password(self):
        del self.valid_payload["password"]
        response = self.client.post(reverse("register"), self.valid_payload)
        json_response = response.data
        expected_status_code = 400
        expected_message = "This field is required."

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["password"][0]))

    def test_registration_existing_email(self):
        response = self.client.post(reverse("register"), self.valid_payload)

        # register again with the same payload
        response = self.client.post(reverse("register"), self.valid_payload)

        json_response = response.data
        expected_status_code = 400
        expected_message = "kami user with this username already exists."

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["username"][0]))


class TestLoginAPI(APITestCase):
    def setUp(self):
        self.valid_payload_registration = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "iamjohndoe",
            "password": "iamjohndoe",
        }
        self.valid_login_credentials = {
            "username": "iamjohndoe",
            "password": "iamjohndoe",
        }
        super().setUp()

    def test_valid_login(self):
        response = self.client.post(
            reverse("register"), self.valid_payload_registration
        )

        response = self.client.post(
            reverse("login"),
            self.valid_login_credentials,
        )
        json_response = response.data
        expected_status_code = 200
        expected_message = "Successfully logged in"
        token = json_response["access_token"]

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["message"])
        self.assertNotEqual(token, "")

    def test_login_wrong_username(self):
        response = self.client.post(
            reverse("register"), self.valid_payload_registration
        )

        self.valid_login_credentials["username"] = "wrong_username"
        response = self.client.post(
            reverse("login"),
            self.valid_login_credentials,
        )

        json_response = response.data
        expected_status_code = 400
        expected_message = "Invalid credentials"

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["error"])

    def test_login_wrong_password(self):
        response = self.client.post(
            reverse("register"), self.valid_payload_registration
        )

        self.valid_login_credentials["password"] = "wrong_password"
        response = self.client.post(
            reverse("login"),
            self.valid_login_credentials,
        )

        json_response = response.data
        expected_status_code = 400
        expected_message = "Invalid credentials"

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["error"])

    def test_login_missing_username(self):
        response = self.client.post(
            reverse("register"), self.valid_payload_registration
        )

        del self.valid_login_credentials["username"]
        response = self.client.post(
            reverse("login"),
            self.valid_login_credentials,
        )

        json_response = response.data
        expected_status_code = 400
        expected_message = "Invalid credentials"

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["error"])

    def test_login_missing_password(self):
        response = self.client.post(
            reverse("register"), self.valid_payload_registration
        )

        del self.valid_login_credentials["password"]
        response = self.client.post(
            reverse("login"),
            self.valid_login_credentials,
        )

        json_response = response.data
        expected_status_code = 400
        expected_message = "Invalid credentials"

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["error"])

    def test_login_missing_payload(self):
        response = self.client.post(
            reverse("register"), self.valid_payload_registration
        )

        self.valid_login_credentials = {}
        response = self.client.post(
            reverse("login"),
            self.valid_login_credentials,
        )

        json_response = response.data
        expected_status_code = 400
        expected_message = "Invalid credentials"

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["error"])
