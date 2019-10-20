from django.test import TestCase

from api.shopping.models import ProductReview, Product


class ProductReviewTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title='pro controller',
            brand='nintendo',
            reviewScore=8,
            price=200.00,
            image='http://example.com/pro_controller',
        )

        self.product_review = ProductReview.objects.create(
            review_title='Amazing product',
            review_text='All is good',
            rating=5,
            product=self.product,
        )

    def test_get_product_review(self):
        product_review = ProductReview.objects.get(id=self.product_review.id)

        self.assertEqual(self.product_review.review_title, product_review.review_title)
        self.assertEqual(self.product_review.review_text, product_review.review_text)
        self.assertEqual(self.product_review.rating, product_review.rating)
