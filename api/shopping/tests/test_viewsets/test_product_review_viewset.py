import json

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from django.urls import reverse

from api.shopping.constants import (
    PRODUCT_SCORE_CANNOT_BE_GREATER_THAN_5_ERROR_MESSAGE,
)
from api.shopping.factories import ProductReviewFactory, ProductFactory, UserFactory
from api.shopping.tests.utils import create_token, get_token_from_user


class TestProductReviewViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory(username='shazam', email='shazam@dc.com', password='password')
        create_token(user=self.user)
        self.product_review = ProductReviewFactory()

    def test_get_all_product_review_score(self):
        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('product-review-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_response_data = json.loads(response.content)

        self.assertEqual(product_response_data['results'][0]['review_title'], self.product_review.review_title)
        self.assertEqual(product_response_data['results'][0]['review_text'], self.product_review.review_text)
        self.assertEqual(product_response_data['results'][0]['rating'], self.product_review.rating)

    def test_create_new_product_review(self):
        product = ProductFactory()
        token = get_token_from_user(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        data = json.dumps({
            'review_title': 'Good product',
            'review_text': 'The product is good like i expected',
            'rating': 3,
            'product_id': product.id,
        })

        response = self.client.post(
            reverse('product-review-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_new_product_review_with_rating_field_more_than_five(self):
        product = ProductFactory()
        token = get_token_from_user(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        data = json.dumps({
            'review_title': 'Good product',
            'review_text': 'The product is good like i expected',
            'rating': 100,
            'product_id': product.id,
        })

        response = self.client.post(
            reverse('product-review-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_product_review_data = json.loads(response.content)

        self.assertEqual(response_product_review_data['non_field_errors'][0], PRODUCT_SCORE_CANNOT_BE_GREATER_THAN_5_ERROR_MESSAGE)
