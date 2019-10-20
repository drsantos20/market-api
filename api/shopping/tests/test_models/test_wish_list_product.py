from django.contrib.auth.models import User
from django.test import TestCase

from api.shopping.models import Product, WishList
from api.shopping.models.wish_list_product import WishListProduct


class WishListProductTestCase(TestCase):

    def setUp(self):
        self.aquaman_user = User.objects.create_user(username='aquaman', email='aquaman@dc.com', password='password')
        self.product = Product.objects.create(
            title='pro controller',
            brand='nintendo',
            reviewScore=8,
            price=200.00,
            image='http://example.com/pro_controller',
        )
        self.santa_claus_wish_list = WishList.objects.create(name='santa_claus_wish_list', user=self.aquaman_user)

        self.wish_list_product = WishListProduct.objects.create(wish_list=self.santa_claus_wish_list, product=self.product)
        self.wish_list_product.save()

    def test_create_wish_list_product(self):
        wish_list_product = WishListProduct.objects.get(wish_list=self.santa_claus_wish_list)
        self.assertEqual(wish_list_product.wish_list.name, self.santa_claus_wish_list.name)
