import pytest
# from django.urls import reverse
# from rest_framework import status
from rest_framework.test import APITestCase
# from myproject.apps.core.models import Account
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from time import sleep
# from os import remove
# pytestmask = pytest.mark.django_db


@pytest.mark.django_db
class FilesTests(APITestCase):
    @pytest.fixture
    def test_post_rent(self):
        # user_t = mixer.blend(
        #     User, username="manuelen12"+"@gmail.com",
        #     first_name="manuel",)

        # self.client.force_authenticate(user=user_t)
        data = {'data': '{"user_id": 1, "bike": "[{"price_by_frecuency_id": 1, "quantity": 1}]"}'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 200)
        assert response.status_code == 200, "send a Post with parameter"
        # error

        data = {'data': '{"user_id": 1, "bike": "[{"price_by_frecuency_id": 2, "quantity": 1}]"}'}
        response = self.client.post("/api/v0/rents/", data)
        self.assertEqual(response.status_code, 200)
        assert response.status_code == 200, "send a Post with parameter"
