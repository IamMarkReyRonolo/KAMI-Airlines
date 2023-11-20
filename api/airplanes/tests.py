from django.core.management import call_command
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.airplanes.models import Airplane
from api.airplanes.serializers import AirplaneSerializer
import json


def authenticate(client):
    response = client.post(
        reverse("register"),
        {
            "first_name": "John",
            "last_name": "Doe",
            "username": "iamjohndoe",
            "password": "iamjohndoe",
        },
    )

    response = client.post(
        reverse("login"),
        {"username": "iamjohndoe", "password": "iamjohndoe"},
    )
    token = response.data["access_token"]
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token)


class TestAddAirplaneAPI(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.valid_payload = {"id": 1, "no_of_passengers": 1}
        self.missing_payload = {}
        self.missing_id_payload = {"no_of_passengers": 1}
        self.missing_passengers_payload = {"id": 1}
        self.invalid_payload_string_id = {"id": "string id", "no_of_passengers": 1}
        self.invalid_payload_string_passengers = {
            "id": 1,
            "no_of_passengers": "string passengers",
        }
        self.invalid_payload_id_less_than_1_value = {
            "id": 0,
            "no_of_passengers": 1,
        }
        self.invalid_payload_passenger_less_than_1_value = {
            "id": 1,
            "no_of_passengers": 0,
        }
        super().setUp()

    def test_unauthenticated_request_to_add_airplane(self):
        response = self.client.post(reverse("add_airplane"), self.valid_payload)
        json_response = response.data
        expected_status_code = 403
        expected_message = "Authentication credentials were not provided."
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["detail"])

    def test_authenticated_request_to_add_airplane(self):
        authenticate(self.client)
        response = self.client.post(reverse("add_airplane"), self.valid_payload)
        json_response = response.data
        expected_status_code = 201
        expected_message = "Successfully added airplane"
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["message"])

        airplane = Airplane.objects.get(pk=self.valid_payload["id"])
        serializer = AirplaneSerializer(airplane)

        self.assertEqual(
            serializer.data["no_of_passengers"],
            json_response["airplane"]["no_of_passengers"],
        )
        self.assertEqual(
            serializer.data["fuel_tank_capacity_in_liters"],
            json_response["airplane"]["fuel_tank_capacity_in_liters"],
        )
        self.assertEqual(
            serializer.data["fuel_consumption_per_minute"],
            json_response["airplane"]["fuel_consumption_per_minute"],
        )
        self.assertEqual(
            serializer.data["maximum_minutes_to_fly"],
            json_response["airplane"]["maximum_minutes_to_fly"],
        )

    def test_missing_payload_upon_create(self):
        authenticate(self.client)
        response = self.client.post(reverse("add_airplane"), self.missing_payload)
        json_response = response.data
        expected_status_code = 400
        expected_message = "This field is required."

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["id"][0]))
        self.assertEqual(expected_message, str(json_response["no_of_passengers"][0]))

    def test_missing_airplane_id_upon_create(self):
        authenticate(self.client)
        response = self.client.post(reverse("add_airplane"), self.missing_id_payload)
        json_response = response.data
        expected_status_code = 400
        expected_message = "This field is required."

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["id"][0]))

    def test_missing_passenger_number_upon_create(self):
        authenticate(self.client)
        response = self.client.post(
            reverse("add_airplane"), self.missing_passengers_payload
        )
        json_response = response.data
        expected_status_code = 400
        expected_message = "This field is required."

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["no_of_passengers"][0]))

    def test_not_valid_str_airplane_id_upon_create(self):
        authenticate(self.client)
        response = self.client.post(
            reverse("add_airplane"), self.invalid_payload_string_id
        )
        json_response = response.data
        expected_status_code = 400
        expected_message = "A valid integer is required."

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["id"][0]))

    def test_not_valid_str_passenger_number_upon_create(self):
        authenticate(self.client)
        response = self.client.post(
            reverse("add_airplane"), self.invalid_payload_string_passengers
        )
        json_response = response.data
        expected_status_code = 400
        expected_message = "A valid integer is required."

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["no_of_passengers"][0]))

    def test_not_valid_amount_airplane_id_upon_create(self):
        authenticate(self.client)
        response = self.client.post(
            reverse("add_airplane"), self.invalid_payload_id_less_than_1_value
        )
        json_response = response.data
        expected_status_code = 400
        expected_message = "Ensure this value is greater than or equal to 1."

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["id"][0]))

    def test_not_valid_amount_passenger_number_upon_create(self):
        authenticate(self.client)
        response = self.client.post(
            reverse("add_airplane"), self.invalid_payload_passenger_less_than_1_value
        )
        json_response = response.data
        expected_status_code = 400
        expected_message = "Ensure this value is greater than or equal to 1."

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["no_of_passengers"][0]))

    def test_exisitng_airplane_id_upon_create(self):
        authenticate(self.client)
        response = self.client.post(reverse("add_airplane"), self.valid_payload)
        json_response = response.data

        response = self.client.post(reverse("add_airplane"), self.valid_payload)
        json_response = response.data
        expected_status_code = 400
        expected_message = "id already exists"

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["id"]))


