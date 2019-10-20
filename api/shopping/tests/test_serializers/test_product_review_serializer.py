from django.test import TestCase

from api.shopping.factories import ProductReviewFactory
from api.shopping.serializers.product_review_serializer import ProductReviewSerializer


class TestProductReviewSerializer(TestCase):
    def setUp(self):
        self.product_review = ProductReviewFactory()

        self.product_review_serializer = ProductReviewSerializer(instance=self.product_review)

    def test_get_product_review_serializer(self):
        serializer_data = self.product_review_serializer.data

        self.assertEqual(serializer_data['review_title'], self.product_review.review_title)
        self.assertEqual(serializer_data['review_text'], self.product_review.review_text)
        self.assertEqual(serializer_data['rating'], self.product_review.rating)
