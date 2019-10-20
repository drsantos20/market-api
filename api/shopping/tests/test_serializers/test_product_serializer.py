from django.test import TestCase

from api.shopping.models import Product
from api.shopping.serializers.product_serializer import ProductSerializer


class TestProductSerializer(TestCase):
    def setUp(self):

        self.product = Product.objects.create(
            title='pro controller',
            brand='nintendo',
            price=200.00,
            image='http://example.com/pro_controller',
        )

        self.product_serializer = ProductSerializer(instance=self.product)

    def test_get_product_serializer(self):
        serializer_data = self.product_serializer.data

        self.assertEqual(serializer_data['title'], 'pro controller')
        self.assertEqual(serializer_data['brand'], 'nintendo')
        self.assertEqual(serializer_data['price'], 200)
        self.assertEqual(serializer_data['image'], 'http://example.com/pro_controller')