class TestFetchSpecificAirplaneAPI(APITestCase):
    def setUp(self):
        self.valid_payload = {"id": 1, "no_of_passengers": 1}
        super().setUp()

    def test_unauthenticated_request_to_fetch_airplane(self):
        response = self.client.get(reverse("get_airplane_by_id", kwargs={"id": 1}))
        json_response = response.data
        expected_status_code = 403
        expected_message = (
            expected_message
        ) = "Authentication credentials were not provided."
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["detail"])

    def test_authenticated_request_to_fetch_airplane(self):
        authenticate(self.client)

        # add airplane
        response = self.client.post(reverse("add_airplane"), self.valid_payload)
        json_response = response.data["airplane"]
        # get airplane by id
        response = self.client.get(
            reverse("get_airplane_by_id", kwargs={"id": json_response["id"]})
        )
        json_response = response.data
        expected_status_code = 200
        response_airplane_data = response.data["airplane"]
        self.assertEqual(expected_status_code, response.status_code)

        # assert airplane data
        airplane = Airplane.objects.get(pk=self.valid_payload["id"])
        serializer = AirplaneSerializer(airplane)

        expected_no_of_passengers = serializer.data["no_of_passengers"]
        expected_fuel_tank_capacity_in_liters = serializer.data[
            "fuel_tank_capacity_in_liters"
        ]
        expected_fuel_consumption_per_minute = serializer.data[
            "fuel_consumption_per_minute"
        ]
        expected_maximum_minutes_to_fly = serializer.data["maximum_minutes_to_fly"]

        self.assertEqual(
            expected_no_of_passengers, response_airplane_data["no_of_passengers"]
        )
        self.assertEqual(
            expected_fuel_tank_capacity_in_liters,
            response_airplane_data["fuel_tank_capacity_in_liters"],
        )
        self.assertEqual(
            expected_fuel_consumption_per_minute,
            response_airplane_data["fuel_consumption_per_minute"],
        )
        self.assertEqual(
            expected_maximum_minutes_to_fly,
            response_airplane_data["maximum_minutes_to_fly"],
        )

    def test_id_not_found_upon_fetch(self):
        authenticate(self.client)

        response = self.client.get(reverse("get_airplane_by_id", kwargs={"id": 1000}))
        json_response = response.data
        expected_status_code = 404
        expected_message = "Airplane not found"
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["message"])


class TestFetchAllAirplaneAPI(APITestCase):
    def setUp(self):
        self.valid_payload1 = {"id": 1, "no_of_passengers": 1}
        self.valid_payload2 = {"id": 2, "no_of_passengers": 1}
        self.valid_payload3 = {"id": 3, "no_of_passengers": 1}

        super().setUp()

    def test_unauthenticated_request_to_fetch_all_airplane(self):
        response = self.client.get(reverse("get_all_airplanes"))
        json_response = response.data
        expected_status_code = 403
        expected_message = (
            expected_message
        ) = "Authentication credentials were not provided."
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["detail"])

    def test_authenticated_request_to_fetch_all_airplane(self):
        authenticate(self.client)

        # add airplanes
        response1 = self.client.post(reverse("add_airplane"), self.valid_payload1)
        response2 = self.client.post(reverse("add_airplane"), self.valid_payload2)
        response3 = self.client.post(reverse("add_airplane"), self.valid_payload3)

        response = self.client.get(reverse("get_all_airplanes"))
        json_response = response.data
        expected_status_code = 200
        expected_length = 3
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_length, len(json_response["airplanes"]))


