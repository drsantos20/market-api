import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from api.shopping.constants import (
    USER_ALREADY_HAS_THIS_EMAIL_ERROR_MESSAGE,
)
from api.shopping.factories import UserFactory, CustomerFactory
from api.shopping.tests.utils import create_token, get_token_from_user


class TestUserViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory(username='shazam', email='shazam@dc.com', password='password')
        self.user.save()
        create_token(user=self.user)

        self.customer = CustomerFactory(user=self.user)

    def test_get_all_users(self):
        token = get_token_from_user(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            reverse('user-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['email'], 'admin@dc.com')

    def test_create_user(self):
        data = json.dumps({
            'email': 'wonder@dc.com',
            'password': 'password',
            'username': 'wonder_dc',
            'customer': {
                'name': 'wonder',
            }
        })

        token = get_token_from_user(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            reverse('user-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email='wonder@dc.com')
        self.assertEqual(user.customer.name, 'wonder')
        self.assertEqual(user.email, 'wonder@dc.com')

    def test_does_not_add_user_with_the_same_email(self):
        data = json.dumps({
            'email': 'shazam@dc.com',
            'password': 'password',
            'username': 'shazam_dc',
            'customer': {
                'name': 'wonder',
            }
        })

        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            reverse('user-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_user_data = json.loads(response.content)

        self.assertEqual(response_user_data['non_field_errors'][0], USER_ALREADY_HAS_THIS_EMAIL_ERROR_MESSAGE.format('shazam@dc.com'))

    def test_update_existing_user(self):
        data = json.dumps({
            'username': 'shazam_dc',
            'password': 'password',
            'customer': {
                'name': 'wonder_updated',
            }
        })

        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            reverse('user-detail', kwargs={'version': 'v1', 'pk': self.user.id}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.customer.name, 'wonder_updated')

    def test_delete_existing_user(self):
        user = UserFactory(username='joker')

        create_token(user=user)

        token = get_token_from_user(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        created_user = User.objects.filter(username='joker')

        self.assertEqual(created_user.first().username, user.username)

        response = self.client.delete(
            reverse('user-detail', kwargs={'version': 'v1', 'pk': user.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        deleted_user = User.objects.filter(username='joker')
        self.assertFalse(deleted_user.exists())
