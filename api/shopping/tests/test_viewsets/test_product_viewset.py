import json

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from django.urls import reverse

from api.shopping.factories import ProductFactory, ProductReviewFactory, UserFactory
from api.shopping.models import Product
from api.shopping.tests.utils import create_token, get_token_from_user


def sort_by_id(result):
    return result['id']


class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory(username='shazam', email='shazam@dc.com', password='password')
        create_token(user=self.user)

        self.product = ProductFactory(
            title='pro controller',
            brand='nintendo',
            price=200.00,
            image='http://example.com/pro_controller',
        )

    def test_get_all_product(self):
        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_response_data = json.loads(response.content)

        self.assertEqual(product_response_data['results'][0]['title'], self.product.title)
        self.assertEqual(product_response_data['results'][0]['brand'], self.product.brand)
        self.assertEqual(product_response_data['results'][0]['reviewScore'], self.product.reviewScore)
        self.assertEqual(product_response_data['results'][0]['price'], self.product.price)
        self.assertEqual(product_response_data['results'][0]['image'], self.product.image)

    def test_get_product_detail(self):
        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('product-detail', kwargs={'version': 'v1', 'pk': self.product.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_response_data = json.loads(response.content)

        self.assertEqual(product_response_data['title'], self.product.title)
        self.assertEqual(product_response_data['brand'], self.product.brand)
        self.assertEqual(product_response_data['reviewScore'], self.product.reviewScore)
        self.assertEqual(product_response_data['price'], self.product.price)
        self.assertEqual(product_response_data['image'], self.product.image)

    def test_get_detail_from_a_non_existing_product(self):
        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('product-detail', kwargs={'version': 'v1', 'pk': 9000})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_product_pagination_limit_by_5(self):

        for _ in range(6):
            ProductFactory()

        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_response_data = json.loads(response.content)

        # total of products
        self.assertEqual(product_response_data['count'], 7)

        # total of products per page
        self.assertEqual(len(product_response_data['results']), 5)

    def test_create_new_product(self):
        data = json.dumps({
            'title': 'samsung gear galaxy',
            'brand': 'samsung',
            'price': 800.00,
            'image': 'http://example.com/samsung_gear.png'
        })

        token = get_token_from_user(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            reverse('product-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title='samsung gear galaxy')

        self.assertEqual(created_product.title, 'samsung gear galaxy')
        self.assertEqual(created_product.brand, 'samsung')
        self.assertEqual(created_product.reviewScore, 0)
        self.assertEqual(created_product.price, 800.00)
        self.assertEqual(created_product.image, 'http://example.com/samsung_gear.png')

    def test_delete_existing_product(self):
        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            reverse('product-detail', kwargs={'version': 'v1', 'pk': self.product.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        removed_product = Product.objects.filter(id=self.product.id)
        self.assertEqual(removed_product.exists(), False)

    def test_delete_a_non_existing_product(self):
        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            reverse('product-detail', kwargs={'version': 'v1', 'pk': 11300}),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product_with_product_review(self):
        product_review = ProductReviewFactory(rating=3)

        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('product-detail', kwargs={'version': 'v1', 'pk': product_review.product.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_response_data = json.loads(response.content)

        self.assertEqual(product_response_data['title'], product_review.product.title)
        self.assertEqual(product_response_data['brand'], product_review.product.brand)
        self.assertEqual(product_response_data['reviewScore'], 3)
        self.assertEqual(product_response_data['price'], product_review.product.price)
        self.assertEqual(product_response_data['image'], product_review.product.image)

        self.assertEqual(product_response_data['product_review'][0]['review_title'], product_review.review_title)
        self.assertEqual(product_response_data['product_review'][0]['review_text'], product_review.review_text)
        self.assertEqual(product_response_data['product_review'][0]['rating'], product_review.rating)

    def test_get_product_with_more_than_one_product_review(self):
        product = ProductFactory(title='mac book pro', brand='apple')
        first_product_review = ProductReviewFactory(product=product, rating=5)
        second_product_review = ProductReviewFactory(product=product, rating=5)

        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('product-detail', kwargs={'version': 'v1', 'pk': product.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_response_data = json.loads(response.content)

        self.assertEqual(product_response_data['title'], product.title)
        self.assertEqual(product_response_data['brand'], product.brand)
        self.assertEqual(product_response_data['reviewScore'], 5)
        self.assertEqual(product_response_data['price'], product.price)
        self.assertEqual(product_response_data['image'], product.image)

        sorted_product_review = sorted(product_response_data['product_review'], key=sort_by_id)

        self.assertEqual(sorted_product_review[0]['review_title'], first_product_review.review_title)
        self.assertEqual(sorted_product_review[0]['review_text'], first_product_review.review_text)
        self.assertEqual(sorted_product_review[0]['rating'], first_product_review.rating)

        self.assertEqual(sorted_product_review[1]['review_title'], second_product_review.review_title)
        self.assertEqual(sorted_product_review[1]['review_text'], second_product_review.review_text)
        self.assertEqual(sorted_product_review[1]['rating'], second_product_review.rating)

    def test_list_of_products_with_product_review(self):
        product_review = ProductReviewFactory(review_title='Amazing Product', rating=5)

        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sorted_product_results = sorted(response.data['results'], key=sort_by_id)

        self.assertEqual(sorted_product_results[0]['title'], self.product.title)
        self.assertEqual(sorted_product_results[0]['brand'], self.product.brand)
        self.assertEqual(sorted_product_results[0]['reviewScore'], self.product.reviewScore)
        self.assertEqual(sorted_product_results[0]['price'], self.product.price)
        self.assertEqual(sorted_product_results[0]['image'], self.product.image)
        self.assertEqual(len(sorted_product_results[0]['product_review']), 0)

        self.assertEqual(sorted_product_results[1]['title'], product_review.product.title)
        self.assertEqual(sorted_product_results[1]['brand'], product_review.product.brand)
        self.assertEqual(sorted_product_results[1]['reviewScore'], 5)
        self.assertEqual(sorted_product_results[1]['price'], product_review.product.price)
        self.assertEqual(sorted_product_results[1]['image'], product_review.product.image)
        self.assertEqual(len(sorted_product_results[1]['product_review']), 1)
        self.assertEqual(sorted_product_results[1]['product_review'][0]['review_title'], product_review.review_title)
        self.assertEqual(sorted_product_results[1]['product_review'][0]['review_text'], product_review.review_text)
        self.assertEqual(sorted_product_results[1]['product_review'][0]['rating'], product_review.rating)

    def test_calculate_product_score_given_a_couple_of_product_reviews(self):
        product = ProductFactory(title='Iphone x', brand='Apple')
        ProductReviewFactory(review_title='Bad Product', rating=2, product=product)
        ProductReviewFactory(review_title='Bad Product', rating=3, product=product)

        token = get_token_from_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(
            reverse('product-detail', kwargs={'version': 'v1', 'pk': product.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_response_data = json.loads(response.content)

        self.assertEqual(product_response_data['title'], product.title)
        self.assertEqual(product_response_data['brand'], product.brand)

        ''' 5 total of rating points / 2 total of reviews from this product = 2 '''

        self.assertEqual(product_response_data['reviewScore'], 2)
        self.assertEqual(product_response_data['price'], product.price)
        self.assertEqual(product_response_data['image'], product.image)
