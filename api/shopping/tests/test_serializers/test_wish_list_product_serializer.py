from django.contrib.auth.models import User
from django.test import TestCase

from api.shopping.models import WishListProduct, WishList, Product
from api.shopping.serializers import WishListProductSerializer


class TestProductWishSerializer(TestCase):
    def setUp(self):

        self.aquaman_user = User.objects.create_user(username='aquaman', email='aquaman@dc.com', password='password')
        self.santa_claus_wish_list = WishList.objects.create(name='santa_claus_wish_list', user=self.aquaman_user)

        self.product = Product.objects.create(title='pro controller',
                                              brand='nintendo',
                                              reviewScore=8,
                                              price=200.00,
                                              image='http://example.com/pro_controller',
                                              )

        self.wish_list_product = WishListProduct.objects.create(wish_list=self.santa_claus_wish_list, product=self.product)
        self.wish_list_product.save()

        self.wish_list_product_serializer = WishListProductSerializer(instance=self.wish_list_product)

    def test_get_wish_list_product_serializer(self):

        serializer_data = self.wish_list_product_serializer.data

        self.assertEqual(serializer_data['product']['title'], 'pro controller')
        self.assertEqual(serializer_data['product']['brand'], 'nintendo')
        self.assertEqual(serializer_data['product']['reviewScore'], 8)
        self.assertEqual(serializer_data['product']['price'], 200)
        self.assertEqual(serializer_data['product']['image'], 'http://example.com/pro_controller')
