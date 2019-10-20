import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from django.urls import reverse
from api.shopping.models import WishList
from api.shopping.tests.utils import create_token, get_token_from_user


class TestUserViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = User.objects.create_user(username='shazam', email='shazam@dc.com', password='password')
        self.user.save()
        create_token(user=self.user)

        self.wish_list = WishList.objects.create(user=self.user, name='santa_claws_wish_list')

    def test_get_all_wish_list(self):
        token = get_token_from_user(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('wish-list-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wish_list_response_data = json.loads(response.content)

        self.assertEqual(wish_list_response_data['results'][0]['name'], self.wish_list.name)

    def test_create_wish_list(self):
        data = json.dumps({
            'name': 'my_personal_product_wishes'
        })

        user = User.objects.create_user(username='batman', email='batman@dc.com', password='password')
        user.save()

        create_token(user=user)
        token = get_token_from_user(user=user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            reverse('wish-list-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        wish_list_response_data = json.loads(response.content)
        wish_list = WishList.objects.get(name='my_personal_product_wishes')
        self.assertEqual(wish_list_response_data['name'], wish_list.name)

