from rest_framework.test import APITestCase
from rest_framework import status


class UserAPITestCase(APITestCase):
    def test_simulation_view(self):
        url = "/simulate/"

        data = {
            "alpha": 0.9,
            "beta": 1.2,
            "rinit": 1000,
            "roff": 10000,
            "ron": 100,
            "vt": 0.7,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