class TestUpdateAirplaneAPI(APITestCase):
    def setUp(self):
        self.valid_payload_for_create1 = {"id": 1, "no_of_passengers": 1}
        self.valid_payload_for_create2 = {"id": 2, "no_of_passengers": 2}
        self.valid_payload_for_update_passengers = {"id": 1, "no_of_passengers": 2}
        self.valid_payload_for_update_id = {"id": 2, "no_of_passengers": 1}
        self.payload_with_existing_id_update = {"id": 2, "no_of_passengers": 1}
        super().setUp()

    def test_unauthenticated_request_to_update_airplane(self):
        response = self.client.put(
            reverse("update_airplane", kwargs={"id": 1}), self.valid_payload_for_create1
        )
        json_response = response.data
        expected_status_code = 403
        expected_message = "Authentication credentials were not provided."
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["detail"])

    def test_authenticated_request_to_update_airplane_passengers(self):
        authenticate(self.client)
        response = self.client.post(
            reverse("add_airplane"), self.valid_payload_for_create1
        )

        response = self.client.put(
            reverse("update_airplane", kwargs={"id": 1}),
            self.valid_payload_for_update_passengers,
        )
        json_response = response.data
        expected_status_code = 200
        expected_message = "Successfully updated airplane"
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["message"])
        self.assertEqual(
            self.valid_payload_for_update_passengers["no_of_passengers"],
            json_response["airplane"]["no_of_passengers"],
        )

    def test_authenticated_request_to_update_airplane_id(self):
        authenticate(self.client)
        response = self.client.post(
            reverse("add_airplane"), self.valid_payload_for_create1
        )

        response = self.client.put(
            reverse("update_airplane", kwargs={"id": 1}),
            self.valid_payload_for_update_id,
        )
        json_response = response.data
        expected_status_code = 200
        expected_message = "Successfully updated airplane"
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["message"])
        self.assertEqual(
            self.valid_payload_for_update_id["id"],
            json_response["airplane"]["id"],
        )

    def test_id_not_found_upon_update(self):
        authenticate(self.client)
        response = self.client.post(
            reverse("add_airplane"), self.valid_payload_for_create1
        )

        response = self.client.put(
            reverse("update_airplane", kwargs={"id": 10000}),
            self.valid_payload_for_update_id,
        )
        json_response = response.data
        expected_status_code = 404
        expected_message = "Airplane not found"
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["message"])

    def test_existing_update_id_upon_update(self):
        authenticate(self.client)
        response = self.client.post(
            reverse("add_airplane"), self.valid_payload_for_create1
        )

        response = self.client.post(
            reverse("add_airplane"), self.valid_payload_for_create2
        )

        response = self.client.put(
            reverse("update_airplane", kwargs={"id": 1}),
            self.payload_with_existing_id_update,
        )
        json_response = response.data
        expected_status_code = 400
        expected_message = "id already exists"
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, str(json_response["id"]))


class TestDeleteAirplaneAPI(APITestCase):
    def setUp(self):
        self.valid_payload_for_create1 = {"id": 1, "no_of_passengers": 1}
        super().setUp()

    def test_unauthenticated_request_to_delete_airplane(self):
        response = self.client.put(reverse("delete_airplane", kwargs={"id": 1}))
        json_response = response.data
        expected_status_code = 403
        expected_message = "Authentication credentials were not provided."
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["detail"])

    def test_authenticated_request_to_delete_airplane(self):
        authenticate(self.client)
        response = self.client.post(
            reverse("add_airplane"), self.valid_payload_for_create1
        )

        response = self.client.delete(reverse("delete_airplane", kwargs={"id": 1}))
        json_response = response.data
        expected_status_code = 200
        expected_message = "Successfully deleted airplane"
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["message"])

        try:
            airplane = Airplane.objects.get(pk=self.valid_payload_for_create1["id"])
        except Airplane.DoesNotExist as e:
            self.assertEqual("Airplane matching query does not exist.", str(e))

    def test_id_not_found_upon_delete(self):
        authenticate(self.client)
        response = self.client.delete(reverse("delete_airplane", kwargs={"id": 1}))
        json_response = response.data
        expected_status_code = 404
        expected_message = "Airplane not found"
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["message"])


class TestDeleteAllAirplaneAPI(APITestCase):
    def setUp(self):
        self.valid_payload_for_create1 = {"id": 1, "no_of_passengers": 1}
        super().setUp()

    def test_unauthenticated_request_to_delete_all_airplane(self):
        response = self.client.put(reverse("delete_all_airplane"))
        json_response = response.data
        expected_status_code = 403
        expected_message = "Authentication credentials were not provided."
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["detail"])

    def test_authenticated_request_to_delete_all_airplane(self):
        authenticate(self.client)
        response = self.client.post(
            reverse("add_airplane"), self.valid_payload_for_create1
        )

        response = self.client.delete(reverse("delete_all_airplane"))
        json_response = response.data
        expected_status_code = 200
        expected_message = "Successfully deleted all airplanes"
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["message"])

        airplanes = Airplane.objects.all()
        expected_count = airplanes.count()
        self.assertEqual(expected_count, 0)

    def test_delete_all_airplane_in_empty_db(self):
        authenticate(self.client)

        response = self.client.delete(reverse("delete_all_airplane"))
        json_response = response.data
        expected_status_code = 200
        expected_message = "Database already empty"
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_message, json_response["message"])

        airplanes = Airplane.objects.all()
        expected_count = airplanes.count()
        self.assertEqual(expected_count, 0)
