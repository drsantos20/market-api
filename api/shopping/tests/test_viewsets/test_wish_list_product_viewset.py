import json

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from api.shopping.constants import (
    PRODUCT_ALREADY_EXISTS_IN_THIS_WISH_LIST_ERROR_MESSAGE,
    PRODUCT_DOES_NOT_EXISTS_ERROR_MESSAGE,
)
from api.shopping.factories import ProductFactory, UserFactory, WishListFactory, WishListProductFactory
from api.shopping.models import WishListProduct
from api.shopping.tests.utils import create_token, get_token_from_user


class TestWishListProductViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory(username='shazam', email='shazam@dc.com', password='password')
        create_token(user=self.user)

        self.wish_list = WishListFactory(user=self.user, name='santa_claws_wish_list')

        self.product = ProductFactory(
            title='pro controller',
            brand='nintendo',
            reviewScore=8,
            price=200.00,
            image='http://example.com/pro_controller',
        )

        self.wish_list_product = WishListProductFactory(wish_list=self.wish_list, product=self.product)

    def test_get_all_wish_list_product_from_given_user(self):
        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('wish-list-product-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_response_data = json.loads(response.content)

        self.assertEqual(product_response_data['results'][0]['wish_list']['name'], self.wish_list.name)

        self.assertEqual(product_response_data['results'][0]['product']['title'], self.product.title)
        self.assertEqual(product_response_data['results'][0]['product']['brand'], self.product.brand)
        self.assertEqual(product_response_data['results'][0]['product']['reviewScore'], self.product.reviewScore)
        self.assertEqual(product_response_data['results'][0]['product']['price'], self.product.price)
        self.assertEqual(product_response_data['results'][0]['product']['image'], self.product.image)

    def test_add_products_to_existing_wish_list(self):
        product = ProductFactory()

        data = json.dumps({
            'product':
                {
                    'id': product.id,
                    'title': product.title,
                    'brand': product.brand,
                    'reviewScore': product.reviewScore,
                    'price': product.price,
                    'image': product.image,
                }
        })

        token = get_token_from_user(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            reverse('wish-list-product-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        wish_list_product = WishListProduct.objects.filter(wish_list=self.wish_list)

        self.assertEqual(len(wish_list_product), 2)
        self.assertEqual(wish_list_product[1].product.title, product.title)
        self.assertEqual(wish_list_product[1].product.brand, product.brand)
        self.assertEqual(wish_list_product[1].product.reviewScore, product.reviewScore)
        self.assertEqual(wish_list_product[1].product.price, product.price)
        self.assertEqual(wish_list_product[1].product.image, product.image)

    def test_add_products_to_a_non_existing_wish_list(self):
        product = ProductFactory()

        data = json.dumps({
            'product':
                {
                    'id': product.id,
                    'title': product.title,
                    'brand': product.brand,
                    'reviewScore': product.reviewScore,
                    'price': product.price,
                    'image': product.image,
                }
        })

        user = UserFactory(username='joker', email='joker@dc.com', password='password')

        create_token(user=user)
        token = get_token_from_user(user=user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            reverse('wish-list-product-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)
        response_wish_list_product_data = json.loads(response.content)
        self.assertEqual(response_wish_list_product_data, 'User has no wish list')

    def test_add_duplicate_product_to_a_existing_wish_list(self):
        data = json.dumps({
            'product':
                {
                    'id': self.product.id,
                    'title': self.product.title,
                    'brand': self.product.brand,
                    'reviewScore': self.product.reviewScore,
                    'price': self.product.price,
                    'image': self.product.image,
                }
        })

        token = get_token_from_user(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            reverse('wish-list-product-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_wish_list_product_data = json.loads(response.content)

        self.assertEqual(response_wish_list_product_data['non_field_errors'][0], PRODUCT_ALREADY_EXISTS_IN_THIS_WISH_LIST_ERROR_MESSAGE)

    def test_add_a_non_existing_product_to_a_existing_wish_list(self):
        data = json.dumps({
            'product':
                {
                    'id': 1220324,
                    'title': 'samsung gear galaxy',
                    'brand': 'samsung',
                    'reviewScore': 8,
                    'price': 800.00,
                    'image': 'http://example.com/samsung_gear.png'
                }
        })

        token = get_token_from_user(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            reverse('wish-list-product-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_user_data = json.loads(response.content)

        self.assertEqual(response_user_data['non_field_errors'][0],
                         PRODUCT_DOES_NOT_EXISTS_ERROR_MESSAGE)
