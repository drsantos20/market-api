from django.test import TestCase

from api.shopping.models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title='pro controller',
            brand='nintendo',
            reviewScore=8,
            price=200.00,
            image='http://example.com/pro_controller',
        )

    def test_get_product(self):
        product_a = Product.objects.get(title='pro controller')
        self.assertEqual(self.product.title, product_a.title)
        self.assertEqual(self.product.brand, product_a.brand)
        self.assertEqual(self.product.reviewScore, product_a.reviewScore)
        self.assertEqual(self.product.price, product_a.price)
        self.assertEqual(self.product.image, product_a.image)
